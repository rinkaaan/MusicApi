from ksuid import Ksuid

from api.app import session
from models.base import MusicModel


class Test:
    def test_add_ksuid(self):
        medias = session.query(MusicModel).all()

        for media in medias:
            media.created_at_ksuid = str(Ksuid(media.created_at))
            # media = session.query(MusicModel).filter(MusicModel.id == media.id).first()
            # media.created_at_ksuid = Ksuid(media.created_at)

        session.commit()
