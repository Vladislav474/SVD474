from django.apps import AppConfig

class BotConfig(AppConfig):
    name = 'bot'

    def ready(self):
        from .signals.handlers import post_save