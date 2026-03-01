import os

from aiogram import Dispatcher
from dotenv import load_dotenv
from gigachat import GigaChatAsyncClient, Chat, Messages, MessagesRole

from bot_logic.ai_roles import ROLES

load_dotenv()

_GIGACHAT_CLIENT = GigaChatAsyncClient(
    credentials=os.getenv("GIGA_API_KEY"),
    scope="GIGACHAT_API_PERS",
    model="GigaChat-2",
    ca_bundle_file="./certs/cert.pem",
)

async def get_gigachat_response(user_text: str, role=str):
    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.SYSTEM,
                content=ROLES.get(role, "emoji")["prompt"],
            ),
            Messages(role=MessagesRole.USER, content=user_text),
        ]
    )

    response = await _GIGACHAT_CLIENT.achat(payload=payload)

    return response.choices[0].message.content