import discord
from discord.ext import commands
from discord import app_commands
from db.bot import init_db  
import time

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = time.time()

    @app_commands.command(name="ping", description="Check the bot's latency and uptime.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)  # Convert to ms
        uptime = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start_time))
        embed = discord.Embed(
            title="Pong!",
            description=f"Latency: **{latency}ms**\nUptime: **{uptime}**",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
        await interaction.followup.send("✅ Ping command executed successfully!")


    @app_commands.command(name="about", description="Learn more about onWhisper.")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 onWhisper Bot",
            description="onWhisper is a Discord bot built for moderation, analytics, and fun!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Developer", value="KpnWorld", inline=False)
        embed.add_field(name="Version", value="1.0.0", inline=False)
        embed.add_field(name="Invite Link", value="[Click here to invite](https://discord.com/oauth2/authorize?client_id=YOUR_BOT_ID&scope=bot&permissions=YOUR_PERMISSIONS)", inline=False)
        embed.add_field(name="Support Server", value="[Join the support server](YOUR_SUPPORT_SERVER_LINK)", inline=False)
        embed.set_footer(text="Made with ❤️ for the community!")
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
