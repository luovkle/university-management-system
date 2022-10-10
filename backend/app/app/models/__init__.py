from .user import (
    User,
    UserCreate,
    UserRead,
    UserReadWithPosts,
    UserUpdate,
)
from .post import (
    Post,
    PostCreate,
    PostRead,
    PostReadWithComments,
    PostUpdate,
)
from .comment import (
    Comment,
    CommentCreate,
    CommentRead,
    CommentReadWithPost,
    CommentUpdate,
)

UserReadWithPosts.update_forward_refs(PostRead=PostRead)
PostReadWithComments.update_forward_refs(CommentRead=CommentRead)
CommentReadWithPost.update_forward_refs(PostRead=PostRead)
