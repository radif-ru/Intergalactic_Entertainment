import os
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from mainapp.models import Publication, PublicationCategory, Likes, Comments, \
    ToComments
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

        IntergalacticUser.objects.all().delete()

        if not IntergalacticUser.objects.filter(
                username='intergalactic').exists():
            # создать суперюзера
            IntergalacticUser.objects.create_superuser(
                username='intergalactic',
                email='admin@intergalactic.local',
                password='intergalactic',
                age='30')

        if not IntergalacticUser.objects.filter(username='user').exists():
            # создать обычный экземпляр моделей, без особенных свойств
            # (обычного пользователя)
            IntergalacticUser.objects.create_user(
                username='user',
                email='user@gintergalactic.local',
                password='user',
                age='25')

        if not IntergalacticUser.objects.filter(username='user2').exists():
            IntergalacticUser.objects.create_user(
                username='user2',
                email='user2@gintergalactic.local',
                password='user2',
                age='32')

        if not IntergalacticUser.objects.filter(username='user3').exists():
            IntergalacticUser.objects.create_user(
                username='user3',
                email='user3@gintergalactic.local',
                password='user3',
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
            # Заменяем id категории объектом
            publication['fields']['category'] = _category

            user_name = publication['fields']['user']
            # Получаем юзера по имени
            _user = IntergalacticUser.objects.get(id=user_name)
            # Заменяем id юзера объектом
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
            # Заменяем id комментария объектом
            comment['fields']['publication'] = _publication

            user_name = comment['fields']['user']
            # Получаем юзера по имени
            _user = IntergalacticUser.objects.get(id=user_name)
            # Заменяем id юзера объектом
            comment['fields']['user'] = _user

            sender = comment['fields']['receiver']
            _sender = IntergalacticUser.objects.get(id=sender)
            comment['fields']['receiver'] = _sender

            new_comments = Comments(**{'id': comment['pk']},
                                    **comment['fields'])
            new_comments.save()

        to_comments = load_from_json('mainapp_tocomments')
        ToComments.objects.all().delete()
        for to_comment in to_comments:
            comment = to_comment['fields']['comment']
            # Получаем комментарий по id
            _comment = Comments.objects.get(id=comment)
            # Заменяем id комментария объектом
            to_comment['fields']['comment'] = _comment

            to_user = to_comment['fields']['to_user']
            # Получаем пользователя по id
            _to_user = IntergalacticUser.objects.get(id=to_user)
            # Заменяем пользователя объектом
            to_comment['fields']['to_user'] = _to_user

            for_comment = to_comment['fields']['for_comment']
            _for_comment = Comments.objects.get(id=for_comment)
            to_comment['fields']['for_comment'] = _for_comment

            new_to_comments = ToComments(**{'id': to_comment['pk']},
                                         **to_comment['fields'])
            new_to_comments.save()

        likes = load_from_json('mainapp_likes')
        Likes.objects.all().delete()
        for like in likes:
            publication_name = like['fields']['publication_id']
            # Получаем категорию по имени
            _publication = Publication.objects.get(id=publication_name)
            # Заменяем id публикации объектом
            like['fields']['publication_id'] = _publication

            user_name = like['fields']['user_id']
            # Получаем юзера по имени
            _user = IntergalacticUser.objects.get(id=user_name)
            # Заменяем имя юзера объектом
            like['fields']['user_id'] = _user

            sender = like['fields']['sender_id']
            _sender = IntergalacticUser.objects.get(id=sender)
            like['fields']['sender_id'] = _sender

            new_likes = Likes(**{'id': like['pk']},
                              **like['fields'])
            new_likes.save()
