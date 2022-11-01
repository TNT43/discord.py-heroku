# bot.py
from curses import beep
from email.mime import base
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

    # g?i?v?e?\s?m?e?\s?l?i?k?e?\s?([0-9]+)
    # i?'?l?l?\s?b?e?\s?(l?i?k?e?|\ban\b|\ba\b)\s?([0-9]+)

    # ill be -> i['’]?l?l?\s*be?
    # give me (and gimme) -> g?iv?e?\s*m{1,2}e
    # back in OR like -> (\bl?i?ke?\b|\bbac?k?\s*i?n?\b)
    # (ill be | give me)(back in | like) -> (i['’]?l?l?\s*be?|g?iv?e?\s*m{1,2}e)\s*(\bl?i?ke?\b|\bbac?k?\s*i?n?\b)
    # (ill be | give me)(back in | like)(a | an | wordNum | intNum) -> (i['’]?l?l?\s*be?|g?iv?e?\s*m{1,2}e)\s*(\bl?i?ke?\b|\bbac?k?\s*i?n?\b)?\s*(\ba\b|\ban\b|\bone\b|[0-9]+)
    # all of above + units (i['’]?l?l?\s*be?|g?iv?e?\s*m{1,2}e)\s*(\bl?i?ke?\b|\bbac?k?\s*i?n?\b)?\s*(\ba\b|\ban\b|\bone\b|[0-9]+)\s*(\bse?c?o?n?d?s?\b|\bmi?n?u?t?e?s?\b|\bho?u?r?s?\b)?
    # add in (couple and few) (i['’]?l?l?\s?be?|g?iv?e?\s?m{1,2}e)\s*(\bl?i?ke?\b|\bbac?k?\s?i?n?\b)?\s*(\ba?\s?(c?o?u?p?l?e?\s*o?f?|f?e?w?)\b|\ban\b|\bone\b|[0-9]+)\s*(\bse?c?o?n?d?s?\b|\bmi?n?u?t?e?s?\b|\bho?u?r?s?\b)?

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
    # god regex string no touch pls "(i['’]?l?l?\s?be?|g?iv?e?\s?m{{1,2}}e)\s?(\\bl?i?ke?\\b|\\bbac?k?\s?i?n?\\b)?\s?(\\ba\\b|\\ban\\b|{'|'.join(all_numwords)}|[0-9]+)\s?(\\bse?c?o?n?d?s?\\b|\\bmi?n?u?t?e?s?\\b|\\bho?u?r?s?\\b)?"
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
       
        base_regex = f"(i['’]?l?l?\s*be?|g?iv?e?\s*m{{1,2}}e)\s*(\\bl?i?ke?\\b|\\bbac?k?\s*i?n?\\b)?\s*(\\ba\s*(\\bco?u?p?l?e?\s*o?f?\\b|\\bf?e?w?\\b){{0,1}}\\b|\\ban\\b|{'|'.join(all_numwords)}|[0-9]+\.?[0-9]*)\s*(\\bse?c?o?n?d?s?\\b|\\bmi?n?u?t?e?s?\\b|\\bho?u?r?s?\\b)?"

        print(base_regex)
        
        def get_true_time_seconds(initial_time, unit_group):
            if(unit_group):
                # if(results.groups(1) == "seconds"): do nothing 
                if re.search("\\bmi?n?u?t?e?s?\\b", unit_group, re.IGNORECASE):
                    initial_time = initial_time * 60
                if re.search("\\bho?u?r?s?\\b", unit_group, re.IGNORECASE):
                    initial_time = initial_time * 60 * 60
            else: # we assume that saying nothing means minutes
                initial_time = initial_time * 60 
            return initial_time

        results = re.search(base_regex, message.content, re.IGNORECASE)

        if not results:
            return
        
        print("==============primary regex groups==============")
        print(results.group(1))
        print(results.group(2))
        print(results.group(3))
        print(results.group(4))
        print(results.group(5))
        print("==============primary regex groups==============")

        wait_time = None
        try:
            wait_time = float(results.group(3))
            wait_time = (int(round(wait_time)))
        except Exception as e:
            if results.group(3):
                print(f"Secondary search on \"{results.group(3).rstrip()}\"")
                sec_regex = "(\\ba\s*(\\bco?u?p?l?e?\s*o?f?\\b|\\bf?e?w?\\b)|\\ban\\b)"
                sec_results = re.search(sec_regex, results.group(3).rstrip(), re.IGNORECASE)
                if sec_results:
                    print("==============secondary regex groups==============")
                    print(sec_results.group(1))
                    print(sec_results.group(2))
                    print("==============secondary regex groups==============")

                    if sec_results.group(2):
                        wait_time = 2
                    else:
                        wait_time = 1
                else:
                    wait_time = text2int(results.group(3), NUMWORDS)
    
        wait_time = get_true_time_seconds(wait_time, results.group(5))
                
        asyncio.create_task(self.send_reminder(wait_time, message))
            

if __name__ == '__main__':
    client = CustomClient(intents=discord.Intents.all())
    client.run(os.getenv('DISCORD_TOKEN'))

