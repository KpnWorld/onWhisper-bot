import discord
from discord.ext import commands
import os

# Enable necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True  

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Managing your server!"))

# Run bot using GitHub Secret
TOKEN = os.getenv("DISCORD_BOT_TOKEN")  
bot.run(TOKEN)
