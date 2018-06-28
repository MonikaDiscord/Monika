import logging
import math
import re
from utilities import checks
import discord
import lavalink
from discord.ext import commands
import asyncio
import sys
import os

global checks
checks = checks.Checks()

time_rx = re.compile('[0-9]+')

class Music:

    def __init__(self, bot):
        self.bot = bot

        self.bot.lavalink.register_hook(self.track_hook)

    async def track_hook(self, event):
        if self.bot.mrepair:
            return
        if isinstance(event, lavalink.Events.TrackStartEvent):
            c = event.player.fetch('channel')
            if c:
                c = self.bot.get_channel(c)
                u = event.player.fetch('user')
                if u:
                    u = self.bot.get_user(u)
                if c:
                    if event.player.fetch('repair') == False:
                        embed = discord.Embed(colour=c.guild.me.color, title="I'm now playing:", description=event.track.title)
                        embed.set_thumbnail(url=event.track.thumbnail)
                        if u:
                            embed.set_footer(text="Requested by {}")
                        await c.send(embed=embed)
        elif isinstance(event, lavalink.Events.QueueEndEvent):
            await event.player.disconnect()
            event.player.repeat = False
            c = event.player.fetch('channel')
            if c:
                c = self.bot.get_channel(c)
                if c:
                    if event.player.fetch('repair') == False:
                        await c.send('Well, I finished playing all those songs. Don\'t be afraid to add another one!')

    @commands.command(aliases=['p'])
    @checks.command()
    async def play(self, ctx, *, query):
        if self.bot.mrepair:
            return await ctx.send("I'm sorry, but music appears to be broken. Try again in a few minutes.")

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            if not ctx.author.voice or not ctx.author.voice.channel:
                return await ctx.send('You need to be in a voice channel to play something.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                return await ctx.send("I'm sorry, but I don't have the permissions to do that.")

            player.store('channel', ctx.channel.id)
            await player.connect(ctx.author.voice.channel.id)
        else:
            if not ctx.author.voice or not ctx.author.voice.channel or player.connected_channel.id != ctx.author.voice.channel.id:
                return await ctx.send('You need to be in my voice channel to play something.')

        query = query.strip('<>')

        if not query.startswith('http'):
            query = f'ytsearch:{query}'

        tracks = await self.bot.lavalink.get_tracks(query)

        if not tracks:
            return await ctx.send('Nothing was found...')

        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)

        if 'list' in query and 'ytsearch:' not in query:
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = "That playlist was added to the queue!"
            embed.description = f"Imported {len(tracks)} tracks from the playlist :)"
            await ctx.send(embed=embed)
        else:
            embed.title = "That track was added to the queue!"
            embed.description = f'[{tracks[0]["info"]["title"]}]({tracks[0]["info"]["uri"]})'
            await ctx.send(embed=embed)
            player.add(requester=ctx.author.id, track=tracks[0])

        if not player.is_playing:
            await player.play()
            # self-repair
            p1 = player.current.uri
            await asyncio.sleep(10)
            p2 = player.current.uri
            if player.is_playing and p1 == p2:
                if lavalink.Utils.format_time(player.position) == "00:00:00" and self.bot.mrepair == False:
                    self.bot.mrepair = True
                    player.store('repair', True)
                    await ctx.send("Music doesn't seem to be working, so I'll fix it right now!")
                    await ctx.send("This will take about 10 minutes, so please try again after that.")
                    await ctx.send("Note: I may restart during this process.")
                    c = self.bot.get_channel(404067028790673409)
                    await c.send("Self-repairing music.")
                    await self.bot.reload_music()
                    player.queue.clear()
                    ts = await self.bot.lavalink.get_tracks("ytsearch:your reality")
                    for t in ts:
                        player.add(requester=ctx.author.id, track=track)
                    await player.play()
                    await asyncio.sleep(10)
                    if lavalink.Utils.format_time(player.position) == "00:00:00":
                        await c.send("Self-repair failed, restarting process.")
                        await self.bot.restart()
                    else:
                        await ctx.send("Music should be fixed! I'll play your requested song now.")
                        await player.skip()
                        for track in tracks:
                            player.add(requester=ctx.author.id, track=track)
                            await player.play()
                            player.store('repair', False)
                            await c.send("Self-repair finished.")


    @commands.command()
    @checks.command()
    @checks.is_patron()
    async def seek(self, ctx, time):
        if self.bot.mrepair:
            return await ctx.send("I'm sorry, but music appears to be broken. Try again in a few minutes.")

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send("I'm not playing anything...")

        pos = '+'
        if time.startswith('-'):
            pos = '-'

        seconds = time_rx.search(time)

        if not seconds:
            return await ctx.send('You need to specify the amount of seconds to skip!')

        seconds = int(seconds.group()) * 1000

        if pos == '-':
            seconds = seconds * -1

        track_time = player.position + seconds

        await player.seek(track_time)

        await ctx.send(f'I moved the track to **{lavalink.Utils.format_time(track_time)}** just for you~')

    @commands.command()
    @checks.command()
    async def skip(self, ctx):
        if self.bot.mrepair:
            return await ctx.send("I'm sorry, but music appears to be broken. Try again in a few minutes.")

        player = self.bot.lavalink.players.get(ctx.guild.id)
        
        if player.fetch('repair') == True:
            return await ctx.send("You can't do that right now. Try again in about 10 minutes.")

        if not player.is_playing:
            return await ctx.send("I'm not playing anything...")

        await ctx.send('I skipped that for you~')
        await player.skip()

    @commands.command()
    @checks.command()
    @commands.has_permissions(manage_messages = True)
    async def stop(self, ctx):
        if self.bot.mrepair:
            return await ctx.send("I'm sorry, but music appears to be broken. Try again in a few minutes.")

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if player.fetch('repair') == True:
            return await ctx.send("You can't do that right now. Try again in about 10 minutes.")

        if not player.is_playing:
            return await ctx.send("I'm not playing anything...")

        player.queue.clear()
        await player.stop()
        await player.disconnect()
        await ctx.send('I stopped the queue just for you~')

    @commands.command()
    @checks.command()
    async def now(self, ctx):
        if self.bot.mrepair:
            return await ctx.send("I'm sorry, but music appears to be broken. Try again in a few minutes.")

        player = self.bot.lavalink.players.get(ctx.guild.id)
        song = 'Nothing'

        if player.current:
            pos = lavalink.Utils.format_time(player.position)
            if player.current.stream:
                dur = 'LIVE'
            else:
                dur = lavalink.Utils.format_time(player.current.duration)
            song = f'**[{player.current.title}]({player.current.uri})**\n({pos}/{dur})'

        embed = discord.Embed(colour=ctx.guild.me.top_role.colour, title="I'm now playing:", description=song)
        await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    @checks.command()
    async def queue(self, ctx, page: int=1):
        if self.bot.mrepair:
            return await ctx.send("I'm sorry, but music appears to be broken. Try again in a few minutes.")

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send("There's nothing in the queue. Don't be afraid to add something!")

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''

        for i, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{i + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(colour=ctx.guild.me.top_role.colour,
                              title=f'{len(player.queue)} tracks are queued.',
                              description=f'{queue_list}')
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['resume'])
    @checks.command()
    @checks.is_patron()
    async def pause(self, ctx):
        if self.bot.mrepair:
            return await ctx.send("I'm sorry, but music appears to be broken. Try again in a few minutes.")

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if player.fetch('repair') == True:
            return await ctx.send("You can't do that right now. Try again in about 10 minutes.")

        if not player.is_playing:
            return await ctx.send('Not playing.')

        if player.paused:
            await player.set_pause(False)
            await ctx.send('I have resumed the track.')
        else:
            await player.set_pause(True)
            await ctx.send('That track has been paused.')

    @commands.command(aliases=['vol'])
    @checks.command()
    async def volume(self, ctx, volume: int=None):
        if self.bot.mrepair:
            return await ctx.send("I'm sorry, but music appears to be broken. Try again in a few minutes.")

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not volume:
            return await ctx.send(f'🔈 | {player.volume}%')

        await player.set_volume(volume)
        await ctx.send(f'🔈 | Set to {player.volume}%')

    @commands.command()
    @checks.command()
    @checks.is_patron()
    async def shuffle(self, ctx):
        if self.bot.mrepair:
            return await ctx.send("I'm sorry, but music appears to be broken. Try again in a few minutes.")

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Nothing is currently playing...')

        player.shuffle = not player.shuffle

        await ctx.send('I have toggled shuffling to ' + ('enabled.' if player.shuffle else 'disabled.'))

    @commands.command()
    @checks.command()
    @checks.is_patron()
    async def repeat(self, ctx):
        if self.bot.mrepair:
            return await ctx.send("I'm sorry, but music appears to be broken. Try again in a few minutes.")

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Nothing is currently playing...')

        player.repeat = not player.repeat

        await ctx.send('I have toggled repeating to ' + ('enabled.' if player.repeat else 'disabled.'))

    @commands.command()
    @checks.command()
    @commands.has_permissions(manage_messages = True)
    async def remove(self, ctx, index: int):
        if self.bot.mrepair:
            return await ctx.send("I'm sorry, but music appears to be broken. Try again in a few minutes.")

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('Nothing is in the queue...')

        if index > len(player.queue) or index < 1:
            return await ctx.send('Index has to be >=1 and <=queue size...')

        index = index - 1
        removed = player.queue.pop(index)

        await ctx.send('I have removed **' + removed.title + '** from the queue.')

    @commands.command()
    @checks.command()
    @commands.has_permissions(manage_messages = True)
    async def disconnect(self, ctx):
        if self.bot.mrepair:
            return await ctx.send("I'm sorry, but music appears to be broken. Try again in a few minutes.")

        player = self.bot.lavalink.players.get(ctx.guild.id)

        if player.fetch('repair') == True:
            return await ctx.send("You can't do that right now. Try again in about 10 minutes.")

        if not player.is_connected:
            return await ctx.send("I'm not connected to a voice channel...")

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send("You have to be in my voice channel to disconnect me.")

        await player.disconnect()
        await ctx.send('I have disconnected from the voice channel.')


def setup(bot):
    bot.add_cog(Music(bot))
