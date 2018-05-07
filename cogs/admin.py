import discord
from discord.ext import commands
import psycopg2

class Administration:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix):
        """Sets a new prefix for your server."""
        db = psycopg2.connect(self.bot.settings.dsn)
        cursor = db.cursor()
        sql1 = "UPDATE guilds SET prefix = %s WHERE id = %s"
        cursor.execute(sql1, [prefix, ctx.message.guild.id])
        db.commit()
        await ctx.send("``{}``'s prefix is now ``{}``!".format(ctx.message.guild.name, prefix))

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def resetprefix(self, ctx):
        """Resets your server's prefix."""
        db = psycopg2.connect(self.bot.settings.dsn)
        cursor = db.cursor()
        sql1 = "UPDATE guilds SET prefix = '$!' WHERE id = %s"
        cursor.execute(sql1, [ctx.message.guild.id])
        db.commit()
        await ctx.send("``{}``'s prefix has been reset to ``$!``.".format(ctx.message.guild.name))

    @commands.group(invoke_without_command=True) 
    @commands.has_permissions(manage_messages=True)
    async def filter(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You need to use a subcommand.")
            await ctx.send("Available subcommands for filter: ``filter add``, ``filter remove``.")
            
    @filter.command()
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, word):
        db = psycopg2.connect(self.bot.settings.dsn)
        cursor = db.cursor()
        sql = "UPDATE guilds SET filteredwords = array_append(filteredwords, %s) WHERE id = %s"
        cursor.execute(sql, [word, ctx.guild.id])
        db.commit()
        await ctx.send("That word has been added to the filter!")
        
    @filter.command()
    @commands.has_permissions(manage_messages=True)
    async def remove(self, ctx, word):
        db = psycopg2.connect(self.bot.settings.dsn)
        cursor = db.cursor()
        sql = "UPDATE guilds SET filteredwords = array_remove(filteredwords, %s) WHERE id = %s"
        cursor.execute(sql, [word, ctx.guild.id])
        db.commit()
        await ctx.send("That word has been removed from the filter!")
        
    @filter.command()
    @commands.has_permissions(manage_messages=True)
    async def list(self, ctx):
        db = psycopg2.connect(self.bot.settings.dsn)
        cursor = db.cursor()
        sql = "SELECT filteredwords FROM guilds WHERE id = %s"
        cursor.execute(sql, [ctx.guild.id])
        list = ""
        for word in cursor.fetchall()[0][0]:
            list += (word + "\n")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        e = discord.Embed(color=color, title=f"List of filtered words in {ctx.guild.name}", description=list)
        await ctx.author.send(embed=e)
    
def setup(bot):
    bot.add_cog(Administration(bot))
