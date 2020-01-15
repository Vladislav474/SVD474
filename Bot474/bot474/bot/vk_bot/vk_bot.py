from django.core.exceptions import ObjectDoesNotExist
from bot474.settings import MEDIA_ROOT
from vk_api import vk_api
import random
import requests
import json
from bot.models import Theme, Material


class DoesNotFill(Exception):
   pass


class VkBot():

    token = "205825285e79dc8a9e130bee96cd0791cf2ff835e55b8b5d0a04b03e17a1940d3cef5c40a81a08b30f0fa"

    def __init__(self):
        self.vk = vk_api.VkApi(token=VkBot.token)
        self.vk._auth_token()

    @staticmethod
    def get_button(type, label, color, payload={}):
        return {
             "action": {
                    "type": type,
                    "payload": json.dumps(payload),
                    "label": label
                },
                "color": color
        }

    @staticmethod
    def get_keyboard():

        keyboard = {
            "one_time": False,
            "buttons": []
        }

        for theme in Theme.objects.all():
            keyboard["buttons"].append([VkBot.get_button(type="text",
                                                   label=theme.name,
                                                   color="positive",
                                                   payload={"button":"{}".format(theme.name)})])

        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def callback_response(self, data):
        try:
            id = str(data['object']['message']['from_id'])
            theme = str(data['object']['message']['text'])
            theme_id = Theme.objects.get(name=theme).id
            materials = Material.objects.filter(theme=theme_id)
            if materials.count() == 0:
                raise DoesNotFill("Данных по {} пока нет".format(theme))

            for material in materials:
                rnd = random.randint(1, 2147483647)
                self.vk_message_send(id=id,file_name=material.file,text=material.text,rnd=rnd)

            rnd = random.randint(1, 2147483647)
            self.vk_message_send(id=id,
                                 rnd=rnd,
                                 text="Все имеющиеся материалы по дисциплине {} предоставлены"
                                 .format(theme))

        except ObjectDoesNotExist:
            rnd = random.randint(1, 2147483647)
            self.vk_message_send(id=id, text="Данного предмета нет", rnd=rnd)
        except DoesNotFill as e:
            rnd = random.randint(1, 2147483647)
            self.vk_message_send(id=id, text=e, rnd=rnd)

    def distribution(self, file_name, text):
        # Получение списка бесед
        messages = self.vk.method("messages.getConversations", {"offset": 0,
                                                               "count": 20,
                                                               "filter": "all"})
        for num in range(messages["count"]):
            # Получение id получателя
            rnd = random.randint(1, 2147483647)
            id = messages["items"][num]["last_message"]["peer_id"]
            self.vk_message_send(text=text, id=id, file_name=file_name, rnd=rnd)

    def vk_message_send(self, text, id, rnd, file_name=''):
        # Если имя файла по какой-либо причине не передано
        if file_name == '':
            self.vk.method("messages.send", {"user_id": id,
                                            "message": text,
                                            "random_id": rnd,
                                            "keyboard": VkBot().get_keyboard()
                                            })
        else:
            # Запрос адреса на который будет загружен файл
            file = self.vk.method("docs.getMessagesUploadServer", {"type": "doc",
                                                                   "peer_id": str(id)})["upload_url"]
            file_path = MEDIA_ROOT + str(file_name)
            # Отправка и сохранение файла на сервере
            response = requests.post(file, files={"file": open(file_path, "rb")}).json()
            res = self.vk.method("docs.save", {'file': response['file']})

            # Отправка сообщения
            self.vk.method("messages.send", {"user_id": id,
                                            "message": text,
                                            "random_id": rnd,
                                            "keyboard": VkBot().get_keyboard(),
                                            "attachment": 'doc' + str(id) + '_' + str(res['doc']['id'])})