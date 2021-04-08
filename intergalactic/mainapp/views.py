from django.shortcuts import render, get_object_or_404
from mainapp.models import Publication, PublicationCategory


def main(request):
    publication_list =Publication.objects.order_by('-created')
    content = {
        'title': 'главная',
        'publication_list': publication_list,
    }
    return render(request, 'mainapp/index.html', content)


def publication_page(request, pk):
    context = {
        'page_title': 'Publication',
        'publication': get_object_or_404(Publication, pk=pk)
    }
    return render(request, 'mainapp/publication.html', context)


def category_page(request, pk):
    links = PublicationCategory.objects.filter(is_active=True)

    if pk:
        category = get_object_or_404(PublicationCategory, pk=pk)
        publications = Publication.objects.filter(category_id=pk, is_active=True,
                                                  category__is_active=True).order_by('created')
        title = category.name
        context = {
            'links': links,
            'title': title,
            'publications': publications
        }
        return render(request, 'mainapp/publication_category.html', context)
