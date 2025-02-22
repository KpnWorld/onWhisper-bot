import discord
from discord.ext import commands, tasks
import os
import asyncio
import random
from db.bot import init_db

# Enable necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

# Create bot instance
bot = commands.Bot(command_prefix="!onWhisper ", intents=intents)

# List of activities
activities = [
    discord.Game(name="Managing your server!"),
    discord.Game(name="Moderating chats!"),
    discord.Game(name="Analyzing data!"),
    discord.Game(name="Having fun with commands!"),
]

# Change activity periodically
@tasks.loop(minutes=5)
async def change_activity():
    new_activity = random.choice(activities)
    print(f"🎮 Changing activity to: {new_activity.name}")  # Debug log
    await bot.change_presence(activity=new_activity)

async def start_change_activity():
    await bot.wait_until_ready()
async def load_cogs():
    try:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
    except Exception as e:
        print(f"Error loading cogs: {e}")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
    init_db()  # Initialize the database (e.g., creating tables, setting up initial data)
@bot.event
async def on_ready():
    init_db()  # Initialize the database
    await load_cogs()  # Load cogs before syncing commands
    print(f"✅ Logged in as {bot.user}")

    await bot.change_presence(activity=random.choice(activities))  # Set initial presence
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync command(s): {e}")

    if not change_activity.is_running():
        await start_change_activity()  # Start the loop only once

@bot.command(name="check_cogs")
@commands.is_owner()
async def check_cogs(ctx):
    """
    Command for the bot owner to check which cogs are currently loaded.
    
    Usage: !onWhisper check_cogs
    """
    cogs = [cog for cog in bot.cogs]
    embed = discord.Embed(title="Online Cogs", description=f"🟢 Online cogs: {', '.join(cogs)}", color=discord.Color.green())
    await ctx.send(embed=embed)

async def main():
    async with bot:
        token = os.getenv("DISCORD_BOT_TOKEN")
        if token is None:
            print("Error: DISCORD_BOT_TOKEN environment variable not set.")
            return
        await bot.start(token)
        await start_change_activity()  # Start the activity change loop
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    print("Starting bot...")
    asyncio.run(main())  # Properly start the bot asynchronously
