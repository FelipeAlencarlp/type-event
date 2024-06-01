from django.urls import path
from . import views

urlpatterns = [
    path('novo_evento/', views.novo_evento, name="novo_evento"),
]