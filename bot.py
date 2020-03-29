import discord
import random
import asyncio
import datetime
from utils.webserver import keep_alive
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
  '''die Response Time'''
  ping = ctx.message
  pong = await ctx.send('**:ping_pong:** Pong!')
  delta = pong.created_at - ping.created_at
  delta = int(delta.total_seconds() * 1000)
  await pong.edit(content=f':ping_pong: Pong! ({delta} ms)\n*Discord WebSocket Latency: {round(bot.latency, 5)} ms*')
keep_alive()
bot.run('Njg1NTIxMjM2NjQ2MDM1NDkw.Xn87cw.4EHBLmUUvUYYcTURtc_js9M7Q9I')


if __name__ == '__main__':
    for extension in inital_extension:
        bot.load_extension(extension)
print(bot.user)
