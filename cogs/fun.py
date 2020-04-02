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
import json
import random
import os
import time

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

        """The leaderboard of the best candy players!"""

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
            return

        if member == ctx.author:
            await ctx.send("You cannot fight yourself!")
            return

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
            with open("db_files/mafialb.json", "w") as f:
                json.dump(l, f, indent=4)

    @mafia.command(aliases=["top", "leaderboard"])
    async def _leaderboard(self, ctx):
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
                print(l[str(a)])

        embed = discord.Embed(
            description=res,
            colour=0x0EF7E2
        )
        embed.set_footer(
            text="Join our support server! `https://discord.gg/YUm2sBD`",
            icon_url=self.bot.user.avatar_url_as(static_format="png")
        )
        await ctx.send(embed=embed)

    @mafia.command()
    async def create(self, ctx, name: str = None):
        print(name)
        if name == None:
            await ctx.send("Please specify a gang to join!")

        for file in os.listdir("gangs"):
            with open(f"gangs/{file}", "r") as f:
                l = json.load(f)
            for user in l:
                if user == str(ctx.author.id):
                    await ctx.send("You are already in a gang! To leave, type `<>mafia leave`.")
                    return

        l[str(ctx.author.id)] = 1

        with open(f"gangs/{name}gang.json", "w") as f:
            json.dump(l, f, indent=4)

        await ctx.send(f"You created `The {name} gang`!")

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
        try:
            p = l[str(ctx.author.id)]
            p2 = l2[str(ctx.author.id)]
        except KeyError:
            await ctx.send("You are missing an account! To get one, play one mafia game with someone and win it!")
            return

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
        embed.set_footer(
            text="Join our support server! `https://discord.gg/YUm2sBD`",
            icon_url=self.bot.user.avatar_url_as(static_format="png")
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
        embed = discord.Embed()
        embed.title = "Gang"
        embed.colour = 0x0EF7E2
        for file in os.listdir("gangs"):
            with open(f"gangs/{file}", "r") as f:
                print(file)
                l = json.load(f)
            for user in l:
                if user == str(ctx.author.id):
                    if file.endswith("gang.json"):
                        file = file[:-9]
                        msg = f"You are in `The {file} Gang`"
                        embed.description = msg

        await ctx.send(embed=embed)

    @mafia.command()
    async def join(self, ctx, gang: str = None):
        print(gang)
        if gang == None:
            await ctx.send("Please specify a gang to join!")

        for file in os.listdir("gangs"):
            with open(f"gangs/{file}", "r") as f:
                l = json.load(f)
            for user in l:
                if user == str(ctx.author.id):
                    await ctx.send("You are already in a gang! To leave, type `<>mafia leave`.")
                    return

        l[str(ctx.author.id)] = 1

        with open(f"gangs/{gang}gang.json", "w") as f:
            json.dump(l, f, indent=4)

        await ctx.send(f"You joined `The {gang} gang`!")

    @mafia.command()
    async def leave(self, ctx):
        for file in os.listdir("gangs"):
            with open(f"gangs/{file}", "r") as f:
                l = json.load(f)
            for user in l:
                if user == str(ctx.author.id):
                    l.pop(str(ctx.author.id))
                with open(f"gangs/{file}", "w") as f:
                    json.dump(l, f, indent=4)
                    file = file[:-9]
                    await ctx.send(f"You left the {file} gang!")
                    break

    @mafia.command()
    async def give(self, ctx, user: discord.User = None, amount: int = None):
        if user == None:
            await ctx.send("Please specify a person to give money to!")
        if amount == None:
            await ctx.send("Please specify an amount to give!")

        with open("db_files/mafiaw.json", "r") as f:
            l = json.load(f)



    @mafia.command()
    async def shop(self, ctx, item: str = None):
        invite = "https://discord.gg/YUm2sBD"
        items = {
            "Pizza": 10,
            "Burger": 15,
            "Taco": 5,
            "Coke": 5,
            "Sprite": 5,
            "Monster": 8
        }
        with open("db_files/mafiaw.json", 'r') as f:
            l = json.load(f)

        if item == None:
            embed = discord.Embed(
                title="Shop",
                description="Food",
                colour=0x0EF7E2
            )
            embed.add_field(
                name="Food",
                value="Pizza ($10) `::` Burger (15$) `::` Taco (5$)",
                inline=False
            )
            embed.add_field(
                name="Drinks",
                value="Coke ($5) `::` Sprite (5$) `::` Monster (8$)",
                inline=True
            )
            embed.set_footer(
                text="Join our support server! `https://discord.gg/YUm2sBD`",
                icon_url=self.bot.user.avatar_url_as(static_format="png")
            )
            await ctx.send(embed=embed)
            return

        for thing in items:
            if thing == item:
                try:
                    if l[str(ctx.author.id)] - items[item] >= 0:
                        l[str(ctx.author.id)] -= 10
                    else:
                        await ctx.send(f"You don't have enough money on you to buy that! Withdraw money to buy this item!.")
                        return
                except KeyError as e:
                    await ctx.send(f"Could not buy item! Try winning a mafia game. More support: `{invite}`")
                    return
                else:
                    with open("db_files/mafiaw.json", "w") as f:
                        json.dump(l, f, indent=4)

                with open("db_files/mafiaw.json", "w") as f:
                    json.dump(l, f, indent=4)

                await ctx.send(f"Successfully bought {item}")


def setup(bot):
    bot.add_cog(Fun(bot))
