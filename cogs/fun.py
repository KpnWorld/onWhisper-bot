from discord import app_commands
from discord.ext import commands
import discord
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="choose", description="Chooses between multiple choices.")
    @app_commands.describe(choices="Comma-separated choices (e.g., 'apple, banana, orange')")
    async def choose(self, interaction: discord.Interaction, choices: str):
        choice_list = choices.split(",")  # Convert string to a list
        selected = random.choice([c.strip() for c in choice_list if c.strip()])
        await interaction.response.send_message(f"I choose: **{selected}**")

async def setup(bot):
    await bot.add_cog(Fun(bot))
