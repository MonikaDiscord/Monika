import discord
from discord.ext import commands
import aiohttp
from utilities import checks
from io import StringIO
import json
import asyncio
import nekos

global checks
checks = checks.Checks()


class Nekos:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.command()
    async def textcat(self, ctx):
        await ctx.send("Here's an ASCII cat: ``{}``".format(nekos.textcat()))

    @commands.command()
    @checks.command()
    async def why(self, ctx):
        await ctx.send(nekos.why())

    @commands.command()
    @checks.command()
    async def fact(self, ctx):
        await ctx.send(nekos.fact())

    @commands.command()
    @checks.command()
    async def cat(self, ctx):
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        url = nekos.cat()
        embed = discord.Embed(color=color, title="Here's your requested cat, {}~".format(ctx.message.author.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by Nekos.life")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.command()
    async def owoify(self, ctx, text: str):
        await ctx.send(nekos.owoify(text))

    @commands.command()
    @checks.command()
    async def eightball(self, ctx):
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        ball = nekos.eightball()
        embed = discord.Embed(color=color, title="{}, {}~".format(ball.__getattr__("text"), ctx.message.author.name))
        embed.set_image(url=ball.__getattr__("image"))
        embed.set_footer(text="Powered by Nekos.life")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Nekos(bot))
