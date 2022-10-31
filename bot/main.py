# bot.py
from multiprocessing.connection import wait
import os

import discord
import re
import threading, time
import asyncio
from random import randrange
NUMWORDS = {}
units = [
"zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
"nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
"sixteen", "seventeen", "eighteen", "nineteen",
]

tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

scales = ["hundred", "thousand", "million", "billion", "trillion"]

all_numwords = units + tens + scales
all_numwords = ["\\b" + word + "\\b" for word in all_numwords if word != '']
NUMWORDS["and"] = (1, 0)
for idx, word in enumerate(units):    NUMWORDS[word] = (1, idx)
for idx, word in enumerate(tens):     NUMWORDS[word] = (1, idx * 10)
for idx, word in enumerate(scales):   NUMWORDS[word] = (10 ** (idx * 3 or 2), 0)

def text2int(textnum, numwords={}):
    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

class CustomClient(discord.Client):

    catch_phrases = {
        "give me like",
        "give me a",
        "give me", 
        "ill be",
        "Ill be",
        "ill be a",
        "Ill be a",
        "i'll be",
        "i'll be a",
        "I'll be",
        "I'll be a",
        "i'll be like",
        "I'll be like",
        "ill be like",
        "Ill be like",
        "Ill be back in",
        "ill be back in",
        "i'll be back in",
        "I'll be back in"
    }

    return_phrases = {
        "I fucking hate you where are you",
        "Please come back I miss you",
        "Hey where are you times up", 
        "Remember when you said you'd be back.. I remember",
        "Cum on me",
    }
    fun_faces = [
        "¯\_(ツ)_/¯",
        "( ͡~ ͜ʖ ͡°)",
        "٩(*❛⊰❛)～❤",
        "﴾͡๏̯͡๏﴿ ",
        "✧♡(◕‿◕✿)",
        "โ๏௰๏ใ ื",
        "(ㆆ _ ㆆ)",
        "'(ᗒᗣᗕ)՞",
        "O=('-'Q)",
        "(◍＞◡＜◍)⋈。✧♡",
        "(ღ˘⌣˘)♥ ℒ♡ⓥℯ ㄚ♡ⓤ",
        "(♡´౪`♡)",
        "∩｡• ᵕ •｡∩ ♡",
        "( ° ᴗ°)~ð (/❛o❛\)",
        "(>^o^)><(^o^<)",
        "♥(ˆ⌣ˆԅ)",
        "(• ε •)",
        "( ͡°❥ ͡°)",
        "(っ˘з(˘⌣˘ )",
        "(๑′ᴗ‵๑)Ｉ Lᵒᵛᵉᵧₒᵤ♥",
        "( ๑ ❛ ڡ ❛ ๑ )❤",
        "╰(✿´⌣`✿)╯♡",
        "(ㅅꈍ﹃ꈍ)*gᵒᵒᒄ ᵑⁱgᑋᵗ♡(ꈍ﹃ꈍㅅ)*",
        "(◟ᅇ)◜",
        "(☞ﾟ∀ﾟ)☞",
        "(╯°o°)ᕗ",
        "('_')┏oo┓('_')",
        "┌( ಠ_ಠ)┘",
        "乁( ⁰͡ Ĺ̯ ⁰͡ ) ㄏ",
        "¯\_( ͡° ͜ʖ ͡°)_/¯",
        "ヽ(゜～゜o)ノ",
        "v( ‘.’ )v",
        "ʕ•ᴥ•ʔ",
        "ʕಠಿᴥಠʔ",
        "｡◕‿‿◕｡ 🗲",
        "(ᵔᴥᵔ)",
        "▼・ᴥ・▼",
        "ᶘ ◕ᴥ◕ᶅ",
        "【≽ܫ≼】",
        "ᶘ ᵒᴥᵒᶅ",
        "ฅ^•ﻌ•^ฅ",
        "Ꮚ˘ꍓ˘Ꮚ",
        "( ͡° ͜ʖ ͡°)",
        "˙ ͜ʟ˙",
        "◟(๑･ิټ･ิ๑)◞",
        "( ಠ ͜ʖರೃ)",
        "( ͡ಠ ͜ʖ ͡ಠ)",
        "\ (•◡•) /",
        "(΄◞ิ౪◟ิ‵)",
        "(ง ͠° ͟ل͜ ͡°)ง",
        "(•̀ᴗ•́)و ̑̑",
        "(｡☉౪ ⊙｡)",
        "( ━☞´◔‿ゝ◔`)━☞",
        "( ͝סּ ͜ʖ͡סּ)",
        "(♡´艸`)",
        "(◕‿◕✿)",
        "◕‿↼",
        "ξξ(∵◕◡◕∵)ξξ",
        "◔̯◔",
        "(ง'̀-'́)ง",
        "(´°ω°`)",
        "(ﾟ∩ﾟ)",
        "ಠ_ಠ",
        "(╯︵╰,)",
        "( ° ʖ̯ ཀ)ᕗ",
        "(;´༎ຶД༎ຶ`)",
        "ཀ ʖ̯ ཀ",
        "(⌯˃̶᷄ ﹏ ˂̶᷄⌯)",
        "(ᗒᗣᗕ)՞",
        "͡ಥ ͜ʖ ͡ಥ",
        "( 　ﾟ,_ゝﾟ)",
        "(つ◉益◉)つ",
        "ლಠ益ಠ)ლ",
        "╚(ಠ_ಠ)=┐",
        "'''⌐(ಠ۾ಠ)¬'''",
        "(ᕗ ͠° ਊ ͠° )ᕗ",
        "ᕙ(⇀‸↼‶)ᕗ",
        "(ಠ ∩ಠ)",
        "(≈`˛ ´≈    з) ",
        "ಠ╭╮ಠ",
        "( ఠൠఠ )",
        "(╯°o°）╯︵ ┻━┻",
        "(ノಠ益ಠ)ノ彡┻━┻",
        "┬──┬ ノ( ゜-゜ノ)",
        "̿̿’̿’\̵͇̿̿\=(•̪●)=/̵͇̿̿/’̿̿ ̿ ̿ ̿",
        "(•̪●)=/̵/’̿̿ ̿ ̿ ̿ ̿",
        "╾━╤デ╦︻(▀̿Ĺ̯▀̿ ̿)",
        "t(-_-t)",
        "(ಠ_ಠ)┌∩┐",
        "(•‾⌣‾•)و ̑̑♡",
        "╭∩╮(-_-)╭∩╮",
        "t(^^t)",
        "♪~ ᕕ(ᐛ)ᕗ",
        "ᕕ( ಠ‿ಠ)ᕗ",
        "/'(´ཀ`)ﬣ∠",
        "( ^​_^）o自自o（^_​^ )",
        "ᕦ(⩾﹏⩽)ᕥ",
        "╰( ⁰ ਊ ⁰ )━☆ﾟ.*･｡ﾟ",
        "\m/_(>_<)_\m/",
        "( -_-)旦~",
        "(︶︹︺)",
        "(¬_¬)",
        "┌( ◕ 益 ◕ )ᓄ",
    ]

    message_queue = []

    async def send_reminder(self, delayIn, message):
        status_tuple = (message.author, message.created_at, delayIn)
        self.message_queue.append(status_tuple)
        print("Current Q status")
        for user, sendtime, waittime in self.message_queue:
            print(f"User: {user} sent at: {sendtime} waiting time: {waittime} ")
            
        print(f"printing in delay:{delayIn}")
        await message.channel.send(f"I'll be waiting :D")
        await asyncio.sleep(delay=delayIn)
        await message.channel.send(f"{message.author.mention} hey where are you times up {self.fun_faces[randrange(len(self.fun_faces))]}")
        self.message_queue.remove(status_tuple)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        print('welcome')
        if message.author == client.user:
            return
        print(f'my message is= [{message.content}]')
        base_regex = '.*('
        for phrase in self.catch_phrases:
            base_regex += f'{phrase}|'
        base_regex = base_regex[:-1] + ")"
        unit_regex = "(seconds|second|sec|minutes|minute|min|hours|hour)?"

        def get_true_time_seconds(initial_time, unit_group):
            if(unit_group):
                # if(results.groups(1) == "seconds"): do nothing 
                if re.search("minutes|minute|min", unit_group):
                    initial_time = initial_time * 60
                if re.search("hours|hour?", unit_group):
                    initial_time = initial_time * 60 * 60
            else: # we assume that saying nothing means minutes
                initial_time = initial_time * 60 
            return initial_time

        regex = base_regex + f"\s([0-9]+)\s?" + unit_regex
        results = re.search(regex, message.content)
        #print(regex)
        if results:
            print('======================ENTRY 1 ========================')
            wait_time = int(results.group(2))
            wait_time = get_true_time_seconds(wait_time, results.group(3))
            asyncio.create_task(self.send_reminder(wait_time, message))
            return

        regex = base_regex + "\s(an|a|couple|few)\s?" + unit_regex
        results = re.search(regex, message.content)
        #print(regex)
        if results:
            print('======================ENTRY 2 ========================')
            if "couple" in results.group(2) or "few" in results.group(2):
                wait_time = 2
            else:
                wait_time = 1
            wait_time = get_true_time_seconds(wait_time, results.group(3))
            asyncio.create_task(self.send_reminder(wait_time, message))
            return
        
        regex = base_regex + "\s?(" + '|'.join(all_numwords) + ")\s?" + unit_regex
        results = re.search(regex, message.content)
        #print(regex)
        if results:
            print('======================ENTRY 3 ========================')
            wait_time = text2int(results.group(2), NUMWORDS)
            wait_time = get_true_time_seconds(wait_time, results.group(3))
            asyncio.create_task(self.send_reminder(wait_time, message))
            return

        
            
            


if __name__ == '__main__':
    client = CustomClient(intents=discord.Intents.all())
    client.run(os.getenv('DISCORD_TOKEN'))

