from __future__ import annotations
from django.db.models import F
from polls.models import Post


def get_posts_published_after_editted_16() -> list[Post]:
    posts = Post.objects.filter(pub_date__gt=F("mod_date")).all()
    return list(posts)


def get_posts_sum_likes_comments_17() -> list[Post]:
    annotated_field = F("number_of_likes") + F("number_of_comments")
    posts = Post.objects.order_by(-1 * annotated_field).all()
    return list(posts)


def get_posts_like_comment_gt_100_18() -> list[Post]:
    posts = Post.objects.filter(number_of_likes__gt=100 - F("number_of_comments"))
    return list(posts)


def get_post_with_author_name_in_desc() -> list[Post]:
    posts = (
        Post.objects.filter(description__icontains=F("authors__name")).distinct().all()
    )
    return list(posts)
