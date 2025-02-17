import discord
from discord.ext import commands
import os
import config
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True  # Needed for moderation features

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Managing your server!"))

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

async def main():
    async with bot:
        await load_cogs()  # ✅ Load extensions before running the bot
        await bot.start(config.TOKEN)  # ✅ Use bot.start instead of bot.run

asyncio.run(main())
