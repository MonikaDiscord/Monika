import discord
from discord.ext import commands
import aiohttp
from utilities import checks
from io import StringIO
import os
from pybooru import Danbooru
import rule34
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
        await ctx.send("Here: ``{}``".format(nekos.textcat()))


def setup(bot):
    bot.add_cog(Nekos(bot))
