from datetime import datetime

from sqlalchemy import text

from models.base import MusicModel
from sql_scripts.clients import session


def get_file_path(url):
    if "nguylinc-photos-test" in url:
        return url.split("nguylinc-photos-test/")[1]
    return url


class Test:
    def test_add_ksuid(self):
        # medias = session.query(MusicModel).all()
        #
        # for media in medias:
        #     media: MusicModel = session.query(MusicModel).filter(MusicModel.id == media.id).first()
        #     media.thumbnail_path = get_file_path(media.thumbnail_path)
        #
        # session.commit()

        # albums = session.query(AlbumModel).all()
        #
        # for album in albums:
        #     album: AlbumModel = session.query(AlbumModel).filter(AlbumModel.id == album.id).first()
        #     # new_path = get_file_path(album.thumbnail_path)
        #     # album.thumbnail_path = new_path
        #
        #     # medias = session.query(MusicModel).filter(MusicModel.album_id == album.id).all()
        #     # for media in medias:
        #     #     media: MusicModel = session.query(MusicModel).filter(MusicModel.id == media.id).first()
        #     sorted_medias = sorted(album.media, key=lambda media: media.created_at, reverse=True)
        #
        #     # If number of hash tags in all medias don't match, output counts
        #
        #     # Create dict to store number of hash tags in each media
        #     hash_tag_counts = {}
        #
        #     # Count number of hash tags in each media
        #     for media in sorted_medias:
        #         # Count number of times "#" occurs in media.id
        #         hash_tag_counts[media.id] = media.id.count("#")
        #
        #     # If number of hash tags in all medias don't match, output counts
        #     if len(set(hash_tag_counts.values())) != 1 and len(sorted_medias) > 1:
        #         print(f"Album {album.name} has different number of hash tags in medias")
        #         print(hash_tag_counts)
        #
        #
        #     # print(f"Album has {len(sorted_medias)} medias")
        #
        # # session.commit()

        # # Find medias that have the same thumbnail_path
        # medias = session.query(MusicModel).all()
        # thumbnail_path_counts = {}
        #
        # for media in medias:
        #     thumbnail_path = media.thumbnail_path
        #     if thumbnail_path in thumbnail_path_counts:
        #         thumbnail_path_counts[thumbnail_path] += 1
        #     else:
        #         thumbnail_path_counts[thumbnail_path] = 1
        #
        # for thumbnail_path, count in thumbnail_path_counts.items():
        #     if count > 1:
        #         print(f"{thumbnail_path} has {count} medias")

        # # Find medias that have "media_type=Videos" in their albums
        # medias = session.query(MusicModel).all()
        # for media in medias:
        #     for album in media.albums:
        #         if "media_type=Videos" in album.name:
        #             # print(media.id)
        #
        #             # If number of hash tags is 1 then append #0 to id
        #             if media.id.count("#") == 1:
        #                 old_media_id = media.id
        #                 new_media_id = f"{media.id}#0"
        #
        #                 # Replace all media ids in media_albums table with new id
        #                 # Use raw SQL to update media_albums table
        #                 # session.execute(f"UPDATE media_albums SET media_id='{new_media_id}' WHERE media_id='{old_media_id}'")
        #                 session.execute(text(f"UPDATE media_albums SET media_id='{new_media_id}' WHERE media_id='{old_media_id}'"))
        #
        #                 media.id = new_media_id
        #                 print(media.id)
        #
        #             break
        #
        # session.commit()





        # Find medias that have "media_type=Photos" in their albums
        medias = session.query(MusicModel).all()
        for media in medias:
            for album in media.albums:
                if "media_type=Photos" in album.name:
                    print(media.id)
                    break




        # # Find medias that have "media_type=Photos" in their albums
        # medias = session.query(MusicModel).all()
        # for media in medias:
        #     for album in media.albums:
        #         if "media_type=Photos" in album.name:
        #             # Decrement last number by 1
        #             website, id, index = media.id.split("#")
        #             new_index = int(index) - 1
        #             if new_index < 0:
        #                 raise ValueError(f"Index is less than 0: {media.id}")
        #
        #             old_id = media.id
        #             new_id = f"{website}#{id}#{new_index}"
        #
        #             # Use raw SQL to update media_albums table
        #             session.execute(text(f"UPDATE media_albums SET media_id='{new_id}' WHERE media_id='{old_id}'"))
        #
        #             # Update media id
        #             media.id = new_id
        #             print(media.id)
        #
        #             break
        #
        #     if media.created_at >= datetime.fromisoformat("2024-04-25 08:29:23.888842"):
        #         break
        #
        # session.commit()
