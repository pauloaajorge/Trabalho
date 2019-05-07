from django.db import models


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=300)
    link = models.CharField(max_length=300)
    hora = models.CharField(max_length=10)
    imagem_jornal = models.CharField(max_length=900)

    def __str__(self):
        return self.title

'''
python manage.py makemigrations <your app name>
python manage.py migrate
python manage.py createsuperuser
'''