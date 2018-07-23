import discord
from discord.ext import commands
import asyncio
import json

class Botlists:

    def __init__(self, bot):
        self.bot = bot
        l = asyncio.get_event_loop()
        l.create_task(self.discordbotsorg())
        l.create_task(self.botsdiscordpw())
        l.create_task(self.botsdisgdpw())
    
    async def discordbotsorg(self):
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
            await self.session.post(url, data=payload, headers=headers)
            await asyncio.sleep(900)
      
      
    async def botsdiscordpw(self):
        while True:
            payload = json.dumps({
                'shard_count': self.bot.shard_count,
                'server_count': len(self.bot.guilds)
            })
            headers = {
                'Authorization': self.bot.config['pwkey'],
                'Content-type' : 'application/json'
            }
            url = f'https://bots.discord.pw/api/bots/{self.bot.user.id}/stats'
            await self.session.post(url, data=payload, headers=headers)
            await asyncio.sleep(900)
            
    async def botsdisgdpw(self):
        while True:
              payload = json.dumps({
                  'server_count': len(self.bot.guilds)
              })
              headers = {
                  'Authorization': self.bot.config['kbkey'],
                  'Content-type' : 'application/json'
              }
              url = f'https://bots.disgd.pw/api/bot/{self.bot.user.id}/stats'
              await self.session.post(url, data=payload, headers=headers)
              await asyncio.sleep(900)
      
def setup(bot):
    bot.add_cog(Botlists(bot))
