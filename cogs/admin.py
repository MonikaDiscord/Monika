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

def setup(bot):
    bot.add_cog(Administration(bot))
