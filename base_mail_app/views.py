import json

from django.http import JsonResponse
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from .models import BaseEmail
from .serializers import BaseEmailSerializer,UploadSerializer
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from MailSender import GmailFileSender
from MqConfigs import RabbitMQHandler

# Create your views here.


def enviar_email(request):
    emails = BaseEmail.objects.filter(status=False)
    mailSender = GmailFileSender()

    if len(emails) == 0:
        return JsonResponse({'status': 'Não há e-mails aguardando o envio'})

    for email in emails:
        try:
            mailSender.send_email(email.receipts_mail,email.subject , email.body , email.attachment.path )
            email.status = True
            email.save()
        except Exception as e:
            print (e)
            continue
    return JsonResponse({'status': 'E-mails enviados com sucesso'})


def enviar_emails_fila(request):
    emails = BaseEmail.objects.all()
    rabbitSender = RabbitMQHandler("emails_a_enviar", "e_mails")

    rabbitSender.connect()

    for item in emails:
        rabbitSender.publish_message(message=json.dumps(BaseEmailSerializer(item).data, indent=2))

    return JsonResponse({'status': 'E-mails enviados para a Fila de processamento'})


def get_messages_from_qeue(request):
    rabbitSender = RabbitMQHandler("emails_a_enviar", "e_mails")

    rabbitSender.connect()

    messages = rabbitSender.get_queue_message_count()


    return JsonResponse({'status': f"Pendentes de envio {messages}"})


class BaseEmailListCreateView(generics.ListCreateAPIView):
    queryset = BaseEmail.objects.all()
    serializer_class = BaseEmailSerializer
    parser_classes = [MultiPartParser, FormParser , FileUploadParser]


class UploadView(ViewSet):

    serializer_class = UploadSerializer


    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        content_type = file_uploaded.content_type
        response = "POST API and you have uploaded a {} file".format(content_type)
        print (file_uploaded.name)
        return Response(response)