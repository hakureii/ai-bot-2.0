import os
import asyncio
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
async def om_ready():
    await asyncio.sleep(5*60*60)
    os.remove(os.environ["CONDITIION"])
    await bot.close()

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.content.startswith("."):
        if message.content == ".update":
            await bot.close()
        if message.content == ".newmem":
            ai.new_memory()
            return
    if message.channel == bot.get_channel(1270529190533271582):
        await message.reply(content=ai.response(message.content)[:2000])

bot.run(os.getenv("TOKEN"))
