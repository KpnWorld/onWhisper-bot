import discord
from discord.ext import commands
from discord import app_commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

async def setup(bot):
    await bot.add_cog(Fun(bot))
