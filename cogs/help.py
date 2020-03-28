import discord
from discord.ext import commands



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #commands.Bot.remove_command(self, name="help")
    @commands.command()
    async def help(self, ctx, branch = None):
        branches = ["MUSIC", "USERINFO"]
        if not branch == None:
            branch == f"{branch}"
        if branch == None:
            embed = discord.Embed(
                title="Help",
                description="Please specify one of the following branches: ",
                colour=0x0EF7E2
            )
            embed.add_field(
                name="Music",
                value="Type: `<>help music`",
                inline=False
            )
            embed.add_field(
                name="User Info",
                value="Type: `<>help userinfo`",
                inline=False
            )
            await ctx.send(embed=embed)
        elif branch in branches:
            if branch.upper() == "MUSIC":
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
                    name="",
                    value= """
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
                    format: `<>volume <value[1 - 1000]>
                    """,
                    inline = False
                )
                await ctx.send(embed=embed)
            elif branch.upper() == "USERINFO":
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

def setup(bot):
    bot.add_cog(Help(bot))