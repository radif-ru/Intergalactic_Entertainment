from mainapp.models import Publication
from django import forms


class CreatePublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('category', 'name', 'image', 'short_desc', 'text')

    def __init__(self, *args, **kwargs):
        super(CreatePublicationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''
