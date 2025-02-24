import discord
from discord.ext import commands
from discord import app_commands
import logging
import asyncio

# Set up logging for the Logging Cog
logger = logging.getLogger(__name__)

class Logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logging_paused = False  # Initialize logging paused state

    @app_commands.command(name="setlogchannel", description="Sets the logging channel for the bot.")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        # ...existing code...

    @app_commands.command(name="pause_logging", description="Pauses the logging functionality.")
    @app_commands.check(slash_owner_check)
    async def pause_logging(self, interaction: discord.Interaction):
        # ...existing code...

    @app_commands.command(name="resume_logging", description="Resumes the logging functionality.")
    @app_commands.check(slash_owner_check)
    async def resume_logging(self, interaction: discord.Interaction):
        # ...existing code...

    async def log_message(self, guild_id, content):
        # ...existing code...

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # ...existing code...

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # ...existing code...

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # ...existing code...

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # ...existing code...

async def setup(bot: commands.Bot):
    await bot.add_cog(Logging(bot))
    logger.info("Logging cog loaded")
