import discord
from discord.ext import commands
from discord import app_commands
import os
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.roll)
        self.bot.tree.add_command(self.choose)

    @app_commands.command(name="roll", description="Rolls a dice in NdN format.")
    async def roll(self, interaction: discord.Interaction, dice: str):
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await interaction.response.send_message('Format has to be in NdN!', ephemeral=True)
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await interaction.response.send_message(result)
    
    @app_commands.command(name="choose", description="Chooses between multiple choices.")
    async def choose(self, interaction: discord.Interaction, *choices: str):
        await interaction.response.send_message(random.choice(choices))

# Enable necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Load all cogs in the 'cogs' folder
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Managing your server!"))
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

def setup(bot):
    bot.add_cog(Fun(bot))

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Run bot using GitHub Secret
bot.run(TOKEN)
