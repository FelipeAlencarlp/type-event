from django.urls import path
from . import views

urlpatterns = [
    path('novo_evento/', views.novo_evento, name="novo_evento"),
    path('gerenciar_evento/', views.gerenciar_evento, name="gerenciar_evento"),
    path('inscrever_evento/<int:evento_id>', views.inscrever_evento, name="inscrever_evento"),
    path('participantes_evento/<int:evento_id>', views.participantes_evento, name="participantes_evento"),
    path('gerar_csv/<int:evento_id>/', views.gerar_csv, name="gerar_csv"),
    path('certificados_evento/<int:evento_id>/', views.certificados_evento, name="certificados_evento"),
    path('gerar_certificado/<int:evento_id>/', views.gerar_certificado, name="gerar_certificado"),
    path('procurar_certificado/<int:evento_id>/', views.procurar_certificado, name="procurar_certificado"),
]