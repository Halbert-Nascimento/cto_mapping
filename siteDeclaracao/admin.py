from django.contrib import admin
from .models import Relationship, Fotos, TemporaryPageData, TemporaryPageImage

# Register your models here.

admin.site.register(Relationship)
admin.site.register(Fotos)
admin.site.register(TemporaryPageData)
admin.site.register(TemporaryPageImage)