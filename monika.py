import discord
from discord.ext import commands
import asyncpg, aiohttp
import json
from raven import Client
from utilities import checks
import asyncio
import os
from utilities import prefix
import traceback
from datadog import api, statsd, initialize
import lavalink
import sys

global checks
checks = checks.Checks()

class Monika(commands.AutoShardedBot):

    def __init__(self):

        self._prefix = prefix.Prefix()
        super().__init__(command_prefix=self._prefix.prefixcall)

        self.config = json.loads(open('config.json', 'r').read())

        datadogkeys = {
            'api_key': self.config['datadog_api_key'],
            'app_key': self.config['datadog_app_key']
        }

        initialize(**datadogkeys)

        self.session = aiohttp.ClientSession()
        self.dogstatsd = statsd
        self.lavalink = lavalink.Client(bot=self, password=self.config['lavapass'], loop=self.loop, ws_port=1337, shard_count=len(self.shards))
        self.mrepair = False

        dbpass = self.config['dbpass']
        dbuser = self.config['dbuser']
        govinfo = {"user": dbuser, "password": dbpass, "database": "monika", "host": "localhost"}

        async def _init_db():
            self.db = await asyncpg.create_pool(**govinfo)
            await self.db.execute("CREATE TABLE IF NOT EXISTS users (id bigint primary key, name text, discrim varchar (4), money text, patron int, staff int, upvoter boolean);")
            await self.db.execute("CREATE TABLE IF NOT EXISTS guilds (id bigint primary key, name text, prefix text, filteredwords text[], disabledcogs text[], disabledcmds text[]);")

        self.loop.create_task(_init_db())

        self.rclient = Client(self.config.get('sentry_dsn'))

        self.remove_command('help')

        for file in os.listdir("modules"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.load_extension(f"modules.{name}")
                except:
                    print(f"Oops! I broke the {file} module...")
                    traceback.print_exc()


    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(name='$!help | monikabot.pw', type=discord.ActivityType.watching))
        print("Monika has fully logged in.")
        self.dogstatsd.event("Monika has fully logged in.", "All shards are ready!")
        self.dogstatsd.gauge("monika.shards", len(self.shards))
        self.dogstatsd.gauge("monika.guilds", len(self.guilds))
        c = self.get_channel(447553320752513053)
        e = discord.Embed(color=discord.Color.blue(), title="All shards ready!")
        try:
            await c.send(embed=e)
        except:
            pass

    async def on_shard_ready(self, id):
        self.dogstatsd.event(f"Shard {id} is ready!", "nice!")
        c = self.get_channel(447553320752513053)
        e = discord.Embed(color=discord.Color.blue(), title=f"Shard {id} ready!")
        try:
            await c.send(embed=e)
        except:
            pass

    async def on_message(self, msg):
        if not msg.author.bot:
            if msg.content == f"<@{self.user.id}> prefix" or msg.content == f"<@!{self.user.id}> prefix":
                p = await self.get_prefix(msg)
                await msg.channel.send(f"My prefix for this server is ``{p}``.")
            user = msg.author
            sql = "SELECT * FROM users WHERE id = $1"
            u = await self.db.fetchrow(sql, user.id)
            if not u:
                sql1 = "INSERT INTO users (id, money, patron, staff, upvoter, name, discrim) VALUES ($1, '0', 0, 0, false, $2, $3)"
                await self.db.execute(sql1, user.id, user.name, user.discriminator)
            else:
                sql1 = "UPDATE users SET name = $1, discrim = $2 WHERE id = $3"
                await self.db.execute(sql1, user.name, user.discriminator, user.id)
            if msg.guild:
                guild = msg.guild
                sql = "SELECT * FROM guilds WHERE id = $1"
                guilds = await self.db.fetchrow(sql, guild.id)
                if not guilds:
                    sql1 = "INSERT INTO guilds (id, prefix, name, filteredwords, disabledcogs, disabledcmds) VALUES ($1, '$!', $2, '{}', '{}', '{}')"
                    await self.db.execute(sql1, guild.id, guild.name)
                else:
                    sql1 = "UPDATE guilds SET name = $1 WHERE id = $2"
                    await self.db.execute(sql1, guild.name, guild.id)
                r = discord.utils.get(msg.author.roles, name="Muted")
                if r:
                    return await msg.delete()
                sql = "SELECT filteredwords FROM guilds WHERE id = $1"
                fw = await self.db.fetchval(sql, guild.id)
                if fw:
                    for word in fw:
                        prefix = await self.get_prefix(msg)
                        thingy = f"{prefix}filter remove {word}"
                        if word.lower() in msg.content.lower() and thingy.lower() != msg.content.lower():
                            await msg.channel.send(f"<@{msg.author.id}>, that word is against this server's filter!")
                            try:
                                return await msg.delete()
                            except:
                                pass
            await self.process_commands(msg)

    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            pass
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You're missing a required argument.")
        elif isinstance(error, discord.ext.commands.MissingPermissions):
            await ctx.send("You don't have the required server permissions to use this command.")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.send("Either you don't have permissions to do this or this command is disabled.")
        else:
            if ctx:
                e = discord.Embed(title="An exception has occured.", description=f"```{error}```\nIf you know how to fix this, then you can check out our [GitHub repository](https://github.com/MonikaDiscord/Monika).\nOtherwise, please report it at the [Monika Discord server](https://discord.gg/DspkaRD).")
                await ctx.send(embed=e)

    async def on_guild_join(self, guild):
        sql = "INSERT INTO guilds (id, prefix, name, filteredwords, disabledcogs, disabledcmds) VALUES ($1, '$!', $2, '{}', '{}', '{}')"
        await self.db.execute(sql, guild.id, guild.name)
        self.dogstatsd.gauge("monika.guilds", len(self.guilds))
        c = self.get_channel(447553435999666196)
        e = discord.Embed(color=discord.Color.blue(), title="New guild!", description=f"We're now in {len(self.guilds)} guilds!")
        e.set_thumbnail(url=guild.icon_url)
        e.add_field(name="Name", value=guild.name)
        e.add_field(name="Owner", value=guild.owner)
        e.add_field(name="Members", value=guild.member_count)
        try:
            await c.send(embed=e)
        except:
            pass

    async def on_guild_remove(self, guild):
        sql = "DELETE FROM guilds WHERE id = $1"
        await self.db.execute(sql, guild.id)
        self.dogstatsd.gauge("monika.guilds", len(self.guilds))
        c = self.get_channel(447553435999666196)
        e = discord.Embed(color=discord.Color.red(), title="We lost a guild...", description=f"But it's okay, we're still in {len(self.guilds)} other guilds!")
        e.set_thumbnail(url=guild.icon_url)
        e.add_field(name="Name", value=guild.name)
        e.add_field(name="Owner", value=guild.owner)
        e.add_field(name="Members", value=guild.member_count)
        try:
            await c.send(embed=e)
        except:
            pass

    async def get_prefix(self, msg):
        return await self._prefix.prefixcall(self, msg)

    async def get_coins(self, id):
        sql = "SELECT coins FROM users WHERE id = $1"
        return await self.db.fetchval(sql, id)
    
    async def reload_music(self):
        del self.lavalink
        self.lavalink = lavalink.Client(bot=self, password=self.config['lavapass'], loop=self.loop, ws_port=1337, shard_count=len(self.shards))
        
    async def restart(self):
        sys.exit(1)

bot = Monika()
config = json.loads(open('config.json', 'r').read())
try:
    bot.run(config.get('token'))
except KeyboardInterrupt:
    bot.dogstatsd.event("Monika is shutting down...", "Goodbye!")
