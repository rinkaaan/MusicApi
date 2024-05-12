import json
import os
import subprocess
import threading
import uuid
from dataclasses import dataclass
from typing import List

from apiflask import HTTPError

from models.base import AlbumModel, MusicModel


@dataclass
class RawMusic:
    id: str
    uploader: str
    thumbnail_src_url: str
    thumbnail_extension: str
    thumbnail_dst_path: str
    # video, image
    media_type: str
    webpage_url: str
    albums: List[str]
    # Instagram, Twitter, YouTube
    website: str
    duration: str | None = None


def download_metadata(cookies_path, media_url) -> List[RawMusic]:
    medias = run_ytdlp(cookies_path, media_url)
    if medias is not None:
        return medias

    medias = run_gallerydl(cookies_path, media_url)
    if medias is not None:
        return medias

    raise HTTPError(400, "Invalid media URL")


def run_ytdlp(cookies_path, media_url) -> List[RawMusic] | None:
    command = f"yt-dlp --dump-single-json --quiet --skip-download --no-playlist -o metadata --cookies {cookies_path} \"{media_url}\""
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, check=False, stderr=subprocess.PIPE)
    if process.returncode != 0:
        if process.stderr and "http.cookiejar.LoadError" in process.stderr.decode():
            raise HTTPError(400, "Invalid or expired cookies file")
        return None

    metadata = json.loads(process.stdout)
    medias = []

    id = metadata["id"]
    website = metadata["extractor_key"]
    uploader = metadata["uploader"]
    webpage_url = metadata["webpage_url"]
    albums = [
        f"website={website}",
        f"uploader={uploader}",
        f"media_type=Videos",
    ]

    if website == "Twitter" and "entries" in metadata:
        for index, entry in enumerate(metadata["entries"]):
            thumbnail = entry["thumbnail"]
            thumbnail_extension = get_extension(thumbnail)
            media = RawMusic(
                id=f"{website}#{id}#{index}",
                uploader=uploader,
                thumbnail_src_url=thumbnail,
                thumbnail_extension=thumbnail_extension,
                thumbnail_dst_path=f"videos/{website}/{id}/{index}_thumbnail.{thumbnail_extension}",
                media_type="video",
                duration=entry["duration"],
                webpage_url=webpage_url,
                albums=albums,
                website=website,
            )
            medias.append(media)
    else:
        thumbnail = metadata["thumbnail"]

        thumbnail_extension = os.path.basename(thumbnail).split(".")[1].split("?")[0]
        media = RawMusic(
            id=f"{website}#{id}#0",
            uploader=uploader,
            thumbnail_src_url=thumbnail,
            thumbnail_extension=thumbnail_extension,
            thumbnail_dst_path=f"videos/{website}/{id}/0_thumbnail.{thumbnail_extension}",
            media_type="video",
            duration=metadata["duration"],
            webpage_url=webpage_url,
            albums=albums,
            website=website,
        )
        medias.append(media)

    return medias if len(medias) > 0 else None


def run_gallerydl(cookies_path, media_url) -> List[RawMusic] | None:
    command = f"gallery-dl --no-download --dump-json --cookies {cookies_path} \"{media_url}\""
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, check=False)
    if process.returncode != 0:
        return None
    if process.stdout and "AuthorizationError" in process.stdout.decode():
        raise HTTPError(400, "Invalid or expired cookies file")

    metadata = json.loads(process.stdout)
    medias = []
    index = 0

    for entry in metadata:
        # Keep only entries with thumbnails
        if len(entry) != 3:
            continue

        thumbnail = entry[1]
        entry = entry[2]
        website = entry["category"].capitalize()
        thumbnail_extension = entry["extension"]
        media_type = "image"
        media_type_album = "Photos"
        folder = "images"

        if website == "Twitter":
            id = entry["tweet_id"]
            uploader = entry["author"]["nick"]
            webpage_url = f"https://twitter.com/{entry["author"]["name"]}/status/{id}"
        elif website == "Instagram":
            id = entry["post_shortcode"]
            uploader = entry["fullname"]
            webpage_url = f"https://www.instagram.com/p/{id}"

            if entry["video_url"]:
                media_type = "video"
                media_type_album = "Videos"
                folder = "videos"
                thumbnail = entry["display_url"]
                thumbnail_extension = get_extension(thumbnail)
        else:
            raise HTTPError(400, "Unsupported photo website")

        media = RawMusic(
            id=f"{website}#{id}#{index}",
            uploader=uploader,
            thumbnail_src_url=thumbnail,
            thumbnail_extension=thumbnail_extension,
            thumbnail_dst_path=f"{folder}/{website}/{id}/{index}_thumbnail.{thumbnail_extension}",
            media_type=media_type,
            webpage_url=webpage_url,
            albums=[f"website={website}", f"uploader={uploader}", f"media_type={media_type_album}"],
            website=website,
        )
        medias.append(media)

        index += 1

    return medias if len(medias) > 0 else None


