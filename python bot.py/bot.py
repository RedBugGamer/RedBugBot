# imports
from PIL import Image
import json
import math
import asyncio
from datetime import datetime
from discord import colour
from discord.ui.item import Item
import nextcord
from nextcord.client import Client
from nextcord.ui import view
from discord import guild
import time
import requests
from random import randrange
from discord.ui import Button,View
import os
from nextcord import *
from discord.colour import Color, Colour
from exaroton import Exaroton
import tinydb
from dotenv import load_dotenv
import discord
from discord.enums import TeamMembershipState
import time
import macro
import random
from typing import List, Mapping
from discord.ext import commands
import discord
from tinydb import *
from mouse import press
from pynput.keyboard import Key
from evalprot import makeeval
import pymongo
from bson.objectid import ObjectId

#load .env filw
load_dotenv()

#define important variables
exa = Exaroton(os.environ["exaroton"])
TOKEN = os.environ["token"]
client = discord.Client()
awaitpoll = False
id = "H6WIxtAqtR1pMJJb"
dice = False
running = False
status=False
myclient = pymongo.MongoClient("mongodb://localhost",port=27017)
RedBugBot = myclient["RedBugBot"]
linkedchannels = RedBugBot["linkedchannels"]
morsealphabet = {'a' : '•-', 'b' : '-•••', 'c' : '-•-•', 'd' : '-••', 'e' : '•', 'f' : '••-•', 'g' : '--•', 'h' : '••••', 'i' : '••', 'j' : '•---', 'k' : '-•-', 'l' : '•-••', 'm' : '--', 'n' : '-•', 'o' : '---', 'p' : '•--•', 'q' : '--•-', 'r' : '•-•', 's' : '•••', 't' : '-', 'u' : '••-', 'v' : '•••-', 'w' : '•--', 'x' : '-••-', 'y' : '-•--', 'z' : '--••', '•' : '•-•-•-', '?' : '••--••', ',' : '--••--', ' ' : ''}
#Button menus
class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "O ist dran"
        else:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "X sit drann"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None
