from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.utils.db import Order

order = Order()


class GetSizeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        call: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        model_id = int(call.data)
        sizes = await order.get_model_sizes(model_id=model_id)
        data['sizes'] = []
        async for size in sizes:
            data['sizes'].append(size)
        return await handler(call, data)
