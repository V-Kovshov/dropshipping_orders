from typing import Callable, Any, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from bot.utils.db import check_user_in_db



class RegisterFilterMiddleware(BaseException):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            msg: Message,
            data: Dict[str, Any]
        ) -> Any:
        check_user = await check_user_in_db(msg.from_user.id)
        if not check_user:
            return await handler(msg, data)
        await msg.answer('Ви вже зареєстровані.')
