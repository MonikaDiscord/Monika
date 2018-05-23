import asyncpg
from discord.ext import commands

class Checks:

    def __init__(self, bot):

        self.bot = bot

        async def _init_db():
            dbpass = self.bot.config['dbpass']
            dbuser = self.bot.config['dbuser']
            govinfo = {"user": dbuser, "password": dbpass, "database": "monika", "host": "localhost"}
            self.db = await asyncpg.create_pool(**govinfo)

        bot.loop.run_until_complete(_init_db())

    async def admin_check(ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        return int(status) == 1

    async def dev_check(ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        nums = [1, 2]
        return int(status) in nums

    async def mod_check(ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        nums = [1, 3]
        return int(status) in nums

    async def staff_check(ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        nums = [1, 2, 3]
        return int(status) in nums

    async def premium_check(ctx):
        sql = "SELECT patron FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        nums = [1, 2]
        return int(status) in nums

    async def gold_check(ctx):
        sql = "SELECT patron FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        return int(status) == 2

    def is_admin():
        return commands.check(admin_check)

    def is_dev():
        return commands.check(dev_check)

    def is_mod():
        return commands.check(mod_check)

    def is_staff():
        return commands.check(staff_check)

    def is_patron():
        return commands.check(premium_check)

    def is_gold():
        return commands.check(gold_check)

    def is_upvoter():
        return commands.check(upvoter_check)
