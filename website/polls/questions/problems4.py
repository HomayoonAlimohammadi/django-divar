from __future__ import annotations
from django.db.models import Q, F
from polls.models import Post, Author, Blog


def q_20() -> None:
    Post.objects.filter(blog_id=1).update(rating=4)


def q_21() -> None:
    Blog.objects.get(pk=1).post_set.filter(number_of_likes__lt=10).update(
        number_of_likes=F("number_of_likes") + 1
    )
    ###############################
    Post.objects.filter(blog_id=1, number_of_likes__lt=10).update(
        umber_of_likes=F("number_of_likes") + 1
    )


def q_22() -> None:
    Post.objects.filter(author_id=1).delete()


def q_23() -> None:
    random_post = Post.objects.order_by("?").first()
    if random_post:
        random_post.number_of_likes = F("number_of_likes") + 1
        random_post.save()
    else:
        print("No Posts available!")
