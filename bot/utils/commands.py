from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
	commands = [
		BotCommand(
			command='start',
			description='Початок роботи з ботом'
		),
		BotCommand(
			command='registration',
			description='Зареєструватися в боті'
		)
	]

	await bot.set_my_commands(commands, BotCommandScopeDefault())
