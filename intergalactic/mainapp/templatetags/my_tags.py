import re
from django import template
from django.conf import settings

from mainapp.models import UserRatings, ArticleRatings

register = template.Library()


def media_folder_publications(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    publications_images/product1.jpg --> /media/publications_images/product1.jpg
    """
    if not string:
        string = 'publications_images/default.png'

    return f'{settings.MEDIA_URL}{string}'


register.filter('media_folder_publications', media_folder_publications)


@register.filter(name='is_liked')
def is_liked(publication, pk):
    return publication.is_liked(pk)


@register.filter(name='media_folder_users')
def media_folder_users(string):
    if not string:
        string = 'users_avatars/default.jpg'

    if bool(re.match('https', str(string))):
        return f'{string}'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='tag_to_user')
def tag_to_user(comment, to_comments):
    # print(comment.pk)
    for to_comment in to_comments:
        # print(comment.pk, to_comment.for_comment.pk, to_comment.to_user)
        if comment.pk == to_comment.comment.pk:
            return to_comment.to_user
    return False


@register.filter(name='average_author_rating')
def average_author_rating(pk):
    return UserRatings.average_author_rating(pk)


@register.filter(name='average_pub_rating')
def average_pub_rating(pk):
    return ArticleRatings.average_pub_rating(pk)
