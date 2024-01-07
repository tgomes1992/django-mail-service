from django.apps import AppConfig


class BaseMailAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_mail_app'
