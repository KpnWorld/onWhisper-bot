import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from db.bot import add_warning, get_warnings

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kicks a member from the server.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        embed = discord.Embed(title="Member Kicked", description=f"{member.mention} has been kicked.", color=discord.Color.red())
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ban", description="Bans a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        embed = discord.Embed(title="Member Banned", description=f"{member.mention} has been banned.", color=discord.Color.red())
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unban", description="Unbans a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str = "No reason provided"):
        await interaction.guild.unban(user, reason=reason)
        embed = discord.Embed(title="Member Unbanned", description=f"{user.mention} has been unbanned.", color=discord.Color.green())
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clear", description="Clears a specified amount of messages.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        embed = discord.Embed(title="Messages Cleared", description=f"{amount} messages have been cleared.", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="mute", description="Mutes a member.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if role is None:
            await interaction.response.send_message("❌ The 'Muted' role does not exist. Please create one first.", ephemeral=True)
            return
        
        await member.add_roles(role)
        embed = discord.Embed(title="Member Muted", description=f"{member.mention} has been muted.", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unmute", description="Unmutes a member.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if role is None:
            await interaction.response.send_message("❌ The 'Muted' role does not exist. Please create one first.", ephemeral=True)
            return
        
        await member.remove_roles(role)
        embed = discord.Embed(title="Member Unmuted", description=f"{member.mention} has been unmuted.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="warn", description="Warns a member.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        add_warning(member.id, interaction.guild.id, reason)
        embed = discord.Embed(title="Member Warned", description=f"{member.mention} has been warned.", color=discord.Color.yellow())
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="warns", description="Displays the number of warnings a member has.")
    async def warns(self, interaction: discord.Interaction, member: discord.Member):
        warnings = get_warnings(member.id, interaction.guild.id)
        count = len(warnings)
        embed = discord.Embed(title="Member Warnings", description=f"{member.mention} has {count} warnings.", color=discord.Color.yellow())
        for reason, timestamp in warnings:
            formatted_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")  # Convert timestamp
            embed.add_field(name=formatted_time, value=reason, inline=False)
        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(Moderation(bot))

