import discord
from discord.ext import commands
import os

# Enable necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True  

# Create bot instance with command tree
bot = commands.Bot(command_prefix="!", intents=intents)
bot.tree = discord.app_commands.CommandTree(bot)  # Ensure the bot tree exists

@bot.event
async def on_ready():
    await bot.tree.sync()  # This ensures commands are registered
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Managing your server!"))

# Example slash command
@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello there!")

# Run bot using GitHub Secret
TOKEN = os.getenv("DISCORD_BOT_TOKEN")  
bot.run(TOKEN)
