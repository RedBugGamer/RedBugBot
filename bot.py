# -*- coding: utf-8 -*-
# imports
import asyncio
from asyncio.tasks import wait_for
import datetime
import math
import os
import random
from random import randint, randrange
from typing import List
import humanfriendly
import nextcord
import pymongo
import requests
from bson.objectid import ObjectId
from dotenv import load_dotenv
from exaroton import Exaroton
from nextcord import *
from nextcord.ext import tasks
from nextcord.ui import Button, View, view
from evalprot import makeeval

#load .env filw
load_dotenv()

#define important variables
intents = Intents.default()
intents.members = True
intents.all()
exa = Exaroton(os.environ["exaroton"])
TOKEN = os.environ["token"]
client = nextcord.Client(intents=intents)
awaitpoll = False
id = "H6WIxtAqtR1pMJJb"
dice = False
running = False
status=False
myclient = pymongo.MongoClient(os.environ["mongourl"],port=27017) #"mongodb://localhost"
RedBugBot = myclient["RedBugBot"]
linkedchannels = RedBugBot["linkedchannels"]
somedata=RedBugBot[" somedata"]
redbuggamer = 772386889817784340
zen = "https://zenquotes.io/api/random"
sadwords=["demotivatet"]
blockeduserdocid="61d191f56c7061e409ed16d6"
linkedchannelsmongoid="61b5d3560d296088f9c970f4"
morsealphabet = {'a' : '.-', 'b' : '-...', 'c' : '-.-.', 'd' : '-..', 'e' : '.', 'f' : '..-.', 'g' : '--.', 'h' : '....', 'i' : '..', 'j' : '.---', 'k' : '-.-', 'l' : '.-..', 'm' : '--', 'n' : '-.', 'o' : '---', 'p' : '.--.', 'q' : '--.-', 'r' : '.-.', 's' : '...', 't' : '-', 'u' : '..-', 'v' : '...-', 'w' : '.--', 'x' : '-..-', 'y' : '-.--', 'z' : '--..', '.' : '.-.-.-', '?' : '..--..', ',' : '--..--', ' ' : ''}
Hicooldown = 0
#Button menus
class TicTacToeButton(nextcord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        
        super().__init__(style=nextcord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = nextcord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "O ist dran"
        else:
            self.style = nextcord.ButtonStyle.success
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
class TicTacToe(nextcord.ui.View):
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
class Schiffefeld(nextcord.ui.View):
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
def getstatuscolor(currentrequest,sendtimestamp):
    
    if currentrequest == "Online":
        return nextcord.Embed(description=f"Aktueller status `{str(currentrequest)}`. Könnte aber nicht aktuell sein",color=0x2ecc71,timestamp=sendtimestamp)
    elif currentrequest == "Offline":
        return nextcord.Embed(description=f"Aktueller status `{str(currentrequest)}`. Könnte aber nicht aktuell sein",color=0x979c9f,timestamp=sendtimestamp)
    elif currentrequest == "Saving":
        return nextcord.Embed(description=f"Aktueller status `{str(currentrequest)}`. Könnte aber nicht aktuell sein",color=0xFEE75C,timestamp=sendtimestamp)
    elif currentrequest == "Loading":
        return nextcord.Embed(description=f"Aktueller status `{str(currentrequest)}`. Könnte aber nicht aktuell sein",color=0xe67e22,timestamp=sendtimestamp)
    elif currentrequest == "Starting":
        return nextcord.Embed(description=f"Aktueller status `{str(currentrequest)}`. Könnte aber nicht aktuell sein",color=0x3498db,timestamp=sendtimestamp)
    else:
        return nextcord.Embed(description=f"Aktueller status `Fail`",color=0xe74c3c)
async def noperms(obj:nextcord.Message,neededpermission=""):
    await obj.reply(embed=nextcord.Embed(title="Du hast keine Berechtigung dazu",description=neededpermission,color=0xe74c3c))
registeredcommands = {"help":"Zeigt dir diese Einbettung `Usage: T!help <command>`",
                    "ping":"Gibt meinen ping `Usage: T!ping`",
                    "block":"Blockiert einen User sodass der den bot nicht nutzen kann `Usage: T!block <@ member>`",
                    "send":"sendet etwas in kanal x `Usage: T!send <# channel> <message>`",
                    "say":"sagt etwas als ich `Usage: T!say <message>`",
                    "activität":"Setzt meine Bot Aktivität `Usage: T!activity <str>`",
                    "dice":"Würfelt für dich `Usage: T!dice`",
                    "tictactoe":"Startet ein TikTakToe game `Usage: T!tictactoe`",
                    "google":"googelt was für dich `Usage: T!google/T!g/T!guckle`",
                    "morse":"gibt die morsetext `Usage: T!morse <text>`",
                    "embed":"Sendet eine Einbettung `Usage: T!embed <description>` um ein feld hinzuzufügen: ` | <name> | <value>`",
                    "stats":"Gibt die Hypixel stats `Usage: T!stats <player>`",
                    "poll":"Macht eine Umfrage `Usage: T!poll <Frage>`",
                    "bind":'Bindet eine [Exaroton](https://exaroton.com) Server id zum channel `Usage: T!bind <serverid/"unbind">`',
                    "mute":"Mutet einen User für x minuten `Usage: T!mute @member <Zeit>`",
                    "reboot":"Startet mich neu `Usage: T!reboot`",
                    "licht":"toggelt licht mit id x `Usage: T!licht <id> <time>`",
                    "web":"Gibt dir den link zu meiner Website `Usage: T!web`"
                        }


@tasks.loop(minutes=4)
async def statuschange():
    await client.change_presence(activity=nextcord.Game(random.choice(activitys)),status=nextcord.Status.online)

#Bot activities
activitys = ["Welteroberungspläne","Deine Voodopuppe","Langeweile","Editierung der eigenen bot.py","Ließt deine Gedanken","definitiv kein Minecraft Server hacken","Fresse Elektrizität","Testet virtuelle Synapsen","Beobachtet Dischordserver"]
#on ready/Change bot activitie
@client.event
async def on_ready():
    if not statuschange.is_running():
        statuschange.start()
    print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_disconnect():
    print("disconnectet")

#commands/ingame chat
@client.event
async def on_message(message:nextcord.Message):
    if message.channel.id == 917083417127055470:
            print("Rebooting")
            await client.change_presence(status=nextcord.Status.dnd,activity=nextcord.Game("Rebooting"))
            await asyncio.sleep(5)
            os.system("./mystartupscript")
            quit()

    if message.content=="T!reboot":
            if message.author.id == redbuggamer:
                await message.channel.trigger_typing()
                await client.change_presence(status=nextcord.Status.dnd,activity=nextcord.Game("Rebooting"))
                await message.channel.send(embed=nextcord.Embed(description="RESTARTING"))
                await message.delete()
                print("Rebooting")
                await asyncio.sleep(5)
                os.system("./mystartupscript")
                quit()
            else:
                noperms(message,"Du brauchst Botowner")
    if str(message.channel.id) in linkedchannels.find_one({}) and not message.content.startswith("T!"):
        if linkedchannels.find_one({})[str(message.channel.id)] != "":
            exa.command(linkedchannels.find_one({})[str(message.channel.id)],f'tellraw @a "<{message.author}> {message.content}"')
    #make global variables
    global awaitpoll
    global dice
    global status
    global running
    global Hicooldown
    # block users
    if not str(message.author.id) in somedata.find_one({"_id":ObjectId("61d191f56c7061e409ed16d6")})["blockeduserid"]:
        #await message from self
        if message.author == client.user:
            if not message.content.startswith("T!"):
                return  
        if message.content == "T!help":
            #zeigt help menu
            Help = nextcord.Embed(description="Hi also ich bin ein bot von RedBugGamer#2069",color=0xe74c3c,timestamp=datetime.datetime.utcnow())
            Help.set_author(name=client.user,icon_url=client.user.avatar.url)
            Help.add_field(name = "Prefix",value="Mein prefix ist `T!`",inline=False)
            Help.add_field(name = "Basic Commands",value="`T!help`,`T!ping`,`T!web`",inline=False)
            Help.add_field(name="Botowner",value="`T!block`,`T!send`,`T!activity`,`T!reboot`,`T!bind`",inline=False)
            Help.add_field(name="Fun stuff",value="`T!dice`,`T!tictactoe`",inline=False)
            Help.add_field(name="Sinnloses Zeug",value="`T!morse`,`T!google`",inline=False)
            Help.add_field(name="Advanced",value="`T!embed`,`T!stats`,`T!poll`",inline=False)
            Help.add_field(name="Admin",value="`T!mute`",inline=False)
            await message.channel.send(embed = Help)
        elif message.content.startswith("T!help "):
            query= message.content.split()[1].replace("T!","",1)
            if query in registeredcommands:
                await message.channel.send(embed=nextcord.Embed(title="T!"+query,description=registeredcommands[query],color=0xe74c3c))
            else:
                await message.channel.send(embed=nextcord.Embed(title="T!"+query,description="Der Command existiert nicht",color=0xe74c3c))
            
        elif message.content.startswith("T!say"):
            if message.author.id == redbuggamer:
                #sagt string
                await message.channel.send(message.content.replace("T!say","",1),embeds=message.embeds,tts=message.tts)
            else:
                    await noperms(message,"Du brauchst Botowner")

        elif message.content.startswith("T!poll"):
            
            await message.channel.trigger_typing()
            #macht einen poll
            if message.author.avatar == None:
                #check avatar exists
                poll = await message.channel.send(embed=nextcord.Embed(color=0xe74c3c,title="Poll",description=message.content.replace("T!poll","",1),timestamp=datetime.datetime.now()).set_author(name=message.author))
            else:
                poll = await message.channel.send(embed=nextcord.Embed(color=0xe74c3c,title="Poll",description=message.content.replace("T!poll","",1),timestamp=datetime.datetime.now()).set_author(name=message.author,icon_url=message.author.avatar.url))
            await poll.add_reaction("👍")
            await poll.add_reaction("👎")
            def check(reaction:nextcord.Reaction, user):
                return poll== reaction.message and message.author == user or not reaction.emoji == "👍" and not reaction.emoji == "👎"
            await message.delete()
            while True:
                reaction, user = await client.wait_for('reaction_add', check=check)
                await poll.remove_reaction(reaction.emoji,user)
                
        
        elif message.content.startswith("T!purge "):
            #botowner only lösch command
            if message.author.id == redbuggamer or message.author.guild_permissions.administrator:
                await message.channel.purge(limit=int(message.content.replace("T!purge ","")))

            else:
                await noperms(message,"Du braucht Admin oder Botowner")

        elif message.content == "T!dice":
            #würfelt
            dice =await message.channel.send(embed=nextcord.Embed(description="Rolling 🎲 "+str(randrange(1,6))))
            for i in range(4):
                await asyncio.sleep(0.75)
                await dice.edit(embed=nextcord.Embed(description="Rolling 🎲 "+str(randint(1,6))))
            await dice.edit(embed=nextcord.Embed(color=0x1f8b4c,description="🎲 "+str(randint(1,6))))

            
        elif message.content == "T!web":
            #link zur website W.I.P.
            await message.channel.send(embed=nextcord.Embed(description="Meine [Website](https://RedBugBot.redbuggamer.repl.co)"))
        elif message.content == "T!tictactoe":
            #startet tictactoe
            await message.channel.send("⠀",view=TicTacToe())
        elif message.content == "T!ping":
            #macht botping
            await message.channel.send(embed=nextcord.Embed(description=f"Latency of `{round(client.latency*1000)}` ms",color=0x3498db))
        elif message.content.startswith("T!send "):
            #sendet was in den channel
            if message.author.id == redbuggamer:
                await message.channel_mentions[0].send(message.content[message.content.find("> ")+1:int(len(message.content))])        
            else:
                await noperms(message,"Du brauchst Botowner")
        elif message.content.startswith("T!embed "):
            await message.channel.trigger_typing()
            arguments = message.content[8:len(message.content)].split("|")
            if (len(arguments) %2) == 0:
                await message.channel.send(embed=nextcord.Embed(description="ERROR Du benötigst mehr input",colour=0xe74c3c))
            else:
                if message.author.avatar == None:
                    customembed = nextcord.Embed(description=arguments[0],color=0x2ecc71).set_author(name=f"{message.author.name}#{message.author.discriminator}")
                else:
                    customembed = nextcord.Embed(description=arguments[0],color=0x2ecc71).set_author(name=f"{message.author.name}#{message.author.discriminator}",icon_url=message.author.avatar.url)
                active = False
                for i in range(int(len(arguments))):
                    if active:
                        customembed.add_field(inline=False,name=arguments[i],value=arguments[i+1])
                        active=False
                    else:
                        active=True
                await message.channel.send(embed=customembed)
        elif message.content.startswith("T!block"):
            blockedusers = somedata.find_one({"_id":ObjectId(blockeduserdocid)})["blockeduserid"]
            if not message.author.id == redbuggamer:
                await noperms(message,"Du brauchst Botowner")
            elif message.mentions[0].id == message.author.id:
                await message.channel.send(embed=nextcord.Embed(description="Block dich nicht selbst!",color=0xe74c3c))
            elif message.author.id == redbuggamer and not message.mentions[0].id == redbuggamer:
                if str(message.mentions[0].id) in blockedusers:
                    somedata.update_one({"_id":ObjectId(blockeduserdocid)},{"$pull":{"blockeduserid":str(message.mentions[0].id)}})
                    
                    await message.channel.send(embed=nextcord.Embed(description=f"<@{message.mentions[0].id}> darf mich wieder benutzen",color=0x2ecc71))
                else:
                    somedata.update_one({"_id":ObjectId(blockeduserdocid)},{"$push":{"blockeduserid":str(message.mentions[0].id)}})
                    await message.channel.send(embed=nextcord.Embed(description=f"<@{message.mentions[0].id}> wurde blockiert",color=0xe74c3c))
        elif message.content.startswith("T!morse "):
            morse = ""
            morse = morse.join(" "+morsealphabet[i.lower()] for i in message.content.replace("T!morse ",""))
            await message.channel.send(embed=nextcord.Embed(description=f"Dein morsecode: `{morse}`",color=0x3498db))
        elif message.content.startswith("T!bind "):
            if message.author.id == redbuggamer:
                if str(message.channel.id) in linkedchannels.find_one({"_id": ObjectId(linkedchannelsmongoid)}):
                    idbefore = linkedchannels.find_one({"_id": ObjectId(linkedchannelsmongoid)})[str(message.channel.id)]
                else:
                    idbefore="None"
                customid = message.content.split()[1]
                if message.content.replace("T!bind ","") == "unbind":
                    linkedchannels.update_one({"_id": ObjectId(linkedchannelsmongoid)},{"$set":{str(message.channel.id):""}})
                    await message.channel.send(embed=nextcord.Embed(description=f"Bindung `{idbefore}` gelöscht",color=0xe74c3c))
                else:
                    linkedchannels.update_one({"_id": ObjectId(linkedchannelsmongoid)},{"$set":{str(message.channel.id):str(message.content.replace("T!bind ",""))}})
                    await message.channel.send(embed=nextcord.Embed(description=f"Bound Exaroton Server `{customid}`",color=0x3498db))
            else:
                await noperms(message,"Du brauchst Botowner")
        elif message.content == "T!bind":
            if str(message.channel.id) in linkedchannels.find_one({"_id": ObjectId(linkedchannelsmongoid)}):
                thatid = linkedchannels.find_one({"_id": ObjectId(linkedchannelsmongoid)})[str(message.channel.id)]
            else:
                thatid="None"
            await message.channel.send(embed=nextcord.Embed(description=f"Channel ist zu Server `{thatid}` gebunden"))

        elif message.content.startswith("T!stats "):
            await message.channel.trigger_typing()
            playerembed = nextcord.Embed(color=0x206694)
            player = message.content.split()[1]
            request = requests.get(url=f"https://api.slothpixel.me/api/players/{player}").json()
            if "error" in request:
                await message.channel.send(embed=nextcord.Embed(color=0xe74c3c,description="Der Player existiert nicht"))
            else:
                uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()["id"]
                # apikey = os.environ["apikey"]
                lastlogin = math.floor(request["last_login"]/1000)
                level = request["level"]
                levelbarpercent= math.ceil((math.floor(level)-level)*-12)
                levelbar=""
                link=request["links"]["DISCORD"]
                rank={"VIP":"[VIP]","VIP_PLUS":"[VIP+]","MVP":"[MVP]","MVP_PLUS":"[MVP+]","MVP_PLUS_PLUS":"[MVP++]",None:""}
                currrank = rank[request["rank"]]
                for i in range(levelbarpercent):
                    levelbar += "<:levelbarful:927896151502495744>"
                for i in range(12-levelbarpercent):
                    levelbar += "<:levelbarempty:927896071798140969>"

                playerembed.set_thumbnail(url=f"https://crafatar.com/renders/body/{uuid}?size=200&default=MHF_Steve&overlay")
                playerembed.set_author(name=f"{currrank} {player}",icon_url=f"https://crafatar.com/avatars/{uuid}?size=200&default=MHF_Steve&overlay")
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
        elif message.content.startswith("T!activity "):
            if message.author.id == redbuggamer:
                if message.content.replace("T!activity ","") == "reset":
                    await client.change_presence(activity=nextcord.Game(random.choice(activitys)),status=nextcord.Status.online)
                    if not statuschange.is_running():
                        statuschange.start()
                else:
                    await client.change_presence(activity=nextcord.Game(message.content.split(" ",1)[1]),status=nextcord.Status.online)
                    if statuschange.is_running():
                        statuschange.stop()
            else:
                await noperms(message,"Du brauchst Botowner")
        elif message.content.startswith("T!guckle") or message.content.startswith("T!google") or message.content.startswith("T!g"):
            myquery = message.content.replace("T!guckle ","").replace("T!google ","").replace("T!g ","").replace(" ","+")
            myurl = f"https://www.google.com/search?q={myquery}"
            myquery = message.content.replace("T!guckle ","").replace("T!google ","").replace("T!g ","")
            await message.channel.send(embed=nextcord.Embed(description=f"[Google: {myquery}]({myurl})",color=0xFEE75C))
        elif message.content.startswith("T!mute"):
            if message.author.guild_permissions.moderate_members or message.author.id == redbuggamer or message.author.guild_permissions.administrator:
                parameter=message.content.split()
                if len(parameter) == 4:
                    theblockeduser = message.mentions[0]
                    muteduration = parameter[2]
                    reason = ""
                    for i in parameter[3:len(parameter)]:
                        reason += i
                    parsed=humanfriendly.parse_timespan(muteduration)
                    await message.mentions[0].edit(timeout=datetime.datetime.utcnow()+datetime.timedelta(hours=1)+datetime.timedelta(seconds=parsed),reason=reason)
                    await message.channel.send(embed=nextcord.Embed(color=0xED4245,description=f"{theblockeduser.mention} wurde für `{muteduration}` gemutet. `Reason {reason}`"))
                else:
                    await message.channel.send(embed=nextcord.Embed(description="Falsches Usage: T!mute @member <time> <reason>",color=0xe74c3c))
            else:
                await noperms(message,"Du brauchst Botowner oder timeout members")
        elif "hi" == message.content.lower().replace("!",""):
            if Hicooldown == 0:
                await message.channel.trigger_typing()
                await asyncio.sleep(random.randrange(1,2))
                await message.channel.send("Hi!")
                Hicooldown =30
                for i in range(Hicooldown):
                    Hicooldown +=-1
                    await asyncio.sleep(1)
        elif message.content == "T!licht":
            if message.author.id == redbuggamer or message.author.id == 381905896546107392 or message.author.id or 772467937436893205:
                embed = nextcord.Embed(description="Liste der Id's",color=0x3498db)
                keller = """Lampe1 : 1
                Flur : 2
                Werkstatt : 4
                Heizungsraum : 13
                West : 20"""
                erdgeschoss = """Bad : 3
                Flur : 6
                Küche : 7
                Wohnzimmer Ost : 8
                Wohnzimmer West : 9
                Esstisch : 15
                Bewegungsmelder Ost : 10
                Bewegungsmelder Haustür : 11"""
                obergeschoß = """Bad : 5
                Bad Spiegel : 17
                Flur : 14
                Schlafzimmer : 16
                Zimmer K : 18
                Zimmer A : 19"""
                dachgeschoß = """Studio : 12"""
                embed.add_field(inline=False,name="`Keller`",value=keller)
                embed.add_field(inline=False,name="`Erdgeschoss`",value=erdgeschoss)
                embed.add_field(inline=False,name="`Obergeschoss`",value=obergeschoß)
                embed.add_field(inline=False,name="`Dachgeschoss`",value=dachgeschoß)
                msg = await message.channel.send(embed=embed)
                def check(m:nextcord.Message):
                    return m.author == message.author and m.content.startswith("T!licht")
                try:
                    await client.wait_for("message",check=check,timeout=20.0)
                except asyncio.TimeoutError:
                    pass
                await msg.delete()
            else:
                await noperms(message,"Du brauchst Botowner")
        elif message.content.startswith("T!licht "):
            if message.author.id == redbuggamer or message.author.id == 381905896546107392 or message.author.id or 772467937436893205:
                args=message.content.split(" ") 
                lichtid=args[1]
                time=humanfriendly.parse_timespan(args[2])
                await message.channel.send(embed=nextcord.Embed(description=f"Licht `{lichtid}` wird in {args[2]} getoggelt",color=0x3498db))
                await asyncio.sleep(time)
                requests.get(f"http://raspberrypi:8088/rest/devices/{lichtid}/methods/1")
                await message.reply(embed=nextcord.Embed(description=f"Licht `{lichtid}` ist jetzt getoggelt",color=0x3498db))
            else:
                await noperms(message,"Du brauchst Botowner")
        
        # other essential stuff here:
        elif message.content.startswith("T!"):
            await message.channel.send(embed=nextcord.Embed(description="Der Command `"+message.content+"` existiert nicht"))
        
    elif message.content.startswith("T!"):
        await message.reply(embed=nextcord.Embed(description="Acces denied - You have been blocked",color=0xe74c3c))
    if message.content.startswith("T!") and not message.content.startswith("T!purge"):
            if not message.guild ==None:
                await message.delete()

@client.event
async def on_member_join(member:nextcord.Member):
    if member.dm_channel == None:
        await member.create_dm()
    if member.avatar== None:
        await member.dm_channel.send(embed=nextcord.Embed(description="Willkommen auf "+str(member.guild)+"!",color=0x206694).set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png"))
    else:
        await member.dm_channel.send(embed=nextcord.Embed(description="Willkommen auf "+str(member.guild)+"!",color=0x206694).set_thumbnail(url=member.avatar))
    print(str(member.name)+" joined "+str(member.guild))

@client.event
async def on_guild_join(guild:nextcord.Guild):
    if guild.owner.dm_channel == None:
        await guild.owner.create_dm()
    await guild.owner.dm_channel.send(embed=nextcord.Embed(description="Hi also ich bin ein bot mach einfach mal `T!help` für eine Liste der commands",color=0x3498db))
#run the bot
client.run(TOKEN)
