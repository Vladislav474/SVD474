from django.db import models

# Create your models here.


class Theme(models.Model):

    name = models.CharField('Дисциплина', max_length=255)

    def __str__(self):
        return self.name


def upload_material_file_folder(instance, filename):
    filename = instance.text + '.' + filename.split('.')[-1]
    return "{}/{}".format(instance.text, filename)


class Material(models.Model):

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    text = models.CharField('Описание', max_length=255)
    pub_date = models.DateTimeField('Дата публикации', auto_now=True)
    file = models.FileField('Материал', upload_to=upload_material_file_folder)

    def __str__(self):
        return self.text
