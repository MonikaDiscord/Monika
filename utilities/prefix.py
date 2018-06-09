import asyncpg
import asyncio
import json

class Prefix:

    def __init__(self):
        asyncio.get_event_loop().run_until_complete(self._init_db())

    async def _init_db(self):
        config = json.loads(open('config.json', 'r').read())
        dbpass = config['dbpass']
        dbuser = config['dbuser']
        govinfo = {"user": dbuser, "password": dbpass, "database": "monika", "host": "localhost"}
        self.db = await asyncpg.create_pool(**govinfo)
        await self.db.execute("CREATE TABLE IF NOT EXISTS users (id bigint primary key, name text, discrim varchar (4), money text, patron int, staff int, upvoter boolean);")
        await self.db.execute("CREATE TABLE IF NOT EXISTS guilds (id bigint primary key, name text, prefix text, filteredwords text[], disabledcogs text[], disabledcmds text[]);")

    async def prefixcall(self, bot, msg):
        if msg.guild is None: return "$!"
        sql = "SELECT prefix FROM guilds WHERE id = $1"
        r = await self.db.fetchval(sql, msg.guild.id)
        if r:
            return r
        else:
            return '$!'
