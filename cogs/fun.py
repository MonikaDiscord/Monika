import discord
from discord.ext import commands
import random
import urllib
import urllib.request
from cogs.scripts import checks
import asyncio
import requests
import aiohttp
from cogs.scripts import poems

class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dog(self, ctx):
        """Provides a random dog."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=animal_dog&nsfw=true', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=animal_dog', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Here's your requested dog, {}~".format(ctx.message.author.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        """Provides a random cat."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=animal_cat&nsfw=true', headers={'Authorization': self.bot.settings.weebtoken}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=animal_cat', headers={'Authorization': self.bot.settings.weebtoken}) as url:
                url = await url.json()
                url = url.get("url")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Here's your requested cat, {}~".format(ctx.message.author.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)

    @commands.command()
    async def duck(self, ctx):
        """Provides a random duck."""
        async with self.bot.session.get('https://api.random-d.uk/random') as r:
            r = await r.json()
            url = r.get("url")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Here's your requested duck, {}~".format(ctx.message.author.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by random-d.uk")
        await ctx.send(embed=embed)

    @commands.command()
    async def delete(self, ctx, *, username):
        """Deletes the specified user."""
        try:
            username: discord.Member
            if username.id == 319503910895222784:
                await ctx.send("You will not touch my boyfriend!")
                return
            elif username.id == 201745963394531328 or username.id == 206197394667208704:
                await ctx.send("That's a funny joke, {}.".format(ctx.message.author.name))
                return
            elif username.id == 399315651338043392:
                await ctx.send("You're so funny, {}.".format(ctx.message.author.name))
                return
            await ctx.send("``characters/{}.chr`` deleted successfully.".format(username.name.lower()))
        except Exception:
            await ctx.send("``characters/{}.chr`` not found.".format(username))

    @commands.command()
    async def message(self, ctx, username: discord.User, *, message):
        """Messages the specified user."""
        try:
            await username.send("{} has sent you this message: ``{}``".format(ctx.message.author.name, message))
        except Exception:
            self.bot.rclient.captureException()
            await ctx.send("I couldn't do that for you... I'm so sorry!")
            return
        await ctx.send("<@{}>, I sent {} this message: ``{}``".format(ctx.message.author.id, username.name, message))

    @commands.command(name="8ball")
    @checks.is_patron()
    async def _8ball(self, ctx, *, question):
        responses = [["Signs point to yes.", "Yes.", "Without a doubt.", "As I see it, yes.", "You may rely on it.", "It is decidedly so.", "Yes - definitely.", "It is certain.", "Most likely.", "Outlook good."],
        ["Reply hazy, try again.", "Concentrate and ask again.", "Better not tell you now.", "Cannot predict now.", "Ask again later."],
        ["My sources say no.", "Outlook not so good.", "Very doubtful.", "My reply is no.", "Don't count on it."]]
        await ctx.send("My magic eight ball said... ``{}``".format(random.choice(random.choice(responses))))

    @commands.command(name="monify", hidden=True)
    @checks.is_dev()
    async def monify(self,ctx,user: discord.Member, time):
        try:
            me = ctx.me
            perms = me.permissions_in(ctx.channel)
            if not perms.manage_messages or not perms.manage_nicknames:
                raise discord.Forbidden(None,"nope")
            reasone = "{} told me to".format(ctx.message.author.name)
            author = ctx.message.author
            nc = user.nick
            ctx.message.delete()
            await user.edit(nick="Monika", reason = reasone)
            author.send("I've monified {}, I hope you know what you're doing.".format(user.name))
            await asyncio.sleep(int(time))
            await user.edit(nick=nc, reason=reasone)
            author.send("{} has been de-monified.".format(user.name))
        except discord.Forbidden as f:
            await ctx.send("I wasn't allowed to do that, sorry!")
        except Exception as e:
            sa = "```"+e+"```"
            await ctx.message.author.send(sa)
            await ctx.message.author.send("I guess it didn't work, sorry <@{}>".format(ctx.message.author.id))

    @commands.command()
    async def urban(self, ctx, *, term):
        """Searches for a term on Urban Dictionary."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://api.urbandictionary.com/v0/define?term={}'.format(term)) as apientry:
                    apientry = await apientry.json()
                    apientry = apientry.get("list")[0]
        except Exception:
            await ctx.send("I'm sorry, but that term isn't on Urban Dictionary...")
            return
        apiword = str(apientry.get("word"))
        apidef = str(apientry.get("definition"))
        apiexample = str(apientry.get("example"))
        apilink = str(apientry.get("permalink"))
        apiauthor = str(apientry.get("author"))
        thumbsup = str(apientry.get("thumbs_up"))
        thumbsdown = str(apientry.get("thumbs_down"))
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        e = discord.Embed(color=color, title="{}".format(apiword), url=apilink, description=apidef)
        e.add_field(name="Example", value=apiexample, inline=False)
        e.add_field(name=":thumbsup:", value=thumbsup)
        e.add_field(name=":thumbsdown:", value=thumbsdown)
        e.set_footer(text="Definiton by {} | Powered by Urban Dictionary".format(apiauthor))
        try:
            await ctx.send(embed=e)
        except HTTPException:
            await ctx.send(embed=discord.Embed(color=color, title="The definition is too long!", description=f"If you still want to see the definition, look at the page [here]({apilink})."))

    @commands.command()
    @checks.is_patron()
    async def poem(self, ctx):
        """Gives you a random poem."""
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        e = discord.Embed(color=color, title="Here's your poem!", description=poems.rpoem())
        await ctx.send(embed=e)

    #@commands.command()
    #@checks.is_admin()
    #async def analyze(self, ctx, *, message):
        #"""Analyzes the specified statement."""
        #async with self.bot.session.post(f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={self.bot.settings.perspectivekey}', data={'comment':{'text':message}}, languages: ["en"], requestedAttributes: {TOXICITY:{}} }) as adata:
            #await ctx.send(adata.status)

def setup(bot):
    bot.add_cog(Fun(bot))
