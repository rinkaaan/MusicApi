from apiflask import Schema
from apiflask.fields import Float, List, Nested, String, DateTime

from utils.misc import validate_ksuid


class AlbumSchema(Schema):
    id = String(validate=validate_ksuid)
    name = String()
    thumbnail_path = String()
    created_at = DateTime()
    updated_at = DateTime()


class MusicSchema(Schema):
    id = String()
    duration = Float()
    webpage_url = String()
    thumbnail_path = String()
    # If download started then "downloading"
    video_path = String()
    # Automatically create album for media's author, website source, media type (photo or video), and date (Jan 2024)
    albums = List(Nested(AlbumSchema))
    created_at = DateTime()
    created_at_ksuid = String()
