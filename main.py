import os
import discord
from ai import Ai
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix=[], intents=intents)

bot = Bot()
ai = Ai()

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.channel == bot.get_channel(1270529190533271582):
        await message.reply(ai.response(message.content))

bot.run(os.getenv("TOKEN"))
