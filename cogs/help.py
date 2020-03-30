import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands.Bot.remove_command(self, name="help")
    @commands.command()
    async def help(self, ctx, branch=None):
        if branch != None and branch == "music" or "Music":
            embed = discord.Embed(
                title="Help",
                description="Music Commands: ",
                colour=0x0EF7E2
            )
            embed.add_field(
                name="Music",
                value="""
                disconnect Disconnects the player from the voice channel and clears its que.
                format: `None`
                find       Lists the first 10 search results from a given query.
                format: `<>find <query>`
                now        Shows some stats about the currently playing song.
                format: `None`
                pause      Pauses/Resumes the current track.
                format: `None`
                play       Searches and plays a song from a given query.
                format: `<>play query / url`
                queue      Shows the player's queue.
                format: `None`
                     """,
                inline=False
            )
            embed.add_field(
                name="Music: ",
                value="""
                remove     Removes an item from the player's queue with the given index.
                format: `<>remove <item>` 
                repeat     Repeats the current song until the command is invoked again.
                format: `None`
                seek       Seeks to a given position in a track.
                format: `<>seek <position[1 - ...]>`
                shuffle    Shuffles the player's queue.
                format: `None`
                skip       Skips the current track.
                format: `None`
                stop       Stops the player and clears its queue.
                format: `None`
                volume     Changes the player's volume. Must be between 0 and 1000.
                format: `<>volume <value[1 - 1000]>`
                     """,
                inline=False
            )
            await ctx.send(embed=embed)
        elif branch != None and branch == "userinfo" or "Userinfo" or "UserInfo" or "userInfo":
                embed = discord.Embed(
                    title="Help",
                    description="Userinfo Commands: ",
                    colour=0x0EF7E2
                )
                embed.add_field(
                    name="Userinfo",
                    value="""
                user       Get user information. format: `None` or `<@user>`
                avatar     Get users profile picture. format: 'None' or `<@user>`
                """,
                    inline=False
                )
                await ctx.send(embed=embed)
        elif branch != None and branch == "moderation" or "Moderation" or "mod" or "Mod":
                embed = discord.Embed(
                    title="Help",
                    description="Moderation Commands: ",
                    colour=0x0EF7E2
                )
                embed.add_field(
                    name="Moderation",
                    value= """
                    ban        Bans a member from the server
                    format: `<>ban <@member> <reason>`
                    hackban    Bans a member by id. this can be used to ban someone who is not in the server
                    format: `<>hackban <memberid>`
                    kick       Kicks a member from the server
                    mute       mutes someone in the server. Must have a role called Muted or muted
                    tempmute   Temporarily mutes someone in the server for a given amount of time. must have a role called Muted or muted
                    format: `<>tempmute <@member> <time> <timevalue> <reason>`
                    """,
                    inline=False
                )
                embed.add_field(
                    name="Moderation",
                    value="""
                    unban      Un-bans a member from the server
                    format: `<>unban <@member>`
                    unhackban  Un-hackbans someone from the server
                    format: `<>unhackban <memberid>`
                    unmute     unmutes someone in the server
                    format: `<>unmute <@member>`
                    warn       Warns a member in the guild.
                    format: `<>warn <@member> <reason>`
                    """,
                    inline=False
                )
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
