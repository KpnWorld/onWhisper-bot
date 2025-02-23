import discord
from discord.ext import commands, tasks
import os
import asyncio
import random
import logging
from db.bot import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the bot owner's ID from environment variable
owner_id = int(os.getenv("OWNER_ID"))  # Retrieve owner ID from environment variable
logger.info(f"✅ Owner ID (from env): {owner_id}")

# Create bot instance with owner_id
bot = commands.Bot(command_prefix="?", intents=discord.Intents.all(),case_sensitive=True,help_command=None, owner_id=owner_id)

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

async def start_change_activity():
    await bot.wait_until_ready()

async def load_cogs():
    try:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                logger.info(f"🔄 Loading cog: {filename}")  # Debug log
                await bot.load_extension(f"cogs.{filename[:-3]}")
        logger.info("✅ All cogs loaded successfully!")
    except Exception as e:
        logger.error(f"❌ Error loading cogs: {e}")
    init_db()  # Initialize the database (e.g., creating tables, setting up initial data)

@bot.event
async def on_ready():
    init_db()  # Initialize the database
    await load_cogs()  # Load cogs before syncing commands
    logger.info(f"✅ Logged in as {bot.user}")

    await bot.change_presence(activity=random.choice(activities))  # Set initial presence
    try:
        synced = await bot.tree.sync()
        logger.info(f"Slash commands synced: {len(synced)} commands")
    except Exception as e:
        logger.error(f"Failed to sync command(s): {e}")

    if not change_activity.is_running():
        await start_change_activity()  # Start the loop only once

# Custom owner check
def is_owner(interaction: discord.Interaction) -> bool:
    return interaction.user.id == owner_id

@bot.tree.command(name="check_cogs", description="Check which cogs are currently loaded")
@discord.app_commands.check(is_owner)
async def check_cogs(interaction: discord.Interaction):
    """
    Slash command for the bot owner to check which cogs are currently loaded.
    
    Usage: /check_cogs
    """
    logger.info("check_cogs command executed")  # Debug print to verify command execution
    cogs = [cog for cog in bot.cogs]
    logger.info(f"Loaded cogs: {cogs}")  # Debug log to verify loaded cogs
    embed = discord.Embed(title="Online Cogs", description=f"🟢 Online cogs: {', '.join(cogs)}", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="list_commands", description="List all registered commands")
async def list_commands(interaction: discord.Interaction):
    """
    Slash command to list all registered commands.
    
    Usage: /list_commands
    """
    commands = [command.name for command in bot.commands]
    await interaction.response.send_message(f"Registered commands: {', '.join(commands)}")

async def main():
    async with bot:
        token = os.getenv("DISCORD_BOT_TOKEN")
        if token is None:
            logger.error("Error: DISCORD_BOT_TOKEN environment variable not set.")
            return
        logger.info("🚀 Starting bot...")
        await bot.start(token)
        await start_change_activity()  # Start the activity change loop

if __name__ == "__main__":
    logger.info("🚀 Starting bot...")
    asyncio.run(main())  # Properly start the bot asynchronously
