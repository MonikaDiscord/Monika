import discord
from discord.ext import commands
from utilities import checks

global checks
checks = checks.Checks()

class Economy:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.command()
    async def coins(self, ctx):
        """Checks the specified user's coins."""
        try:
            user = ctx.message.mentions[0]
        except Exception:
            user = ctx.message.author
        if user.id == self.bot.user.id:
            await ctx.send("I don't have any money, because I don't need any.")
            return
        sql = "SELECT money FROM users WHERE id = $1"
        m = await self.bot.db.fetchval(sql, user.id)
        money = float(m)
        e = discord.Embed(title="{}'s Money".format(user.name), description="Here is the amount of coins {} has:".format(user.name))
        e.add_field(name="Coins", value=money)
        e.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=e)

    @commands.command()
    @checks.command()
    async def give(self, ctx, user: discord.User, amount: float):
        """Gives the specified user some coins."""
        if user.id == self.bot.user.id:
            await ctx.send("I don't need any more money. You should give your money to someone who needs it.")
            return
        elif user.id == ctx.author.id:
            await ctx.send("What did you expect to happen?")
            return
        sql = "SELECT money FROM users WHERE id = $1"
        thing = await self.bot.db.fetchval(sql, ctx.author.id)
        auamount = float(thing)
        if float(auamount) < float(amount):
            await ctx.send("You don't have enough money!")
            return
        auamount -= int(amount)
        sql = "UPDATE users SET money = $1 WHERE id = $2"
        await self.bot.db.execute(sql, str(auamount), ctx.author.id)
        sql = "SELECT money FROM users WHERE id = $1"
        camount = await self.bot.db.fetchval(sql, ctx.author.id)
        newamount = float(camount) + float(amount)
        sql = "UPDATE users SET money = $1 WHERE id = $2"
        await self.bot.db.execute(sql, str(auamount), user.id)
        await ctx.send("I gave {} coins to {}.".format(amount, user.name))

    @commands.command()
    @checks.command()
    @checks.is_staff()
    async def generate(self, ctx, user: discord.User, amount: float):
        """Generates money for someone."""
        if user.id == self.bot.user.id:
            await ctx.send("I don't need any more money. You should give your money to someone who needs it.")
            return
        sql = "SELECT money FROM users WHERE id = $1"
        camount = await self.bot.db.fetchval(sql, user.id)
        newamount = float(camount) + float(amount)
        sql = "UPDATE users SET money = $1 WHERE id = $2"
        await self.bot.db.execute(sql, str(newamount), user.id)
        await ctx.send("I gave {} coins to {}.".format(amount, user.name))

def setup(bot):
    bot.add_cog(Economy(bot))
