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

# Load all cogs in the 'cogs' folder
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

# Load specific extensions
for ext in ["cogs.moderation", "cogs.fun", "cogs.info"]:
    try:
        bot.load_extension(ext)
        print(f"✅ Loaded {ext}")
    except Exception as e:
        print(f"❌ Failed to load {ext}: {e}")

@bot.event
async def on_ready():
    await load_cogs()  # Load cogs before syncing commands
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Managing your server!"))
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync command(s): {e}")

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Run bot using GitHub Secret
bot.run(TOKEN)
