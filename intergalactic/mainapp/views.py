import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from mainapp.models import Publication, PublicationCategory, Likes, Dislikes, \
    Comments, ToComments, ArticleRatings, UserRatings, ViewCounter

from django.db.models import Count

from authapp.models import IntergalacticUser
from itertools import chain

from mainapp.forms import CreatePublicationForm, ToPublishForm
from .decorators import counted


def get_notifications(user):
    notifications = chain(
        Likes.objects.filter(user_id=user.id, is_read=False),
        Comments.objects.filter(
            receiver=user.id, is_read=False))
    return list(notifications)


def get_comments(pk):
    return Comments.objects.filter(publication=pk)


def get_ratings():
    return [2, 4, 6, 8, 10]


def take_trendy_publication_id_list(category_pk):
    if category_pk == 0:
        trendy_publication_id_counts = Likes.objects.filter(status=1).values(
            "publication_id").annotate(Count("id"))
    else:
        trendy_publication_id_counts = Likes.objects.filter(
            publication_id__category_id=category_pk, status=1).values(
            "publication_id").annotate(Count("id"))

    trendy_publication_id_counts = sorted(trendy_publication_id_counts,
                                          key=lambda x: x['id__count'],
                                          reverse=True)
    id_list = []
    for vocabulary in trendy_publication_id_counts:
        id_list.append(vocabulary["publication_id"])
    return id_list


def take_now_read_publication_id_list(category_pk):
    if category_pk == 0:
        now_read_publication_id_counts = Comments.objects.values(
            "publication").annotate(Count("id"))
    else:
        now_read_publication_id_counts = Comments.objects.filter(
            publication__category_id=category_pk).values(
            "publication").annotate(Count("id"))

    now_read_publication_id_counts = sorted(now_read_publication_id_counts,
                                            key=lambda x: x['id__count'],
                                            reverse=True)
    id_list = []
    for vocabulary in now_read_publication_id_counts:
        id_list.append(vocabulary["publication"])
    return id_list


def main(request):
    categories = PublicationCategory.objects.filter(is_active=True)
    print(request)
    trendy_id_list = take_trendy_publication_id_list(0)
    now_read_id_list = take_now_read_publication_id_list(0)
    get_request_sort = {
        'date': Publication.objects.filter(is_active=True,
                                           category__is_active=True).order_by(
            '-created'),
        'like': [Publication.objects.get(id=i) for i in trendy_id_list],
        'comment': [Publication.objects.get(id=i) for i in now_read_id_list]
    }
    try:
        publications = get_request_sort[request.GET['sort']]
    except:
        publications = Publication.objects.filter(is_active=True,
                                                  category__is_active=True).order_by(
            '-created')

    trendy_publications = [Publication.objects.get(id=trendy_id_list[i]) for i
                           in range(4)]

    now_read_publications = [Publication.objects.get(id=now_read_id_list[i])
                             for i in range(5)]

    notifications = get_notifications(request.user)

    content = {
        'categories': categories,
        'title': 'главная',
        'publications': publications,
        'trendy_publications': trendy_publications,
        'now_read_publications': now_read_publications,
        'notifications': notifications,
    }

    return render(request, 'mainapp/index.html', content)


@counted
def publication_page(request, pk):
    publication = Publication.objects.get(pk=pk)
    categories = PublicationCategory.objects.filter(is_active=True)
    comments = get_comments(pk)
    likes = Likes.objects.all()
    notifications = get_notifications(request.user)

    now_read_id_list = take_now_read_publication_id_list(0)
    now_read_publications = [Publication.objects.get(id=now_read_id_list[i])
                             for i in range(5)]

    to_comments = ToComments.objects.all()

    # Получение количества просмотров для конкретной публикации из таблицы
    count = ViewCounter.objects.get(publication_id=pk)

    user_pub_rating = 0
    average_pub_rating = ArticleRatings.average_pub_rating(pk)

    user_author_rating = 0
    average_author_rating = UserRatings.average_author_rating(
        publication.user.pk)

    if request.user.is_authenticated:
        try:
            user_pub_rating = ArticleRatings.article_ratings(pk).get(
                user=request.user).rating
        except Exception as e:
            print(e)
            user_pub_rating = 0

        try:
            user_author_rating = UserRatings.objects.filter(
                user=request.user).get(
                author=publication.user).rating
        except Exception as e:
            print(e)
            user_author_rating = 0

    context = {
        'page_title': 'Publication',
        'categories': categories,
        'publication': get_object_or_404(Publication, pk=pk),
        'comments': comments,
        'likes': likes,
        'now_read_publications': now_read_publications,
        'notifications': notifications,

        'count': count.count,

        'to_comments': to_comments,

        'user_pub_rating': user_pub_rating,
        'average_pub_rating': average_pub_rating,
        'user_author_rating': user_author_rating,
        'average_author_rating': average_author_rating,
        'ratings': get_ratings()

    }
    return render(request, 'mainapp/publication.html', context)


