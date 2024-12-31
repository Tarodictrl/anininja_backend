from app.core.controllers.base import CRUDBase
from app.core.models.comment import Comment
from app.core.schemas.comment import CommentCreate, CommentUpdate


class CommentCRUD(
    CRUDBase[
        Comment,
        CommentCreate,
        CommentUpdate,
    ]
):
    """ Comment CRUD. """


comment_crud = CommentCRUD(Comment)
