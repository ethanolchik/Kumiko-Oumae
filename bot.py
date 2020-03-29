import discord
import random
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix="<>")
bot.remove_command("help")

inital_extension = [
  'cogs.userinfo',
  'cogs.music',
  'cogs.help',
]

@bot.event
async def on_ready():
  bot.load_extension("jishaku")
  for extension in inital_extension:
    bot.load_extension(extension)


@bot.command()
async def ping(ctx):
  """
  die response time
  """
  await ctx.send(f"Pong! Bot latency: {round(bot.latency, 5)}")

bot.run('Njg1NTIxMjM2NjQ2MDM1NDkw.Xn87cw.4EHBLmUUvUYYcTURtc_js9M7Q9I')


if __name__ == '__main__':
    for extension in inital_extension:
        bot.load_extension(extension)
print(bot.user)