def category_page(request, pk):
    categories = PublicationCategory.objects.filter(is_active=True)

    now_read_id_list = take_now_read_publication_id_list(0)
    now_read_publications = [Publication.objects.get(id=now_read_id_list[i])
                             for i in range(5)]

    if pk is not None:
        if pk == 0:
            title = 'Все потоки'
            trendy_id_list = take_trendy_publication_id_list(0)
            now_read_id_list = take_now_read_publication_id_list(0)

            get_request_sort = {
                'date': Publication.objects.filter(is_active=True,
                                                   category__is_active=True).order_by(
                    '-created'),
                'like': [Publication.objects.get(id=i) for i in
                         trendy_id_list],
                'comment': [Publication.objects.get(id=i) for i in
                            now_read_id_list]
            }
            try:
                publications = get_request_sort[request.GET['sort']]
            except:
                publications = Publication.objects.filter(is_active=True,
                                                          category__is_active=True).order_by(
                    'created')

        else:
            category = get_object_or_404(PublicationCategory, pk=pk)
            trendy_id_list = take_trendy_publication_id_list(pk)
            now_read_id_list = take_now_read_publication_id_list(pk)

            get_request_sort = {
                'date': Publication.objects.filter(category_id=pk,
                                                   is_active=True,
                                                   category__is_active=True).order_by(
                    'created'),
                'like': [Publication.objects.get(id=i) for i in
                         trendy_id_list],
                'comment': [Publication.objects.get(id=i) for i in
                            now_read_id_list]
            }
            try:
                publications = get_request_sort[request.GET['sort']]
            except:
                publications = Publication.objects.filter(category_id=pk,
                                                          is_active=True,
                                                          category__is_active=True).order_by(
                    'created')

            title = category.name

        notifications = get_notifications(request.user)

        context = {
            'pk': pk,
            'categories': categories,
            'title': title,
            'publications': publications,
            'now_read_publications': now_read_publications,
            'notifications': notifications,

        }
        return render(request, 'mainapp/publication_category.html', context)


def comment(request):
    data = dict()
    if request.method == 'POST':
        message = request.POST.get('message')
        if message != '':
            if request.user.is_authenticated:
                print('POST_DATA', request.POST,
                      request.POST.get('publication_id'))
                user = IntergalacticUser.objects.get(username=request.user)
                publication = Publication.objects.get(
                    id=request.POST.get('publication_id'))
                receiver = publication.user

                new_comments_obj = Comments.objects.create(
                    publication=publication,
                    user=user,
                    description=message,
                    receiver=receiver)
                comments = Comments.objects.filter(publication=publication)

                comment_id = request.POST.get('comment_id')
                comment_user_id = request.POST.get('comment_user_id')

                if comment_id and comment_user_id:
                    comment_id_obj = Comments.objects.get(id=comment_id)
                    comment_user_id_obj = IntergalacticUser.objects.get(
                        id=comment_user_id)

                    new_to_comments_obj = ToComments.objects.create(
                        comment=new_comments_obj,
                        to_user=comment_user_id_obj,
                        for_comment=comment_id_obj)

                to_comments = ToComments.objects.all()

                data['form_is_valid'] = True
                data['form_html'] = render_to_string(
                    'mainapp/includes/inc_comments.html',
                    {'comments': comments, 'to_comments': to_comments},
                    request=request)

            else:
                data['form_is_valid'] = 'AnonymousUser'
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)
    else:
        return HttpResponse("Invalid request")


