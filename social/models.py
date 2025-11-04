from django.db import models
from blog.models import Post
from user.models import User


# The %(class)s placeholder gets replaced with the lowercase child class name:
class PostInteractionBase(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="%(class)ss")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Like(PostInteractionBase):
    class Meta:
        unique_together = ("post", "user")
        verbose_name = "Like"
        verbose_name_plural = "Likes"


class Comment(PostInteractionBase):
    comment = models.TextField()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
        unique_together = ("follower", "following")
