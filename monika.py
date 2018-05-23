import discord
from discord.ext import commands
import asyncpg, aiohttp
import json
from raven import Client
from utilities import checks
import asyncio
import os
import psycopg2

def _prefixcall(bot, msg):
    config = json.loads(open('config.json', 'r').read())
    if msg.guild is None: return "$!"
    dsn = f"dbname='monika' user='{config.get('dbuser')}' host='localhost' password='{config.get('dbpass')}'"
    db = psycopg2.connect(dsn)
    cursor = db.cursor()
    sql = "SELECT prefix FROM guilds WHERE id = %s"
    cursor.execute(sql, [msg.guild.id])
    r = cursor.fetchone()
    if r:
        return r[0]
    else:
        return '$!'

class Monika(commands.AutoShardedBot):

    def __init__(self):

        super().__init__(command_prefix=_prefixcall)

        self.config = json.loads(open('config.json', 'r').read())
        self.checks = checks

        dbpass = self.config['dbpass']
        dbuser = self.config['dbuser']
        govinfo = {"user": dbuser, "password": dbpass, "database": "monika", "host": "localhost"}

        async def _init_db():
            self.db = await asyncpg.create_pool(**govinfo)
            await self.db.execute("CREATE TABLE IF NOT EXISTS users (id bigint primary key, name text, discrim varchar (4), money text, patron int, staff int, upvoter boolean);")
            await self.db.execute("CREATE TABLE IF NOT EXISTS guilds (id bigint primary key, name text, prefix text, filteredwords text[], disabledcogs text[]);")

        self.loop.create_task(_init_db())



        self.rclient = Client(self.config.get('sentry_dsn'))

        for file in os.listdir("modules"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.load_extension(f"modules.{name}")
                except:
                    print(f"Oops! I broke the {file} module...")
                    self.rclient.captureException()

    def run(self):
        super().run(self.config.get('token'))

    def prefix(self, msg):
        return _prefixcall(self, msg)

    async def get_coins(id):
        sql = "SELECT coins FROM users WHERE id = $1"
        return await self.db.fetchval(sql, id)

bot = Monika()

bot.run()
