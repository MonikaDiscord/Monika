import discord
from discord.ext import commands
from .scripts import checks
import psycopg2

class Economy:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coins(self, ctx):
        """Checks the specified user's coins."""
        db = psycopg2.connect(self.bot.settings.dsn)
        cursor = db.cursor()
        try:
            user = ctx.message.mentions[0]
        except Exception:
            user = ctx.message.author
        if user.id == 399315651338043392:
            await ctx.send("I don't have any money, because I don't need any.")
            return
        sql = "SELECT money FROM users WHERE id = %s"
        cursor.execute(sql, [user.id])
        m = cursor.fetchall()
        money = float(m[0][0])
        e = discord.Embed(title="{}'s Money".format(user.name), description="Here is the amount of coins {} has:".format(user.name))
        e.add_field(name="Coins", value=money)
        e.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=e)

    @commands.command()
    async def give(self, ctx, user: discord.User, amount: float):
        """Gives the specified user some coins."""
        db = psycopg2.connect(self.bot.settings.dsn)
        cursor = db.cursor()
        if user.id == self.bot.user.id:
            await ctx.send("I don't need any more money. You should give your money to someone who needs it.")
            return
        elif user.id == ctx.author.id:
            await ctx.send("You can't give yourself money!")
            return
        sql = "SELECT money FROM users WHERE id = %s"
        cursor.execute(sql, [ctx.author.id])
        auamount = float(cursor.fetchall()[0][0])
        if float(auamount) < float(amount):
            await ctx.send("You don't have enough money!")
            return
        auamount -= int(amount)
        sql = "UPDATE users SET money = %s WHERE id = %s"
        cursor.execute(sql, [str(auamount), ctx.author.id])
        sql = "SELECT money FROM users WHERE id = %s"
        cursor.execute(sql, [ctx.author.id])
        camount = cursor.fetchall()[0][0]
        newamount = float(camount) + float(amount)
        sql = "UPDATE users SET money = %s WHERE id = %s"
        cursor.execute(sql, [str(auamount), user.id])
        db.commit()
        await ctx.send("I gave {} coins to {}.".format(amount, user.name))

    @commands.command()
    @checks.is_staff()
    async def generate(self, ctx, user: discord.User, amount: float):
        """Generates money for someone."""
        db = psycopg2.connect(self.bot.settings.dsn)
        cursor = db.cursor()
        if user.id == self.bot.user.id:
            await ctx.send("I don't need any more money. You should give your money to someone who needs it.")
            return
        sql = "SELECT money FROM users WHERE id = %s"
        cursor.execute(sql, [user.id])
        camount = cursor.fetchall()[0][0]
        newamount = float(camount) + float(amount)
        sql = "UPDATE users SET money = %s WHERE id = %s"
        cursor.execute(sql, [str(newamount), user.id])
        db.commit()
        await ctx.send("I gave {} coins to {}.".format(amount, user.name))

def setup(bot):
    bot.add_cog(Economy(bot))
