class Prefix:

    async def prefixcall(self, bot, msg):
        if msg.guild is None:
            return "$!"
        sql = "SELECT prefix FROM guilds WHERE id = $1"
        r = await bot.db.fetchval(sql, msg.guild.id)
        if r:
            return r
        else:
            return '$!'
