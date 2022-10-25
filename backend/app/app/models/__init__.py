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
    UserReadWithPosts,
    UserReadWithProfile,
    UserUpdate,
)
from .profile import Profile, ProfileRead, ProfileUpdate

UserReadWithPosts.update_forward_refs(PostRead=PostRead)
UserReadWithProfile.update_forward_refs(ProfileRead=ProfileRead)
PostReadWithComments.update_forward_refs(CommentRead=CommentRead)
CommentReadWithPost.update_forward_refs(PostRead=PostRead)
