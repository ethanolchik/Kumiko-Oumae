"""
Copyright 2020 EraseKesu (class Erase#0027)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
            description=f"""
```css
[ {msg} ] ~{ctx.author}
```         """,
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
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Meta(bot))
