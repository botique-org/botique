import discord
from discord.ext import commands
import aiohttp
import io
import inspect


class DiscordBot(commands.Bot):
    def __init__(self, bot_instance, command_prefix="!", intents=None):
        if intents is None:
            intents = discord.Intents.default()
            intents.messages = True
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.bot_instance = bot_instance
        self.bot_token = bot_instance.bot_token

    async def on_ready(self):
        print(f"We have logged in as {self.user}")

    async def send_image_response(self, channel, image_url=None, image_bytes=None):
        try:
            if image_url:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as resp:
                        if resp.status == 200:
                            image_bytes = await resp.read()
                        else:
                            raise Exception(f"HTTP error {resp.status}")
            if image_bytes:
                file = discord.File(fp=io.BytesIO(image_bytes), filename="response.png")
                await channel.send(file=file)
            else:
                await channel.send("Failed to generate or fetch image.")
        except Exception as e:
            await channel.send(f"Error sending image: {e}")

    async def on_message(self, message):
        if message.author.bot:
            return

        if (
            message.channel.type != discord.ChannelType.private
            and self.user not in message.mentions
        ):
            return

        content = message.content
        if self.user in message.mentions:
            content = (
                content.replace(f"<@{self.user.id}>", "")
                .replace(f"@{self.user.name}", "")
                .strip()
            )

        if inspect.iscoroutinefunction(self.bot_instance.process_message):
            response = await self.bot_instance.process_message(content)
        else:
            response = self.bot_instance.process_message(content)

        if isinstance(response, dict) and (
            "image_url" in response or "image_bytes" in response
        ):
            await self.send_image_response(
                message.channel,
                image_url=response.get("image_url"),
                image_bytes=response.get("image_bytes"),
            )
        else:
            await message.channel.send(response)

        await self.process_commands(message)

    def run(self):
        super().run(self.bot_token)
