from datetime import date, timedelta
from polls.models import Post
from django.db.models import Q


def find_in_titles_1(word: str):
    posts = Post.objects.filter(
        title__icontains=word, pub_date__gte=date.today() - timedelta(days=30)
    )
    return posts


def find_today_10_likes_2():
    today = date.today()
    posts = Post.objects.filter(number_of_likes__gt=10, pub_date=today)
    return posts


def fetch_today_titles_3():
    today = date.today()
    qs = Post.objects.filter(pub_date=today).all()
    post_titles = [post.title for post in qs]
    return post_titles


def fetch_comments_between_50_100_4():
    posts = Post.objects.filter(
        title__endswith="?", number_of_comments__range=(50, 101)
    ).all()
    return posts


def exclude_like_comment_5():
    posts = (
        Post.objects.exclude(number_of_comments__gte=100)
        .exclude(number_of_likes__lte=50)
        .all()
    )
    return posts


# def fetch_comments_or_likes_6():
#     posts_with_likes = Post.objects.filter(number_of_likes__gt=50).all()
#     posts_with_comments = Post.objects.filter(number_of_comments__lt=100).all()
#     valid_posts = set(list(posts_with_comments) + list(posts_with_likes))
#     return valid_posts


def fetch_comments_or_likes_with_q_6():
    posts = Post.objects.filter(
        Q(number_of_likes__gt=50) | Q(number_of_comments__lt=100)
    ).all()
    return posts


def find_question_in_title_and_description_7():
    post = Post.objects.filter(title__contains="?", description__contains="?").first()
    return post


def find_favorites_8(new: bool = False, hot: bool = False, question: bool = False):
    qs = Post.objects.all()
    if new:
        qs = qs.filter(pub_date__gte=date.today() - timedelta(days=30))
    if hot:
        qs = qs.filter(number_of_likes__gt=50)
    if question:
        qs = qs.filter(title__contains="?", description__contains="?")

    return qs
