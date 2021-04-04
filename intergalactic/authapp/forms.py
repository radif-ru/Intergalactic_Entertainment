from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from authapp.models import IntergalacticUser
from django import forms


class IntergalacticUserLoginForm(AuthenticationForm):
    class Meta:
        model = IntergalacticUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(IntergalacticUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''


class IntergalacticUserRegisterForm(UserCreationForm):
    class Meta:
        model = IntergalacticUser
        fields = ('username', 'password1', 'password2', 'email', 'age')

    def __init__(self, *args, **kwargs):
        super(IntergalacticUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''


class IntergalacticUserEditForm(UserChangeForm):
    class Meta:
        model = IntergalacticUser
        fields = ('username', 'email', 'age', 'avatar', 'about', 'company')

    def __init__(self, *args, **kwargs):
        super(IntergalacticUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
