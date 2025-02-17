import discord
from discord.ext import commands
from discord import app_commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.userinfo)
        self.bot.tree.add_command(self.serverinfo)

    @app_commands.command(name="userinfo", description="Displays information about a user.")
    async def userinfo(self, interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(title="User Info", description=f"Information about {user.name}", color=discord.Color.blue())
        embed.add_field(name="Username", value=user.name, inline=True)
        embed.add_field(name="Discriminator", value=user.discriminator, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Bot", value=user.bot, inline=True)
        embed.set_thumbnail(url=user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Displays information about the server.")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title="Server Info", description=f"Information about {guild.name}", color=discord.Color.green())
        embed.add_field(name="Server Name", value=guild.name, inline=True)
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Member Count", value=guild.member_count, inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.set_thumbnail(url=guild.icon.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ping", description="Pings the bot.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")
    

def setup(bot):
    bot.add_cog(Info(bot))

