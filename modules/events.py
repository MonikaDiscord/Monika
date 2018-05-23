import discord
from discord.ext import commands

class Events:

    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(name='$!help | monikabot.pw', type=discord.ActivityType.watching))
        print("Monika has fully logged in.")
        c = self.bot.get_channel(447553320752513053)
        e = discord.Embed(color=discord.Color.blue(), title="All shards ready!")
        try:
            await c.send(embed=e)
        except:
            pass

    async def on_shard_ready(self, id):
        c = self.bot.get_channel(447553320752513053)
        e = discord.Embed(color=discord.Color.blue(), title=f"Shard {id} ready!")
        try:
            await c.send(embed=e)
        except:
            pass

    async def on_message(self, msg):
        if not msg.author.bot:
            if msg.content == f"<@{self.bot.user.id}> prefix" or msg.content == f"<@!{self.bot.user.id}> prefix":
                p = self.bot.prefix(msg)
                await msg.channel.send(f"My prefix for this server is ``{p}``.")
            user = msg.author
            sql = "SELECT * FROM users WHERE id = $1"
            u = await self.bot.db.fetchrow(sql, user.id)
            if not u:
                sql1 = "INSERT INTO users (id, money, patron, staff, upvoter, name, discrim) VALUES ($1, '0', 0, 0, false, $2, $3)"
                await self.bot.db.execute(sql1, user.id, user.name, user.discriminator)
            if msg.guild:
                guild = msg.guild
                sql = "SELECT * FROM guilds WHERE id = $1"
                guilds = await self.bot.db.fetchrow(sql, guild.id)
                if not guild:
                    sql1 = "INSERT INTO guilds (id, prefix, name, filteredwords, disabledcogs) VALUES ($1, '$!', $2, '{}', '{}')"
                    await self.bot.db.execute(sql1, guild.id, guild.name)
                sql = "SELECT filteredwords FROM guilds WHERE id = $1"
                fw = await self.bot.db.fetchval(sql, guild.id)
                if fw:
                    for word in fw:
                        prefix = self.bot.prefix(msg)
                        thingy = f"{prefix}filter remove {word}"
                        if word.lower() in msg.content.lower() and thingy.lower() != msg.content.lower():
                            await msg.channel.send(f"<@{msg.author.id}>, that word is against this server's filter!")
                            try:
                                return await msg.delete()
                            except:
                                pass
            await self.bot.process_commands(msg)
            if msg.author.id == 319503910895222784:
                await ctx.send(self.bot.prefix(msg))

    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            pass
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You're missing a required argument.")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            if self.bot.checks.upvoter_check in ctx.command.checks:
                f = "upvoter"
            elif self.bot.checks.premium_check in ctx.command.checks:
                f = "patron"
            elif self.bot.checks.gold_check in ctx.command.checks:
                f = "gold patron"
            elif self.bot.checks.admin_check in ctx.command.checks:
                f = "admin"
            elif self.bot.checks.dev_check in ctx.command.checks:
                f = "developer"
            elif self.bot.checks.mod_check in ctx.command.checks:
                f = "moderator"
            elif self.bot.checks.staff_check in ctx.command.checks:
                f = "staff"
            else:
                await ctx.send("You need to have a server permission to do this.")
                return await ctx.send("Please look at the command page to find the permission.")
            await ctx.send(f"You need to have the ``{f}`` permission to do this.")
        else:
            if ctx:
                e = discord.Embed(title="An exception has occured.", description=f"```{error}```\nIf you know how to fix this, then you can check out our [GitHub repository](https://github.com/MonikaDiscord/Monika).\nOtherwise, please report it at the [Monika Discord server](https://discord.gg/DspkaRD).")
                await ctx.send(embed=e)

    async def on_guild_join(self, guild):
        c = self.bot.get_channel(447553435999666196)
        e = discord.Embed(color=discord.Color.blue(), title="New guild!", description=f"We're now in {len(self.bot.guilds)} guilds!")
        e.set_thumbnail(url=guild.icon_url)
        e.add_field(name="Name", value=guild.name)
        e.add_field(name="Owner", value=guild.owner)
        e.add_field(name="Members", value=guild.member_count)
        try:
            await c.send(embed=e)
        except:
            pass

    async def on_guild_remove(self, guild):
        c = self.bot.get_channel(447553435999666196)
        e = discord.Embed(color=discord.Color.red(), title="We lost a guild...", description=f"But it's okay, we're still in {len(self.bot.guilds)} other guilds!")
        e.set_thumbnail(url=guild.icon_url)
        e.add_field(name="Name", value=guild.name)
        e.add_field(name="Owner", value=guild.owner)
        e.add_field(name="Members", value=guild.member_count)
        try:
            await c.send(embed=e)
        except:
            pass

def setup(bot):
    bot.add_cog(Events(bot))
