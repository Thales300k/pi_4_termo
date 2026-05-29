from django.contrib import admin
from .models import DispositivoESP, LeituraSensor, PrevisaoClimatica

@admin.register(DispositivoESP)
class DispositivoESPAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'localizacao', 'ativo', 'criado_em')
    search_fields = ('nome', 'codigo', 'localizacao')
    list_filter = ('ativo',)

@admin.register(LeituraSensor)
class LeituraSensorAdmin(admin.ModelAdmin):
    list_display = ('dispositivo', 'temperatura', 'umidade', 'pressao', 'chuva', 'criado_em')
    list_filter = ('dispositivo', 'criado_em')

@admin.register(PrevisaoClimatica)
class PrevisaoClimaticaAdmin(admin.ModelAdmin):
    list_display = ('leitura', 'condicao', 'probabilidade_chuva', 'alerta', 'criado_em')
    list_filter = ('condicao', 'alerta', 'criado_em')
