from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def unregistered_users_commands(bot: Bot):
	commands = [
		BotCommand(
			command='registration',
			description='Зареєструватися в боті'
		),
		BotCommand(
			command='check_availability',
			description='Перевірити наявність'
		)
	]

	await bot.set_my_commands(commands)


async def registered_users_commands(bot: Bot):
	await bot.delete_my_commands()
	commands = [
		BotCommand(
			command='create_order',
			description='Оформити замовлення'
		),
		BotCommand(
			command='check_availability',
			description='Перевірити наявність'
		),
		BotCommand(
			command='profile',
			description='Особистий кабінет'
		),
		BotCommand(
			command='requisites',
			description='Реквізити'
		)
	]

	await bot.set_my_commands(commands, BotCommandScopeDefault())
