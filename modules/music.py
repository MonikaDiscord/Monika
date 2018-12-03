import discord
from discord.ext import commands
import lavalink
from utilities import checks

global checks
checks = checks.Checks()

class Music:

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    @commands.command()
    @checks.is_dev()
    @checks.command()
    async def play(self, ctx, *, song):
        vc = ctx.message.author.voice.channel
        if not vc:
            return await ctx.send("I'm sorry, but you need to be in a voice channel.")
        self.players[ctx.guild.id] = await lavalink.connect(vc)
        tracks = self.players[ctx.guild.id].search_yt(song)
        if not tracks[0]:
            return await ctx.send("I'm sorry, but I couldn't find anything.")
        self.players[ctx.guild.id].add(tracks[0])
        await self.players[ctx.guild.id].play()

    @commands.command()
    @checks.is_dev()
    @checks.command()
    async def repeat(self, ctx):
        if not self.players[ctx.guild.id].is_playing:
            return await ctx.send("I'm sorry, but you need to play a song for this to work.")
        self.players[ctx.guild.id].repeat = not self.players[ctx.guild.id].repeat
        await ctx.send("Repeat has been toggled.")

    @commands.command()
    @checks.is_dev()
    @checks.command()
    async def disconnect(self, ctx):
        if not self.players[ctx.guild.id]:
            return await ctx.send("I'm sorry, but I don't think I'm in a voice channel.")
        await self.players[ctx.guild.id].disconnect()
        await ctx.send("I have disconnected from the voice channel.")

    @commands.command()
    @checks.is_dev()
    @checks.command()
    async def queue(self, ctx):
        p = self.players[ctx.guild.id]
        listname = []
        if not p:
            return await ctx.send("I'm sorry, but I don't think I'm in a voice channel.")
        q = p.queue
        if not q[0]:
            return await ctx.send("There are no items in my queue.")
        for s in q:
            listname.append(s.title + "\n")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Songs in the queue:", description=listname)
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_dev()
    @checks.command()
    async def skip(self, ctx):
        p = self.players[ctx.guild.id]
        if not p.is_playing:
            await ctx.send("I'm not playing anything.")
        p.skip()
        await ctx.send("I have skipped the song.")

def setup(bot):
    bot.add_cog(Music(bot))