class Schiffefeld(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @nextcord.ui.button(label="⠀",style=nextcord.ButtonStyle.blurple)
    async def Spielfeld1(self,button : nextcord.ui.Button,interaction:nextcord.Interaction):
        while True:
            await interaction.response.send_message("Dein spielfeld XD2",ephemeral=True)
class Schiffetot():
    def __init__(self):
        super().__init__()
        self.value = None
    
    @nextcord.ui.button(label="Spielfeld",style=nextcord.ButtonStyle.grey)
    async def Field1(self,button : nextcord.ui.Button,interaction:nextcord.Interaction):
        await interaction.response.send_message("Dein spielfeld XD",ephemeral=True,view=Schiffefeld())
        await interaction.edit_original_message()
class stopstatus(discord.ui.View):
                def __init__(self):
                    super().__init__()
                    self.value = None
                @nextcord.ui.button(label="Cancel",style=nextcord.ButtonStyle.danger)
                async def Stopstatus(self,button : nextcord.ui.Button,interaction:nextcord.Interaction):
                    global running
                    running = False
def getstatuscolor(currentrequest,sendtimestamp):
    
    if currentrequest == "Online":
        return discord.Embed(description=f"Aktueller status `{str(currentrequest)}`. Könnte aber nicht aktuell sein",color=0x2ecc71,timestamp=sendtimestamp)
    elif currentrequest == "Offline":
        return discord.Embed(description=f"Aktueller status `{str(currentrequest)}`. Könnte aber nicht aktuell sein",color=0x979c9f,timestamp=sendtimestamp)
    elif currentrequest == "Saving":
        return discord.Embed(description=f"Aktueller status `{str(currentrequest)}`. Könnte aber nicht aktuell sein",color=0xFEE75C,timestamp=sendtimestamp)
    elif currentrequest == "Loading":
        return discord.Embed(description=f"Aktueller status `{str(currentrequest)}`. Könnte aber nicht aktuell sein",color=0xe67e22,timestamp=sendtimestamp)
    elif currentrequest == "Starting":
        return discord.Embed(description=f"Aktueller status `{str(currentrequest)}`. Könnte aber nicht aktuell sein",color=0x3498db,timestamp=sendtimestamp)
    else:
        return discord.Embed(description=f"Aktueller status `Fail`",color=0xe74c3c)

#Help menu
Help = discord.Embed(description="Hi also ich bin ein bot von RedBugGamer#2069",color=0xe74c3c,timestamp=datetime.now())
Help.add_field(name = "`Prefix`",value="Mein prefix ist `T!`",inline=True)
Help.add_field(name = "`T!help`",value="Der Command hilft dir",inline=True)
Help.add_field(name="`T!controll`",value="Ist ein Botowner only command")
Help.add_field(name="`T!say`",value="Sagt etwas",inline=True)
Help.add_field(name="`T!poll`",value="Macht einen vote",inline=True)
Help.add_field(name="`T!dice`",value="Würfelspiele 🎲",inline=True)
Help.add_field(name="`T!web`",value="Gibt den link zu meiner Website",inline=True)
Help.add_field(name="`T!tictactoe`",value="Macht ein TikTakToe game.",inline=True)
Help.add_field(name="`T!ping`",value="Gibt den botping",inline=True)
Help.add_field(name="`T!send`",value="Sendet eine nachricht in den channel",inline=True)
Help.add_field(name="`T!purge`",value="Löscht x nachrichten",inline=True)
Help.add_field(name="`T!block`",value="Blockiert User x vom bot use",inline=True)
Help.add_field(name="`T!eval`",value="Evaluiert code",inline=True)
Help.add_field(name="`T!embed`",value="Macht ein embed mit description + evtl. `|` für felder",inline=True)
Help.add_field(name="`T!morse`",value="Gibt morsecode zurück",inline=True)
Help.add_field(name="`T!bind`",value="bindet einen server zum channel",inline=True)
Help.add_field(name="`T!stats`",value="Gibt ein paar Minecraft stats",inline=True)


#Bot activities
activitys = ["Welteroberungspläne","Deine Voodopuppe","Langeweile","Editierung der eigenen bot.py","Ließt deine Gedanken","definitiv kein Minecraft Server hacken"]
blockedusers = []
#on ready/Change bot activitie
@client.event
async def on_ready():
    Help.set_author(name=client.user,icon_url=client.user.avatar.url)
    print(f'{client.user} has connected to Discord!')
    while True:
        await client.change_presence(activity=discord.Game(activitys[randrange(0,len(activitys))]),status=discord.Status.online)
        await asyncio.sleep(random.randrange(15,60))

#commands/ingame chat
@client.event
async def on_message(message):
    if str(message.channel.id) in linkedchannels.find_one({"_id": ObjectId("61b5d3560d296088f9c970f4")}) and not message.content.startswith("T!"):
        if linkedchannels.find_one({"_id": ObjectId("61b5d3560d296088f9c970f4")})[str(message.channel.id)] != "":
            exa.command(linkedchannels.find_one({"_id": ObjectId("61b5d3560d296088f9c970f4")})[str(message.channel.id)],f'tellraw @a "<{message.author}> {message.content}"')
    #make global variables
    global awaitpoll
    global dice
    global status
    global running
    # block users
    if not message.author in blockedusers:
        #await message from self
        if message.author == client.user:
            if awaitpoll:
                #macht poll
                awaitpoll = False
                await message.add_reaction("👍")
                await message.add_reaction("👎")
            elif dice:
                #macht würfel
                dice = False
                for i in range(4):
                    await asyncio.sleep(0.75)
                    await message.edit(embed=discord.Embed(description="Rolling 🎲 "+str(randrange(1,6))))
                await message.edit(embed=discord.Embed(color=0x1f8b4c,description="🎲 "+str(randrange(1,6))))
            elif status:
                #bearbeitet die nachricht für status
                status=False
                running = True
                await asyncio.sleep(1)
                while running:
                    await asyncio.sleep(15)
                    await message.edit(embed=getstatuscolor(exa.get_server(id=id).status,datetime.now()))
                await message.edit(embed=discord.Embed(description="Disabled"))
            return  
        if message.content == "T!help":
            #zeigt help menu
            await message.channel.send(embed = Help)
            
        elif message.content.startswith("T!say"):
            #sagt string
            await message.channel.send(message.content.replace("T!say",""))
            
        elif message.content.startswith("T!poll"):
            #macht einen poll
            awaitpoll = True
            if message.author.avatar == None:
                #check avatar exists
                await message.channel.send(embed=discord.Embed(color=0xe74c3c,title="Poll",description=message.content.replace("T!poll",""),timestamp=datetime.now()).set_author(name=message.author))
            else:
                await message.channel.send(embed=discord.Embed(color=0xe74c3c,title="Poll",description=message.content.replace("T!poll",""),timestamp=datetime.now()).set_author(name=message.author,icon_url=message.author.avatar.url))
        elif message.content.startswith("T!controll "):
            #control computer
            if message.author.id == 772386889817784340:
                if message.content.replace("T!controll ","") == "hotspot":
                    macro.hotspot()
                    await message.channel.send(embed=discord.Embed(description="Hotspot eingeschalten"))
                elif message.content.replace("T!controll ","") == "shutdown":
                    await message.channel.send(embed=discord.Embed(description="Ausschalten"))
                    macro.shutdown()
                elif message.content.replace("T!controll ","").startswith("message"):
                    await message.channel.send(embed=discord.Embed(description="Du hast `"+message.content.replace("T!controll","").replace(" message ","")+"` gesendet"))
                    macro.message(message.content.replace("T!controll","").replace(" message",""),15)
                elif message.content.replace("T!controll ","") == "restart":
                    await message.channel.send(embed=discord.Embed(description="Neustarten"))
                    macro.restart()
                elif message.content.replace("T!controll ","") == "gamer":
                    macro.win_r("C:/Users/RedBugGamer/AppData/Roaming/MultiMC/Multimc.exe")
                    time.sleep(2)
                    macro.press(Key.enter)
                    await message.channel.send(embed=discord.Embed(description="Aktuelle instanz gestartet"))
                
            else:
                #keine perms
                await message.channel.send(embed=discord.Embed(description="Du hast keine Berechtigung dazu"))
        
        elif message.content.startswith("T!purge "):
            #botowner only lösch command
            if message.author.id == 772386889817784340:
                await message.channel.purge(limit=int(message.content.replace("T!purge ","")))

            else:
                await message.channel.send(embed=discord.Embed(description="Du hast keine Berechtigung dazu",color=nextcord.Color.red))

        elif message.content == "T!dice":
            #würfelt
            dice=True
            await message.channel.send(embed=discord.Embed(description="Rolling 🎲 "+str(randrange(1,6))))

            
        elif message.content == "T!web":
            #link zur website W.I.P.
            await message.channel.send(embed=discord.Embed(description="Meine [Website](https://RedBugBot-in-python.redbuggamer.repl.co)"))
        elif message.content == "T!tictactoe":
            #startet tictactoe
            await message.channel.send("⠀",view=TicTacToe())
        elif message.content == "T!schiffetot":
            #macht schiffeversenken W.I.P.
            await message.channel.send("⠀",view=Schiffetot())
        elif message.content == "T!ping":
            #macht botping
            await message.channel.send(embed=discord.Embed(description=f"Latency of `{round(client.latency*1000)}` ms",color=0x3498db))
        elif message.content.startswith("T!send "):
            #sendet was in den channel
            if message.author.id == 772386889817784340:
                await message.channel_mentions[0].send(message.content[message.content.find("> ")+1:int(len(message.content))])        
            else:
                await message.channel.send(embed=discord.Embed(description="Du hast keine Berechtigung dazu",color=0xe74c3c))
        elif message.content.startswith("T!embed "):
            arguments = message.content[8:len(message.content)].split(" | ")
            if (len(arguments) %2) == 0:
                await message.channel.send(embed=discord.Embed(description="ERROR Du benötigst mehr input",colour=0xe74c3c))
            else:
                customembed = discord.Embed(description=arguments[0],color=0x2ecc71).set_author(name=f"{message.author.name}#{message.author.discriminator}",icon_url=message.author.avatar.url)
                active = False
                for i in range(int(len(arguments))):
                    if active:
                        customembed.add_field(inline=False,name=arguments[i],value=arguments[i+1])
                        active=False
                    else:
                        active=True
                await message.channel.send(embed=customembed)
        elif message.content.startswith("T!block"):
            if message.author.id == 772386889817784340:
                if message.mentions[0] in blockedusers:
                    blockedusers.remove(message.mentions[0])
                    
                    await message.channel.send(embed=discord.Embed(description=f"<@{message.mentions[0].id}> darf mich wieder benutzen",color=0x2ecc71))
                else:
                    blockedusers.append(message.mentions[0])
                    await message.channel.send(embed=discord.Embed(description=f"<@{message.mentions[0].id}> wurde blockiert",color=0xe74c3c))
            else:
                await message.channel.send(embed=discord.Embed(description="Acces denied",color=0xe74c3c))

        elif message.content.startswith("T!eval"):
            myeval = makeeval(message.content.replace("```py","").replace("```","").replace("print(","evalprint(")[6:len(message.content)])
            await message.channel.send(embed=discord.Embed(description=f"Output: `{myeval}`"))
        elif message.content.startswith("T!morse "):
            morse = ""
            morse = morse.join(" "+morsealphabet[i.lower()] for i in message.content.replace("T!morse ",""))
            await message.channel.send(embed=discord.Embed(description=f"Dein morsecode: `{morse}`",color=0x3498db))
        elif message.content.startswith("T!bind "):
            if message.author.id == 772386889817784340 or message.author.adminstrator:
                idbefore = linkedchannels.find_one({"_id": ObjectId("61b5d3560d296088f9c970f4")})[str(message.channel.id)]
                customid = message.content.replace("T!bind ","")
                if message.content.replace("T!bind ","") == "unbind":
                    linkedchannels.update_one({"_id": ObjectId("61b5d3560d296088f9c970f4")},{"$set":{str(message.channel.id):""}})
                    await message.channel.send(embed=discord.Embed(description=f"Bindung `{idbefore}` gelöscht",color=0xe74c3c))
                else:
                    linkedchannels.update_one({"_id": ObjectId("61b5d3560d296088f9c970f4")},{"$set":{str(message.channel.id):str(message.content.replace("T!bind ",""))}})
                    await message.channel.send(embed=discord.Embed(description=f"Bound Exaroton Server `{customid}`",color=0x3498db))
            else:
                await message.channel.send(embed=discord.Embed(description="Du hast keine Berechtigung dazu",color=0xe74c3c))
        elif message.content == "T!bind":
            thatid = linkedchannels.find_one({"_id": ObjectId("61b5d3560d296088f9c970f4")})[str(message.channel.id)]
            await message.channel.send(embed=discord.Embed(description=f"Channel ist zu Server `{thatid}` gebunden"))

        elif message.content.startswith("T!stats "):
            playerembed = discord.Embed(color=0x206694)
            player = message.content.replace("T!stats ","")
            request = requests.get(url=f"https://api.slothpixel.me/api/players/{player}").json()
            if "error" in request:
                await message.channel.send(embed=discord.Embed(color=0xe74c3c,description="Der Player existiert nicht"))
            else:
                uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()["id"]
                apikey = os.environ["apikey"]
                lastlogin = math.floor(request["last_login"]/1000)
                level = request["level"]
                levelbarpercent= math.ceil((math.floor(level)-level)*-12)
                levelbar=""
                link=request["links"]["DISCORD"]
                rank={"VIP":"VIP","VIP_PLUS":"VIP+","MVP":"MVP","MVP_PLUS":"MVP+","MVP_PLUS_PLUS":"MVP++"}
                currrank = rank[request["rank"]]
                for i in range(levelbarpercent):
                    levelbar += "🟩"
                for i in range(12-levelbarpercent):
                    levelbar += "🔳"

                playerembed.set_thumbnail(url=f"https://crafatar.com/renders/body/{uuid}?size=200&default=MHF_Steve&overlay")
                playerembed.set_author(name=f"[{currrank}] {player}",icon_url=f"https://crafatar.com/avatars/{uuid}?size=200&default=MHF_Steve&overlay")
                playerembed.add_field(inline=False,name="`uuid`",value=uuid)
                playerembed.add_field(inline=False,name="`Last Login`",value=f"<t:{lastlogin}:F>")
                playerembed.add_field(inline=False,name="`Version`",value=request["mc_version"])
                if request["online"]:
                    playerembed.add_field(inline=False,name="`Online`",value="🟩")
                else:
                    playerembed.add_field(inline=False,name="`Offline`",value="🔲")
                playerembed.add_field(inline=False,name="`Discord`",value=f"{link}")
                playerembed.add_field(inline=False,name=f"`Level {math.floor(level)}`",value=f"{levelbar}")
                await message.channel.send(embed=playerembed)

        
        elif message.content.startswith("T!"):
            await message.channel.send(embed=discord.Embed(description="Der Command `"+message.content+"` existiert nicht"))
        
    elif message.content.startswith("T!"):
        await message.channel.send(embed=discord.Embed(description="Acces denied - You have been blocked",color=0xe74c3c))
    if message.content.startswith("T!") and not message.content.startswith("T!purge"):
            await message.delete()

#run the bot
client.run(TOKEN)
