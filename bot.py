import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import asyncio
import logging 
import random

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Grab environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
TEST_MODE = os.getenv("TEST_MODE", "true").lower() == "true"
OWNER_ID = os.getenv("OWNER_ID")
logger.info(f"✅ Determined Test mode: {TEST_MODE}")
logger.info(f"✅ Grabbed Owner ID: {OWNER_ID}")

# Create Bot instance
intents = discord.Intents.all()
if OWNER_ID is not None:
    owner_id = int(OWNER_ID)
else:
    owner_id = None
bot = commands.Bot(command_prefix=".", intents=intents, owner_id=owner_id, help_command=None)

# List of activities
activities = [
    discord.Game(name="Managing your server!"),
    discord.Game(name="Moderating chats!"),
    discord.Game(name="Analyzing data!"),
    discord.Game(name="Version 1.0.0 is coming soon!"),
]

@tasks.loop(minutes=5)
async def change_activity():
    if TEST_MODE:
        activity = discord.Game(name="Testing in progress...")
    else:
        activity = random.choice(activities)
    logger.info(f"🎮 Changing activity to: {activity}")
    await bot.change_presence(activity=activity)

@change_activity.before_loop
async def before_change_activity():
    await bot.wait_until_ready()

# On Ready event
@bot.event
async def on_ready():
    if TEST_MODE:
        print("Running in TEST MODE!")
        await bot.change_presence(activity=discord.Game(name="Testing in progress..."))
    else:
        await bot.change_presence(activity=discord.Game(name="Online!"))

    change_activity.start()  # Start the activity loop when the bot is ready
    print(f"Logged in as {bot.user}")

@bot.event
async def on_disconnect():
    logger.warning("Bot has been disconnected!")

# Reconnect logic
@tasks.loop(minutes=1)
async def ensure_connection():
    if bot.is_closed():
        logger.warning("Bot is closed, attempting to reconnect...")
        await bot.start(TOKEN)

async def main():
    async with bot:
        # Load cogs
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                extension = f"cogs.{filename[:-3]}"
                if extension not in bot.extensions:
                    await bot.load_extension(extension)

        # Ensure the owner cog is loaded
        if "cogs.owner" not in bot.extensions:
            await bot.load_extension("cogs.owner")
        
        # Ensure the logs cog is loaded
        if "cogs.logs" not in bot.extensions:
            await bot.load_extension("cogs.logs")
        
        # Start the ensure_connection loop
        ensure_connection.start()

        # Run the bot with the token
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
