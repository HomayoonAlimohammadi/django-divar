from __future__ import annotations
from polls.models import Post, Blog


def get_most_comment_posts() -> list[Post]:
    posts = Post.objects.order_by("-number_of_comments")[:5]
    return list(posts)


def get_most_liked_post() -> Post | None:
    post = Post.objects.order_by("-number_of_likes").first()
    return post


def get_posts_by_like_and_comment() -> list[Post]:
    posts = Post.objects.order_by("-number_of_likes", "number_of_comments").all()
    return list(posts)


def get_mohammd_posts() -> list[Post]:
    posts = Post.objects.filter(authors__name="Mohammad").distinct().all()
    return list(posts)


def get_user_most_liked_post(user_ids: list[int]) -> dict[str, Post]:
    mapping = {}
    for _id in user_ids:
        most_liked_post = (
            Post.objects.filter(author_id=_id).order_by("-number_of_likes").first()
        )
        mapping[_id] = most_liked_post
    return mapping


def get_top_posts_with_users(users: list[str]) -> list[Post]:
    posts = (
        Post.objects.filter(author__name__in=users)
        .order_by("-number_of_likes")
        .distinct()[:10]
    )
    return list(posts)


def get_1_2_user_blogs() -> list[Blog]:
    blogs = Blog.objects.filter(post__author_id__in=[1, 2])
    return list(blogs)


def get_blogs_without_question_and_low_comments() -> list[Post]:
    posts = Post.objects.exclude(
        post__title__contains="?", post__number_of_likes_gt=10
    ).all()
    return list(posts)
