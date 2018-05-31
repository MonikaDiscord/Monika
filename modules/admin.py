import discord
from discord.ext import commands
from utilities import checks

global checks
checks = checks.Checks()

class Administration:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix):
        """Sets a new prefix for your server."""
        sql = "UPDATE guilds SET prefix = $1 WHERE id = $2"
        await self.bot.db.execute(sql, prefix, ctx.message.guild.id)
        await ctx.send("``{}``'s prefix is now ``{}``!".format(ctx.message.guild.name, prefix))

    @commands.command()
    @checks.command()
    @commands.has_permissions(manage_guild=True)
    async def resetprefix(self, ctx):
        """Resets your server's prefix."""
        sql = "UPDATE guilds SET prefix = '$!' WHERE id = $1"
        await self.bot.db.execute(sql, ctx.message.guild.id)
        await ctx.send("``{}``'s prefix has been reset to ``$!``.".format(ctx.message.guild.name))

    @commands.group(invoke_without_command=True)
    @checks.command()
    @commands.has_permissions(manage_messages=True)
    async def filter(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You need to use a subcommand.")
            await ctx.send("Available subcommands for filter: ``filter add``, ``filter remove``, ``filter list``.")

    @filter.command()
    @checks.command()
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, word):
        sql = "UPDATE guilds SET filteredwords = array_append(filteredwords, $1) WHERE id = $2"
        await self.bot.db.execute(sql, word, ctx.guild.id)
        await ctx.send("That word has been added to the filter!")

    @filter.command()
    @checks.command()
    @commands.has_permissions(manage_messages=True)
    async def remove(self, ctx, word):
        sql = "UPDATE guilds SET filteredwords = array_remove(filteredwords, $1) WHERE id = $1"
        await self.bot.db.execute(sql, word, ctx.guild.id)
        await ctx.send("That word has been removed from the filter!")

    @filter.command()
    @checks.command()
    @commands.has_permissions(manage_messages=True)
    async def list(self, ctx):
        sql = "SELECT filteredwords FROM guilds WHERE id = $1"
        words = await self.bot.db.fetchval(sql, [ctx.guild.id])
        list = ""
        for word in words:
            list += (word + "\n")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        e = discord.Embed(color=color, title=f"List of filtered words in {ctx.guild.name}", description=list)
        await ctx.author.send(embed=e)

def setup(bot):
    bot.add_cog(Administration(bot))
