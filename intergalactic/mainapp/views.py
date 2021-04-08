from django.shortcuts import render, get_object_or_404
from mainapp.models import Publication, PublicationCategory


def main(request):
    categories = PublicationCategory.objects.filter(is_active=True)
    publication_list =Publication.objects.filter(is_active=True, category__is_active=True).order_by('-created')
    content = {
        'categories': categories,
        'title': 'главная',
        'publication_list': publication_list,
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
