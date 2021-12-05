import asyncio
from datetime import datetime
from glob import glob
from logging import disable
from discord import colour
from discord.ui.item import Item
import mouse
import nextcord
from nextcord.client import Client
from nextcord.ui import view
from discord import guild

from pynput.keyboard import Key, Controller as KeyboardController
#from pynput.mouse import Button, Controller as MouseController
import time
from random import randrange
from discord.ui import Button,View
from gc import DEBUG_SAVEALL
import os
from nextcord import *
from discord.colour import Color, Colour
from exaroton import Exaroton
from mouse import press
import tinydb
from dotenv import load_dotenv
load_dotenv()
exa = Exaroton(os.environ["exaroton"])
import discord
from discord.enums import TeamMembershipState

import time
import macro
import random
from typing import List, Mapping
from discord.ext import commands
import discord
from discord.ext import commands
from tinydb import *


# Defines a custom button that contains the logic of the game.
# The ['TicTacToe'] bit is for type hinting purposes to tell your IDE or linter
# what the type of `self.view` is. It is not required.
class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
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
running = True
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
TOKEN = os.environ["token"]
Help = discord.Embed(description="Hi also ich bin ein bot von RedBugGamer#2069",color=0xe74c3c,timestamp=datetime.now())
Help.add_field(name = "`Prefix`",value="Mein prefix ist `T!`",inline=False)
Help.add_field(name = "`T!help`",value="Der Command hilft dir",inline=False)
Help.add_field(name="`T!controll`",value="Ist ein Botowner only command")
Help.add_field(name="`T!say`",value="Sagt etwas",inline=False)
Help.add_field(name="`T!poll`",value="Macht einen vote",inline=False)
Help.add_field(name="`T!dice`",value="Würfelspiele 🎲",inline=False)
Help.add_field(name="`T!startserver`",value="startet den Server",inline=False)
Help.add_field(name="`T!status`",value="Gibt den aktuellen status des servers alle 20 sekunden zurück",inline=False)
Help.add_field(name="`T!web`",value="Gibt den link zu meiner Website",inline=False)
Help.add_field(name="`T!tictactoe`",value="Macht ein TikTakToe game `ohne` commands. Marco",inline=False)
client = discord.Client()
mycolors={
    1:0x1abc9c,
    2:0x11806a,
    3:0x2ecc71, 
    4:0x1f8b4c,
    5:0x3498db,
    6:0x206694,
    7:0x9b59b6,
    8:0x71368a,
}
activitys = ["Welteroberungspläne","Deine Voodopuppe","Langeweile","Editierung der eigenen bot.py","Ließt deine Gedanken","definitiv kein Minecraft Server hacken"]

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    while True:
        await client.change_presence(activity=discord.Game(activitys[randrange(0,len(activitys))]),status=discord.Status.online)
        await asyncio.sleep(random.randrange(15,60))
awaitpoll = False
id = "H6WIxtAqtR1pMJJb"
dice = False
running = False
status=False
@client.event
async def on_message(message):
    global awaitpoll
    global dice
    global status
    global running
    if message.channel.id == 898635630966353950 and not message.content.startswith("T!"):
        exa.command(id="H6WIxtAqtR1pMJJb",command=f'tellraw @a "<{message.author}> {message.content}"')
    if message.author == client.user:
        if awaitpoll:
            awaitpoll = False
            await message.add_reaction("👍")
            await message.add_reaction("👎")
        elif dice:
            dice = False
            for i in range(4):
                await asyncio.sleep(0.75)
                await message.edit(embed=discord.Embed(description="Rolling 🎲 "+str(randrange(1,6))))
            await message.edit(embed=discord.Embed(color=0x1f8b4c,description="🎲 "+str(randrange(1,6))))
        elif status:
            
            status=False
            running = True
            await asyncio.sleep(1)
            while running:
                await asyncio.sleep(15)
                await message.edit(embed=getstatuscolor(exa.get_server(id=id).status,datetime.now()))
            await message.edit(embed=discord.Embed(description="Disabled"))
        return  
    elif message.content == "T!help":
        await message.reply(embed = Help)
        
    elif message.content.startswith("T!say"):
        
         await message.channel.send(message.content.replace("T!say",""))
         
    elif message.content.startswith("T!poll"):
        
        awaitpoll = True
        if message.author.avatar == None:
            await message.channel.send(embed=discord.Embed(color=0xe74c3c,title="Poll",description=message.content.replace("T!poll",""),timestamp=datetime.now()).set_author(name=message.author))
        else:
            await message.channel.send(embed=discord.Embed(color=0xe74c3c,title="Poll",description=message.content.replace("T!poll",""),timestamp=datetime.now()).set_author(name=message.author,icon_url=message.author.avatar.url))
    elif message.content.startswith("T!controll "):
        if message.author.id == 772386889817784340:
            if message.content.replace("T!controll ","") == "hotspot":
                macro.hotspot()
                await message.reply(embed=discord.Embed(description="Hotspot eingeschalten"))
            elif message.content.replace("T!controll ","") == "shutdown":
                await message.reply(embed=discord.Embed(description="Ausschalten"))
                macro.shutdown()
            elif message.content.replace("T!controll ","").startswith("message"):
                await message.reply(embed=discord.Embed(description="Du hast `"+message.content.replace("T!controll","").replace(" message ","")+"` gesendet"))
                macro.message(message.content.replace("T!controll","").replace(" message",""),15)
            elif message.content.replace("T!controll ","") == "restart":
                await message.reply(embed=discord.Embed(description="Neustarten"))
                macro.restart()
            elif message.content.replace("T!controll ","") == "gamer":
                macro.win_r("C:/Users/RedBugGamer/AppData/Roaming/MultiMC/Multimc.exe")
                time.sleep(2)
                macro.press(Key.enter)
                await message.channel.send(embed=discord.Embed(description="Aktuelle instanz gestartet"))
            
        else:
            await message.reply(embed=discord.Embed(description="Du hast keine Berechtigung dazu"))
    elif message.content.startswith("T!purge "):
        if message.author.id == 772386889817784340:
           await message.channel.purge(limit=int(message.content.replace("T!purge ",""))+1)

        else:
            await message.reply(embed=discord.Embed(description="Du hast keine Berechtigung dazu"))
    elif message.content == "T!dice":
        dice=True
        await message.channel.send(embed=discord.Embed(description="Rolling 🎲 "+str(randrange(1,6))))

    elif message.content == "T!startserver":
        exa.start(id="H6WIxtAqtR1pMJJb")
        await message.reply(embed=discord.Embed(description="Server gestartet"))
    elif message.content == "T!status":
        
        status=True
        running = True
        await message.reply(view=stopstatus(),embed=getstatuscolor(exa.get_server(id=id).status,datetime.now()))
        
    elif message.content == "T!web":
        await message.reply(embed=discord.Embed(description="Meine [Website](https://RedBugBot-in-python.redbuggamer.repl.co)"))
    elif message.content == "T!tictactoe":
        await message.channel.send("⠀",view=TicTacToe())
    
    
        
    

    elif message.content.startswith("T!"):
        await message.reply(embed=discord.Embed(description="Der Command `"+message.content+"` existiert nicht"))
    if message.content.startswith("T!"):
        await message.delete()


client.run(TOKEN)
