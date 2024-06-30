from django.contrib import admin
from .models import Splitter, CtoPrimaria, CtoSecundaria, Cliente

# Register your models here.

admin.site.register(Splitter)
admin.site.register(CtoPrimaria)
admin.site.register(CtoSecundaria)
admin.site.register(Cliente)