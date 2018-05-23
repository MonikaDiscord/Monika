import discord
from discord.ext import commands
import asyncpg, aiohttp
import json
from raven import Client
from .utilities import checks
import asyncio

class Monika(commands.AutoShardedBot):

    def __init__(self):

        self.config = json.loads(open('config.json', 'r').read())

        dbpass = self.config['dbpass']
        dbuser = self.config['dbuser']
        govinfo = {"user": dbuser, "password": dbpass, "database": "monika", "host": "localhost"}

        async def _init_db():
            self.db = await asyncpg.create_pool(**govinfo)
            await self.db.execute("CREATE TABLE IF NOT EXISTS users (id bigint primary key, name text, discrim varchar (4), money text, patron int, staff int, upvoter boolean);")
            await self.db.execute("CREATE TABLE IF NOT EXISTS guilds (id bigint primary key, name text, prefix text, filteredwords text[], disabledcogs text[]);")

        self.loop.create_task(_init_db())

        self.rclient = Client(self.config['sentry_dsn'])

        async def _prefixcall(bot, msg):
            if msg.guild is None: return commands.when_mentioned_or('$!')
            sql = "SELECT prefix FROM guilds WHERE id = $1"
            return await self.db.fetchval(sql, msg.guild.id)

        def _runprefixcall(bot, msg):
            self.loop.run_until_complete(_prefixcall(bot, msg))

        super().__init__(command_prefix=_runprefixcall,
                         description="Hi, I'm Monika! Welcome to the Literature Club! Here are my commands:",
                         pm_help=None)

        for file in os.listdir("modules"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.load_extension(f"modules.{name}")
                except:
                    print(f"Oops! I broke the {file} module...")
                    self.rclient.captureException()

    def get_prefix(msg):
        return _runprefixcall(self, msg)

    async def get_coins(id):
        sql = "SELECT coins FROM users WHERE id = $1"
        return await self.db.fetchval(sql, id)
