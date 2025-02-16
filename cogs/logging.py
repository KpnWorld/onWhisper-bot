import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome")
        if channel:
            await channel.send(f"👋 Welcome {member.mention} to {member.guild.name}!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="goodbye")
        if channel:
            await channel.send(f"😢 {member.name} has left the server.")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            await before.channel.send(f"✏️ **Message Edited**\n**Before:** {before.content}\n**After:** {after.content}")

async def setup(bot):
    await bot.add_cog(Logging(bot))
