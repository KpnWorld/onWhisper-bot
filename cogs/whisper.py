import discord
from discord.ext import commands
from discord import app_commands
import logging
import asyncio
import re

class Whisper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="test", description="test if whisper cog is working")
    async def test(self, interaction: discord.Interaction):
       await interaction.response.send_message("Whisper cog is working")

async def setup(bot):
    await bot.add_cog(Whisper(bot))