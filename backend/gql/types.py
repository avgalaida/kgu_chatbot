import strawberry_django

from . import models


@strawberry_django.type(models.Fruit)
class Fruit:
    id: int
    name: str
    color: str
