import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True  # Ensure privileged intents are enabled

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")  # ✅ Ensure this is awaited

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Managing your server!"))
    await load_cogs()  # ✅ Ensure cogs are loaded before syncing commands
    await bot.tree.sync()
    print("✅ Slash commands synced.")

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
