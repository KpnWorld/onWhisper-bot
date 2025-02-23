import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
import aiohttp
import logging
import re  # Import regular expressions module

# Set up logging for the Fun Cog
logger = logging.getLogger(__name__)

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Rolls a dice in NdN format.")
    async def roll(self, interaction: discord.Interaction, dice: str):
        try:
            rolls, limit = map(int, dice.lower().split('d'))
            if rolls <= 0 or limit <= 0:
                raise ValueError  # Prevent negative or zero values
        except ValueError:
            await interaction.response.send_message("❌ Format must be `NdN` (e.g., `2d6`).", ephemeral=True)
            return

        results = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        embed = discord.Embed(title="🎲 Dice Roll", description=f"{interaction.user.mention}, you rolled: **{results}**", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="choose", description="Chooses between multiple choices.")
    async def choose(self, interaction: discord.Interaction, choices: str):
        options = [choice.strip() for choice in choices.split(",") if choice.strip()]
        if len(options) < 2:
            await interaction.response.send_message("❌ Provide at least two choices, separated by commas.", ephemeral=True)
            return

        selected = random.choice(options)
        embed = discord.Embed(title="🎯 Choice", description=f"{interaction.user.mention}, I choose: **{selected}**", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coinflip", description="Flips a coin.")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(title="🪙 Coin Flip", description=f"{interaction.user.mention}, it's **{result}**!", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rps", description="Plays rock-paper-scissors.")
    async def rps(self, interaction: discord.Interaction, choice: str):
        choices = ["rock", "paper", "scissors"]
        user_choice = choice.lower().strip()

        if user_choice not in choices:
            await interaction.response.send_message("❌ Choose either 'rock', 'paper', or 'scissors'.", ephemeral=True)
            return

        bot_choice = random.choice(choices)
        if user_choice == bot_choice:
            result = "It's a tie!"
        elif (user_choice == "rock" and bot_choice == "scissors") or (user_choice == "paper" and bot_choice == "rock") or (user_choice == "scissors" and bot_choice == "paper"):
            result = "You win! 🎉"
        else:
            result = "I win! 😈"

        embed = discord.Embed(title="🗿 Rock-Paper-Scissors", description=f"{interaction.user.mention}, you chose: **{user_choice}**\n🤖 I chose: **{bot_choice}**\n🏆 {result}", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="joke", description="Tell a random joke.")
    async def joke(self, interaction: discord.Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://official-joke-api.appspot.com/random_joke") as response:
                    if response.status == 200:
                        joke_data = await response.json()
                        joke = f"{joke_data['setup']} - {joke_data['punchline']}"
                    else:
                        joke = f"❌ Failed to fetch a joke. API error {response.status}."
        except Exception as e:
            logger.error(f"❌ Error fetching joke: {e}")
            joke = f"❌ Error fetching joke: {e}"

        embed = discord.Embed(title="😂 Joke", description=f"{interaction.user.mention}, here's a joke for you: {joke}", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="countdown", description="Start a countdown timer.")
    async def countdown(self, interaction: discord.Interaction, seconds: int):
        if seconds < 1 or seconds > 3600:
            await interaction.response.send_message("❌ Please enter a time between 1 and 3600 seconds.", ephemeral=True)
            return

        await interaction.response.defer()
        message = await interaction.followup.send(f"⏳ {interaction.user.mention}, countdown started for {seconds} seconds...")

        while seconds > 0:
            await asyncio.sleep(1)
            seconds -= 1
            if seconds % 10 == 0 or seconds <= 5:  # Update every 10 seconds, and last 5 seconds
                await message.edit(content=f"⏳ {interaction.user.mention}, {seconds} seconds remaining...")

        await message.edit(content=f"🎉 {interaction.user.mention}, countdown has ended!")

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

            selected_channel = self.channel.values[0] if self.channel.values else None  # Get selected channel
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
        try:
            await interaction.response.send_modal(self.WhisperModal(interaction))
        except Exception as e:
            logger.exception("Failed to send modal: %s", e)
            await interaction.response.send_message("An error occurred while opening the modal.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))

