import discord
from discord.ext import commands
import platform
from utilities import checks
import traceback
import time

global checks
checks = checks.Checks()


class General:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.command()
    async def ping(self, ctx):
        """Calculates the ping time."""
        t_1 = time.perf_counter()
        await ctx.trigger_typing()
        t_2 = time.perf_counter()
        time_delta = round((t_2 - t_1) * 1000)
        await ctx.send("I'm not that good at playing Pong, {}... ``Time: {}ms``".format(ctx.author.name, time_delta))

    @commands.command(name="help")
    @checks.command()
    async def _help(self, ctx):
        """Tells you Monika's commands."""
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        if ctx.message.guild is not None:
            cmdpf = await self.bot.get_prefix(ctx.message)
            embed = discord.Embed(color=color, title="Hi! I'm Monika!", description="In {}, my prefix is ``{}``.".format(ctx.message.guild.name, cmdpf))
        else:
            embed = discord.Embed(color=color, title="Hi! I'm Monika!", description="My prefix is ``$!``.")
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="https://monikabot.pw")
        embed.add_field(name="Commands", value="Want to see my commands? Check out my command list [here](https://monikabot.pw/commands)!", inline=False)
        embed.add_field(name="Invite", value="Want to invite me to your server? Just click [here](https://discordapp.com/oauth2/authorize?client_id=502528950946496512&permissions=8&scope=bot) and click Authorize.", inline=False)
        embed.add_field(name="Server", value="Want to join my server? Just click [here](https://discordapp.com/invite/DspkaRD).", inline=False)
        embed.add_field(name="Donate", value="Want to become a Patron? You can become one by donating [here](https://patreon.com/gpago).", inline=False)
        embed.add_field(name="Upvote", value="Want to become an upvoter? You can become one by voting [here](https://discordbots.org/bot/monika/vote).")
        embed.add_field(name="More Information", value="Want to see more information? Just use the ``info`` command!", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @checks.command()
    async def info(self, ctx):
        '''Gives you information about Monika.'''
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        users = sum(1 for _ in self.bot.get_all_members())
        embed = discord.Embed(color=color, title="Monika Information", description="Hi! I'm Monika. Welcome to the Literature Club!")
        embed.set_footer(text="I love you, {}.".format(ctx.message.author.name))
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Stats: ", value="Servers: **{}**\nShards: **{}**\nUsers: **{}**".format(len(self.bot.guilds), len(self.bot.shards), users))
        try:
            embed.add_field(name="Version: ", value="Monika: **1.0.0**\ndiscord.py: **{}**\nPython: **{}**\nShard ID: **{}**".format(discord.__version__, platform.python_version(), str(ctx.message.guild.shard_id)))
        except Exception:
            embed.add_field(name="Version: ", value="Monika: **1.0.0**\ndiscord.py: **{}**\nPython: **{}**".format(discord.__version__, platform.python_version()))
        embed.add_field(name="Other: ", value="Website: https://monikabot.pw\nDiscord: https://discord.gg/DspkaRD\nPatreon: https://www.patreon.com/monikabot")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.command()
    async def user(self, ctx):
        """Shows info on the specified user."""
        try:
            user = ctx.message.mentions[0]
        except Exception:
            user = ctx.message.author
        roles = []
        for r in user.roles:
            roles.append(r.name)
            usr_roles = "\n".join(roles)
        embed = discord.Embed(color=user.color, description="Here's some information about {}!".format(user.name))
        if checks.staff_check(ctx):
            embed.title = "{} <:staff:314068430787706880>".format(user)
        elif checks.gold_check(ctx):
            embed.title = "{} <:gold:423521455246934027>".format(user)
        elif checks.premium_check(ctx):
            embed.title = "{} <:premium:423521432547622926>".format(user)
        else:
            embed.title = "{}".format(user)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Username", value=user.name, inline=False)
        embed.add_field(name="Discriminator", value=user.discriminator, inline=False)
        embed.add_field(name="ID", value=str(user.id), inline=False)
        embed.add_field(name="Roles", value=usr_roles, inline=False)
        try:
            embed.add_field(name="Playing", value=user.game.name, inline=False)
        except:
            pass
        embed.add_field(name="Date of Account Creation", value=user.created_at, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @checks.command()
    async def server(self, ctx):
        """Gives an invite to Monika's server!"""
        embed = discord.Embed(title="Join my server!", description="You can join ~~the literature club~~ my server [here](https://discord.gg/DspkaRD).")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.command()
    async def invite(self, ctx):
        """Gives you an invite for Monika!"""
        embed = discord.Embed(title="Invite me!", description="You can invite me [here](https://discordapp.com/api/oauth2/authorize?client_id=399315651338043392&permissions=8&scope=bot).")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.command()
    async def upvote(self, ctx):
        """Gives you the link to upvote Monika."""
        embed = discord.Embed(title="Upvote me!", description="You can upvote me [here](https://discordbots.org/bot/monika/vote).")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.command()
    async def suggest(self, ctx, *, suggestion: str):
        """Sends a suggestion to the developers of Monika."""
        channel = self.bot.get_channel(506793254201851906)
        color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="New suggestion!", description="I'm so excited to read it!")
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="Suggestion", value="{} sent this suggestion: ``{}``".format(ctx.message.author, suggestion))
        try:
            await channel.send(embed=embed)
        except Exception:
            self.bot.rclient.captureException()
            await ctx.send("There was an error... Don't worry! You can contact my developers in my server. To enter my server, just say ``$!server``!")
            traceback.print_exc()
        await ctx.send("I sent your suggestion, <@{}>~".format(ctx.message.author.id))

    @commands.command()
    @checks.command()
    async def report(self, ctx, *, report: str):
        """Sends a bug report to the developers of Monika."""
        channel = self.bot.get_channel(506793254201851906)
        color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="New report!", description="Hopefully, you guys can fix it..")
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="Report", value="{} sent this report: ``{}``".format(ctx.message.author, report))
        try:
            await channel.send(embed=embed)
        except Exception:
            self.bot.rclient.captureException()
            await ctx.send("There was an error... Don't worry! You can contact my developers in my server. To enter my server, just say ``$!server``!")
            traceback.print_exc()
        await ctx.send("I sent your report, <@{}>~".format(ctx.message.author.id))

    @commands.command(aliases=["patreon", "patron", "support"])
    @checks.command()
    async def donate(self, ctx):
        embed = discord.Embed(title="Donate to me!", description="You can support development [here](https://www.patreon.com/gpago).")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
