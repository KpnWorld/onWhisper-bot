import discord
from discord.ext import commands
import os

# Enable intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True  

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync commands globally
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Managing your server!"))

# Example slash command (works in any server)
@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello there!")

# Run bot using GitHub Secret
TOKEN = os.getenv("DISCORD_BOT_TOKEN")  
bot.run(TOKEN)