# Downloads thumbnail, uploads to bucket, returns bucket file url
def upload_thumbnail(media: RawMusic):
    from api.app import bucket
    ext = media.thumbnail_extension

    # Download thumbnail
    filename = f"{uuid.uuid4()}_thumbnail.{ext}"
    command = f"curl -o {filename} \"{media.thumbnail_src_url}\""
    process = subprocess.run(command, shell=True, check=False)
    if process.returncode != 0:
        raise HTTPError(400, "Failed to download thumbnail")

    # Upload thumbnail to bucket
    try:
        bucket.upload_local_file(
            local_file=filename,
            file_name=media.thumbnail_dst_path,
        )
    except Exception as e:
        raise HTTPError(400, f"Failed to upload thumbnail: {e}")

    subprocess.run(f"rm {filename}", shell=True)


# Create albums if not exists, return list of albums
def create_albums_if_not_exists(media: RawMusic) -> List[AlbumModel]:
    from api.app import session

    albums = []
    for album_name in media.albums:
        album = session.query(AlbumModel).filter(AlbumModel.name == album_name).first()
        if not album:
            album = AlbumModel(
                name=album_name,
            )
            session.add(album)
        albums.append(album)

    return albums


def get_extension(url):
    return os.path.basename(url).split(".")[1].split("?")[0]


def download_medias_helper(media_ids: List[str], cookies_path):
    from api.app import session

    media_ids_to_download = []

    # Validate media_ids
    for media_id in media_ids:
        media: MusicModel = session.query(MusicModel).filter(MusicModel.id == media_id).first()
        media.video_path = "downloading"
        if not media:
            raise HTTPError(404, "Music not found")

        try:
            int(media.id.split("#")[-1])
        except ValueError:
            raise HTTPError(400, "Failed to parse index from media id")

        media_ids_to_download.append(media.id)

    session.commit()

    def start_downloading():
        for media_id in media_ids_to_download:
            media: MusicModel = session.query(MusicModel).filter(MusicModel.id == media_id).first()
            print(media.webpage_url)
            print(media.id)
            print(media.thumbnail_path)
            # Twitter#<id>#0
            index = int(media.id.split("#")[-1]) + 1
            filename = f"{uuid.uuid4()}_video"
            command = f"yt-dlp \"{media.webpage_url}\" --cookies \"{cookies_path}\" -I {index} -o {filename}"
            process = subprocess.run(command, shell=True, check=False, stderr=subprocess.PIPE)
            if process.returncode != 0:
                if "No status found with that ID" in process.stderr.decode():
                    # raise Exception("Post has been deleted")
                    print("Post has been deleted")
                    media.video_path = "deleted"
                    session.commit()
                    continue
                else:
                    media.video_path = "error"
                    session.commit()
                raise Exception(f"Failed to download media: {process.stderr}")

            # Find file starting with filename
            files = os.listdir()
            for file in files:
                if file.startswith(filename):
                    filename = file
                    break
            extension = filename.split(".")[-1]

            # Upload video to bucket
            try:
                from api.app import bucket
                video_path = media.thumbnail_path.replace("thumbnail", "video")
                video_path = ".".join(video_path.split(".")[:-1]) + f".{extension}"
                media.video_path = video_path
                bucket.upload_local_file(
                    local_file=filename,
                    file_name=video_path,
                )
                print(f"Uploaded video to {video_path}")
            except Exception as e:
                raise Exception(f"Failed to upload video: {e}")

            subprocess.run(f"rm {filename}", shell=True)
            print(f"Deleted {filename}")

        session.commit()
        print("Committed")

    # Start download in separate thread
    threading.Thread(target=start_downloading).start()
    # start_downloading()

    return {}
