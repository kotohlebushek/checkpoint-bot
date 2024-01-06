from environs import Env
from dataclasses import dataclass

@dataclass
class Bot:
    bot_token: str

@dataclass
class Settings:
    bot: Bot

def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bot=Bot(
            bot_token=env.str("TOKEN")
        )
    )

settings = get_settings('input')