from app.core.models.anime import Anime
from app.core.schemas.anime import AnimeCreate, AnimeUpdate
from app.core.controllers.base import CRUDBase


class AnimeCRUD(
    CRUDBase[
        Anime,
        AnimeCreate,
        AnimeUpdate,
    ]
):
    """ Anime CRUD. """


anime_crud = AnimeCRUD(Anime)
