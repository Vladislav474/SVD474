from django.db.models.signals import post_save
from django.dispatch import receiver
from bot.models import Material
from bot.vk_bot.vk_bot import VkBot

@receiver(post_save, sender=Material, dispatch_uid="my_id")
def my_handler(sender, **kwargs):
    obj = kwargs['instance']
    file_name = obj.file
    text = obj.text
    vk = VkBot()
    vk.distribution(file_name, text)