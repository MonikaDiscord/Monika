import asyncpg
from discord.ext import commands
import asyncio
import json

class Checks:

    async def admin_check(self, ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await ctx.bot.db.fetchval(sql, ctx.author.id)
        return int(status) == 1

    async def dev_check(self, ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await ctx.bot.db.fetchval(sql, ctx.author.id)
        nums = [1, 2]
        return int(status) in nums

    async def mod_check(self, ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await ctx.bot.db.fetchval(sql, ctx.author.id)
        nums = [1, 3]
        return int(status) in nums
    
    async def ss_check(self, ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await ctx.bot.db.fetchval(sql, ctx.author.id)
        nums = [1, 4]
        return int(status) in nums

    async def staff_check(self, ctx):
        sql = "SELECT staff FROM users WHERE id = $1"
        status = await ctx.bot.db.fetchval(sql, ctx.author.id)
        nums = [1, 2, 3]
        return int(status) in nums

    async def upvoter_check(self, ctx):
        sql = "SELECT upvoter FROM users WHERE id = $1"
        status = await ctx.bot.db.fetchval(sql, ctx.author.id)
        return bool(status) == True

    async def premium_check(self, ctx):
        #sql = "SELECT patron FROM users WHERE id = $1"
        #status = await ctx.bot.db.fetchval(sql, ctx.author.id)
        #nums = [1, 2]
        #return int(status) in nums
        return True

    async def gold_check(self, ctx):
        sql = "SELECT patron FROM users WHERE id = $1"
        status = await ctx.bot.db.fetchval(sql, ctx.author.id)
        return int(status) == 2

    async def cog_disabler(self, ctx):
        sql = "SELECT disabledcogs FROM guilds WHERE id = $1"
        dcogs = await ctx.bot.db.fetchval(sql, ctx.guild.id)
        sql = "SELECT disabledcmds FROM guilds WHERE id = $1"
        dcmds = await ctx.bot.db.fetchval(sql, ctx.guild.id)
        return ctx.command.cog_name not in dcogs or ctx.command.name not in dcmds

    def is_admin(self):
        return commands.check(self.admin_check)

    def is_dev(self):
        return commands.check(self.dev_check)

    def is_mod(self):
        return commands.check(self.mod_check)
    
    def is_ss(self):
        return commands.check(self.ss_check)

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
