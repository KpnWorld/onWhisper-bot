import discord
from discord.ext import commands
from discord import app_commands
from db.bot import set_log_channel, get_log_channel

# Set this to your desired owner user ID
OWNER_ID = 895767962722660372  # Replace with the actual owner ID

def owner_check(ctx):
    if ctx.author.id != OWNER_ID:
        raise commands.CheckFailure("You are not authorized to use this command.")
    return True

def slash_owner_check(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        raise app_commands.CheckFailure("You are not authorized to use this command.")
    return True

class Logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logging_paused = False  # Initialize logging paused state

    @app_commands.command(name="setlogchannel", description="Sets the logging channel for the bot.")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        set_log_channel(interaction.guild.id, channel.id)
        embed = discord.Embed(
            title="Logging Channel Set",
            description=f"Logging channel set to {channel.mention}",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pause_logging", description="Pauses the logging functionality.")
    @app_commands.check(slash_owner_check)
    async def pause_logging(self, interaction: discord.Interaction):
        self.logging_paused = True
        embed = discord.Embed(
            title="Logging Paused",
            description="Logging has been paused.",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="resume_logging", description="Resumes the logging functionality.")
    @app_commands.check(slash_owner_check)
    async def resume_logging(self, interaction: discord.Interaction):
        self.logging_paused = False
        embed = discord.Embed(
            title="Logging Resumed",
            description="Logging has been resumed.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    async def log_message(self, guild_id, content):
        # Only send logs if a channel is set and logging is not paused
        if not self.logging_paused:
            channel_id = get_log_channel(guild_id)
            if channel_id:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    # If content is an embed, send it directly; otherwise, wrap the string in an embed.
                    if isinstance(content, discord.Embed):
                        await channel.send(embed=content)
                    else:
                        embed = discord.Embed(
                            description=content,
                            color=discord.Color.blue()
                        )
                        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or self.logging_paused:
            return
        embed = discord.Embed(
            title="Message Deleted",
            description=f"{message.author.mention}'s message was deleted: {message.content}",
            color=discord.Color.red()
        )
        await self.log_message(message.guild.id, embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or self.logging_paused:
            return
        embed = discord.Embed(
            title="Message Edited",
            description=f"{before.author.mention}'s message was edited.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Before", value=before.content or "Empty", inline=False)
        embed.add_field(name="After", value=after.content or "Empty", inline=False)
        await self.log_message(before.guild.id, embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.logging_paused:
            return
        embed = discord.Embed(
            title="Member Joined",
            description=f"{member.mention} has joined the server.",
            color=discord.Color.green()
        )
        await self.log_message(member.guild.id, embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.logging_paused:
            return
        embed = discord.Embed(
            title="Member Left",
            description=f"{member.mention} has left the server.",
            color=discord.Color.red()
        )
        await self.log_message(member.guild.id, embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Logging(bot))
    print("Logging cog loaded")
