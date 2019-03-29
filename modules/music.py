# because im actually super lazy this was just basically copied from lavalink.py's source
# there are some changes, like dialogue and check stuff, but the original code is below
# https://github.com/Devoxin/Lavalink.py/blob/master/examples/music-v3.py
# maybe later ill write my own module
# probably not lol
# ok ill end this now
# oh yeah i forgot to say i deleted some of the commands nobody will use
# ok ill really end this now

import logging
import math
import re
import discord
import lavalink
from discord.ext import commands
from utilities import checks

time_rx = re.compile('[0-9]+')
url_rx = re.compile('https?:\/\/(?:www\.)?.+')

global checks
checks = checks.Checks()


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):
            lavalink.Client(bot=bot, password=bot.config["lavapass"],
                            loop=bot.loop, log_level=logging.INFO, ws_port=2333)
            self.bot.lavalink.register_hook(self._track_hook)

    def __unload(self):
        for guild_id, player in self.bot.lavalink.players:
            self.bot.loop.create_task(player.disconnect())
            player.cleanup()
        # Clear the players from Lavalink's internal cache
        self.bot.lavalink.players.clear()
        self.bot.lavalink.unregister_hook(self._track_hook)

    async def _track_hook(self, event):
        if isinstance(event, lavalink.Events.StatsUpdateEvent):
            return
        channel = self.bot.get_channel(event.player.fetch('channel'))
        if not channel:
            return

        if isinstance(event, lavalink.Events.TrackStartEvent):
            await channel.send(embed=discord.Embed(title='Now playing:',
                                                   description=event.track.title,
                                                   color=discord.Color.blurple()))

        elif isinstance(event, lavalink.Events.QueueEndEvent):
            await channel.send('Your queue has ended~ It isn\'t a bad idea to play another song, though!')

    @commands.command(name='play', aliases=['p'])
    @checks.command()
    @commands.guild_only()
    async def _play(self, ctx, *, query: str):
        """ Searches and plays a song from a given query. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await self.bot.lavalink.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('I couldn\'t find anything~')

        embed = discord.Embed(color=discord.Color.blurple())

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'I put the playlist in your queue, {}~'.format(ctx.author.name)
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
            await ctx.send(embed=embed)
        else:
            track = results['tracks'][0]
            embed.title = 'I put the song in your queue, {}~'.format(ctx.author.name)
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            await ctx.send(embed=embed)
            player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()

    @commands.command(name='previous', aliases=['pv'])
    @checks.command()
    @commands.guild_only()
    async def _previous(self, ctx):
        """ Plays the previous song. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        try:
            await player.play_previous()
        except lavalink.NoPreviousTrack:
            await ctx.send("I can't find any previous songs...")

    @commands.command(name='playnow', aliases=['pn'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    @checks.command()
    async def _playnow(self, ctx, *, query: str):
        """ Plays immediately a song. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue and not player.is_playing:
            return await ctx.invoke(self._play, query=query)

        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await self.bot.lavalink.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('I couldn\'t find any songs...')

        tracks = results['tracks']
        track = tracks.pop(0)

        if results['loadType'] == 'PLAYLIST_LOADED':
            for _track in tracks:
                player.add(requester=ctx.author.id, track=_track)

        await player.play_now(requester=ctx.author.id, track=track)

    @commands.command(name='skip', aliases=['forceskip', 'fs'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    @checks.command()
    async def _skip(self, ctx):
        """ Skips the current track. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send("I don't think I'm playing anything.")

        await player.skip()
        await ctx.send('I skipped that for you~')

    @commands.command(name='stop')
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    @checks.command()
    async def _stop(self, ctx):
        """ Stops the player and clears its queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('I don\'t think I\'m playing anything.')

        player.queue.clear()
        await player.stop()
        await ctx.send('I stopped that for you~')

    @commands.command(name='now', aliases=['np', 'n', 'playing'])
    @commands.guild_only()
    @checks.command()
    async def _now(self, ctx):
        """ Shows some stats about the currently playing song. """
        player = self.bot.lavalink.players.get(ctx.guild.id)
        song = 'Nothing'

        if player.current:
            position = lavalink.Utils.format_time(player.position)
            if player.current.stream:
                duration = '🔴 LIVE'
            else:
                duration = lavalink.Utils.format_time(player.current.duration)
            song = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'

        embed = discord.Embed(color=discord.Color.blurple(),
                              title='Now Playing', description=song)
        await ctx.send(embed=embed)

    @commands.command(name='queue', aliases=['q'])
    @commands.guild_only()
    @checks.command()
    async def _queue(self, ctx, page: int = 1):
        """ Shows the player's queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('I can\'t find anything in the queue...')

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(colour=discord.Color.blurple(),
                              description=f'**{len(player.queue)} tracks**\n\n{queue_list}')
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        await ctx.send(embed=embed)

    @commands.command(name='pause', aliases=['resume'])
    @commands.guild_only()
    @checks.command()
    async def _pause(self, ctx):
        """ Pauses/Resumes the current track. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send("I'm not playing anything~")

        if player.paused:
            await player.set_pause(False)
            await ctx.send('I resumed that for you!')
        else:
            await player.set_pause(True)
            await ctx.send('I paused that for you!')

    @commands.command(name='volume', aliases=['vol'])
    @commands.guild_only()
    @checks.command()
    async def _volume(self, ctx, volume: int = None):
        """ Changes the player's volume. Must be between 0 and 1000. Error Handling for that is done by Lavalink. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not volume:
            return await ctx.send(f'I set the volume to {player.volume}% for you~')

        await player.set_volume(volume)
        await ctx.send(f'I set the volume to {player.volume}% for you~')

    @commands.command(name='shuffle')
    @commands.guild_only()
    @checks.command()
    async def _shuffle(self, ctx):
        """ Shuffles the player's queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send("I'm not playing anything..")

        player.shuffle = not player.shuffle
        await ctx.send('Shuffling ' + ('enabled' if player.shuffle else 'disabled') + " !")

    @commands.command(name='repeat', aliases=['loop'])
    @commands.guild_only()
    @checks.command()
    async def _repeat(self, ctx):
        """ Repeats the current song until the command is invoked again. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send("I'm not playing anything~")

        player.repeat = not player.repeat
        await ctx.send('Repeating ' + ('enabled' if player.repeat else 'disabled') + " !")

    @commands.command(name='disconnect', aliases=['dc'])
    @commands.guild_only()
    @checks.command()
    @commands.has_permissions(manage_messages = True)
    async def _disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send("Um.. I'm not connected to a voice channel~")

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("You don't seem to be in my voice channel.")

        player.queue.clear()
        await player.disconnect()
        await ctx.send('I disconnected from your voice channel~')

    @_playnow.before_invoke
    @_previous.before_invoke
    @_play.before_invoke
    async def ensure_voice(self, ctx):
        """ A few checks to make sure the bot can join a voice channel. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            if not ctx.author.voice or not ctx.author.voice.channel:
                await ctx.send('You aren\'t connected to any voice channel.')
                raise commands.CommandInvokeError(
                    'Author not connected to voice channel.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                await ctx.send('Missing permissions `CONNECT` and/or `SPEAK`.')
                raise commands.CommandInvokeError(
                    'Bot has no permissions CONNECT and/or SPEAK')

            player.store('channel', ctx.channel.id)
            await player.connect(ctx.author.voice.channel.id)
        else:
            if player.connected_channel.id != ctx.author.voice.channel.id:
                return await ctx.send('Join my voice channel!')


def setup(bot):
    bot.add_cog(Music(bot))
