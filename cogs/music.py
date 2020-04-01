"""
Chorus discord bot
~ EraseKesu - class Erase#0027
"""

import math
import re
import copy
from urllib.parse import quote

import asyncio
import discord
import lavalink
from discord.ext import commands, menus, tasks



# ----- define constants ----- #
time_rx = re.compile("[0-9]+")
url_rx = re.compile("https?:\\/\\/(?:www\\.)?.+")
REPEAT_EMOJI = "🔁"
STOP_EMOJI = "⏹️"
SHUFFLE_EMOJI = "🔀"
YOUTUBE_EMOJI = "<:youtube:520999601931812893>"
VOLUME_OFF_EMOJI = "🔇"
VOLUME_ON_EMOJI = "🔈"
PAUSE_EMOJI = "⏸️"
PLAY_EMOJI = "🎵"
VOLUME_UP_EMOJI = "<:vOlUme_up:693020638515822634>"
VOLUME_DOWN_EMOJI = "<:arrowdownicon:693020997384929340>"
LYRIC_EMOJI = "\U0001f4cb"
TRASH_EMOJI = "\U0001f5d1"
EMBED_COLOR = 0x0EF7E2
SKIP_EMOJI = "⏭️"
BACK_EMOJI = "◀️"
DC_EMOJI = ""
DEL_AFTER_TIME = 5
OFF_EMOJI = "📴"
# ---------------------------- #
print(lavalink.__version__)

