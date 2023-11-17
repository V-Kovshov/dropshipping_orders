from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
	bot_token: str
	admin_id: list


@dataclass
class DB:
	user: str
	database: str
	password: str


@dataclass
class NovaPost:
	api: str
	phone: str


@dataclass
class Settings:
	bots: Bots
	db: DB
	post: NovaPost


def get_settings() -> Settings:
	env = Env()
	env.read_env()

	bot_token = env.str('BOT_TOKEN')
	admins_list = env.list('ADMIN_ID')

	user_db = env.str('USER_DB')
	database_name = env.str('DATABASE_NAME')
	password_db = env.str('PASSWORD_DB')

	api_key = env.str('API_KEY_NOVA_POST')
	phone_number = env.str('PHONE_NUMBER')

	return Settings(
		bots=Bots(
			bot_token=bot_token,
			admin_id=admins_list,
		),
		db=DB(
			user=user_db,
			database=database_name,
			password=password_db
		),
		post=NovaPost(
			api=api_key,
			phone=phone_number
		)
	)


settings = get_settings()
