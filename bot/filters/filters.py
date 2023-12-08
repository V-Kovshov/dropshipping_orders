from typing import Any
from aiogram.types import Message
from aiogram.filters import BaseFilter

from bot.utils.db import check_user_in_db


class RegisterUserFilter(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        check_user = await check_user_in_db(msg.from_user.id)
        if not check_user:
            return True
        else:
            await msg.answer('Ви вже зареєстровані.')
            return False
