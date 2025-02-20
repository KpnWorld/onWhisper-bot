import discord
from discord.ext import commands
from discord import app_commands

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)  # Convert to ms
        await interaction.response.send_message(f"🏓 Pong! Latency: **{latency}ms**")

    @app_commands.command(name="about", description="Learn more about onWhisper.")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 onWhisper Bot",
            description="onWhisper is a Discord bot built for moderation, analytics, and fun!",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Developed by KpnWorld")
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
