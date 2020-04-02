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
import asyncio

from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands.Bot.remove_command(self, name="help")
    @commands.command()
    async def help(self, ctx, *, command: str = None):

        error = f'```css\nThat command, "{command}", does not exist!\n```'
        if command:
            cmd = self.bot.get_command(command)

        fun = ""
        for a in self.bot.commands:
            print(a.cog_name)
            if a.cog_name == "Fun":
                if not a.hidden:
                    fun += f"`{a.name}` | "
                    try:
                        for b in a.commands:
                            fun += f"`{a.name} {b.name}` | "
                    finally:
                        pass

        music = ""

        for a in self.bot.commands:
            if a.cog_name == "Music":
                if not a.hidden:
                    music += f"`{a.name}` | "
                    try:
                        for b in a.commands:
                            music += f"`{a.name} {b.name} | "
                    except:
                        pass

        userinfo = ""

        for a in self.bot.commands:
            if a.cog_name == "Userinfo":
                if not a.hidden:
                    userinfo += f"`{a.name}` | "
                    try:
                        for b in a.commands:
                            userinfo += f"`{a.name} {b.name} | "
                    except:
                        pass

        meta = ""

        for a in self.bot.commands:
            if a.cog_name == "Meta":
                if not a.hidden:
                    meta += f"`{a.name}` | "
                    try:
                        for b in a.commands:
                            meta += f"`{a.name} {b.name} | "
                    except:
                        pass

        moderation = ""

        for a in self.bot.commands:
            if a.cog_name == "Moderation":
                if not a.hidden:
                    moderation += f"`{a.name}` | "
                    try:
                        for b in a.commands:
                            moderation += f"`{a.name} {b.name} | "
                    except:
                        pass

        fdescription = f"""
**FUN**
{fun}

**MUSIC**
{music}

**USERINFO**
`user` | `avatar` | 

**META**
{meta}

**MODERATION**
{moderation}

"""
        print(fun)
        embed = discord.Embed(
            title="Help",
            description=fdescription,
            colour=0x0EF7E2
        )
        embed.set_footer(
            text="Join our support server! `https://discord.gg/YUm2sBD`",
            icon_url=self.bot.user.avatar_url_as(static_format="png")
        )

        mesg = await ctx.send(embed=embed)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '<:redTick:596576672149667840>'

        try:
            await self.bot.wait_for('reaction_add', check=check, timeout=120.0)
            await mesg.delete()
        except asyncio.TimeoutError:
            return


def setup(bot):
    bot.add_cog(Help(bot))
