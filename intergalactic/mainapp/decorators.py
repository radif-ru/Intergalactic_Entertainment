from functools import wraps
from django.db.models import F
from django.db import transaction
from mainapp.models import ViewCounter, Publication


# декоратор для подсчета количество просмотров статей (прибавляется при каждой перезагрузке страницы)
def counted(f):
    @wraps(f)
    def decorator(request, *args, **kwargs):
        with transaction.atomic():
            url = request.path
            if url == '/create_publication/':
                obj = Publication.objects.latest('id')
                publ_id_of_url = obj.id
                counter, created = ViewCounter.objects.get_or_create(publication_id=publ_id_of_url)
                counter.count = F('count') + 1
                counter.save()
            else:
                try:
                    publ_id_of_url = int(url[13:])
                except ValueError:
                    publ_id_of_url = int(url[18:])
                counter, created = ViewCounter.objects.get_or_create(publication_id=publ_id_of_url)
                counter.count = F('count') + 1
                counter.save()
        return f(request, *args, **kwargs)
    return decorator