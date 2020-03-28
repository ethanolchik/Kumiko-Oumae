import discord
import random
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix="<>")

bot.remove_command("help")

inital_extension = [
  'cogs.userinfo',
  'cogs.music',
  'cogs.help'
]

@bot.command()
async def ping(ctx):
  """
  die response time
  """
  await ctx.send(f"Pong! Bot latency: {round(bot.latency, 5)}")


@bot.command(aliases=["lc name"])
@commands.is_owner()
async def load_cog(ctx, cog):
  """
  loads a cog
  """
  toLoad = f"cogs.{cog}"
  msg = await ctx.send(f"Loading cog {cog} <a:typing:597589448607399949>")
  try:
    bot.load_extension(toLoad)
  except NameError as e:
    await msg.delete()
    await ctx.message.add_reaction('<:redTick:596576672149667840>')
    await ctx.send(f"<:yikes:596577035313348629> Error while loading cog! details: {e}")
  else:
    await asyncio.sleep(random.randint(0, 3))
    await ctx.message.add_reaction(
      '<:greenTick:596576670815879169>'
    )
    await msg.delete()


@bot.command(aliases=["load"])
@commands.is_owner()
async def load_bot(ctx):
  msg = await ctx.send("loading <a:typing:597589448607399949>")
  await asyncio.sleep(random.randint(0, 3))
  for extension in inital_extension:
    bot.load_extension(extension)
  await msg.delete()
  await ctx.message.add_reaction("<:greenTick:596576670815879169>")



@bot.command()
@commands.is_owner()
async def reload(ctx):
  for extension in inital_extension:
    bot.unload_extension(extension)
  msg = await ctx.send("reloading <a:typing:597589448607399949>")
  await asyncio.sleep(random.randint(0, 3))
  for extension in inital_extension:
    bot.load_extension(extension)
  await msg.delete()
  await ctx.message.add_reaction('<:greenTick:596576670815879169>')


@bot.command(aliases=["uc name"])
@commands.is_owner()
async def unload_cog(ctx, cog):
  """
  unloads a cog
  """
  toUnload = f"cogs.{cog}"
  msg = await ctx.send(f"Unloading cog '{cog}' <a:typing:597589448607399949>")
  try:
    bot.unload_extension(toUnload)
  except NameError as e:
    await ctx.send(f"<:yikes:596577035313348629> Error while unloading cog! details: {e}")
  else:
    await asyncio.sleep(random.randint(0, 3))
    await ctx.message.add_reaction(
      '<:greenTick:596576670815879169>'
    )
    await msg.delete()


@bot.command()
async def help(ctx, branch = None):
  branches = ["MUSIC", "USERINFO"]
  if branch == None:
    embed = discord.Embed(
      title="Help",
      description="Please specify one of the following branches: ",
      colour = 0x0EF7E2
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
            disconnect Disconnects the player from the voice channel and clears its que... format: `None`
            find       Lists the first 10 search results from a given query. format: `<>find <query>`
            now        Shows some stats about the currently playing song. format: `None`
            pause      Pauses/Resumes the current track. format: `None`
            play       Searches and plays a song from a given query. format: `<>play query / url`
            queue      Shows the player's queue. format: `None`
            remove     Removes an item from the player's queue with the given index. format: `<>remove <item>` 
            repeat     Repeats the current song until the command is invoked again. format: `None`
            seek       Seeks to a given position in a track. format: `<>seek <position[1 - ...]>`
            shuffle    Shuffles the player's queue. format: `None`
            skip       Skips the current track. format: `None`
            stop       Stops the player and clears its queue. format: `None`
            volume     Changes the player's volume. Must be between 0 and 1000. format: `<>volume <value[1 - 1000]>
            """,
        inline=False
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


bot.run('Njg1NTIxMjM2NjQ2MDM1NDkw.Xn87cw.4EHBLmUUvUYYcTURtc_js9M7Q9I')




if __name__ == '__main__':
  for extension in inital_extension:
    bot.load_extension(extension)
print(bot.user)

