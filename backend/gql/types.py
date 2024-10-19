import strawberry_django

from . import models


@strawberry_django.type(models.Fruit)
class Fruit:
    id: int
    name: str
    color: str


@strawberry_django.type(models.Message)
class Message:
    id: int
    author: int
    text: str