def like(request, id, pk, model_type):
    data = dict()
    model = Likes if model_type == 'like' else Dislikes
    if request.is_ajax():
        if request.user.is_authenticated:
            publication = Publication.objects.get(id=id)
            sender = IntergalacticUser.objects.get(username=request.user)
            receiver = IntergalacticUser.objects.get(id=pk)
            try:
                model = model.objects.get(sender_id=sender,
                                          publication_id=publication)
                data['plus'] = False if model.status else True
                changed = model.change_status()
            except:
                changed = model.create(user=receiver, sender=sender,
                                       publication=publication)
                data['plus'] = True
            data['minus'] = True if changed else False
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


def notification_read(request, pk, name):
    if name == 'like':
        like = Likes.objects.get(id=pk)
        like.is_read = True
        like.save()
    elif name == 'comment':
        comment = Comments.objects.get(id=pk)
        comment.is_read = True
        comment.save()

    notifications = get_notifications(request.user)

    return JsonResponse({'length': len(notifications)})


def create_publication(request):
    if request.method == 'POST':
        create_publication_form = CreatePublicationForm(request.POST,
                                                        request.FILES)
        if create_publication_form.is_valid():
            instance = create_publication_form.save(commit=False)
            instance.user = request.user  # подстановка в форму создания статьи залогиневшегося пользователя
            instance.is_active = 0
            instance.save()
            # return HttpResponseRedirect(reverse('main:publication_page'))
            return publication_page(request, pk=instance.id)
    else:
        create_publication_form = CreatePublicationForm()

    context = {
        'page_title': 'пользователи/создание',
        'create_publication_form': create_publication_form,
    }

    return render(request, 'mainapp/create_publication.html', context)


class IndexView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'mainapp/personal_area.html'
    model = Publication
    context_object_name = 'publications_list'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user.pk)

    def test_func(self):
        return self.request.user.is_active

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('main:main'))


def edit_publication(request, pk):
    publ = get_object_or_404(Publication, pk=pk)
    if request.method == 'POST':
        update_publication_form = CreatePublicationForm(request.POST,
                                                        request.FILES,
                                                        instance=publ)
        if update_publication_form.is_valid():
            instance = update_publication_form.save(commit=False)
            instance.is_active = 0
            instance.save()
            return publication_page(request, pk=instance.id)
    else:
        update_publication_form = CreatePublicationForm(instance=publ)

    context = {
        'page_title': 'пользователи/создание',
        'update_publication_form': update_publication_form,
    }

    return render(request, 'mainapp/edit_publication.html', context)


def to_publish(request, pk):
    publ = get_object_or_404(Publication, pk=pk)
    views = get_object_or_404(ViewCounter, publication_id=pk)
    if request.method == 'POST':
        to_publish_form = ToPublishForm(request.POST, request.FILES,
                                        instance=publ)
        if to_publish_form.is_valid():
            instance = to_publish_form.save(commit=False)
            if request.user.is_staff:
                instance.is_active = True
                instance.on_moderator_check = False

            else:
                instance.on_moderator_check = True

            instance.save()
            # Обнуление количества просмотров статьи в момент опубликования
            views.count = 0
            views.save()
            return HttpResponseRedirect(reverse('main:main'))
    else:
        to_publish_form = ToPublishForm(instance=publ)

    context = {
        'to_publish_form': to_publish_form,
    }

    return render(request, 'mainapp/to_publish.html', context)


def admin_room(request):
    users_list = IntergalacticUser.objects.order_by("id")
    if request.method == 'POST':
        user = get_object_or_404(IntergalacticUser, pk=request.POST['pk'])
        to_publish_form = ToPublishForm(request.POST, request.FILES,
                                        instance=user)
        if to_publish_form.is_valid():
            instance = to_publish_form.save(commit=False)
            if 'is_staff' in request.POST.keys():
                print(request.POST)
                instance.is_staff = request.POST['is_staff']
            if 'is_active' in request.POST.keys():
                print(request.POST)
                instance.is_active = request.POST['is_active']
            instance.save()
            return HttpResponseRedirect(reverse('main:admin_room'))
    context = {
        'users_list': users_list
    }
    return render(request, 'mainapp/admin_room.html', context)


