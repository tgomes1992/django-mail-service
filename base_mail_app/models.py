from django.db import models

# Create your models here.

class BaseEmail(models.Model):
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sender_mail = models.CharField(max_length=150)
    receipts_mail = models.CharField(max_length=150)
    attachment = models.FileField(upload_to='uploads')
    attachment_name = models.CharField(max_length=150)
    status = models.BooleanField(default=False)




