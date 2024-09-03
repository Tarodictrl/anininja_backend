from app.core.models.director import Director
from app.core.schemas.director import DirectorCreate, DirectorUpdate
from app.core.controllers.base import CRUDBase


class DirectorCRUD(
    CRUDBase[
        Director,
        DirectorCreate,
        DirectorUpdate,
    ]
):
    """ Director CRUD. """


director_crud = DirectorCRUD(Director)
