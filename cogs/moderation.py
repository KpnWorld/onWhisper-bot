import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = self.load_warnings()
        self.bot.tree.add_command(self.kick)
        self.bot.tree.add_command(self.ban)
        self.bot.tree.add_command(self.unban)
        self.bot.tree.add_command(self.clear)
        self.bot.tree.add_command(self.mute)
        self.bot.tree.add_command(self.unmute)
        self.bot.tree.add_command(self.warn)
        self.bot.tree.add_command(self.warns)

    def load_warnings(self):
        if os.path.exists("warnings.json"):
            with open("warnings.json", "r") as f:
                return json.load(f)
        return {}

    def save_warnings(self):
        with open("warnings.json", "w") as f:
            json.dump(self.warnings, f)

    @app_commands.command(name="kick", description="Kicks a member from the server.")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.kick(reason=reason)
        await interaction.response.send_message(f'{member} has been kicked. Reason: {reason}')

    @app_commands.command(name="ban", description="Bans a member from the server.")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.ban(reason=reason)
        await interaction.response.send_message(f'{member} has been banned. Reason: {reason}')

    @app_commands.command(name="unban", description="Unbans a member from the server.")
    async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str = None):
        await interaction.guild.unban(user, reason=reason)
        await interaction.response.send_message(f'{user} has been unbanned. Reason: {reason}') 

    @app_commands.command(name="clear", description="Clears a specified amount of messages.")
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f'{amount} messages have been cleared.')

    @app_commands.command(name="mute", description="Mutes a member.")
    async def mute(self, interaction: discord.Interaction, member: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        await member.add_roles(role)
        await interaction.response.send_message(f'{member} has been muted.')
    
    @app_commands.command(name="unmute", description="Unmutes a member.")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name="Muted")
        await member.remove_roles(role)
        await interaction.response.send_message(f'{member} has been unmuted.')
    
    @app_commands.command(name="warn", description="Warns a member.")
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        if str(member.id) not in self.warnings:
            self.warnings[str(member.id)] = []
        self.warnings[str(member.id)].append(reason)
        self.save_warnings()
        await interaction.response.send_message(f'{member} has been warned. Reason: {reason}')

    @app_commands.command(name="warns", description="Displays the number of warnings a member has.")
    async def warns(self, interaction: discord.Interaction, member: discord.Member):
        count = len(self.warnings.get(str(member.id), []))
        await interaction.response.send_message(f'{member} has {count} warnings.')
    
def setup(bot):
    bot.add_cog(Moderation(bot))
