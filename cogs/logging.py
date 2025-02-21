import discord
from discord.ext import commands
from discord import app_commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = None  # Initialize log channel ID

    @app_commands.command(name="setlogchannel", description="Sets the logging channel for the bot.")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.log_channel_id = channel.id
        await interaction.response.send_message(f"✅ Logging channel set to {channel.mention}")

    async def log_message(self, content: str):
        if self.log_channel_id:
            channel = self.bot.get_channel(self.log_channel_id)
            if channel:
                await channel.send(content)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        await self.log_message(f"{message.author}: {message.content}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.log_message(f"{message.author}'s message was deleted: {message.content}")
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.log_message(f"{before.author}'s message was edited: {before.content} -> {after.content}")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.log_message(f"{member} has joined the server.")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.log_message(f"{member} has left the server.")

async def setup(bot):
    await bot.add_cog(Logging(bot))