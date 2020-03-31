import discord

from discord.ext import commands

class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self, ctx):
        embed = discord.Embed(
            title="Source",
            description="https://github.com/EraseKesu/Chorus"
        )


def setup(bot):
    bot.add_cog(Meta(bot))
