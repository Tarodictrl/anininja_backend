from app.core.models.studio import Studio
from app.core.schemas.studio import StudioCreate, StudioUpdate
from app.core.controllers.base import CRUDBase


class StudioCRUD(
    CRUDBase[
        Studio,
        StudioCreate,
        StudioUpdate,
    ]
):
    """ Studio CRUD. """


studio_crud = StudioCRUD(Studio)
