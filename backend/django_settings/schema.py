from typing import Tuple

import strawberry
from chat.bot import respond
from chat.rec import recognize
from chat.speech import generate_speech


@strawberry.type
class Query:
    @strawberry.field
    def respond(self, text: str) -> Tuple[str, str]:
        return respond(text)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def upload_audio(self, audio_data: str) -> str:
        return recognize(audio_data)

    @strawberry.mutation
    def generate_speech(self, text: str, speaker: str) -> str:
        return generate_speech(text, speaker)


schema = strawberry.Schema(query=Query, mutation=Mutation)
