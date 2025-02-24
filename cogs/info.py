import discord
from discord.ext import commands
from discord import app_commands
import time
import logging

# Set up logging for the Info Cog
logger = logging.getLogger(__name__)

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = time.time()

    def format_uptime(self):
        """Format uptime into days, hours, minutes, and seconds."""
        uptime_seconds = int(time.time() - self.start_time)
        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s" if days > 0 else f"{hours}h {minutes}m {seconds}s"
        return uptime_str

    @app_commands.command(name="ping", description="Check the bot's latency and uptime.")
    async def ping(self, interaction: discord.Interaction):
        try:
            latency = round(self.bot.latency * 1000)  # Convert to ms
            uptime = self.format_uptime()

            embed = discord.Embed(
                title="🏓 Pong!",
                description=f"🟢 **Latency:** {latency}ms\n⏳ **Uptime:** {uptime}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(f"Error while processing ping: {e}")
            await interaction.response.send_message("❌ Something went wrong while fetching bot data.", ephemeral=True)

    @app_commands.command(name="about", description="Learn more about onWhisper.")
    async def about(self, interaction: discord.Interaction):
        try:
            bot_id = self.bot.user.id  # Get bot's ID dynamically
            invite_link = f"https://discord.com/oauth2/authorize?client_id={bot_id}&scope=bot&permissions=8"
            support_server = "https://discord.gg/YOUR_SUPPORT_SERVER"  # Replace with actual support server link

            embed = discord.Embed(
                title="🤖 About onWhisper",
                description="onWhisper is a Discord bot built for moderation, analytics, and fun!",
                color=discord.Color.blue()
            )
            embed.add_field(name="🛠 Developer", value="KpnWorld", inline=False)
            embed.add_field(name="📌 Version", value="1.0.0", inline=False)  # Update version dynamically if needed
            embed.add_field(name="🔗 Invite Me", value=f"[Click here to invite]({invite_link})", inline=False)
            embed.add_field(name="💬 Support Server", value=f"[Join Here]({support_server})", inline=False)
            embed.set_footer(text="Made with ❤️ for the community!")

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(f"Error in about command: {e}")
            await interaction.response.send_message("❌ Something went wrong while fetching bot information.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))

