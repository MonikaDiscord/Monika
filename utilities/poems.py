import random
import asyncpg
import asyncio
import aiohttp


async def rpoem(self, bot):

    dbhost = bot.config['dbhost']
    dbname = bot.config['dbname']
    dbpass = bot.config['dbpass']
    dbuser = bot.config['dbuser']
    govinfo = {"user": dbuser, "password": dbpass, "database": dbname, "host": dbhost}

    # Add ability to add poems via the dev.py file (Discord management server)

    self.db = await asyncpg.create_pool(**govinfo)
    sql = "SELECT COUNT(*) FROM poems"
    count = await self.db.fetchval(sql)
    print(count)
    num = random.randint(1, count)
    sql = "SELECT poem FROM poems WHERE id = $1"
    poem = await self.db.fetchval(sql, num)
    return poem