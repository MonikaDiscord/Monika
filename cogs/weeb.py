import discord
from discord.ext import commands
import aiohttp
from .scripts import checks
from PIL import Image
from io import StringIO
import os

class Weeb:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hug(self, ctx, user: discord.Member):
        """Aww! Hugs the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=hug&nsfw=true', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=hug', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Hug!", description="{} hugged {}... Aww...".format(ctx.message.author.name, user.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx, user: discord.Member):
        """Aww! Kisses the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=kiss&nsfw=true', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=kiss', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Kiss!", description="{} kissed {}... Aww...".format(ctx.message.author.name, user.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_upvoter()
    async def pat(self, ctx, user: discord.Member):
        """Aww! Pats the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=pat&nsfw=true', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=pat', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Pat!", description="{} patted {}... Aww...".format(ctx.message.author.name, user.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_upvoter()
    async def tickle(self, ctx, user: discord.Member):
        """Aww! Tickles the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=tickle&nsfw=true', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=tickle', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Tickle!", description="{} tickled {}... Aww...".format(ctx.message.author.name, user.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_upvoter()
    async def insult(self, ctx, user: discord.Member):
        """Oh! Insults the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=insult&nsfw=true', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=insult', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        if user.id == 319503910895222784:
            await ctx.send("Ahaha, very funny.")
            return
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Insult!", description="Oh! {} insulted {}!".format(ctx.message.author.name, user.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)

    @commands.command()
    async def poke(self, ctx, user: discord.Member):
        """Oh! Pokes the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=poke&nsfw=true', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=poke', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Poke!", description="{} poked {}...".format(ctx.message.author.name, user.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_patron()
    async def bite(self, ctx, user: discord.Member):
        """Oww! Bites the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=bite&nsfw=true', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=bite', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Bite!", description="Oww! {} bit {}...".format(ctx.message.author.name, user.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_patron()
    async def slap(self, ctx, user: discord.Member):
        """Oww! Slaps the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=slap&nsfw=true', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=slap', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Slap!", description="Oww! {} slapped {}...".format(ctx.message.author.name, user.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_patron()
    async def waifuinsult(self, ctx, user: discord.Member):
        """Hehe... Insults the specified waifu."""
        async with self.bot.session.post('https://api-v2.weeb.sh/auto-image/waifu-insult', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}, data={'avatar': user.avatar_url}) as resp:
            if resp.status == 200:
                with open(f'/var/www/luki.pw/monika/waifuinsult/{user.id}-wi.png', 'wb') as f:
                    f.write(await resp.read())
                    f.close()
            else:
                raise Exception((await resp.json())['message'])
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        url = f"https://luki.pw/monika/waifuinsult/{user.id}-wi.png"
        embed = discord.Embed(color=color, title="Hehe...", description="{} insulted the waifu known as {}!".format(ctx.message.author.name, user.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)


    @commands.command()
    @checks.is_upvoter()
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member):
        """Hehe... Insults the specified waifu."""
        async with self.bot.session.post('https://api-v2.weeb.sh/auto-image/love-ship', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}, data={'targetOne': user1.avatar_url, 'targetTwo': user2.avatar_url}) as resp:
            if resp.status == 200:
                with open(f'/var/www/luki.pw/monika/shipping/{user1.id}-{user2.id}-ship.png', 'wb') as f:
                    f.write(await resp.read())
                    f.close()
            else:
                raise Exception((await resp.json())['message'])
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        url = f"https://luki.pw/monika/shipping/{user1.id}-{user2.id}-ship.png"
        embed = discord.Embed(color=color, title="I ship it!", description="{} has been shipped with {}!".format(user1.name, user2.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)

class Images:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tag(self, ctx, tag):
        """Posts an image with the specified weeb.sh tag."""
        if "&nsfw=true" in tag:
            await ctx.send("That's really lewd, {}!".format(ctx.message.author.name))
            return
        try:
            if ctx.message.channel.is_nsfw():
                async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type={}&nsfw=true'.format(tag),
                                       headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                    url = await url.json()
                    url = url.get("url")
            else:
                async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type={}'.format(tag),
                                       headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                    url = await url.json()
                    url = url.get("url")
        except Exception:
            async with session.get('https://api-v2.weeb.sh/images/random?type={}&nsfw=true'.format(tag),
                                   headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Image with the {} tag:".format(tag), description="Here's your image, {}~".format(ctx.message.author.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        try:
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send("The ``{}`` tag doesn't seem to exist...".format(str(tag)))

    @commands.command()
    async def taglist(self, ctx):
        """Gives you a list with all available weeb.sh tags."""
        async with self.bot.session.get('https://api-v2.weeb.sh/images/types', headers={'Authorization': self.bot.settings.weebtoken, 'User-Agent': 'Monika/1.0.0'}) as typelist:
            typelist = await typelist.json()
            typelist = typelist.get("types")
        types = []
        for t in typelist:
            types.append(t)
            embedtypes = "\n".join(types)
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="All Image Tags", description="Here are all of the available tags on weeb.sh:")
        embed.add_field(name="Tags", value=embedtypes, inline=False)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.message.author.send(embed=embed)
        if ctx.message.guild is not None:
            await ctx.send("I sent the full tag list in our DMs, <@{}>~".format(ctx.message.author.id))

def setup(bot):
    bot.add_cog(Weeb(bot))
    bot.add_cog(Images(bot))
