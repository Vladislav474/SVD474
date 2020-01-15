from django.test import TestCase
from bot.vk_bot import vk_bot
from bot.models import Theme, Material, upload_material_file_folder
from vk_api import vk_api
import random
import json


class TestModelMaterial:
    pass


class BotTest(TestCase):

    token = "205825285e79dc8a9e130bee96cd0791cf2ff835e55b8b5d0a04b03e17a1940d3cef5c40a81a08b30f0fa"
    test_id = '111993598'

    @classmethod
    def setUpTestData(cls):
        cls.vk = vk_api.VkApi(token=BotTest.token)
        cls.vk._auth_token()
        pass

    def setUp(self):
        pass

    def test_message_send_with_file_name_1(self):
        rnd = random.randint(1, 2147483647)
        test_object = vk_bot.VkBot()
        test_text = 'Тест'
        test_file_path = 'gg\gg.docx'
        test_file_name = 'gg.docx'
        test_object.vk_message_send(text=test_text, id=BotTest.test_id, file_name=test_file_path, rnd=rnd)

        res = self.vk.method("messages.getConversations", {"offset": 0,
                                                            "count": 1,
                                                            "filter": "all"})
        self.assertEquals(res['items'][0]["last_message"]['attachments'][0]['doc']['title'], test_file_name)

    def test_message_send_with_file_name_2(self):
        rnd = random.randint(1, 2147483647)
        test_object = vk_bot.VkBot()
        test_text = 'Тест'
        test_file_path = 'gsad\gsad.docx'
        test_file_name = 'gsad.docx'
        test_object.vk_message_send(text=test_text, id=BotTest.test_id, file_name=test_file_path, rnd=rnd)

        res = self.vk.method("messages.getConversations", {"offset": 0,
                                                            "count": 1,
                                                            "filter": "all"})
        self.assertEquals(res['items'][0]["last_message"]['attachments'][0]['doc']['title'] ,test_file_name)

    def test_message_send_with_bad_file_name(self):
        try:
            rnd = random.randint(1, 2147483647)
            test_object = vk_bot.VkBot()
            test_text = 'Тест'
            test_file_path = 'gsad\grf3sad.docx'
            test_object.vk_message_send(text=test_text, id=BotTest.test_id, file_name=test_file_path, rnd=rnd)

            res = self.vk.method("messages.getConversations", {"offset": 0,
                                                                "count": 1,
                                                                "filter": "all"})
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_message_send_empty_file_name(self):
        rnd = random.randint(1, 2147483647)
        test_object = vk_bot.VkBot()
        test_text = 'Тест'
        test_object.vk_message_send(text=test_text, id=BotTest.test_id, file_name='', rnd=rnd)

        res = self.vk.method("messages.getConversations", {"offset": 0,
                                                            "count": 1,
                                                            "filter": "all"})
        self.assertEquals(res['items'][0]["last_message"]['text'] , test_text)

    def test_callback_response_theme_empty(self):
        data = {
            "object": {
                "message": {
                    "from_id": BotTest.test_id,
                    "text": "Тест_"
                }
            }
        }
        vk_bot_test = vk_bot.VkBot()
        vk_bot_test.callback_response(data)
        res = self.vk.method("messages.getConversations", {"offset": 0,
                                                           "count": 1,
                                                           "filter": "all"})
        self.assertEquals(res['items'][0]["last_message"]['text'], "Данного предмета нет")

    def test_callback_response_material_empty(self):
        Theme.objects.create(name='test_obj_11')
        data = {
            "object": {
                "message": {
                    "from_id": BotTest.test_id,
                    "text": "test_obj_11"
                }
            }
        }
        vk_bot_test = vk_bot.VkBot()
        vk_bot_test.callback_response(data)
        res = self.vk.method("messages.getConversations", {"offset": 0,
                                                            "count": 1,
                                                            "filter": "all"})

        self.assertEquals(res['items'][0]["last_message"]['text'],
                          "Данных по test_obj_11 пока нет")

    def test_callback_response_with_test_object_1(self):
        Theme.objects.create(name='test_obj_1')
        test_object = TestModelMaterial()
        test_object.theme = Theme.objects.get(id=1)
        test_object.text = "gg"
        test_object.pub_date = '12.12.2020'
        Material.objects.create(theme=test_object.theme,
                                text=test_object.text,
                                pub_date=test_object.pub_date,
                                file=upload_material_file_folder(test_object, 'gg.docx'))
        data = {
            "object": {
                "message": {
                    "from_id": BotTest.test_id,
                    "text": "test_obj_1"
                }
            }
        }
        vk_bot_test = vk_bot.VkBot()
        vk_bot_test.callback_response(data)
        res = self.vk.method("messages.getConversations", {"offset": 0,
                                                            "count": 1,
                                                            "filter": "all"})

        self.assertEquals(res['items'][0]["last_message"]['text'],
                          "Все имеющиеся материалы по дисциплине test_obj_1 предоставлены")

    def test_callback_response_with_test_object_2(self):
        Theme.objects.create(name='test_obj_2')
        test_object = TestModelMaterial()
        test_object.theme = Theme.objects.get(id=1)
        test_object.text = "gg"
        test_object.pub_date = '12.12.2020'
        Material.objects.create(theme=test_object.theme,
                                text=test_object.text,
                                pub_date=test_object.pub_date,
                                file=upload_material_file_folder(test_object, 'gg.docx'))
        data = {
            "object": {
                "message": {
                    "from_id": BotTest.test_id,
                    "text": "test_obj_2"
                }
            }
        }
        vk_bot_test = vk_bot.VkBot()
        vk_bot_test.callback_response(data)
        res = self.vk.method("messages.getConversations", {"offset": 0,
                                                            "count": 1,
                                                            "filter": "all"})

        self.assertEquals(res['items'][0]["last_message"]['text'],
                          "Все имеющиеся материалы по дисциплине test_obj_2 предоставлены")

    def test_get_keyboard_empty_base(self):
        test_name = []
        res = vk_bot.VkBot.get_keyboard()
        res = json.loads(res)
        self.assertEquals(res["buttons"], test_name)

    def test_get_keyboard_with_test_object_1(self):
        test_name = 'test_obj_1'
        Theme.objects.create(name=test_name)
        res = vk_bot.VkBot.get_keyboard()
        res = json.loads(res)
        self.assertEquals(res["buttons"][0][0]["action"]["label"], test_name)

    def test_get_keyboard_with_test_object_2(self):
        test_name_1 = 'test_obj_1'
        test_name_2 = 'test_obj_2'
        Theme.objects.create(name=test_name_1)
        Theme.objects.create(name=test_name_2)
        res = vk_bot.VkBot.get_keyboard()
        res = json.loads(res)
        self.assertEquals(res["buttons"][0][0]["action"]["label"], test_name_1)
        self.assertEquals(res["buttons"][1][0]["action"]["label"], test_name_2)

    def test_get_keyboard_with_test_object_3(self):
        test_name_1 = 'test_obj_1'
        test_name_2 = 'test_obj_2'
        test_name_3 = 'test_obj_3'
        Theme.objects.create(name=test_name_1)
        Theme.objects.create(name=test_name_2)
        Theme.objects.create(name=test_name_3)
        res = vk_bot.VkBot.get_keyboard()
        res = json.loads(res)
        self.assertEquals(res["buttons"][0][0]["action"]["label"], test_name_1)
        self.assertEquals(res["buttons"][1][0]["action"]["label"], test_name_2)
        self.assertEquals(res["buttons"][2][0]["action"]["label"], test_name_3)

