import discord
from discord.ext import commands
import traceback
from .scripts import checks
import textwrap
from contextlib import redirect_stdout
import io
import psycopg2

class Staff:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    @commands.command(pass_context=True, hidden=True, name='eval')
    @checks.is_dev()
    async def _eval(self, ctx, *, body: str):
        """Evaluates code."""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }
        env.update(globals())
        body = self.cleanup_code(body)
        stdout = io.StringIO()
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            self.bot.rclient.captureException()
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(hidden=True)
    @checks.is_dev()
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_cog(module)
        except Exception as e:
            self.bot.rclient.captureException()
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('Done!')

    @commands.command(hidden=True)
    @checks.is_dev()
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_cog(module)
        except Exception as e:
            self.bot.rclient.captureException()
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('Done!')

    @commands.command(name='reload', hidden=True)
    @checks.is_dev()
    async def _reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.reload_cog(module)
        except Exception as e:
            self.bot.rclient.captureException()
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('Done!')

    @commands.command(hidden=True)
    @checks.is_dev()
    async def poststats(self, ctx):
        await ctx.send("Posting server count to Discord Bot List...")
        try:
            self.bot.dblpost()
        except Exception:
            self.bot.rclient.captureException()
            await ctx.send("I couldn't post my server count to Discord Bot List.")
        else:
            await ctx.send("Server count posted to Discord Bot List.")

    @commands.command(hidden=True)
    @checks.is_staff()
    async def say(self, ctx, *, message: str):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        await ctx.send(message)

    @commands.command()
    @checks.is_dev()
    async def restart(self, ctx):
        await ctx.send("Restarting...")
        self.bot.restart()

    @commands.command()
    @checks.is_staff()
    async def patronize(self, ctx, type: int, user: discord.User):
        """Makes someone a Patron."""
        db = psycopg2.connect(self.bot.settings.dsn)
        cursor = db.cursor()
        sql = "UPDATE users SET patron = %s WHERE id = %s"
        cursor.execute(sql, [type, user.id])
        db.commit()
        t = "placeholder"
        if type == 1:
            t = "premium"
        elif type == 2:
            t = "gold"
        else:
            t = "You shouldn't be reading this, but if you are, please report it at the Monika Discord."
        await ctx.send("<@{}> ({}) is now a {} patron.".format(user.id, user, t))

    @commands.command()
    @checks.is_admin()
    async def hire(self, ctx, type: int, user: discord.User):
        """Makes someone a staff member.."""
        db = psycopg2.connect(self.bot.settings.dsn)
        cursor = db.cursor()
        if type != 0 and type != 1 and type != 2 and type != 3:
            await ctx.send("``type`` must be a number between 0-3. Look at ``settings.py`` for more info.")
            return
        sql = "UPDATE users SET staff = %s WHERE id = %s"
        cursor.execute(sql, [type, user.id])
        db.commit()
        t = "placeholder"
        if type == 0:
            t = "user"
        elif type == 1:
            t = "administrator"
        elif type == 2:
            t = "developer"
        elif type == 3:
            t = "general staff member"
        else:
            t = "You shouldn't be reading this, but if you are, please report it at the Monika Discord."
        await ctx.send("<@{}> ({}) is now a {}.".format(user.id, user, t))

def setup(bot):
    bot.add_cog(Staff(bot))
