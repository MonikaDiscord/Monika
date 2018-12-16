import aiohttp
import asyncio

class DiscordBL:
    def __init__(self,bot):
        self.bot = bot
        asyncio.get_event_loop().create_task(self.guild_count_loop())
    async def guild_count_loop(self):
        while True:
            payload = json.dumps({
                'shard_count': self.bot.shard_count,
                'server_count': len(self.bot.guilds)
            })
            headers = {
                'Authorization': self.bot.config['dblkey'],
                'Content-type' : 'application/json'
            }
            url = f'https://discordbots.org/api/bots/{self.bot.user.id}/stats'
            await self.bot.session.post(url, data=payload, headers=headers)
            await asyncio.sleep(900)

    async def get_vote_count(self):
        print ('test')
        pass

def setup(bot):
    bot.add_cog(DiscordBL(bot))