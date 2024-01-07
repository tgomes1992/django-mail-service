from .models import BaseEmail
from rest_framework.serializers import Serializer, FileField,ModelSerializer

class BaseEmailSerializer(ModelSerializer):
    class Meta:
        model = BaseEmail
        fields = ['subject', 'sender_mail', 'body' ,  'receipts_mail', 'attachment_name', "attachment"]




# Serializers define the API representation.
class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']