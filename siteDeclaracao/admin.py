from django.contrib import admin
from .models import Relationship, Fotos, TemporaryPageData, TemporaryPageImage, PageRelationship, PageRelationshipImage, DataUserPayment

# Register your models here.

admin.site.register(DataUserPayment)
admin.site.register(PageRelationship)
admin.site.register(PageRelationshipImage)

admin.site.register(Relationship)
admin.site.register(Fotos)
admin.site.register(TemporaryPageData)
admin.site.register(TemporaryPageImage)