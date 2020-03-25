import discord
import random
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix="<>")


@bot.command()
async def ping(ctx):
  """
  die response time
  """
  await ctx.send(f"Pong! Bot latency: {round(bot.latency, 5)}")


@bot.command()
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


@bot.command()
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




inital_extension = [
  'cogs.userinfo',
  'cogs.music'
]

if __name__ == '__main__':
  for extension in inital_extension:
    bot.load_extension(extension)

bot.run('Njg1NTIxMjM2NjQ2MDM1NDkw.XmJ4Hw.B5evj9Sn91JrmAFvbM8ory_ST6g')
