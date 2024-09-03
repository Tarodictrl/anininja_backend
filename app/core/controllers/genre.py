from app.core.models.genre import Genre
from app.core.schemas.genre import GenreCreate, GenreUpdate
from app.core.controllers.base import CRUDBase


class GenreCRUD(
    CRUDBase[
        Genre,
        GenreCreate,
        GenreUpdate,
    ]
):
    """ Genre CRUD. """


genre_crud = GenreCRUD(Genre)
