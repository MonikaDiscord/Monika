import discord
from discord.ext import commands
import asyncio
import math

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    async def process_deletion(self, messages, channel):
        while messages:
            if len(messages) > 1:
                await channel.delete_messages(messages[:100])
                messages = messages[100:]
            else:
                await messages.delete()
                messages = []
            await asyncio.sleep(1.5)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def prune(self, ctx, number: int):
        """Deletes the specified number of messages."""

        if ctx.invoked_subcommand is None:
            channel = ctx.message.channel
            author = ctx.message.author
            server = author.guild
            has_permissions = channel.permissions_for(server.me).manage_messages

            to_delete = []

            if not has_permissions:
                await ctx.send("I can't delete messages...")
                return

            async for message in channel.history(limit=number+1):
                to_delete.append(message)

            await self.process_deletion(to_delete, ctx.message.channel)
            if number == 1:
                await ctx.send("Yay! I pruned a message~")
                return
            else:
                await ctx.send("Yay! I pruned {} messages~".format(number))

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.User, *, reason=None):
        """Kicks a user."""
        try:
            await ctx.message.guild.kick(user, reason=reason)
        except Exception:
            self.bot.rclient.captureException()
            await ctx.send("I couldn't do that for you... I'm so sorry!")
            return
        await ctx.send("I kicked " + str(user) + " for you, <@{}>~".format(ctx.message.author.id))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason=None):
        """Bans a user."""
        try:
            await ctx.message.guild.ban(user, reason=reason)
        except Exception:
            self.bot.rclient.captureException()
            await ctx.send("I couldn't do that for you... I'm so sorry!")
            return
        await ctx.send("I banned " + str(user) + " for you, <@{}>~".format(ctx.message.author.id))

def setup(bot):
    bot.add_cog(Moderation(bot))
