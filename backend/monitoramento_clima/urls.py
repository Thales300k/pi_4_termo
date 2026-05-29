from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from monitoramento_clima.clima.api import router as clima_router

api = NinjaAPI(title='API Monitoramento Climático ESP32')
api.add_router('/clima/', clima_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
