# bot.py
import os

import discord
import re
import threading, time
import asyncio

class CustomClient(discord.Client):

    async def send_reminder(self, delayIn, message):
        await asyncio.sleep(delay=delayIn)
        await message.channel.send(":3")

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        print('welcome')
        if message.author == client.user:
            return
        print(f'my message is= [{message.content}]')
        results = re.search(".*[give me]? [like]?([0-9]+)(seconds|minutes|hours)?", message.content)
        # returns a tuple. First index is full string. Every index after is a captured string
        if results:
            wait_time = int(results.group(1))
            if(results.group(2)):
                # if(results.groups(1) == "seconds"): do nothing 
                if(results.group(2) == "minutes"):
                    wait_time = wait_time * 60
                if(results.group(2) == "hours"):
                    wait_time = wait_time * 60 * 60
        asyncio.create_task(self.send_reminder(wait_time, message))
            
            


if __name__ == '__main__':
    client = CustomClient(intents=discord.Intents.all())
    client.run(os.getenv('DISCORD_TOKEN'))

