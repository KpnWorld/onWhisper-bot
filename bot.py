import discord
from discord.ext import commands
import os
import asyncio  # Required for async loading

intents = discord.Intents.default()
intents.message_content = True  # Make sure it's enabled in Discord Developer Portal

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    for filename in os.listdir("./cogs"):  # Ensure the path is correct
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Managing your server!"))
    await bot.tree.sync()
    print("✅ Slash commands synced.")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())  # Properly start the bot asynchronously
