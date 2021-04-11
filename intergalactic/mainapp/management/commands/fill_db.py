import os
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from mainapp.models import Publication, PublicationCategory, Likes, Comments
from authapp.models import IntergalacticUser


def load_from_json(file_name):
    with open(
            os.path.join(settings.JSON_PATH, f'{file_name}.json'),
            encoding='utf-8'
    ) as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):
        if not IntergalacticUser.objects.filter(username='intergalactic').exists():
            # создать суперюзера
            IntergalacticUser.objects.create_superuser(username='intergalactic',
                                                       email='admin@intergalactic.local',
                                                       password='intergalactic',
                                                       age='30')

        if not IntergalacticUser.objects.filter(username='user').exists():
            # создать обычный экземпляр моделей, без особенных свойств
            # (обычного пользователя)
            IntergalacticUser.objects.create(username='user',
                                    email='user@gintergalactic.local',
                                    password='user',
                                    age='33')

        categories = load_from_json('mainapp_publicationcategory')
        PublicationCategory.objects.all().delete()
        [PublicationCategory.objects.create(
            **{'id': category['pk']}, **category['fields'])
            for category in categories]

        publications = load_from_json('mainapp_publication')
        Publication.objects.all().delete()
        for publication in publications:
            category_name = publication['fields']['category']
            # Получаем категорию по имени
            _category = PublicationCategory.objects.get(id=category_name)
            # Заменяем название категории объектом
            publication['fields']['category'] = _category

            user_name = publication['fields']['user']
            # Получаем юзера по имени
            _user = IntergalacticUser.objects.get(id=user_name)
            # Заменяем имя юзера объектом
            publication['fields']['user'] = _user

            new_publications = Publication(
                **{'id': publication['pk']}, **publication['fields'])
            new_publications.save()

        comments = load_from_json('mainapp_comments')
        Comments.objects.all().delete()
        for comment in comments:
            publication_name = comment['fields']['publication']
            # Получаем публикацию по имени
            _publication = Publication.objects.get(id=publication_name)
            # Заменяем название комментария объектом
            comment['fields']['publication'] = _publication

            user_name = comment['fields']['user']
            # Получаем юзера по имени
            _user = IntergalacticUser.objects.get(id=user_name)
            # Заменяем имя юзера объектом
            comment['fields']['user'] = _user

            new_comments = Comments(**{'id': comment['pk']},
                                    **comment['fields'])
            new_comments.save()

        likes = load_from_json('mainapp_likes')
        Likes.objects.all().delete()
        for like in likes:
            publication_name = like['fields']['publication_id']
            # Получаем категорию по имени
            _publication = Publication.objects.get(id=publication_name)
            # Заменяем название публикации объектом
            like['fields']['publication_id'] = _publication

            user_name = like['fields']['user_id']
            # Получаем юзера по имени
            _user = IntergalacticUser.objects.get(id=user_name)
            # Заменяем имя юзера объектом
            like['fields']['user_id'] = _user

            new_likes = Likes(**{'id': like['pk']},
                              **like['fields'])
            new_likes.save()
