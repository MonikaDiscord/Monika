import discord
from discord.ext import commands
import sys
import aiohttp
import json
import platform
from cogs.scripts.settings import settings
import logging
from raven import Client
import asyncio
import psycopg2
from cogs.scripts import checks


def prefixcall(bot, msg):
    prefixes = []
    if msg.guild is None:
        prefixes.append("$!")
        return prefixes
    s = settings()
    db = psycopg2.connect(s.dsn)
    cursor = db.cursor()
    sql = "SELECT * FROM guilds WHERE id = %s"
    cursor.execute(sql, [msg.guild.id])
    server = cursor.fetchall()
    if server == []:
        prefixes.append("$!")
        return prefixes
    else:
        sql = "SELECT prefix FROM guilds WHERE id = %s"
        cursor.execute(sql, [msg.guild.id])
        newprefixes = cursor.fetchall()
        newprefix = newprefixes[0][0]
        prefixes.append(newprefix)
        return prefixes


class Monika(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=prefixcall,
                         description="Hi, I'm Monika! Welcome to the Literature Club! but will you promise to spend the most time with me? Here are my commands:",
                         pm_help=None)

        self.session = aiohttp.ClientSession(loop=self.loop)
        self.settings = settings()
        self.rclient = Client(self.settings.sentry)

        self.remove_command('help')
        self.loop.create_task(self.updatedbl())

        if __name__ == '__main__':
            for cog in self.settings.cogs:
                try:
                    self.load_extension(cog)
                except Exception as e:
                    print(f'Oops! I think I broke {cog}...', file=sys.stderr)
                    self.rclient.captureException()


    async def updatedbl(self):
        while not self.is_closed():
            try:
                await self.dblpost()
            except Exception:
                self.rclient.captureException()
            await asyncio.sleep(600)


    async def dblpost(self):
        payload = json.dumps({
            'shard_id': self.shard_id,
            'shard_count': self.shard_count,
            'server_count': len(self.guilds)
        })
        headers = {
            'Authorization': self.settings.dbltoken,
            'Content-type' : 'application/json'
        }
        url = f'https://discordbots.org/api/bots/{self.user.id}/stats'
        async with self.session.post(url, data=payload, headers=headers) as req:
            if req.status == 200:
                logging.info("Successfully posted server count to DBL. [{} servers | {} shards]".format(len(self.guilds), len(self.shards)))
            else:
                logging.info("Failed posting server count to DBL.")


    async def on_ready(self):
        await self.change_presence(activity=discord.Streaming(name='$!help | https://luki.pw/monika', url='https://www.twitch.tv/dansalvato'))
        print("Monika has logged in.")


    async def on_message(self, message):
        if not message.author.bot:
            if message.content == f"<@{self.user.id}> prefix" or message.content == f"<@!{self.user.id}> prefix":
                await message.channel.send("My prefix for this server is ``{}``.".format(self.prefix(message)))
            db = psycopg2.connect(self.settings.dsn)
            cursor = db.cursor()
            user = message.author
            sql = "SELECT * FROM users WHERE id = %s"
            cursor.execute(sql, [user.id])
            users = cursor.fetchall()
            if users == []:
                sql1 = "INSERT INTO users (id, money, patron, staff, upvoter, name, discrim) VALUES (%s, '0', 0, 0, false, %s, %s)"
                cursor.execute(sql1, [user.id, user.name, user.discriminator])
                db.commit()
            guild = message.guild
            if guild is not None:
                sql = "SELECT * FROM guilds WHERE id = %s"
                cursor.execute(sql, [guild.id])
                guilds = cursor.fetchall()
                if guilds == []:
                    sql1 = "INSERT INTO guilds (id, prefix, name, filteredwords) VALUES (%s, '$!', %s, '{}')"
                    cursor.execute(sql1, [guild.id, guild.name])
                    db.commit()
            sql = "SELECT filteredwords FROM guilds WHERE id = %s"
            cursor.execute(sql, [guild.id])
            fw = cursor.fetchall()[0][0]
            for word in fw:
                prefix = self.prefix(message)
                thingy = f"{prefix}filter remove {word}"
                if word.lower() in message.content.lower() and thingy.lower() != message.content.lower():
                    await message.channel.send(f"<@{message.author.id}>, that word is against this server's filter!")
                    try:
                        return await message.delete()
                    except:
                        pass
            await self.process_commands(message)


    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            pass
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You're missing a required argument.")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            if checks.upvoter_check in ctx.command.checks:
                f = "upvoter"
            elif checks.patron_check in ctx.command.checks:
                f = "patron"
            elif checks.gold_check in ctx.command.checks:
                f = "gold patron"
            elif checks.admin_check in ctx.command.checks:
                f = "admin"
            elif checks.dev_check in ctx.command.checks:
                f = "developer"
            elif checks.mod_check in ctx.commands.checks:
                f = "moderator"
            elif checks.staff_check in ctx.commands.checks:
                f = "staff"
            else:
                await ctx.send("You need to have a server permission to do this.")
                return await ctx.send("Please look at the command page to find the permission.")
            await ctx.send(f"You need to have the ``{f}`` permission to do this.")
        elif isinstance(error, discord.ext.commands.errors.NoPrivateMessage):
            await ctx.send("This command can't be used in DMs.")
        else:
            if ctx:
                e = discord.Embed(title="An exception has occured.", description=f"```{error}```\nThe Monika developer team has been alerted to this issue and will fix it soon.\nIf you know how to fix this, then you can also check out our [GitHub repository](https://github.com/MonikaDiscord/Monika).")
                await ctx.send(embed=e)


    def run(self):
        super().run(self.settings.token, bot=True, reconnect=True)


    def load_cog(self, cname):
        self.load_extension(cname)


    def unload_cog(self, cname):
        self.unload_extension(cname)


    def reload_cog(self, cname):
        self.unload_cog(cname)
        self.load_cog(cname)


    def restart(self):
        sys.exit(1)


    def prefix(self, msg):
        return self.command_prefix(self, msg)[0]


    async def get_coins(self, userid):
        db = psycopg2.connect(self.settings.dsn)
        cursor = db.cursor()
        cursor.execute("SELECT money FROM users WHERE id = ?", [userid])
        return cursor.fetchall()[0][0]


bot = Monika()
bot.run()
