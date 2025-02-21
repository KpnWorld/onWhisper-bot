import discord
from discord.ext import commands
from discord import app_commands

class Logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel_id = None  # Initialize log channel ID
        self.logging_paused = False  # Initialize logging paused state

    @app_commands.command(name="setlogchannel", description="Sets the logging channel for the bot.")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.log_channel_id = channel.id
        embed = discord.Embed(title="Logging Channel Set", description=f"Logging channel set to {channel.mention}", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @commands.command(name="pause_logging")
    @commands.is_owner()
    async def pause_logging(self, ctx):
        self.logging_paused = True
        embed = discord.Embed(title="Logging Paused", description="Logging has been paused.", color=discord.Color.orange())
        await ctx.send(embed=embed)

    @commands.command(name="resume_logging")
    @commands.is_owner()
    async def resume_logging(self, ctx):
        self.logging_paused = False
        embed = discord.Embed(title="Logging Resumed", description="Logging has been resumed.", color=discord.Color.green())
        await ctx.send(embed=embed)

    async def log_message(self, content: str):
        if self.log_channel_id and not self.logging_paused:
            channel = self.bot.get_channel(self.log_channel_id)
            if channel:
                embed = discord.Embed(description=content, color=discord.Color.blue())
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not self.logging_paused:
            await self.log_message(f"{message.author.mention}'s message was deleted: {message.content}")
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not self.logging_paused:
            await self.log_message(f"{before.author.mention}'s message was edited: {before.content} -> {after.content}")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.logging_paused:
            await self.log_message(f"{member.mention} has joined the server.")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not self.logging_paused:
            await self.log_message(f"{member.mention} has left the server.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Logging(bot))
    print("Logging cog loaded")
