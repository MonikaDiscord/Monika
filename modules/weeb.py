import discord
from discord.ext import commands
import aiohttp
from utilities import checks
from io import StringIO
import os
from pybooru import Danbooru
import json
import asyncio

global checks
checks = checks.Checks()


class Weeb:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.command()
    async def hug(self, ctx, user: discord.Member):
        """Aww! Hugs the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=hug&nsfw=true',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=hug',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
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
    @checks.command()
    async def kiss(self, ctx, user: discord.Member):
        """Aww! Kisses the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=kiss&nsfw=true',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=kiss',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
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
    @checks.command()
    @checks.is_upvoter()
    async def pat(self, ctx, user: discord.Member):
        """Aww! Pats the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=pat&nsfw=true',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=pat',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
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
    @checks.command()
    @checks.is_upvoter()
    async def tickle(self, ctx, user: discord.Member):
        """Aww! Tickles the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=tickle&nsfw=true',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=tickle',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
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
    @checks.command()
    @checks.is_upvoter()
    async def insult(self, ctx, user: discord.Member):
        """Oh! Insults the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=insult&nsfw=true',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=insult',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
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
    @checks.command()
    @checks.is_patron()
    async def bite(self, ctx, user: discord.Member):
        """Oww! Bites the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=bite&nsfw=true',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=bite',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
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
    @checks.command()
    @checks.is_patron()
    async def slap(self, ctx, user: discord.Member):
        """Oww! Slaps the specified user."""
        if ctx.message.channel.is_nsfw():
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=slap&nsfw=true',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
                url = await url.json()
                url = url.get("url")
        else:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type=slap',
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
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
    @checks.command()
    @checks.is_patron()
    async def waifuinsult(self, ctx, user: discord.Member):
        """Hehe... Insults the specified waifu."""
        async with self.bot.session.post('https://api-v2.weeb.sh/auto-image/waifu-insult', headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'},
                                         data={'avatar': user.avatar_url}) as resp:
            if resp.status == 200:
                with open(f'/var/www/luki/monika/waifuinsult/{user.id}-wi.png', 'wb') as f:
                    f.write(await resp.read())
                    f.close()
            else:
                raise Exception((await resp.json())['message'])
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        url = f"https://luki.monikabot.pw/monika/waifuinsult/{user.id}-wi.png"
        embed = discord.Embed(color=color, title="Hehe...", description="{} insulted the waifu known as {}!".format(ctx.message.author.name, user.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)
        await asyncio.sleep(10)
        os.remove(f.name)

    @commands.command()
    @checks.command()
    @checks.is_upvoter()
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member):
        """Ships the 2 users together."""
        async with self.bot.session.post('https://api-v2.weeb.sh/auto-image/love-ship', headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'},
                                         data={'targetOne': user1.avatar_url, 'targetTwo': user2.avatar_url}) as resp:
            if resp.status == 200:
                with open(f'/var/www/luki/monika/shipping/{user1.id}-{user2.id}-ship.png', 'wb') as f:
                    f.write(await resp.read())
                    f.close()
            else:
                raise Exception((await resp.json())['message'])
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        url = f"https://luki.monikabot.pw/monika/shipping/{user1.id}-{user2.id}-ship.png"
        embed = discord.Embed(color=color, title="I ship it!", description="{} has been shipped with {}!".format(user1.name, user2.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by weeb.sh")
        await ctx.send(embed=embed)
        await asyncio.sleep(10)
        os.remove(f.name)


class Images:
    def __init__(self, bot):
        self.bot = bot

    def fixDanbooruJSON(self, temp):
        temp = temp.replace("{\'", "{\"")
        temp = temp.replace("\': ", "\": ")
        temp = temp.replace("\": \'", "\": \"")
        temp = temp.replace("\', \'", "\", \"")
        temp = temp.replace(", \'", ", \"")
        temp = temp.replace("\'}", "\"}")
        temp = temp.replace("True", "\"True\"")
        temp = temp.replace("False", "\"False\"")
        temp = temp.replace("None", "\"None\"")
        temp = temp.replace("[", "")
        temp = temp.replace("]", "")
        return temp

    @commands.command()
    @checks.command()
    async def danbooru(self, ctx):
        """Posts an image directly from Project Danbooru."""
        client = Danbooru('danbooru', username='Kanielyochanan', api_key=self.bot.config['danboorukey'])
        if ctx.message.channel.is_nsfw():
            temp = str(client.post_list(random=True, limit=1))
            temp = temp.replace("\'", "\"")
            temp = temp.replace("True", "\"True\"")
            temp = temp.replace("False", "\"False\"")
            temp = temp.replace("None", "\"None\"")
            temp = temp.replace("[", "")
            temp = temp.replace("]", "")
            data = json.loads(temp)
            url = data['file_url']
        else:
            await ctx.send("Sorry, but I can't load anything from Project Danbooru unless you're in a NSFW channel.")
            return
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Image from Project Danbooru!", description="Here's your image, {}~".format(ctx.message.author.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by Project Danbooru.")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.command()
    async def safebooru(self, ctx):
        """Same as danbooru, but looks for safe images."""
        client = Danbooru('danbooru', username='Kanielyochanan', api_key=self.bot.config['danboorukey'])
        image_found = False
        while not image_found:
            temp = self.fixDanbooruJSON(str(client.post_list(random=True, limit=1, tags="rating:s -status:deleted")))
            data = json.loads(temp)
            if 'file_url' in data:
                image_found = True
        url = data['file_url']
        if ctx.message.guild is not None:
            color = ctx.message.guild.me.color
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Image from Project Danbooru!", description="Here's your image, {}~".format(ctx.message.author.name))
        embed.set_image(url=url)
        embed.set_footer(text="Powered by Project Danbooru.")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.command()
    async def tag(self, ctx, tag):
        """Posts an image with the specified weeb.sh tag."""
        if "&nsfw=true" in tag:
            await ctx.send("That's really lewd, {}!".format(ctx.message.author.name))
            return
        try:
            if ctx.message.channel.is_nsfw():
                async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type={}&nsfw=true'.format(tag),
                                                headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
                    url = await url.json()
                    url = url.get("url")
            else:
                async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type={}'.format(tag),
                                                headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
                    url = await url.json()
                    url = url.get("url")
        except Exception:
            async with self.bot.session.get('https://api-v2.weeb.sh/images/random?type={}&nsfw=true'.format(tag),
                                            headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as url:
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
    @checks.command()
    async def taglist(self, ctx):
        """Gives you a list with all available weeb.sh tags."""
        async with self.bot.session.get('https://api-v2.weeb.sh/images/types', headers={'Authorization': self.bot.config['weebkey'], 'User-Agent': 'Monika/2.0.0'}) as typelist:
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
