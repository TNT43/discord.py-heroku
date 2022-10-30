# bot.py
import os

import discord
import re
import threading, time
import asyncio
from random import randrange

class CustomClient(discord.Client):

    catch_phrases = {
        "give me like",
        "give me", 
        "ill be",
        "Ill be",
        "i'll be",
        "I'll be",
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

    async def send_reminder(self, delayIn, message):
        print(f"printing in delay:{delayIn}")
        await asyncio.sleep(delay=delayIn)
        await message.channel.send(f"{message.author.mention} hey where are you times up {self.fun_faces[randrange(len(self.fun_faces))]}")

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        print('welcome')
        if message.author == client.user:
            return
        print(f'my message is= [{message.content}]')
        regex = '.*'
        for phrase in self.catch_phrases:
            regex += f'[{phrase}]?'
        regex += "\s([0-9]+|\\ba\\b|\\ban\\b|\\bcouple\\b|\\bfew\\b)\s(second[s]?|minute[s]?|hour[s]?)?"
        print('???')
        print(regex)
        print('???')
        results = re.search(regex, message.content)
        # returns a tuple. First index is full string. Every index after is a captured string
        if results:
            wait_time = None
            try:
                wait_time = int(results.group(1))
            except Exception as e: # user type a or an
                print(results.group(1))
                if "couple" in results.group(1) or "few" in results.group(1):
                    wait_time = 2
                else:
                    wait_time = 1
            
            
            if(results.group(2)):
                # if(results.groups(1) == "seconds"): do nothing 
                if(results.group(2) == "minutes" or results.group(2) == "minute"):
                    wait_time = wait_time * 60
                if(results.group(2) == "hours" or results.group(2) == "hour"):
                    wait_time = wait_time * 60 * 60
            else: # we assume that saying nothing means minutes
                wait_time = wait_time * 60 
            asyncio.create_task(self.send_reminder(wait_time, message))
            
            


if __name__ == '__main__':
    client = CustomClient(intents=discord.Intents.all())
    client.run(os.getenv('DISCORD_TOKEN'))

