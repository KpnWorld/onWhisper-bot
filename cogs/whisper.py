import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import re  # Import regular expressions module

class Whisper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    class WhisperModal(discord.ui.Modal, title="Whisper Message"):
        def __init__(self, interaction: discord.Interaction):
            super().__init__()
            self.interaction = interaction

            # Text input for the whisper message
            self.message = discord.ui.TextInput(
                label="Your message",
                placeholder="Enter your whispered message...",
                required=True,
                max_length=200
            )
            self.add_item(self.message)

            # Text input for the time duration
            self.duration = discord.ui.TextInput(
                label="Time (seconds)",
                placeholder="Enter how long the message should last...",
                required=True,
                max_length=4
            )
            self.add_item(self.duration)

            # Channel selection
            self.channel = discord.ui.ChannelSelect(
                label="Select Channel",
                placeholder="Choose a channel to send the message...",
                required=True,
                channel_types=[discord.ChannelType.text]
            )
            self.add_item(self.channel)

            # User mention input
            self.mention = discord.ui.TextInput(
                label="Mention User (optional)",
                placeholder="Enter the user ID to mention...",
                required=False,
                max_length=20
            )
            self.add_item(self.mention)

        async def on_submit(self, interaction: discord.Interaction):
            whisper_message = self.message.value  # Get message input
            try:
                duration = int(self.duration.value)  # Get time input and convert to int
                if duration <= 0:
                    raise ValueError
            except ValueError:
                await interaction.response.send_message("❌ Please enter a valid positive number for the time.", ephemeral=True)
                return

            # Ensure duration is at least 1 second
            if duration < 1:
                await interaction.response.send_message("❌ The duration must be at least 1 second.", ephemeral=True)
                return

            selected_channel = self.channel.value  # Get selected channel
            if not selected_channel:
                await interaction.response.send_message("❌ Please select a valid channel.", ephemeral=True)
                return

            # Check if the bot has permission to send messages in the selected channel
            if not selected_channel.permissions_for(interaction.guild.me).send_messages:
                await interaction.response.send_message("❌ I do not have permission to send messages in the selected channel.", ephemeral=True)
                return

            mention_user = None
            if self.mention.value:
                try:
                    mention_user = await self.interaction.guild.fetch_member(int(self.mention.value))
                except Exception:
                    await interaction.response.send_message("❌ Invalid user ID for mention.", ephemeral=True)
                    return

            # Parse and replace @user mentions with proper user mentions
            mention_pattern = re.compile(r'<@!?(\d+)>')  # Match @user or @user#1234
            matches = mention_pattern.findall(whisper_message)
            for match in matches:
                member = discord.utils.get(interaction.guild.members, id=int(match))
                if member:
                    whisper_message = whisper_message.replace(f"<@{match}>", member.mention)

            embed = discord.Embed(
                title="Whisper",
                description=f"🗣 {interaction.user.mention} whispered: **{whisper_message}**",
                color=discord.Color.purple()
            )
            
            # Send the whisper message to the selected channel
            try:
                if mention_user:
                    whispered_message = await selected_channel.send(content=mention_user.mention, embed=embed)
                else:
                    whispered_message = await selected_channel.send(embed=embed)

                # Confirm the message was sent
                await interaction.response.send_message(f"Your whisper has been sent to {selected_channel.mention} and will be deleted in {duration} seconds.", ephemeral=True)

                # Wait for the specified time before deleting
                await asyncio.sleep(duration)
                await whispered_message.delete()

            except discord.Forbidden:
                await interaction.response.send_message("❌ I do not have permission to send the whisper message.", ephemeral=True)
            except discord.HTTPException as e:
                await interaction.response.send_message(f"❌ An error occurred: {str(e)}", ephemeral=True)

    @app_commands.command(name="whisper", description="Send a temporary whispered message.")
    async def whisper(self, interaction: discord.Interaction):
        """Opens a modal for the user to input a whisper message, time duration, and select a channel."""
        await interaction.response.send_modal(self.WhisperModal(interaction))

async def setup(bot: commands.Bot):
    await bot.add_cog(Whisper(bot))
