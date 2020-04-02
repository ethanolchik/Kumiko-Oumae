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

import config
import discord
import random
import asyncio
import os
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
  'cogs.help',
  'cogs.fun',
  'cogs.meta'
]


@bot.event
async def on_ready():
  bot.load_extension("jishaku")
  for extension in inital_extension:
    bot.load_extension(extension)


@bot.command(aliases=['mem', 'm'], hidden=True)
@commands.is_owner()
async def memory(ctx):
    await ctx.send(f'im currently using **{round(Process(getpid()).memory_info().rss/1024/1024, 2)} MB** of memory.')


@bot.command()
async def ping(ctx):
    '''die Response Time'''
    ping = ctx.message
    pong = await ctx.send('**:ping_pong:** Pong!')
    delta = pong.created_at - ping.created_at
    delta = int(delta.total_seconds() * 1000)
    await pong.edit(content=f':ping_pong: Pong! ({delta} ms)\n*Discord WebSocket Latency: {round(bot.latency, 5)} ms*')

bot.run(config.token)


if __name__ == '__main__':
    for extension in inital_extension:
        bot.load_extension(extension)
print(bot.user)
