import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from datetime import timedelta

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Rolls a dice in NdN format.")
    async def roll(self, interaction: discord.Interaction, dice: str):
        try:
            rolls, limit = map(int, dice.lower().split('d'))
        except Exception:
            await interaction.response.send_message("❌ Format must be in `NdN` (e.g., `2d6`)", ephemeral=True)
            return

        results = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        embed = discord.Embed(title="Dice Roll", description=f"🎲 {interaction.user.mention}, you rolled: {results}", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="choose", description="Chooses between multiple choices.")
    async def choose(self, interaction: discord.Interaction, choices: str):
        options = choices.split(",")  # User provides comma-separated choices
        if len(options) < 2:
            await interaction.response.send_message("❌ Please provide at least two choices, separated by commas.", ephemeral=True)
            return
        selected = random.choice(options).strip()
        embed = discord.Embed(title="Choice", description=f"🤖 {interaction.user.mention}, I choose: **{selected}**", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coinflip", description="Flips a coin.")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(title="Coin Flip", description=f"🪙 {interaction.user.mention}, it's **{result}**!", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rps", description="Plays rock-paper-scissors.")
    async def rps(self, interaction: discord.Interaction, choice: str):
        choices = ["rock", "paper", "scissors"]
        if choice.lower() not in choices:
            await interaction.response.send_message("❌ Please choose either 'rock', 'paper', or 'scissors'.", ephemeral=True)
            return

        bot_choice = random.choice(choices)
        if choice.lower() == bot_choice:
            result = "It's a tie!"
        elif (choice.lower() == "rock" and bot_choice == "scissors") or (choice.lower() == "paper" and bot_choice == "rock") or (choice.lower() == "scissors" and bot_choice == "paper"):
            result = "You win!"
        else:
            result = "I win!"

        embed = discord.Embed(title="Rock-Paper-Scissors", description=f"🗿 {interaction.user.mention}, you chose: **{choice}**\n🤖 I chose: **{bot_choice}**\n🏆 {result}", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="joke", description="Tell a random joke.")
    async def joke(self, interaction: discord.Interaction):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't skeletons fight each other? They don't have the guts."
        ]
        joke = random.choice(jokes)
        embed = discord.Embed(title="Joke", description=f"😂 {interaction.user.mention}, here's a joke for you: {joke}", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    # New whisper command
    @app_commands.command(name="whisper", description="Send a temporary whispered message.")
    async def whisper(self, interaction: discord.Interaction, message: str):
        # Create a modal for the user to edit their message and time
        modal = discord.ui.Modal(title="Edit Whisper Message", custom_id="whisper_modal")

        # Create a TextInput for the whispered message
        text_input_message = discord.ui.TextInput(
            label="Your message",
            placeholder="Edit your message...",
            default=message,
            required=True,
            max_length=200
        )

        # Create a TextInput for the time
        text_input_time = discord.ui.TextInput(
            label="Time (seconds)",
            placeholder="Enter the time in seconds...",
            required=True,
            max_length=6
        )

        modal.add_item(text_input_message)
        modal.add_item(text_input_time)

        # Handle the submission of the modal
        modal.callback = self.on_submit
        await interaction.response.send_modal(modal)

    async def on_submit(self, interaction: discord.Interaction, message: str):
        whisper_message = interaction.data['components'][0]['components'][0]['value']  # Get the edited message
        try:
            time = int(interaction.data['components'][1]['components'][0]['value'])  # Get the time and convert to int
            if time <= 0:
                await interaction.response.send_message("❌ The time must be a positive integer.", ephemeral=True)
                return
        except ValueError:
            await interaction.response.send_message("❌ Please enter a valid number for the time.", ephemeral=True)
            return

        embed = discord.Embed(title="Whisper", description=f"🗣 {interaction.user.mention} whispered: **{whisper_message}**", color=discord.Color.purple())
         # Send the message
        whispered_message = await interaction.channel.send(embed=embed)
    
        # Confirm message deletion
        await interaction.response.send_message(f"Your whisper has been sent and will be deleted in {time} seconds.", ephemeral=True)

        # Delete the message after the specified time
        await asyncio.sleep(time)
        await whispered_message.delete()
        async def delete_message_after(self, message: discord.Message, delay: int):
            await asyncio.sleep(delay)
            await message.delete()
        # Create a modal for the user to edit their message and time
        modal = discord.ui.Modal(title="Edit Whisper Message", custom_id="whisper_modal")

        # Create a TextInput for the whispered message
        text_input_message = discord.ui.TextInput(
            label="Your message",
            placeholder="Edit your message...",
            default=message,
            required=True,
            max_length=200
        )

        # Create a TextInput for the time
        text_input_time = discord.ui.TextInput(
            label="Time (seconds)",
            placeholder="Enter the time in seconds...",
            required=True,
            max_length=4
        )

        modal.add_item(text_input_message)
        modal.add_item(text_input_time)

        # Handle the submission of the modal
        modal.callback = self.on_submit
        modal.on_submit = self.on_submit

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
