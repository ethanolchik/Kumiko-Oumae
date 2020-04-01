"""
Chorus discord bot
~ EraseKesu - class Erase#0027
"""

import discord
import asyncio

from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *args):
        """Kicks a member from the server"""
        msg = ' '.join(args)

        embed = discord.Embed(
            title="Kick",
            description=f"{member.mention} has been kicked from the server by {ctx.author.mention} for {msg}!",
            colour=discord.Colour.from_rgb(255, 0, 0)
        )

        embed.set_footer(
            text="Join our support server! `https://discord.gg/YUm2sBD`",
            icon_url=self.bot.user.avatar_url_as(static_format="png")
        )

        await ctx.guild.kick(member)
        await member.send(embed=embed)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *args):
        """Bans a member from the server"""
        msg = ' '.join(args)

        embed = discord.Embed(
            title="Ban",
            description=f"{member.mention} has been banned from the server by {ctx.author.mention} fro {msg}!",
            colour=discord.Colour.from_rgb(225, 0, 0)
        )
        embed.set_footer(
            text="Join our support server! `https://discord.gg/YUm2sBD`",
            icon_url=self.bot.user.avatar_url_as(static_format="png")
        )


        await member.send(embed=embed)
        await ctx.guild.ban(member)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member):
        """Un-bans a member from the server"""

        await ctx.guild.unban(member)
        await ctx.send(f"{member.mention} has been successfully unbanned!")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, id):
        """Bans a member by id. this can be used to ban someone who is not in the server."""

        await ctx.guild.ban(discord.Object(id))
        await ctx.send(f"Member Has been hackbanned!")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unhackban(self, ctx, id):
        """Un-hackbans someone from the server"""


        await ctx.guild.unban(discord.Object(id))
        await ctx.send(f"Member's hackban has been infracted!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, *args):
        """mutes someone in the server. Must have a role called Muted or muted"""
        msg = ' '.join(args)
        role = discord.utils.get(ctx.guild.roles, name="Muted" or "muted")
        embed = discord.Embed(
            title="Mute",
            description=f"{member.mention} has been muted by {ctx.author.mention} for {msg}!",
            colour=discord.Colour.from_rgb(255, 0, 0)
        )
        embed.set_footer(
            text="Join our support server! `https://discord.gg/YUm2sBD`",
            icon_url=self.bot.user.avatar_url_as(static_format="png")
        )

        await member.add_roles(role)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """unmutes someone in the server"""
        role = discord.utils.get(ctx.guild.roles, name="Muted" or "muted")


        await member.remove_roles(role)
        await ctx.send(f"{member.mention} has been unmuted! Try to follow the rules next time..")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def tempmute(self, ctx, member : discord.Member, time:int, timeval, *args):
        """Temporarily mutes someone in the server for a given amount of time. must have a role called Muted or muted."""
        msg = ' '.join(args)
        role = discord.utils.get(ctx.guild.roles, name="Muted" or "muted")
        realtime = 0
        timetodivide = 0

        if timeval == 'h':
            realtime = time * 3600
            timetodivide = 3600

        elif timeval == 'm':
            realtime = time * 2592000
            timetodivide = 2592000

        elif timeval == 'y':
            realtime = time * 31536000
            timetodivide = 31536000

        elif timeval == 'mins':
            realtime = time * 60
            timetodivide = 60

        elif timeval == 's':
            realtime = time * 1
            timetodivide = 1

        embed = discord.Embed(
            title="TempMute",
            description=f"Member Has been Temporarily Muted for {realtime / timetodivide}{timeval}",
            colour=0xe74c3c
        )
        embed.set_footer(
            text="Join our support server! `https://discord.gg/YUm2sBD`",
            icon_url=self.bot.user.avatar_url_as(static_format="png")
        )

        await member.add_roles(role)
        await ctx.send(embed=embed)
        await asyncio.sleep(realtime)
        await member.remove_roles(role)
        await ctx.author.send(f"{member} has been unmuted after {realtime/timetodivide}{timeval}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, *args):
        """Warns a member in the guild."""
        msg = ' '.join(args)
        x = []
        warns = 1

        with open("db_files/warns.txt", "r") as f:
            for word in f.readlines():
                x.append(word)
                if str(member.id) in str(word):
                    warns += 1

        with open("db_files/warns.txt", "a") as f:
            y = str(member.id) + "\n//============================\n"
            f.write(y)

            embed = discord.Embed(
                title="Warn",
                description=f"{member.mention} has been warned for {msg}",
                colour=discord.Colour.from_rgb(255, 0, 0)
            )

            embed.add_field(
                name="warns",
                value=str(warns),
                inline=False
            )

            embed.set_footer(
                text="Join our support server! `https://discord.gg/YUm2sBD`",
                icon_url=self.bot.user.avatar_url_as(static_format="png")
            )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
