import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from gql.types import Fruit


@strawberry.type
class Query:
    fruits: list[Fruit] = strawberry.django.field()


schema = strawberry.Schema(
    query=Query,
    extensions=[
        DjangoOptimizerExtension,  # not required, but highly recommended
    ],
)
