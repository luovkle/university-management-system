from .comment import (
    Comment,
    CommentCreate,
    CommentRead,
    CommentReadWithPost,
    CommentUpdate,
)
from .post import Post, PostCreate, PostRead, PostReadWithComments, PostUpdate
from .user import (
    User,
    UserCreate,
    UserRead,
    UserReadWithProfile,
    UserUpdate,
)
from .profile import Profile, ProfileRead, ProfileReadWithPosts, ProfileUpdate

UserReadWithProfile.update_forward_refs(ProfileRead=ProfileRead)
ProfileReadWithPosts.update_forward_refs(PostRead=PostRead)
PostReadWithComments.update_forward_refs(CommentRead=CommentRead)
CommentReadWithPost.update_forward_refs(PostRead=PostRead)
