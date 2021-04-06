from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('publication/<int:pk>', mainapp.publication_page, name='publication_page'),
]
