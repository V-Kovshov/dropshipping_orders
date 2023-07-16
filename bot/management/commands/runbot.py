from django.core.management.base import BaseCommand

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from bot.handlers.users import start
from bot.config import settings

import logging


async def start_bot(bot: Bot) -> None:
	await bot.send_message(settings.bots.admin_id[0], f"Bot ran!")


async def end_bot(bot: Bot) -> None:
	await bot.send_message(settings.bots.admin_id[0], f"Bot finished!")


async def run():
	bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
	storage = RedisStorage.from_url('redis://localhost:6379/0')
	dp = Dispatcher(storage=storage)

	dp.startup.register(start_bot)
	dp.shutdown.register(end_bot)

	dp.include_router(start.router)

	try:
		await dp.start_polling(bot)
	except Exception:
		await bot.session.close()


class Command(BaseCommand):
	help = 'RIN COMMAND: python manage.py runbot'

	def handle(self, *args, **options):
		asyncio.run(run())



# logging.basicConfig(level=logging.INFO,
# 					format='%(filename)s -> [LINE:%(lineno)d] -> %(levelname)-8s [%(asctime)s] -> %(message)s',
# 					filename=f'logs.log',
# 					filemode='w')
