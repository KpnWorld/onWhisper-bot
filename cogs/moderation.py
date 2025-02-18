import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = self.load_warnings()

    def load_warnings(self):
        if os.path.exists("warnings.json"):
            with open("warnings.json", "r") as f:
                return json.load(f)
        return {}

    def save_warnings(self):
        with open("warnings.json", "w") as f:
            json.dump(self.warnings, f)

    @app_commands.command(name="kick", description="Kicks a member from the server.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f'✅ {member} has been kicked. Reason: {reason}')

    @app_commands.command(name="ban", description="Bans a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f'✅ {member} has been banned. Reason: {reason}')

    @app_commands.command(name="unban", description="Unbans a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str = "No reason provided"):
        await interaction.guild.unban(user, reason=reason)
        await interaction.response.send_message(f'✅ {user} has been unbanned. Reason: {reason}') 

    @app_commands.command(name="clear", description="Clears a specified amount of messages.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f'🧹 {amount} messages have been cleared.', ephemeral=True)

    @app_commands.command(name="mute", description="Mutes a member.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if role is None:
            await interaction.response.send_message("❌ The 'Muted' role does not exist. Please create one first.", ephemeral=True)
            return
        
        await member.add_roles(role)
        await interaction.response.send_message(f'🔇 {member} has been muted.')

    @app_commands.command(name="unmute", description="Unmutes a member.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        if role is None:
            await interaction.response.send_message("❌ The 'Muted' role does not exist. Please create one first.", ephemeral=True)
            return
        
        await member.remove_roles(role)
        await interaction.response.send_message(f'🔊 {member} has been unmuted.')

    @app_commands.command(name="warn", description="Warns a member.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        if str(member.id) not in self.warnings:
            self.warnings[str(member.id)] = []
        self.warnings[str(member.id)].append(reason)
        self.save_warnings()
        await interaction.response.send_message(f'⚠️ {member} has been warned. Reason: {reason}')

    @app_commands.command(name="warns", description="Displays the number of warnings a member has.")
    async def warns(self, interaction: discord.Interaction, member: discord.Member):
        count = len(self.warnings.get(str(member.id), []))
        await interaction.response.send_message(f'📜 {member} has {count} warnings.')
    
async def setup(bot):
    await bot.add_cog(Moderation(bot))

