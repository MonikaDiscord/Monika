import discord

def embed(ctx, title, desc):
    if ctx.message.guild is not None:
        color = ctx.message.guild.me.color
    else:
        color = discord.Colour.blue()
    e = discord.Embed(color=color, title=title, description=desc)
    return e