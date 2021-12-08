# https://intergalactic.radif.ru/
В этом проекте, кроме меня, участвовали рандомные участники. Целью проекта была отработка командного взаимодействия по методологии `Agile`, `SCRUM`. Посмотреть в `Trello` - https://trello.com/b/hzmUNlWf/itergalacticintertainment-копия-без-активности-и-участников Залогиниться от суперпользователя: login: intergalactic / password: intergalactic


Перед использованием проекта выполнить обновление пакетов из requirements.txt

#Консольные команды:
1. python manage.py fill_db - 
   1.1 наполнение данными бд на основе json файлов в
   папке json корня проекта.
   1.2 Создание суперюзера Username: intergalactic Password: intergalactic
   1.3 Создание юзера Username: user2 Password: user2
   1.4 Создание юзера Username: user3 Password: user3
2. python manage.py fill_db_win - для Windows, 
   2.1 автоматизация удаления бд, 
   2.2 создания и выполнения миграций, 
   2.3 наполнение бд на основе созданного ранее fill_db
3. По умолчанию с помощью ckeditor изображения в публикации могут добавлять только пользователи с ролью персонала (is_staff). Чтобы в свои публикации изображения могли добавлять    все залогиневшиеся пользователи, нужно сделать следующее: 
   3.1 В файлах библиотек зайти в site-packages\ckeditor_uploader\urls.py вместо staff_member_required прописать login_required, т.е. весь код заменить на:

       from future import absolute_import

       from django.conf.urls import url

       from django.contrib.admin.views.decorators import staff_member_required, login_required

       from django.views.decorators.cache import never_cache

       from . import views

       urlpatterns = [

       url(r"^upload/", login_required(views.upload), name="ckeditor_upload"),

       url(

           r"^browse/",
    
           never_cache(login_required(views.browse)),
    
           name="ckeditor_browse",
    
           ),
       ]

   3.2 В файле Lib\site-packages\django\contrib\admin\views\decorators.py добавить следующий код:

       def login_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='admin:login'):

       """

       Decorator for views that checks that the user is logged in, redirecting to the login page if necessary.

       """

       actual_decorator = user_passes_test(

        lambda u: u.is_active, # and u.is_staff,
 
        login_url=login_url,
 
        redirect_field_name=redirect_field_name
       )

       if view_func:

        return actual_decorator(view_func)
       return actual_decorator

   from django.conf.urls import url
   
   from django.contrib.admin.views.decorators import staff_member_required, login_required
   
   from django.views.decorators.cache import never_cache

   from . import views

   urlpatterns = [
   
       url(r"^upload/", login_required(views.upload), name="ckeditor_upload"),
       
       url(
       
           r"^browse/",
           
           never_cache(login_required(views.browse)),
           
           name="ckeditor_browse",
           
           ),
           
   ]
   
   3.2 В файле Lib\site-packages\django\contrib\admin\views\decorators.py добавить следующий код:
   
   def login_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                          login_url='admin:login'):
    
    """
    
    Decorator for views that checks that the user is logged in, redirecting to the login page if necessary.
    
    """
    
    actual_decorator = user_passes_test(
        
        lambda u: u.is_active, # and u.is_staff,
        
        login_url=login_url,
        
        redirect_field_name=redirect_field_name
        
    )
    
    if view_func:
    
        return actual_decorator(view_func)
        
    return actual_decorator
