from django import template
from django.conf import settings

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
