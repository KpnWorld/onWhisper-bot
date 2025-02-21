import discord
from discord.ext import commands, tasks
import os
import asyncio
import random
from db.logdb import init_db

# Enable necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# List of activities
activities = [
    discord.Game(name="Managing your server!"),
    discord.Game(name="Moderating chats!"),
    discord.Game(name="Analyzing data!"),
    discord.Game(name="Having fun with commands!"),
]

# Change activity periodically
@tasks.loop(minutes=10)
async def change_activity():
    new_activity = random.choice(activities)
    await bot.change_presence(activity=new_activity)

# Load all cogs in the 'cogs' folder
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    init_db()  # Initialize the database
    await load_cogs()  # Load cogs before syncing commands
    print(f"✅ Logged in as {bot.user}")
    change_activity.start()  # Start the activity change loop
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync command(s): {e}")

@bot.command(name="check_cogs")
@commands.is_owner()
async def check_cogs(ctx):
    cogs = [cog for cog in bot.cogs]
    embed = discord.Embed(title="Online Cogs", description=f"🟢 Online cogs: {', '.join(cogs)}", color=discord.Color.green())
    await ctx.send(embed=embed)

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    print("Starting bot...")
    asyncio.run(main())  # Properly start the bot asynchronously
