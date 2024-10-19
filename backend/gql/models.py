from django.db import models


class Fruit(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=20)


class Message(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    author = models.CharField(max_length=4)
    text = models.CharField(max_length=500)
