# bot.py
import os

import discord
import re
import threading, time

class CustomClient(discord.Client):

    def handle_message(self, message):
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
            
            time.sleep(wait_time)
            print(':3')

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        thread = threading.Thread(target=self.handle_message, args=(message,))
        thread.start()
        
if __name__ == '__main__':
    client = CustomClient(intents=discord.Intents.all())
    client.run(os.getenv('DISCORD_TOKEN'))

