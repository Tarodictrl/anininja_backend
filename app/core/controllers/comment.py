from app.core.controllers.base import CRUDBase
from app.core.controllers.base import ModelType
from app.core.models.comment import Comment


class CommentCRUD(
    CRUDBase[
        Comment,
        ModelType,
        ModelType,
    ]
):
    """ Comment CRUD. """


comment_crud = CommentCRUD(Comment)
