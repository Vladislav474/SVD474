from django.test import TestCase
from django.db.models import signals
# Create your tests here.

from bot.models import Theme, Material, upload_material_file_folder


class TestModelMaterial:
     pass


class BdTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        signals.post_save.disconnect(sender=Material, dispatch_uid="my_id")
        Theme.objects.create(name='test_obj_1')
        test_object = TestModelMaterial()
        test_object.theme = Theme.objects.get(id=1)
        test_object.text = "Тест"
        test_object.pub_date='12.12.2020'
        Material.objects.create(theme=test_object.theme ,
                                text=test_object.text,
                                pub_date=test_object.pub_date,
                                file=upload_material_file_folder(test_object, 'Вкусная_еда.docx'))
        pass

    def setUp(self):
        pass

    def test_theme_get(self):
            test_object = Theme.objects.get(id=1).name
            self.assertEquals(test_object, 'test_obj_1')

    def test_theme_label(self):
            test_object = Material.objects.get(id=1)
            field_label = test_object._meta.get_field('theme').verbose_name
            self.assertEquals(field_label, 'theme')

    def test_text_get(self):
        test_object = Material.objects.get(id=1).text
        self.assertEquals(test_object, 'Тест')

    def test_text_label(self):
            test_object = Material.objects.get(id=1)
            field_label = test_object._meta.get_field('text').verbose_name
            self.assertEquals(field_label, 'Описание')

    def test_text_max_length(self):
            test_object = Material.objects.get(id=1)
            max_length = test_object._meta.get_field('text').max_length
            self.assertEquals(max_length, 255)

    def test_upload_material_file_folder_1(self):
            # This will also fail if the urlconf is not defined.
            test_object = TestModelMaterial()
            test_object.theme = Theme.objects.get(id=1)
            test_object.text = "Тест1"
            test_object.pub_date = '12.12.2020'
            self.assertEquals(upload_material_file_folder(test_object, 'Вкусная_еда.docx'), 'Тест1/Тест1.docx')

    def test_upload_material_file_folder_2(self):
            # This will also fail if the urlconf is not defined.
            test_object = TestModelMaterial()
            test_object.theme = Theme.objects.get(id=1)
            test_object.text = "Тест2"
            test_object.pub_date = '12.12.2020'
            self.assertEquals(upload_material_file_folder(test_object, 'Вкусная_еда.docx'), 'Тест2/Тест2.docx')

    def test_upload_material_file_folder_3(self):
            # This will also fail if the urlconf is not defined.
            test_object = TestModelMaterial()
            test_object.theme = Theme.objects.get(id=1)
            test_object.text = "Тест3"
            test_object.pub_date = '12.12.2020'
            self.assertEquals(upload_material_file_folder(test_object, 'Вкусная_еда.docx'), 'Тест3/Тест3.docx')