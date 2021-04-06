from django.shortcuts import render, get_object_or_404
from mainapp.models import Publication


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



