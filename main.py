import argparse
from bot_registry import get_bot
from telegram_bot import TelegramBot
from discord_bot import DiscordBot
import bots  # Register all bots here
import yaml
from dotenv import load_dotenv
import os

load_dotenv()


def load_config(config_file: str) -> dict:
    """Load configuration from a YAML file."""
    with open(config_file, "r") as f:
        return yaml.safe_load(f)


def get_default_config(bot_type: str) -> dict:
    config_path = f"bots/{bot_type}/config.yaml"
    if os.path.exists(config_path):
        return load_config(config_path)
    else:
        raise FileNotFoundError(
            f"Default config file not found for bot type: {bot_type}"
        )


def create_and_run_bot(
    bot_type: str, bot_token: str, platform: str, bot_config: dict, user_id: any = None
):
    bot_class = get_bot(bot_type)
    if not bot_class:
        raise ValueError(f"Unsupported bot type: {bot_type}")
    bot_instance = bot_class(bot_config, bot_token, user_id)

    if platform.lower() == "telegram":
        client = TelegramBot(bot_instance)
    elif platform.lower() == "discord":
        client = DiscordBot(bot_instance)
    else:
        raise ValueError(f"Unsupported platform: {platform}")

    client.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a bot on a chosen platform")
    parser.add_argument(
        "--platform",
        type=str,
        default="telegram",
        help="Platform to run the bot on (telegram or discord)",
    )
    parser.add_argument(
        "--bot", type=str, required=True, help="Bot type to load (e.g., persona)"
    )
    parser.add_argument(
        "--bot_token",
        type=str,
        required=True,
        help="Bot token to use for authentication",
    )
    parser.add_argument("--config-yaml", type=str, required=False)
    args = parser.parse_args()
    if args.config_yaml:
        bot_config = load_config(args.config_yaml)
    else:
        bot_config = get_default_config(args.bot)

    create_and_run_bot(args.bot, args.bot_token, args.platform, bot_config)
