from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
	bot_token: str
	admin_id: list


@dataclass
class Settings:
	bots: Bots


def get_settings() -> Settings:
	env = Env()
	env.read_env()

	bot_token = env.str('BOT_TOKEN')
	admins_list = env.list('ADMIN_ID')

	return Settings(bots=Bots(
		bot_token=bot_token,
		admin_id=admins_list
	))


settings = get_settings()
