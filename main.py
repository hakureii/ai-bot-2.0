import os
import json
import asyncio
import discord
from groq import Groq
from discord.ext import commands


intents = discord.Intents.all()
bot = commands.Bot(["* "], intents=intents)
client = Groq(api_key=os.getenv("GROQ"))
model = "llama-3.1-70b-versatile"

with open("./ai_history.json") as file:
    default_history = json.load(file)

def update_history(message:str, history:list, role: str = "user"):
    history.append(
        {
            "role": role,
            "content": message
        }
    )
    return history

def fix_discord_message(message: str):
    # fix the discord embed issues.
    special_syms = ["*", "_", "-", "~", "#"]
    fixed_message = ""
    for char in message:
        if char in special_syms:
            fixed_message += "\\" + char
        else:
            fixed_message += char
    # fix overlapping size for discord limit
    return fixed_message.split(".\n")

global ai_mode, ai_channels
ai_channels = {}

@bot.command(name="ai")
async def ai(ctx: commands.Context):
    chan_id = ctx.channel.id
    if len(ai_channels) >= 1:
        if chan_id in ai_channels:
            ai_channels.pop(chan_id)
            await ctx.reply("disabled!")
            return
    ai_channels[chan_id] = default_history
    await ctx.reply("enabled!")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot or message.author == bot.user:
        return
    if message.content.startswith("* "):
        await bot.process_commands(message)
        return
    if message.channel.id in ai_channels:
        await message.channel.trigger_typing()
        response = client.chat.completions.create(model=model,messages=update_history(message.content, ai_channels[message.channel.id]), max_tokens=512)
        update_history(response.choices[0].message.content, ai_channels[message.channel.id], "assistant")
        for chunk in fix_discord_message(response.choices[0].message.content):
            await message.channel.send(content=chunk)

@bot.command(name="update")
async def update(ctx: commands.Context):
    await ctx.send("-# Soon™")
    await bot.close()

@bot.event
async def on_ready():
    await asyncio.sleep(5 * 60 * 60)
    os.remove(os.environ["CONDITION"])
    await bot.close()

bot.run(os.getenv("TOKEN"))
