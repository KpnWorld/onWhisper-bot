import discord
from discord.ext import commands
import os
import config

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True  # Needed for moderation features

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Managing your server!"))

# Automatically load cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(config.TOKEN)
