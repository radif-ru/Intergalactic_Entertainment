from django.urls import reverse_lazy

from authapp.forms import IntergalacticUserLoginForm, IntergalacticUserRegisterForm, \
    IntergalacticUserEditForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import UpdateView, CreateView

from authapp.models import IntergalacticUser


class Login(LoginView):
    form_class = IntergalacticUserLoginForm
    template_name = 'authapp/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context


class Logout(LogoutView):
    next_page = '/'


class Registration(CreateView):
    form_class = IntergalacticUserRegisterForm
    template_name = 'authapp/registration.html'
    success_url = reverse_lazy('auth:login')


class Profile(UpdateView):
    model = IntergalacticUser
    template_name = 'authapp/edit.html'
    success_url = reverse_lazy('auth:profile')
    form_class = IntergalacticUserEditForm

    def get_object(self, queryset=None):
        return IntergalacticUser.objects.get(pk=self.request.user.pk)
