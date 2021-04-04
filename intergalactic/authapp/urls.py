from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.Login.as_view(), name='login'),
    path('logout/', authapp.Logout.as_view(), name='logout'),
    path('register/', authapp.Registration.as_view(), name='register'),
    path('edit/', authapp.Profile.as_view(), name='profile'),
]
