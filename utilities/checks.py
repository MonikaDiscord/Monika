import asyncpg
from discord.ext import commands
import asyncio
import json

class Checks:

    def __init__(self):
        asyncio.get_event_loop().run_until_complete(self._init_db())

    async def _init_db(self):
        config = json.loads(open('config.json', 'r').read())
        dbpass = config['dbpass']
        dbuser = config['dbuser']
        govinfo = {"user": dbuser, "password": dbpass, "database": "monika", "host": "localhost"}
        self.db = await asyncpg.create_pool(**govinfo)

    async def admin_check(self, ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        return int(status) == 1

    async def dev_check(self, ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        nums = [1, 2]
        return int(status) in nums

    async def mod_check(self, ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        nums = [1, 3]
        return int(status) in nums

    async def staff_check(self, ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        nums = [1, 2, 3]
        return int(status) in nums

    async def upvoter_check(self, ctx):
        sql = "SELECT upvoter FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        return bool(status) == True

    async def premium_check(self, ctx):
        sql = "SELECT patron FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        nums = [1, 2]
        return int(status) in nums

    async def gold_check(self, ctx):
        sql = "SELECT patron FROM users WHERE id = $1"
        status = await self.db.fetchval(sql, ctx.author.id)
        return int(status) == 2

    async def cog_disabler(self, ctx):
        sql = "SELECT disabledcogs FROM guilds WHERE id = $1"
        dcogs = await self.db.fetchval(sql, ctx.guild.id)
        sql = "SELECT disabledcmds FROM guilds WHERE id = $1"
        dcmds = await self.db.fetchval(sql, ctx.guild.id)
        return ctx.command.cog_name not in dcogs or ctx.command.name not in dcmds

    def is_admin(self):
        return commands.check(self.admin_check)

    def is_dev(self):
        return commands.check(self.dev_check)

    def is_mod(self):
        return commands.check(self.mod_check)

    def is_staff(self):
        return commands.check(self.staff_check)

    def is_patron(self):
        return commands.check(self.premium_check)

    def is_gold(self):
        return commands.check(self.gold_check)

    def is_upvoter(self):
        return commands.check(self.upvoter_check)

    def command(self):
        return commands.check(self.cog_disabler)
