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
        time_delta = round((t_2-t_1)*1000)
        await ctx.send("I'm not that good at playing Pong, {}... ``Time: {}ms``".format(ctx.author.name, time_delta))

    @commands.command(name="help")
    @checks.command()
    async def _help(self, ctx):
        """Tells you Monika's commands."""
        if ctx.message.guild is not None:
            cmdpf = await self.bot.get_prefix(ctx.message)
            embed = discord.Embed(color=color, title="Commands", description="In {}, my prefix is ``{}``.".format(ctx.message.guild.name, cmdpf))
        else:
            embed = discord.Embed(color=color, title="Commands", description="My prefix is ``$!``.")
        for cog in self.bot.cogs:
            cogcmds = self.bot.get_cog_commands(cog)
            list = ""
            for c in cogcmds:
                list += f"``{c}`` "
            embed.add_field(name=cog, value=list)
        embed.set_footer(icon_url=self.bot.user.avatar_url, text="Just Monika.")
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
        embed.add_field(name="Other: ", value = "Website: Currently down\nDiscord: https://discord.gg/heZJZ5M")
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
        embed = discord.Embed(title="Join my server!", description="You can join my server [here](https://discord.gg/heZJZ5M).")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.command()
    async def invite(self, ctx):
        """Gives you an invite for Monika!"""
        embed = discord.Embed(title="Invite me!", description="You can invite me [here](https://discordapp.com/api/oauth2/authorize?client_id=399315651338043392&permissions=8&scope=bot).")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.command()
    async def suggest(self, ctx, *, suggestion: str):
        """Sends a suggestion to the developers of Monika."""
        channel = self.bot.get_channel(518984377674498053)
        color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="New suggestion!", description="I'm so excited to read it!")
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="Suggestion", value="{} sent this suggestion: ``{}``".format(ctx.message.author, suggestion))
        try:
            await channel.send(embed=embed)
        except Exception:
            await ctx.send("There was an error... Don't worry! You can contact my developers in my server. To enter my server, just say ``$!server``!")
            traceback.print_exc()
        await ctx.send("I sent your suggestion, <@{}>~".format(ctx.message.author.id))

    @commands.command()
    @checks.command()
    async def report(self, ctx, *, report: str):
        """Sends a bug report to the developers of Monika."""
        channel = self.bot.get_channel(518984454849691678)
        color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="New report!", description="Hopefully, you guys can fix it..")
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="Report", value="{} sent this report: ``{}``".format(ctx.message.author, report))
        try:
            await channel.send(embed=embed)
            await ctx.send("There was an error... Don't worry! You can contact my developers in my server. To enter my server, just say ``$!server``!")
        except Exception:
            traceback.print_exc()
        await ctx.send("I sent your report, <@{}>~".format(ctx.message.author.id))

def setup(bot):
    bot.add_cog(General(bot))