def get_bar(current, total):
    n = 20
    num = int(current / total * n)
    return "▬" * num + "▭" + "=" * (n - num)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.paginator_queue = dict()
        self.get_bar = get_bar
        self.open_menus = dict()
        bot.open_menus = self.open_menus
        self.ksoft_lyrics_base_url = "https://api.ksoft.si/lyrics/search?q={}"
        # This ensures the client isn't overwritten during cog reloads.
        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('127.0.0.1', 2100, 'youshallnotpass', 'eu',
                                  'default-node')  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        bot.lavalink.add_event_hook(self.track_hook)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)

        return guild_check
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                title="An Unexpected Error Occurred!",
                description=f"""
                ```cmd
                {error.original}
                ```
                """,
                inline=False
            )
            await ctx.send(embed=embed)


    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @staticmethod
    def rq_check(ctx):
        return (
            ctx.author.id
            == ctx.bot.lavalink.player_manager.get(ctx.guild.id).current.requester
        )

    @commands.command(aliases=["p"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx, *, query: str):
        """ Searches and plays a song from a given query. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        query = query.strip("<>")

        if not url_rx.match(query):
            query = f"ytsearch:{query}"

        results = await player.node.get_tracks(query)

        if not results or not results["tracks"]:
            return await ctx.send("Nothing found!", delete_after=DEL_AFTER_TIME)

        embed = discord.Embed(color=EMBED_COLOR)

        if results["loadType"] == "PLAYLIST_LOADED":
            tracks = results["tracks"]

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = f"{PLAY_EMOJI} Playlist Added To The Queue!"
            other = f"Repeat: {(REPEAT_EMOJI if player.repeat else OFF_EMOJI)} - Shuffle: {(SHUFFLE_EMOJI if player.shuffle else OFF_EMOJI)}"
            embed.description = (
                f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks\n{other}'
            )
            await ctx.send(embed=embed)
        else:
            track = results["tracks"][0]
            embed.title = f"{PLAY_EMOJI} Track Added To The Queue"
            other = f"Repeat: {(REPEAT_EMOJI if player.repeat else OFF_EMOJI)} - Shuffle: {(SHUFFLE_EMOJI if player.shuffle else OFF_EMOJI)}"
            embed.description = (
                f'[{track["info"]["title"]}]({track["info"]["uri"]})\n{other}'
            )
            embed.set_image(
                url=f"https://img.youtube.com/vi/{track['info']['identifier']}/maxresdefault.jpg"
            )
            embed.set_footer(
                text=f"Tip: Use {ctx.prefix}now for playing status",
                icon_url=self.bot.user.avatar_url_as(static_format="png"),
            )
            await ctx.send(embed=embed)
            player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def seek(self, ctx, *, time: str):
        """ Seeks to a given position in a track. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        seconds = time_rx.search(time)
        if not seconds:
            return await ctx.send("You need to specify the amount of seconds to skip!")

        seconds = int(seconds.group()) * 1000
        if time.startswith("-"):
            seconds *= -1
        track_time = player.position + seconds
        await player.seek(track_time)

        await ctx.send(
            f"ℹ Moved track to **{lavalink.utils.format_time(track_time)}**"
        )

    @commands.command(aliases=["forceskip"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def skip(self, ctx):
        """ Skips the current track. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send(
                f"{PAUSE_EMOJI} Not playing.", delete_after=DEL_AFTER_TIME
            )

        await player.skip()
        embed = discord.Embed(title="⏭ Skipped.", color=EMBED_COLOR)
        await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stop(self, ctx):
        """ Stops the player and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send(
                f"{PAUSE_EMOJI} Not playing.", delete_after=DEL_AFTER_TIME
            )

        player.queue.clear()
        await player.stop()
        embed = discord.Embed(
            title=f"{STOP_EMOJI} Stopped. (Queue cleared)", color=EMBED_COLOR
        )
        await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

    @commands.command(aliases=["np", "n", "playing"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def now(self, ctx):
        """ Shows some stats about the currently playing song. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.current:
            return await ctx.send(
                f"{PAUSE_EMOJI} Nothing playing.", delete_after=DEL_AFTER_TIME
            )

        old_menu = self.open_menus.get(ctx.channel.id)
        if old_menu:
            old_menu.stop()
        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = "🔴 LIVE"
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        cur = None
        dur = None
        if not player.current.stream:
            cur = int(player.position / 1000)
            dur = int(player.current.duration / 1000)
            timeleft = dur - cur
        bar = "\n" + self.get_bar(cur, dur) if (cur and dur) else ""
        other = f"Repeat: {(REPEAT_EMOJI if player.repeat else OFF_EMOJI)} - Shuffle: {(SHUFFLE_EMOJI if player.shuffle else OFF_EMOJI)}"
        cleaned_title = await (commands.clean_content(escape_markdown=True)).convert(
            ctx, player.current.title
        )

        song = f"**[{cleaned_title}]({player.current.uri})**\n"

        embed = discord.Embed(
            color=EMBED_COLOR, title=f"{PLAY_EMOJI} Now Playing", description=song
        )
        embed.add_field(
            name="Requested by",
            value=f"{self.bot.get_user(player.current.requester).mention}",
            inline=True
        )
        print(player.current)
        embed.add_field(
            name="Time Left",
            value=f"""{timeleft} seconds left""",
            inline=True
        )
        embed.add_field(
            name="Volume",
            value=f"{player.volume}",
            inline=True
        )
        embed.set_thumbnail(
            url=f"https://img.youtube.com/vi/{player.current.identifier}/mqdefault.jpg"
        )
        embed.set_footer(
            text="Join our support server! `https://discord.gg/YUm2sBD`",
            icon_url=self.bot.user.avatar_url_as(static_format="png")
        )
        m = await ctx.send(embed=embed)
        menu = ReactionMenu(m)
        await menu.start(ctx)
        self.open_menus[ctx.channel.id] = menu


    @commands.command(aliases=["q"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def queue(self, ctx, page: int = 1):
        """ Shows the player's queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send(
                f"{PAUSE_EMOJI} Nothing is in the queue.", delete_after=DEL_AFTER_TIME
            )

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ""
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f"{index + 1}. [**{track.title}**]({track.uri})\n"

        embed = discord.Embed(
            colour=EMBED_COLOR,
            description=f'{len(player.queue)} {"tracks" if len(player.queue) > 1 else "track"}\n\n{queue_list}',
        )
        embed.set_footer(text=f"Viewing page {page}/{pages}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["resume"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pause(self, ctx):
        """ Pauses/Resumes the current track. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send(
                f"{PAUSE_EMOJI} Not playing.", delete_after=DEL_AFTER_TIME
            )

        if player.paused:
            await player.set_pause(False)
            embed = discord.Embed(title=f"{PLAY_EMOJI} Resumed", color=EMBED_COLOR)
            await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)
        else:
            await player.set_pause(True)
            embed = discord.Embed(title=f"{PAUSE_EMOJI} Paused", color=EMBED_COLOR)
            await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

    @commands.command(aliases=["vol"])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def volume(self, ctx, volume: int = None):
        """ Changes the player's volume. Must be between 0 and 1000. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not volume:
            embed = discord.Embed(
                title=f"{VOLUME_ON_EMOJI} {player.volume}%", color=EMBED_COLOR
            )
            return await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

        await player.set_volume(volume)
        embed = discord.Embed(
            title=f"{VOLUME_ON_EMOJI} Set to {player.volume}%", color=EMBED_COLOR
        )
        await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def shuffle(self, ctx):
        """ Shuffles the player's queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed = discord.Embed(
                title=f"{PAUSE_EMOJI} Nothing playing.", color=EMBED_COLOR
            )
            return await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)
        player.shuffle = not player.shuffle
        embed = discord.Embed(
            title=f"{SHUFFLE_EMOJI} Shuffle "
            + ("enabled" if player.shuffle else "disabled"),
            color=EMBED_COLOR,
        )
        await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

    @commands.command(aliases=["loop"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def repeat(self, ctx):
        """ Repeats the current song until the command is invoked again. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            embed = discord.Embed(
                title=f"{PAUSE_EMOJI} Nothing playing.", color=EMBED_COLOR
            )
            return await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

        player.repeat = not player.repeat
        embed = discord.Embed(
            title=f"{REPEAT_EMOJI} Repeat "
            + ("`ON`" if player.repeat else "`OFF`"),
            color=EMBED_COLOR,
        )
        await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def remove(self, ctx, index: int):
        """ Removes an item from the player's queue with the given index. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.queue:
            embed = discord.Embed(
                title=f"{PAUSE_EMOJI} Nothing in the queue.", color=EMBED_COLOR
            )
            return await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

        if index > len(player.queue) or index < 1:
            embed = discord.Embed(
                title=f"Index has to be between 1 and {len(player.queue)}.",
                color=EMBED_COLOR,
            )
            return await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)
        index -= 1
        removed = player.queue.pop(index)

        embed = discord.Embed(
            title=f"Removed **{removed.title}** from the queue.", color=EMBED_COLOR
        )
        await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def find(self, ctx, *, query):
        """ Lists the first 10 search results from a given query. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not query.startswith("ytsearch:") and not query.startswith("scsearch:"):
            query = "ytsearch:" + query

        results = await player.node.get_tracks(query)

        if not results or not results["tracks"]:
            return await ctx.send("Sorry, i couldn't find anything...", delete_after=DEL_AFTER_TIME)

        tracks = results["tracks"][:10]  # First 10 results

        o = ""
        for index, track in enumerate(tracks, start=1):
            track_title = track["info"]["title"]
            track_uri = track["info"]["uri"]
            o += f"`{index}.` [{track_title}]({track_uri})\n"

        embed = discord.Embed(color=EMBED_COLOR, description=o)
        embed.set_footer(
            text="Join our support server! `https://discord.gg/YUm2sBD`",
            icon_url=self.bot.user.avatar_url_as(static_format="png")
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["dc"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            embed = discord.Embed(title="Not connected.", color=EMBED_COLOR)
            return await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

        if not ctx.author.voice or (
            player.is_connected
            and ctx.author.voice.channel.id != int(player.channel_id)
        ):
            embed = discord.Embed(
                title="Please get in my voicechannel first.", color=EMBED_COLOR
            )

            return await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        embed = discord.Embed(title=f"{STOP_EMOJI} Disconnected", color=EMBED_COLOR)
        embed.set_footer(
            text="Thanks For using Chorus! Join our support server! `https://discord.gg/YUm2sBD`",
            icon_url=self.bot.user.avatar_url_as(static_format="png")
        )
        await ctx.send(embed=embed, delete_after=DEL_AFTER_TIME)

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(
            ctx.guild.id, endpoint=str(ctx.guild.region)
        )
        should_connect = ctx.command.name in ("play",)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError("Join a voicechannel first.")

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError("Not connected.")

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                raise commands.CommandInvokeError(
                    "I need the `CONNECT` and `SPEAK` permissions."
                )

            player.store("channel", ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError("You need to be in my voicechannel.")


class ReactionMenu(menus.Menu):
    def __init__(self, msg):
        super().__init__(timeout=60.0, delete_message_after=True)
        self.msg = msg
        self.result = None
        self.get_bar = get_bar

    @tasks.loop(seconds=10, count=6)
    async def update_playbar(self):
        try:
            if not self._running:
                self.update_playbar.stop()
            position = lavalink.utils.format_time(self.player.position)
            if self.player.current.stream:
                duration = "🔴 LIVE"
            else:
                duration = lavalink.utils.format_time(self.player.current.duration)
            cur = None
            dur = None

            if not self.player.current.stream:
                cur = int(self.player.position / 1000)
                dur = int(self.player.current.duration / 1000)
            bar = "\n" + self.get_bar(cur, dur) if (cur and dur) else ""
            other = f"Repeat: {(REPEAT_EMOJI if self.player.repeat else OFF_EMOJI)} - Shuffle: {(SHUFFLE_EMOJI if self.player.shuffle else OFF_EMOJI)}"
            cleaned_title = await (
                commands.clean_content(escape_markdown=True)
            ).convert(self.ctx, self.player.current.title)
            song = f"**[{cleaned_title}]({self.player.current.uri})**\n({position}/{duration}){bar}\n{other}"

            # actually format the new embed from the old one
            emb = self.msg.embeds[0]
            emb.description = song
            await self.msg.edit(embed=emb)
        except (AttributeError, discord.errors.NotFound):
            self.update_playbar.stop()

    async def send_initial_message(self, ctx, channel):
        self.ctx = ctx
        self.bot = ctx.bot
        self.player = self.bot.lavalink.player_manager.get(self.ctx.guild.id)
        copy.copy(self.update_playbar).start()
        return self.msg

    def reaction_check(self, payload):
        if payload.message_id != self.message.id:
            return False
        if payload.user_id not in (self.bot.owner_id, self._author_id):
            return False
        if payload.user_id != self.player.current.requester:
            self.bot.loop.create_task(
                self.msg.channel.send(
                    "Sorry, only the requester of this song can use these buttons.",
                    delete_after=DEL_AFTER_TIME,
                )
            )
            return False

        return payload.emoji in self.buttons

    @menus.button(REPEAT_EMOJI.strip("<>"))
    async def on_repeat_emoji(self, payload):
        await self.ctx.invoke(self.bot.get_command("repeat"))

    @menus.button(SHUFFLE_EMOJI.strip("<>"))
    async def on_shuffle_emoji(self, payload):
        await self.ctx.invoke(self.bot.get_command("shuffle"))

    @menus.button(PAUSE_EMOJI.strip("<>"))
    async def on_pause_emoji(self, payload):
        await self.ctx.invoke(self.bot.get_command("pause"))

    @menus.button(STOP_EMOJI.strip("<>"))
    async def on_stop_emoji(self, payload):
        await self.ctx.invoke(self.bot.get_command("stop"))

    @menus.button(VOLUME_UP_EMOJI.strip("<>"))
    async def on_vol_up_emoji(self, payload):
        volume = self.player.volume
        new_vol = volume + 25
        await self.ctx.invoke(self.bot.get_command("volume"), volume=new_vol)

    @menus.button(VOLUME_DOWN_EMOJI.strip("<>"))
    async def on_vol_down_emoji(self, payload):
        volume = self.player.volume
        new_vol = volume - 25
        await self.ctx.invoke(self.bot.get_command("volume"), volume=new_vol)

    @menus.button(TRASH_EMOJI.strip("<>"))
    async def on_trash_emoji(self, payload):
        self.stop()

def setup(bot):
    bot.add_cog(Music(bot))
