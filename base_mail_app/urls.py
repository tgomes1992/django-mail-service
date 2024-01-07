from django.urls import path ,include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'upload', UploadView, basename="upload")


urlpatterns = [
    path('e_mails/', BaseEmailListCreateView.as_view(), name='listar_emails'),
    path('', include(router.urls)),
    path('enviar/' ,enviar_email , name="enviar_emails"  )
]