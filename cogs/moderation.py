import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.kick)
        self.bot.tree.add_command(self.ban)

    @app_commands.command(name="kick", description="Kicks a member from the server.")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.kick(reason=reason)
        await interaction.response.send_message(f'{member} has been kicked. Reason: {reason}')

    @app_commands.command(name="ban", description="Bans a member from the server.")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.ban(reason=reason)
        await interaction.response.send_message(f'{member} has been banned. Reason: {reason}')

    @app_commands.command(name="unban", description="Unbans a member from the server.")
    async def unban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.unban(reason=reason)
        await interaction.response.send_message(f'{member} has been unbanned. Reason: {reason}') 

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
        await interaction.response.send_message(f'{member} has been warned. Reason: {reason}')

    @app_commands.command(name="warns", description="Displays the number of warnings a member has.")
    async def warns(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f'{member} has 0 warnings.')
    



def setup(bot):
    bot.add_cog(Moderation(bot))
