from django.shortcuts import render, get_object_or_404
from mainapp.models import Publication, PublicationCategory, Likes, Comments
from django.db.models import Count
import operator


def take_trendy_publication_id_list():
    trendy_publication_id_counts = Likes.objects.values("publication_id").annotate(Count("id"))
    trendy_publication_id_counts = sorted(trendy_publication_id_counts, key=lambda x: x['id__count'], reverse=True)
    id_list = []
    for vocabulary in trendy_publication_id_counts:
        id_list.append(vocabulary["publication_id"])
    return id_list


def take_publications_list_of_dict(publications_list):
    publications_list_of_dict = []
    for publication in publications_list:
        likes = Likes.objects.filter(publication_id=publication).count()
        comments = Comments.objects.filter(publication=publication).count()
        publications_list_of_dict.append({"publication": publication, "likes": likes, "comments": comments})
    return publications_list_of_dict


def main(request):
    categories = PublicationCategory.objects.filter(is_active=True)

    publication_list = Publication.objects.filter(is_active=True, category__is_active=True).order_by('-created')
    publication_list_of_dict = take_publications_list_of_dict(publication_list)

    trendy_id_list = take_trendy_publication_id_list()
    trendy_publication_list = [
        Publication.objects.get(id=trendy_id_list[0]),
        Publication.objects.get(id=trendy_id_list[1]),
        Publication.objects.get(id=trendy_id_list[2]),
        Publication.objects.get(id=trendy_id_list[3])
    ]
    trendy_publication_list_of_dict = take_publications_list_of_dict(trendy_publication_list)

    content = {
        'categories': categories,
        'title': 'главная',
        'publication_list_of_dict': publication_list_of_dict,
        'trendy_publication_list_of_dict': trendy_publication_list_of_dict
    }
    return render(request, 'mainapp/index.html', content)


def publication_page(request, pk):
    categories = PublicationCategory.objects.filter(is_active=True)
    context = {
        'page_title': 'Publication',
        'categories': categories,
        'publication': get_object_or_404(Publication, pk=pk)
    }
    return render(request, 'mainapp/publication.html', context)


def category_page(request, pk):
    categories = PublicationCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == 0:
            title = 'Все потоки'
            publications = Publication.objects.filter(is_active=True, category__is_active=True).order_by('created')
        else:
            category = get_object_or_404(PublicationCategory, pk=pk)
            publications = Publication.objects.filter(category_id=pk, is_active=True,
                                                      category__is_active=True).order_by('created')
            title = category.name
        context = {
            'categories': categories,
            'title': title,
            'publications': publications
        }
        return render(request, 'mainapp/publication_category.html', context)