def moderator_room(request):
    publications_list = Publication.objects.filter(is_active=False,
                                                   on_moderator_check=True).order_by(
        '-created')
    if request.method == 'POST':
        print(request.POST)
        publ = get_object_or_404(Publication, pk=request.POST['pk'])
        if request.method == 'POST':
            to_publish_form = ToPublishForm(request.POST, request.FILES,
                                            instance=publ)
            if to_publish_form.is_valid():
                instance = to_publish_form.save(commit=False)
                instance.is_active = False
                instance.on_moderator_check = False
                instance.moderator_refuse = instance.moderator_refuse + '<h5>Отказ в публикации.</h5> ' \
                                            '<p>Нарушены правила №: '

                for i in range(5):
                    rule = f'rule{i + 1}'
                    if rule in request.POST.keys():
                        if request.POST[rule] == 'selected':
                            instance.moderator_refuse = instance.moderator_refuse + f'{i + 1}; '
                instance.moderator_refuse = instance.moderator_refuse + f'</p> <p>Дополнительный комментарий: {request.POST["reason"]}</p><hr>'
                instance.save()
                return HttpResponseRedirect(reverse('main:moderator_room'))

    context = {
        "publications_list": publications_list
    }
    return render(request, 'mainapp/moderator_room.html', context)


@csrf_exempt
def user_pub_rating(request):
    data = dict()
    if request.method == 'POST':
        user_pub_rat = request.POST.get('user_pub_rating')
        pub_id = request.POST.get('pub_id')

        author_id = request.POST.get('author_id')
        if user_pub_rat != '' and pub_id != 0:
            if request.user.is_authenticated:

                article_ratings = ArticleRatings.article_ratings(pk=pub_id)

                user_pub_rating = 0
                try:
                    user_pub_rating = article_ratings.get(
                        user=request.user).rating
                except Exception as e:
                    print(e)
                    user_pub_rating = 0
                if int(user_pub_rat) == int(user_pub_rating):
                    user_pub_rat = 0

                if not article_ratings.filter(user=request.user):
                    article_ratings.create(
                        publication=Publication.objects.get(pk=pub_id),
                        user=IntergalacticUser.objects.get(pk=request.user.pk),
                        rating=user_pub_rat
                    )
                else:
                    article_ratings.filter(user=request.user).update(
                        rating=user_pub_rat)

                average_pub_rating = ArticleRatings.average_pub_rating(
                    pk=pub_id)

                average_author_rating = UserRatings.average_author_rating(
                    pk=author_id)

                data['form_is_valid'] = True
                data['user_pub_rating'] = user_pub_rat
                data['average_pub_rating'] = average_pub_rating

                data['average_author_rating'] = average_author_rating
            else:
                data['form_is_valid'] = 'AnonymousUser'
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)
    else:
        return HttpResponse("Invalid request")


@csrf_exempt
def author_rating(request):
    data = dict()
    if request.method == 'POST':
        user_author_rating = request.POST.get('user_author_rating')
        author_id = request.POST.get('author_id')

        if user_author_rating != '' and author_id != 0:
            if request.user.is_authenticated:
                user_ratings = UserRatings.objects.filter(author_id=author_id)

                user_author_rating_old = 0
                try:
                    user_author_rating_old = UserRatings.objects.filter(
                        user=request.user).get(
                        author=IntergalacticUser.objects.get(
                            pk=author_id)).rating
                except Exception as e:
                    print(e)
                    user_author_rating_old = 0

                if int(user_author_rating) == int(user_author_rating_old):
                    user_author_rating = 0

                if not user_ratings.filter(user=request.user):
                    user_ratings.create(
                        author=IntergalacticUser.objects.get(pk=author_id),
                        user=IntergalacticUser.objects.get(pk=request.user.pk),
                        rating=user_author_rating
                    )
                else:
                    user_ratings.filter(user=request.user).update(
                        rating=user_author_rating)

                average_author_rating = UserRatings.average_author_rating(
                    pk=author_id)

                data['form_is_valid'] = True
                data['user_author_rating'] = user_author_rating
                data['average_author_rating'] = average_author_rating
            else:
                data['form_is_valid'] = 'AnonymousUser'
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)
    else:
        return HttpResponse("Invalid request")
