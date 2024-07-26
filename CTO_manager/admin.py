from django.contrib import admin
from .models import Splitter, CtoPrimaria, CtoSecundaria, Cliente

# Register your models here.

class CtoSecundariaAdmin(admin.ModelAdmin):
    # class para exibir no admin somente os cliente da cada cto
    # 

    def get_form(self, request, obj=None, **kwargs):
        # Obtém o formulário padrão
        form = super().get_form(request, obj, **kwargs)

        # Personaliza o queryset dos clientes
        if obj:
            # Se estiver editando uma CTO secundária existente
            # Exibe apenas os clientes associados a essa CTO
            form.base_fields['clientes'].queryset = obj.clientes.all()
        else:
            # Se estiver criando uma nova CTO secundária
            # Exibe todos os clientes (ou personalize conforme necessário)
            pass

        return form

admin.site.register(Splitter)
admin.site.register(CtoPrimaria)
admin.site.register(CtoSecundaria, CtoSecundariaAdmin)
admin.site.register(Cliente)
