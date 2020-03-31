"""
Chorus discord bot
~ EraseKesu - class Erase#0027
"""

import discord
import json
import random

from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def candy(self, ctx):

        """Get the candy before anyone else!"""

        embed = discord.Embed(description="🍬 | First one to take the candy gets the candy!", colour=0x0EF7E2)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🍬")

        def check(reaction, user):
            return user != self.bot.user and str(reaction.emoji) == '🍬' and reaction.message.id == msg.id

        msg0 = await self.bot.wait_for("reaction_add", check=check)

        embed.description = f"🍬 | {msg0[1].mention} won and ate the candy!"

        await msg.edit(embed=embed)

        with open("db_files/candylb.json", "r") as f:

            l = json.load(f)

        try:

            l[str(msg0[1].id)] += 1

        except KeyError:

            l[str(msg0[1].id)] = 1

        with open("db_files/candylb.json", "w") as f:

            json.dump(l, f, indent=4)

    @candy.command(aliases=["lb", "top"])
    async def leaderboard(self, ctx):

        """The leaderboard of the best candy players! do you see yourself on there?"""

        with open("db_files/candylb.json", "r") as f:

            l = json.load(f)

        lb = sorted(l, key=lambda x: l[x], reverse=True)
        print(lb)
        res = ""

        counter = 0

        for a in lb:

            counter += 1

            if counter > 10:

                pass

            else:

                u = self.bot.get_user(int(a))
                res += f"\n**{counter}.** `{u}` - **{l[str(a)]} 🍬**"

        embed = discord.Embed(
            description=res,
            colour=0x0EF7E2
        )
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def mafia(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.send("Please Choose a person to fight for money!")
        if member != None:
            embed = discord.Embed(description="💰 | First one to react to the message wins the fight!", colour=0x0EF7E2)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("💰")

            def check(reaction, user):
                return user == ctx.author  or member and not self.bot.user and str(reaction.emoji) == '💰' and reaction.message.id == msg.id

            msg0 = await self.bot.wait_for("reaction_add", check=check)

            embed.description = f"💰 | {msg0[1].mention} won and got $100!"

            await msg.edit(embed=embed)
            with open("db_files/mafialb.json", "r") as f:
                l = json.load(f)
            with open("db_files/mafiaw.json", "r") as f:
                l2 = json.load(f)

            try:
                l[str(msg0[1].id)] = 0
                l2[str(msg0[1].id)] += 100

            except KeyError:
                l[str(msg0[1].id)] = 0
                l2[str(msg0[1].id)] = 100

            with open("db_files/mafiaw.json", "w") as f:

                json.dump(l2, f, indent=4)

    @mafia.command(aliases=["top"])
    async def leaderboard(self, ctx):
        with open("db_files/mafialb.json", "r") as f:
            l = json.load(f)

        with open("db_files/mafiaw.json", "r") as f:
            l2 = json.load(f)

        lb = sorted(l, key=lambda x: l[x], reverse=True)
        print(lb)
        res = ""

        counter = 0

        for a in lb:

            counter += 1

            if counter > 10:

                pass

            else:

                u = self.bot.get_user(int(a))
                res += f"\n**{counter}.** `{u}` - **{l[str(a)] + l2[str(a)]} 💰**"
                print(l[str(a)])

        embed = discord.Embed(
            description=res,
            colour=0x0EF7E2
        )
        await ctx.send(embed=embed)

    @mafia.command(hidden=True)
    @commands.is_owner()
    async def add(self, ctx, user: discord.User, amount: int):
        with open("db_files/mafialb.json", "r") as f:
            l = json.load(f)
        try:
            l[str(user.id)] += amount

        except KeyError:
            l[str(user.id)] = 1

        with open("db_files/mafialb.json", "w") as f:
            json.dump(l, f, indent=4)

        await ctx.send(f"{user.mention}'s balance has been increased by {amount} and is now {l[str(user.id)]}")

    @mafia.command(hidden=True)
    @commands.is_owner()
    async def remove(self, ctx, user: discord.User, amount: int):
        x = 0
        with open("db_files/mafialb.json", "r") as f:
            l = json.load(f)
        lb = sorted(l, key=lambda x: l[x], reverse=True)
        for a in lb:
            while True:
                x += 100
                print(x)
                if x == amount:
                    l[str(user.id)] -= amount
                    break

        with open("db_files/mafialb.json", "w") as f:
            json.dump(l, f, indent=4)

        await ctx.send(f"removed {amount} from {user}'s balance and their balance is now {l[str(user.id)]}")

    @mafia.command(aliases=["bal"])
    async def balance(self, ctx):
        with open("db_files/mafialb.json", "r") as f:
            l = json.load(f)
        with open("db_files/mafiaw.json", "r") as f:
            l2 = json.load(f)
        lb = sorted(l, key=lambda x: l[x], reverse=True)
        print(lb)
        res = ""

        counter = 0

        for a in lb:

            counter += 1

            if counter > 10:

                pass

            else:
                p = l[str(ctx.author.id)]
                p2 = l2[str(ctx.author.id)]

                u = self.bot.get_user(int(a))
                res += f"\n**{counter}.** `{u}` - **{l[str(a)]} 💰**"

                embed = discord.Embed(
                    title="Balance",
                    description=f"""```
--------------------------------
|   in bank     |   on you     |
|------------------------------|
       {p}           {p2}      
                        
```""",
                    colour=0x0EF7E2
                )

                await ctx.send(embed=embed)

    @mafia.command(aliases=["with"])
    async def withdraw(self, ctx, amount: int):
        with open("db_files/mafialb.json", "r") as f:
            l = json.load(f)

        with open("db_files/mafiaw.json", 'r') as f:
            l2 = json.load(f)
        p = l[str(ctx.author.id)] - amount
        p2 = l2[str(ctx.author.id)] + amount
        if l[str(ctx.author.id)] - amount >= 0:
            l[str(ctx.author.id)] -= amount
            l2[str(ctx.author.id)] += amount

        else:
            await ctx.send("You can't withdraw more than your balance!")
            return

        with open("db_files/mafialb.json", "w") as f:
            json.dump(l, f, indent=4)

        with open("db_files/mafiaw.json", "w") as f:
            json.dump(l2, f, indent=4)

        await ctx.send(
            f""" ```
        --------------------------------
        |   in bank     |   on you     |
        |------------------------------|
              {p}           {p2}      
                        
        ```"""
        )

    @mafia.command(aliases=["dep"])
    async def deposit(self, ctx, amount: int):
        with open("db_files/mafialb.json", "r") as f:
            l = json.load(f)

        with open("db_files/mafiaw.json", 'r') as f:
            l2 = json.load(f)
        p = l[str(ctx.author.id)] + amount
        p2 = l2[str(ctx.author.id)] - amount
        if l[str(ctx.author.id)] - amount >= 0:
            l[str(ctx.author.id)] += amount
            l2[str(ctx.author.id)] -= amount

        else:
            await ctx.send("You can't withdraw more than your balance!")
            return

        with open("db_files/mafialb.json", "w") as f:
            json.dump(l, f, indent=4)

        with open("db_files/mafiaw.json", "w") as f:
            json.dump(l2, f, indent=4)

        await ctx.send(
            f""" ```
        -------------------------------
        |   in bank     |   on you     |
        |------------------------------|
              {p}           {p2}      

        ```"""
        )

    @mafia.command(aliases=["group"])
    async def gang(self, ctx):
        with open("db_files/bloodgang.json", "r") as f:
            l = json.load(f)
        x = ""
        y = 0
        embed = discord.Embed()
        embed.title = "Gang"
        embed.colour = 0x0EF7E2
        for name in l:
            if name == str(ctx.author.id):
                x = "The Blood Gang"
                embed.title = "The Blood Gang"

        if not str(ctx.author.id) in l:
            y += 1

        with open("db_files/hoodgang.json", "r") as f:
            l2 = json.load(f)

        for name in l2:
            if name == str(ctx.author.id):
                x = "The Hood Gang"
                embed.title = "The Hood Gang"

        embed.description = f"You are part of {x}"

        if not str(ctx.author.id) in l2:
            y += 1

        if y == 2:
            embed.description="You are not part of a gang yet. To join, type in `<>mafia join`."
            embed.colour = discord.Colour.from_rgb(0, 150, 140)
        await ctx.send(embed=embed)

    @mafia.command()
    async def join(self, ctx, gang: str = None):
        print(gang)
        if gang == None:
            await ctx.send("Please specify a gang to join!")

        with open("db_files/bloodgang.json", "r") as f:
                l = json.load(f)

        for user in l:
                if user == str(ctx.author.id):
                    await ctx.send("You are already in a gang! To leave your current one, type `<>mafia leave`")
                    return

        with open("db_files/hoodgang.json", "r") as f:
                l2 = json.load(f)

        for user in l2:
                if user == str(ctx.author.id):
                    await ctx.send("You are already in a gang! To leave your current one, type `<>mafia leave`")
                    return

        if gang == "blood":
                with open("db_files/bloodgang.json", "w") as f:
                    l[str(ctx.author.id)] = 1
                    json.dump(l, f, indent=4)
                    msg = "You are now part of `The Blood Gang`!"
                    await ctx.send(msg)

        if gang == "hood":
                with open("db_files/hoodgang.json", "w") as f:
                    l2[str(ctx.author.id)] = 1
                    json.dump(l2, f, indent=4)
                    msg = "You are now part of `The Hood Gang`!"
                    await ctx.send(msg)

    @mafia.command()
    async def leave(self, ctx):
        y = 0
        with open("db_files/bloodgang.json", "r") as f:
            l = json.load(f)
        if str(ctx.author.id) in l:
            msg = "You left `The Blood Gang`!"
            await ctx.send(msg)
            l.pop(str(ctx.author.id))
            with open("db_files/bloodgang.json", "w") as f:
                json.dump(l, f, indent=4)

        if str(ctx.author.id) not in l:
            y += 1

        with open("db_files/hoodgang.json", "r") as f:
            l2 = json.load(f)
        if str(ctx.author.id) in l2:
            l2.pop(str(ctx.author.id))
            msg = "You left `The Hood Gang`!"
            await ctx.send(msg)
            with open("db_files/hoodgang.json", "w") as f:
                json.dump(l2, f, indent=4)

        if str(ctx.author.id) not in l2:
            y += 1

        if y == 2:
            msg = "You are not part of a gang! To join one, type `<>mafia join <gang>`"
            await ctx.send(msg)
            return


def setup(bot):
    bot.add_cog(Fun(bot))
