from django.contrib import admin

from mainapp.models import Publication, PublicationCategory

admin.site.register(Publication)
admin.site.register(PublicationCategory)
