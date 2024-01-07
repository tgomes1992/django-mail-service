from django.http import JsonResponse
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from .models import BaseEmail
from .serializers import BaseEmailSerializer,UploadSerializer
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from .MailSender import GmailFileSender

# Create your views here.


def enviar_email(request):
    emails = BaseEmail.objects.filter(status=False)
    mailSender = GmailFileSender()

    if len(emails) == 0:
        return JsonResponse({'status': 'Não há e-mails aguardando o envio'})

    for email in emails:
        try:
            print (email.attachment)
            mailSender.send_email(email.receipts_mail,email.subject , email.body , email.attachment.path )
            email.status = True
            email.save()
        except Exception as e:
            print (e)
            continue
    return JsonResponse({'status': 'E-mails enviados com sucesso'})


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