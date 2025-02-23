import discord
from discord.ext import commands, tasks
import os
import asyncio
import random
import time
import logging
import signal
from db.bot import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

# Set the bot owner's ID from environment variable
owner_id = os.getenv("OWNER_ID")
if owner_id is None:
    logger.error("❌ ERROR: OWNER_ID environment variable not set!")
    exit(1)
owner_id = int(owner_id)  # Ensure it's an integer
logger.info(f"✅ Owner ID (from env): {owner_id}")  # Debugging owner ID

# Create bot instance
bot = commands.Bot(command_prefix="!onWhisper ", intents=intents, owner_id=owner_id)

# List of activities
activities = [
    discord.Game(name="Managing your server!"),
    discord.Game(name="Moderating chats!"),
    discord.Game(name="Analyzing data!"),
    discord.Game(name="Version 1.0.0 is coming soon!"),
]

# Change activity periodically
@tasks.loop(minutes=5)
async def change_activity():
    new_activity = random.choice(activities)
    logger.info(f"🎮 Changing activity to: {new_activity.name}")  # Debug log
    await bot.change_presence(activity=new_activity)

async def load_cogs():
    """Loads all cogs from the 'cogs' directory."""
    try:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                logger.info(f"🔄 Loading cog: {filename}")  # Debug log
                await bot.load_extension(f"cogs.{filename[:-3]}")
        logger.info("✅ All cogs loaded successfully!")
    except Exception as e:
        logger.error(f"❌ Error loading cogs: {e}")
        raise

@bot.event
async def on_ready():
    """Event triggered when the bot is ready."""
    try:
        init_db()  # Initialize the database
        await load_cogs()  # Load cogs

        logger.info(f"✅ Logged in as {bot.user}")

        await bot.change_presence(activity=random.choice(activities))  # Set initial presence

        # Sync slash commands
        start_time = time.time()
        try:
            synced = await bot.tree.sync()
            end_time = time.time()
            logger.info(f"✅ Slash commands synced: {len(synced)} commands in {end_time - start_time:.2f} seconds")
        except Exception as e:
            logger.error(f"❌ Failed to sync commands: {e}")

        # Start the activity loop if not running
        if not change_activity.is_running():
            change_activity.start()

    except Exception as e:
        logger.error(f"❌ Error during on_ready: {e}")

# Graceful shutdown handling
def shutdown_signal_handler(sig, frame):
    logger.info("🛑 Shutdown signal received. Cleaning up and shutting down...")
    asyncio.create_task(bot.close())

signal.signal(signal.SIGTERM, shutdown_signal_handler)
signal.signal(signal.SIGINT, shutdown_signal_handler)

@bot.tree.command(name="check_cogs", description="Check which cogs are currently loaded")
@discord.app_commands.checks.is_owner()
async def check_cogs(interaction: discord.Interaction):
    """Slash command for the bot owner to check which cogs are loaded."""
    logger.info("✅ check_cogs command executed")  # Debug print
    cogs = [cog for cog in bot.cogs]
    embed = discord.Embed(title="Online Cogs", description=f"🟢 Online cogs: {', '.join(cogs)}", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="list_commands", description="List all registered commands")
async def list_commands(interaction: discord.Interaction):
    """Slash command to list all registered bot commands."""
    commands_list = [command.name for command in bot.commands]
    await interaction.response.send_message(f"📜 Registered commands: {', '.join(commands_list)}")

async def main():
    """Starts the bot."""
    try:
        token = os.getenv("DISCORD_BOT_TOKEN")
        if token is None:
            logger.error("❌ ERROR: DISCORD_BOT_TOKEN environment variable not set!")
            return
        logger.info("🚀 Starting bot...")
        await bot.start(token)
    except Exception as e:
        logger.error(f"❌ Error starting the bot: {e}")

if __name__ == "__main__":
    logger.info("🚀 Starting bot...")
    asyncio.run(main())

