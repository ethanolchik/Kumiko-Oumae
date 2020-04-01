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
        await ctx.send(embed=embed)

    @commands.command()
    async def feedback(self, ctx, *feedback):
        msg = ' '.join(feedback)

        embed = discord.Embed(
            title="Feedback",
            description=f"{msg} \n~\n   ctx.author",
            colour=0x0EF7E2
        )
        emb = discord.Embed(
            title="Thanks For Your Feedback!",
            description="Thanks for your feedback! We will try to improve as soon as possible!",
            colour=0x0EF7E2
        )
        emb.set_footer(
            text="Join our support server! `https://discord.gg/YUm2sBD`",
            icon_url=self.bot.user.avatar_url_as(static_format="png")
        )

        channel = await self.bot.fetch_channel(694887120669507635)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Meta(bot))
