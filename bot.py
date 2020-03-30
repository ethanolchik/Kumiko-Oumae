import discord
import random
import asyncio
import datetime
from discord.ext import commands
from psutil import Process
from os import getpid
bot = commands.Bot(command_prefix="<>")
bot.remove_command("help")

inital_extension = [
  'cogs.userinfo',
  'cogs.music',
  'cogs.moderation',
  'cogs.help'
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

bot.run('Njg1NTIxMjM2NjQ2MDM1NDkw.XoHdZQ.zvf3UcNXaJVzP6ZAmQZrfpV-56c')


@bot.command(aliases=['mem', 'm'], hidden=True)
@commands.is_owner()
async def memory(ctx):
    await ctx.send(f'im currently using **{round(Process(getpid()).memory_info().rss/1024/1024, 2)} MB** of memory.')


if __name__ == '__main__':
    for extension in inital_extension:
        bot.load_extension(extension)
print(bot.user)
