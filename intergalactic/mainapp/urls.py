from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('publication/<int:pk>', mainapp.publication_page, name='publication_page'),
    path('category/<int:pk>', mainapp.category_page, name='category'),
    path('comment/', mainapp.comment, name='comment'),
    path('like/<int:id>/<int:pk>', mainapp.like, name='like'),
    path('notification_read/<int:pk>/<name>', mainapp.notification_read, name='notification_read'),
    path('create_publication/', mainapp.create_publication, name='create_publication'),
    path('personality/', mainapp.IndexView.as_view(extra_context={'title': 'Личный кабинет'}), name='personality'),
    path('edit_publication/<int:pk>', mainapp.edit_publication, name='edit_publication'),
    path('to_publish/<int:pk>', mainapp.to_publish, name='to_publish'),
]
