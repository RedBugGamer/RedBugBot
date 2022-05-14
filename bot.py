# -*- coding: utf-8 -*-
# imports
import asyncio
import datetime
import math
import os
import random
import sqlite3
from random import randint, randrange
from pistonapi import PistonAPI
import humanfriendly
import nextcord
import requests
from dotenv import load_dotenv
from exaroton import Exaroton
from nextcord.ext import tasks
from views import *
from utilitie import *
from vars import *

import secretlib

# load .env filw
load_dotenv()

# define important variables

exa = Exaroton(os.environ["exaroton"])
TOKEN = os.environ["token"]
running = False
status = False
developer_mode = os.environ["developer_mode"] == "True"
# new database


cursor.execute(
    "CREATE TABLE if not exists polls (id int PRIMARY KEY, up int, down int, owner int, voted TEXT, expires DATE)"
)
cursor.execute(
    "CREATE TABLE if not exists userdata (id int PRIMARY KEY, blocked bool)")
cursor.execute(
    "CREATE TABLE if not exists exaroton (serverid string PRIMARY KEY, channel int)"
)
cursor.execute(
    "CREATE TABLE if not exists embeds (id int PRIMARY KEY, json string, expires DATE)"
)

zen = "https://zenquotes.io/api/random"
sadwords = ["demotivatet", "traurig", "demotiviert", "sad"]
morsealphabet = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    ".": ".-.-.-",
    "?": "..--..",
    ",": "--..--",
    " ": "",
}
Hicooldown = 0
startuptime = datetime.datetime.now()
githubcooldown = 180
temp = []
for user in cursor.execute("SELECT * FROM userdata WHERE blocked = true"):
    temp.append(user[1])
blockedusers = temp
del temp

chatboton = False


def user_in_db(id: int):
    if (
        len(cursor.execute("SELECT * FROM userdata WHERE id = ?", (id,)).fetchall())
        == 0
    ):
        cursor.execute("INSERT INTO userdata VALUES(?,?)", (id, False))
        connection.commit()


registeredcommands = {
    "help": "Zeigt dir diese Einbettung `Usage: T!help <command>`",
    "ping": "Gibt meinen ping `Usage: T!ping`",
    "block": "Blockiert einen User sodass der den bot nicht nutzen kann `Usage: T!block <@ member>`",
    "send": "sendet etwas in kanal x `Usage: T!send <# channel> <message>`",
    "say": "sagt etwas als ich `Usage: T!say <message>`",
    "activität": "Setzt meine Bot Aktivität `Usage: T!activity <str>`",
    "dice": "Würfelt für dich `Usage: T!dice`",
    "tictactoe": "Startet ein TikTakToe game `Usage: T!tictactoe`",
    "google": "googelt was für dich `Usage: T!google/T!g/T!guckle`",
    "morse": "gibt die morsetext `Usage: T!morse <text>`",
    "embed": "Sendet eine Einbettung `Usage: T!embed wert1=parameter1;wer2=parameter2` oder `T!embed`",
    "stats": "Gibt die Hypixel stats `Usage: T!stats <player>`",
    "poll": "Macht eine Umfrage `Usage: T!poll <Frage>`",
    "bind": 'Bindet eine [Exaroton](https://exaroton.com) Server id zum channel `Usage: T!bind <serverid/"unbind">`',
    "mute": "Mutet einen User für x minuten `Usage: T!mute @member <Zeit>`",
    "reboot": "Startet mich neu `Usage: T!reboot`",
    "licht": "toggelt licht mit id x `Usage: T!licht <id> <time>`",
    "web": "Gibt dir den link zu meiner Website `Usage: T!web`",
    "uptime": "Gibt die zeit zurück, die ich Online war `Usage: T!uptime`",
    "chatbot": "Imitiert ein Gespräch mit mir `Usage: T!chatbot [message1|message2|...]`",
    "schiffetot": "startet ein Schiffeversenken Spiel `Usage: T!schiffetot`",
    "exec": "Führt den beiliegenden Python code direkt im Bot aus `Usage: T!exec <code>`",
    "code": "Führt den beiliegenden Python code in einer Sandbox aus `Usage: T!code ```<code>```",
}


@tasks.loop(minutes=4)
async def statuschange():
    await client.change_presence(
        activity=nextcord.Game(random.choice(activitys)), status=nextcord.Status.online
    )


@tasks.loop(minutes=1)
async def refreshblockedplayers():
    global blockedusers
    temp = []
    for user in cursor.execute("SELECT * FROM userdata WHERE blocked = true"):
        temp.append(user[1])
    blockedusers = temp


@tasks.loop(count=1, seconds=1)
async def cooldowngithub():
    global githubcooldown
    for i in range(githubcooldown):
        await asyncio.sleep(1)
        githubcooldown -= 1


@tasks.loop(hours=1)
async def garbagecollection():
    # delete all expired polls
    garbagenum = 0
    garbagenum += len(
        cursor.execute(
            "SELECT * FROM polls WHERE expires < ?", (datetime.datetime.now(),)
        ).fetchall()
    )
    garbagenum += len(
        cursor.execute(
            "SELECT * FROM embeds WHERE expires < ?", (datetime.datetime.now(),)
        ).fetchall()
    )
    print("[" + str(datetime.datetime.now()) +
          f"] collecting {garbagenum} garbage")
    cursor.execute("delete from polls where expires < ?",
                   (datetime.datetime.now(),))
    cursor.execute("delete from embeds where expires < ?",
                   (datetime.datetime.now(),))
    connection.commit()


# Bot activities
activitys = [
    "Welteroberungspläne",
    "Deine Voodopuppe",
    "Langeweile",
    "Editierung der eigenen bot.py",
    "Ließt deine Gedanken",
    "definitiv kein Minecraft Server hacken",
    "Fresse Elektrizität",
    "Testet virtuelle Synapsen",
    "Beobachtet Discordserver",
    "Training neural network",
]
# on ready/Change bot activitie


@client.event
async def on_ready():
    if not developer_mode:
        if not statuschange.is_running():
            statuschange.start()
    else:
        await client.change_presence(
            activity=nextcord.Game("Under Maintence"), status=nextcord.Status.idle
        )
    if not refreshblockedplayers.is_running():
        refreshblockedplayers.start()
    if not cooldowngithub.is_running():
        cooldowngithub.start()
    if not garbagecollection.is_running():
        garbagecollection.start()
    client.add_view(mypoll())
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_disconnect():
    time = datetime.datetime.now()
    print(f"[{time}] disconnectet")


# commands/ingame chat
@client.event
async def on_message(message: nextcord.Message):
    if message.channel.id == 917083417127055470:
        print("Rebooting in", githubcooldown)
        await asyncio.sleep(githubcooldown)
        await client.change_presence(
            status=nextcord.Status.dnd, activity=nextcord.Game("Rebooting")
        )
        os.system("./mystartupscript")
        quit()

    if message.content == "T!reboot":
        if message.author.id == redbuggamer:
            await message.channel.trigger_typing()
            await client.change_presence(
                status=nextcord.Status.dnd, activity=nextcord.Game("Rebooting")
            )
            if githubcooldown != 0:
                await message.channel.send(
                    embed=nextcord.Embed(
                        description=f"awaiting restart in {githubcooldown} seconds"
                    )
                )
            await message.delete()
            print("Rebooting")
            await asyncio.sleep(githubcooldown)
            await message.channel.send(embed=nextcord.Embed(description="RESTARTING"))
            os.system("./mystartupscript")
            quit()
        else:
            noperms(message, "Du brauchst Botowner")
    if (
        not message.author.bot
        and len(
            cursor.execute(
                "SELECT * FROM exaroton where channel = ?", (message.channel.id,)
            ).fetchall()
        )
        and not message.content.startswith("T!")
    ):
        exa.command(
            cursor.execute(
                "SELECT * FROM exaroton where channel = ?", (message.channel.id,)
            ).fetchall()[0][0],
            f'tellraw @a "<{message.author}> {message.clean_content}"',
        )
    # make global variables
    global chatboton
    global status
    global running
    global Hicooldown
    global blockedusers
    # block users
    if not message.author.id in blockedusers:
        if (
            developer_mode
            and message.content.startswith("T!")
            and not message.author.id == redbuggamer
        ):
            await message.reply(
                embed=nextcord.Embed(
                    color=nextcord.Color.red(),
                    description="Aktuell werde ich weiter programmiert.\nManche Befehle werden kaum oder gar nicht funktionieren.",
                    title="Warnung",
                ),
                delete_after=10,
            )
        delete = True
        # await message from self
        if message.author == client.user:
            if not message.content.startswith("T!"):
                return
        if message.content == "T!help":
            # zeigt help menu
            Help = nextcord.Embed(
                description="Hi also ich bin ein bot von RedBugGamer#2069",
                color=0xE74C3C,
                timestamp=datetime.datetime.utcnow(),
            )
            Help.set_author(name=client.user, icon_url=client.user.avatar.url)
            Help.add_field(
                name="Prefix", value="Mein prefix ist `T!`", inline=False)
            Help.add_field(
                name="Basic Commands",
                value="`T!help`,`T!ping`,`T!web`,`T!uptime`",
                inline=False,
            )
            Help.add_field(
                name="Botowner",
                value="`T!block`,`T!send`,`T!activity`,`T!reboot`,`T!bind`,T!exec",
                inline=False,
            )
            Help.add_field(
                name="Fun stuff",
                value="`T!dice`,`T!tictactoe`,`T!schiffetot`",
                inline=False,
            )
            Help.add_field(
                name="Sinnloses Zeug", value="`T!morse`,`T!google`", inline=False
            )
            Help.add_field(
                name="Advanced",
                value="`T!embed`,`T!stats`,`T!poll`,`T!chatbot`",
                inline=False,
            )
            Help.add_field(name="Admin", value="`T!mute`", inline=False)
            await message.channel.send(embed=Help)
        elif message.content.startswith("T!help "):
            query = message.content.split()[1].replace("T!", "", 1)
            if query in registeredcommands:
                await message.channel.send(
                    embed=nextcord.Embed(
                        title="T!" + query,
                        description=registeredcommands[query],
                        color=0xE74C3C,
                    )
                )
            else:
                await message.channel.send(
                    embed=nextcord.Embed(
                        title="T!" + query,
                        description="Der Command existiert nicht",
                        color=0xE74C3C,
                    )
                )

        elif message.content.startswith("T!say"):
            if message.author.id == redbuggamer:
                # sagt string
                await message.channel.send(
                    message.content.replace("T!say", "", 1),
                    embeds=message.embeds,
                    tts=message.tts,
                )
            else:
                await noperms(message, "Du brauchst Botowner")

        elif message.content.startswith("T!poll"):

            await message.channel.trigger_typing()
            if await check_developer_mode_msg(message):
                delete = False
                await message.delete()
                return
            # macht einen poll
            if message.author.avatar == None:
                # check avatar exists
                poll = await message.channel.send(
                    embed=nextcord.Embed(
                        color=0xE74C3C,
                        title="Poll",
                        description=message.content.replace("T!poll", "", 1),
                        timestamp=datetime.datetime.now(),
                    ).set_author(name=message.author),
                    view=mypoll(),
                )
            else:
                poll = await message.channel.send(
                    embed=nextcord.Embed(
                        color=0xE74C3C,
                        title="Poll",
                        description=message.content.replace("T!poll", "", 1),
                        timestamp=datetime.datetime.now(),
                    ).set_author(
                        name=message.author, icon_url=message.author.avatar.url
                    ),
                    view=mypoll(),
                )
            t = datetime.datetime.now()
            cursor.execute(
                "INSERT into polls VALUES (?,?,?,?,?,?)",
                (
                    poll.id,
                    0,
                    0,
                    message.author.id,
                    "",
                    t + datetime.timedelta(days=30),
                ),
            )
            connection.commit()

        elif message.content.startswith("T!purge "):
            # botowner only lösch command
            if (
                message.author.id == redbuggamer
                or message.author.guild_permissions.administrator
            ):
                delete = False
                await message.channel.purge(
                    limit=int(message.content.replace("T!purge ", ""))
                )

            else:
                await noperms(message, "Du braucht Admin oder Botowner")

        elif message.content == "T!dice":
            # würfelt
            dice = await message.channel.send(
                embed=nextcord.Embed(
                    description="Rolling 🎲 " + str(randrange(1, 6)))
            )
            for i in range(4):
                await asyncio.sleep(0.75)
                await dice.edit(
                    embed=nextcord.Embed(
                        description="Rolling 🎲 " + str(randint(1, 6)))
                )
            await dice.edit(
                embed=nextcord.Embed(
                    color=0x1F8B4C, description="🎲 " + str(randint(1, 6))
                )
            )

        elif message.content == "T!web":
            # link zur website W.I.P.
            await message.channel.send(
                embed=nextcord.Embed(
                    description="Aktuell keine website",
                    color=nextcord.Colour.blue(),
                )
            )
        elif message.content == "T!tictactoe":
            # startet tictactoe
            await message.channel.send("⠀", view=TicTacToe())
        elif message.content == "T!ping":
            # macht botping
            await message.channel.send(
                embed=nextcord.Embed(
                    description=f"Latency of `{round(client.latency*1000)}` ms",
                    color=0x3498DB,
                )
            )
        elif message.content.startswith("T!send "):
            # sendet was in den channel
            if message.author.id == redbuggamer:
                await message.channel_mentions[0].send(
                    message.content.replace("T!send ", "", 1)
                )
            else:
                await noperms(message, "Du brauchst Botowner")
        elif message.content.startswith("T!embed"):
            await message.channel.trigger_typing()
            d = {
                "titel": "",
                "description": "Description is None",
                "color": "",
                "footer": "",
                "image": "",
                "thumbnail": "",
            }
            colors = {
                "red": nextcord.Color.red(),
                "orange": nextcord.Color.orange(),
                "yellow": nextcord.Color.yellow(),
                "green": nextcord.Color.green(),
                "blue": nextcord.Color.blue(),
                "white": nextcord.Color.from_rgb(255, 255, 255),
                "black": nextcord.Color.from_rgb(0, 0, 0),
                "": nextcord.Embed.Empty,
            }
            for key_value in (
                message.content.replace("T!embed", "", 1).strip().split(";")
            ):
                x = key_value.split("=")
                if len(x) == 2:
                    key = x[0].strip().lower()
                    value = x[1].strip()
                    d[key] = value
            if d["color"] in colors:
                e = nextcord.Embed(
                    title=d["titel"],
                    description=d["description"],
                    color=colors[d["color"]],
                )
                e.set_author(
                    name=message.author, icon_url=message.author.display_avatar.url
                )
                e.set_footer(text=d["footer"])
                e.set_image(url=d["image"])
                e.set_thumbnail(url=d["thumbnail"])

                description = nextcord.Embed(
                    title="Erklärung", color=nextcord.Color.blue()
                )
                description.add_field(
                    name="titel",
                    value="Der Titel der Einbettung",
                    inline=False,
                )
                description.add_field(
                    name="description",
                    value="Die Beschreibung der Einbettung",
                    inline=False,
                )
                description.add_field(
                    name="color",
                    value="Setzt die Farbe der Einbettung",
                    inline=False,
                )
                description.add_field(
                    name="color",
                    value="Setzt die Farbe der Einbettung\nAlle Farben:\nred\norange\nyellow\ngreen\nblue\nwhite\nblack",
                    inline=False,
                )
                description.add_field(
                    name="footer",
                    value="Der Footer text der Einbettung",
                    inline=False,
                )
                description.add_field(
                    name="image",
                    value="Der Link zum Bild",
                    inline=False,
                )
                description.add_field(
                    name="thumbnail",
                    value="Der Link zum Titelbild",
                    inline=False,
                )
                description_msg = await message.reply(embed=description)
                await message.reply(
                    embed=e,
                    view=EmbedBuilder(
                        e.to_dict(), message.author.id, description_msg),
                )
            else:
                await message.reply(
                    embed=nextcord.Embed(
                        title="Fehler",
                        description="Du musst eine korrekte Farbe angeben",
                    )
                )
        elif message.content.startswith("T!deploy "):
            if await check_developer_mode_msg(message): return
            try:
                id = message.content.split(" ")[1]
                element = cursor.execute(
                    "SELECT * FROM embeds where id = ?", (int(id),)
                ).fetchall()[0]
                cursor.execute(
                    "DELETE FROM embeds WHERE id = ?", (element[0],))
                connection.commit()
                await message.channel.send(
                    embed=nextcord.Embed.from_dict(json.loads(element[1]))
                )
            except IndexError:
                await message.reply(
                    "Du musst eine korrekte Id angeben, oder du bist 10 Minuten zu spät",
                    delete_after=10,
                )
        elif message.content.startswith("T!block"):
            user_in_db(message.mentions[0].id)
            if not message.author.id == redbuggamer:
                await noperms(message, "Du brauchst Botowner")
            elif message.mentions[0].id == message.author.id:
                await message.channel.send(
                    embed=nextcord.Embed(
                        description="Block dich nicht selbst!", color=0xE74C3C
                    )
                )
            elif (
                message.author.id == redbuggamer
                and not message.mentions[0].id == redbuggamer
            ):
                # print(cursor.execute("SELECT * FROM userdata WHERE id = ?",(message.mentions[0].id,)).fetchall())
                if cursor.execute(
                    "SELECT * FROM userdata WHERE id = ?", (
                        message.mentions[0].id,)
                ).fetchall()[0][1]:
                    cursor.execute("UPDATE userdata SET blocked = false")
                    await message.channel.send(
                        embed=nextcord.Embed(
                            description=f"<@{message.mentions[0].id}> darf mich wieder benutzen",
                            color=nextcord.Color.green(),
                        )
                    )
                else:
                    cursor.execute("UPDATE userdata SET blocked = true")
                    await message.channel.send(
                        embed=nextcord.Embed(
                            description=f"<@{message.mentions[0].id}> darf mich leider nicht mehr verwenden",
                            color=nextcord.Color.red(),
                        )
                    )
                connection.commit()
        elif message.content.startswith("T!morse "):
            morse = ""
            morse = morse.join(
                " " + morsealphabet[i.lower()]
                for i in message.content.replace("T!morse ", "")
            )
            await message.channel.send(
                embed=nextcord.Embed(
                    description=f"Dein morsecode: `{morse}`", color=0x3498DB
                )
            )
        elif message.content.startswith("T!bind "):
            if message.author.id == redbuggamer:
                if (
                    len(
                        cursor.execute(
                            "SELECT * FROM exaroton where channel = ?",
                            (message.channel.id,),
                        ).fetchall()
                    )
                    >= 1
                ):
                    idbefore = cursor.execute(
                        "SELECT * From exaroton where channel = ?",
                        (message.channel.id,),
                    ).fetchall()[0][0]
                else:
                    idbefore = "None"
                customid = message.content.split()[1]
                if message.content.replace("T!bind ", "") == "unbind":
                    cursor.execute(
                        "DELETE from exaroton where channel = ?", (
                            message.channel.id,)
                    )
                    await message.channel.send(
                        embed=nextcord.Embed(
                            description=f"Bindung `{idbefore}` gelöscht", color=0xE74C3C
                        )
                    )
                else:
                    if (
                        len(
                            cursor.execute(
                                "SELECT * FROM exaroton where serverid = ?", (customid,)
                            ).fetchall()
                        )
                        == 0
                    ):
                        cursor.execute(
                            "INSERT INTO exaroton VALUES (?,?)",
                            (customid, message.channel.id),
                        )
                    else:
                        cursor.execute(
                            "UPDATE exaroton SET serverid = ? where channel = ?",
                            (customid, message.channel.id),
                        )
                    await message.channel.send(
                        embed=nextcord.Embed(
                            description=f"Bound Exaroton Server `{customid}`",
                            color=0x3498DB,
                        )
                    )
                connection.commit()
            else:
                await noperms(message, "Du brauchst Botowner")
        elif message.content == "T!bind":
            if (
                len(
                    cursor.execute(
                        "SELECT * FROM exaroton where channel = ?",
                        (message.channel.id,),
                    ).fetchall()
                )
                >= 1
            ):
                thatid = cursor.execute(
                    "SELECT * FROM exaroton where channel = ?", (message.channel.id,)
                ).fetchall()[0][0]
            else:
                thatid = "None"
            await message.channel.send(
                embed=nextcord.Embed(
                    description=f"Channel ist zu Server `{thatid}` gebunden"
                )
            )

        elif message.content.startswith("T!stats "):
            await message.channel.trigger_typing()
            playerembed = nextcord.Embed(color=0x206694)
            player = message.content.split()[1]
            request = requests.get(
                url=f"https://api.slothpixel.me/api/players/{player}"
            ).json()
            if "error" in request:
                await message.channel.send(
                    embed=nextcord.Embed(
                        color=0xE74C3C, description="Der Player existiert nicht"
                    )
                )
            else:
                uuid = requests.get(
                    f"https://api.mojang.com/users/profiles/minecraft/{player}"
                ).json()["id"]
                # apikey = os.environ["apikey"]
                lastlogin = math.floor(request["last_login"] / 1000)
                level = request["level"]
                levelbarpercent = math.ceil((math.floor(level) - level) * -12)
                levelbar = ""
                link = request["links"]["DISCORD"]
                rank = {
                    "VIP": "[VIP]",
                    "VIP_PLUS": "[VIP+]",
                    "MVP": "[MVP]",
                    "MVP_PLUS": "[MVP+]",
                    "MVP_PLUS_PLUS": "[MVP++]",
                    None: "",
                }
                currrank = rank[request["rank"]]
                for i in range(levelbarpercent):
                    levelbar += "<:levelbarful:927896151502495744>"
                for i in range(12 - levelbarpercent):
                    levelbar += "<:levelbarempty:927896071798140969>"

                playerembed.set_thumbnail(
                    url=f"https://crafatar.com/renders/body/{uuid}?size=200&default=MHF_Steve&overlay"
                )
                playerembed.set_author(
                    name=f"{currrank} {player}",
                    icon_url=f"https://crafatar.com/avatars/{uuid}?size=200&default=MHF_Steve&overlay",
                )
                playerembed.add_field(inline=False, name="`uuid`", value=uuid)
                playerembed.add_field(
                    inline=False, name="`Last Login`", value=f"<t:{lastlogin}:F>"
                )
                playerembed.add_field(
                    inline=False, name="`Version`", value=request["mc_version"]
                )
                if request["online"]:
                    playerembed.add_field(
                        inline=False, name="`Online`", value="🟩")
                else:
                    playerembed.add_field(
                        inline=False, name="`Offline`", value="🔲")
                playerembed.add_field(
                    inline=False, name="`Discord`", value=f"{link}")
                playerembed.add_field(
                    inline=False,
                    name=f"`Level {math.floor(level)}`",
                    value=f"{levelbar}",
                )
                await message.channel.send(embed=playerembed)
        elif message.content.startswith("T!activity "):
            if message.author.id == redbuggamer:
                if message.content.replace("T!activity ", "") == "reset":
                    await client.change_presence(
                        activity=nextcord.Game(random.choice(activitys)),
                        status=nextcord.Status.online,
                    )
                    if not statuschange.is_running():
                        statuschange.start()
                else:
                    await client.change_presence(
                        activity=nextcord.Game(
                            message.content.split(" ", 1)[1]),
                        status=nextcord.Status.online,
                    )
                    if statuschange.is_running():
                        statuschange.stop()
            else:
                await noperms(message, "Du brauchst Botowner")
        elif (
            message.content.startswith("T!guckle")
            or message.content.startswith("T!google")
        ):
            myquery = (
                message.content.replace("T!guckle ", "")
                .replace("T!google ", "")
                .replace("T!g ", "")
                .replace(" ", "+")
            )
            myurl = f"https://www.google.com/search?q={myquery}"
            await message.channel.send(
                embed=nextcord.Embed(
                    description=f"[Google: {myquery}]({myurl})", color=0xFEE75C
                )
            )
        elif message.content.startswith("T!mute"):
            if (
                message.author.guild_permissions.moderate_members
                or message.author.id == redbuggamer
                or message.author.guild_permissions.administrator
            ):
                parameter = message.content.split()
                if len(parameter) == 4:
                    theblockeduser = message.mentions[0]
                    muteduration = parameter[2]
                    reason = ""
                    for i in parameter[3: len(parameter)]:
                        reason += i
                    parsed = humanfriendly.parse_timespan(muteduration)
                    await message.mentions[0].edit(
                        timeout=datetime.datetime.utcnow()
                        + datetime.timedelta(hours=1)
                        + datetime.timedelta(seconds=parsed),
                        reason=reason,
                    )
                    await message.channel.send(
                        embed=nextcord.Embed(
                            color=0xED4245,
                            description=f"{theblockeduser.mention} wurde für `{muteduration}` gemutet. `Reason {reason}`",
                        )
                    )
                else:
                    await message.channel.send(
                        embed=nextcord.Embed(
                            description="Falsches Usage: T!mute @member <time> <reason>",
                            color=0xE74C3C,
                        )
                    )
            else:
                await noperms(message, "Du brauchst Botowner oder timeout members")
        elif "hi" == message.content.lower().replace("!", ""):
            if Hicooldown == 0 and not chatboton:
                await message.channel.trigger_typing()
                await asyncio.sleep(random.randrange(1, 2))
                await message.channel.send("Hi!")
                Hicooldown = 30
                for i in range(Hicooldown):
                    Hicooldown += -1
                    await asyncio.sleep(1)
        elif message.content == "T!licht":
            if (
                message.author.id == redbuggamer
                or message.author.id == 381905896546107392
                or message.author.id == 772467937436893205
            ):
                embed = secretlib.haus()
                msg = await message.channel.send(embed=embed)

                def check(m: nextcord.Message):
                    return m.author == message.author and m.content.startswith(
                        "T!licht"
                    )

                try:
                    await client.wait_for("message", check=check, timeout=20.0)
                except asyncio.TimeoutError:
                    pass
                await msg.delete()
            else:
                await noperms(message, "Du brauchst Botowner")
        elif message.content.startswith("T!licht "):
            if (
                message.author.id == redbuggamer
                or message.author.id == 381905896546107392
                or message.author.id
                or 772467937436893205
            ):
                args = message.content.split(" ")
                if int(len(args)) == 3:
                    lichtid = args[1]
                    time = humanfriendly.parse_timespan(args[2])
                    await message.channel.send(
                        embed=nextcord.Embed(
                            description=f"Licht `{lichtid}` wird in {args[2]} getoggelt",
                            color=0x3498DB,
                        )
                    )
                    await asyncio.sleep(time)
                    requests.get(
                        f"http://raspberrypi:8088/rest/devices/{lichtid}/methods/1"
                    )
                    await message.reply(
                        embed=nextcord.Embed(
                            description=f"Licht `{lichtid}` ist jetzt getoggelt",
                            color=0x3498DB,
                        )
                    )
                elif int(len(args)) == 2:
                    await message.channel.send(
                        f"Lichtschalter für Licht {args[1]}",
                        view=lichtschalter(args[1]),
                    )
            else:
                await noperms(message, "Du brauchst Botowner")
        elif message.content == "T!uptime":
            m = await message.channel.send(
                embed=nextcord.Embed(
                    title="Uptime",
                    description=str(datetime.datetime.now() - startuptime),
                )
            )
        elif any(word in message.content.lower() for word in sadwords):
            await message.channel.trigger_typing()
            await asyncio.sleep(2)
            request = requests.get(zen).json()
            await message.reply(f"""{request[0]["q"]}\n   -{request[0]["a"]}""")
        elif message.content == "T!chatbot":
            delete = False
            if message.author.id == 772386889817784340:
                chatboton = True
            await secretlib.chatbot(message, client)
            if message.author.id == 772386889817784340:
                chatboton = False
        elif message.content.startswith("T!chatbot "):
            if message.author.id == redbuggamer:
                secretlib.verlauf = message.content.replace("T!chatbot ", "", 1).split(
                    "|"
                )
        elif message.content == "T!schiffetot":
            await message.channel.send("temp", view=Schiffetot())
        elif message.content.startswith("T!exec "):
            if message.author.id == redbuggamer:
                mytimestamp = datetime.datetime.now()
                executet = "None"
                code = message.content[7:]
                try:
                    executet = exec(code, globals(), locals())
                    doneafter = str(datetime.datetime.now() - mytimestamp)
                    await message.channel.send(
                        embed=nextcord.Embed(title="Done nach " + doneafter)
                    )

                except Exception as e:
                    await message.channel.send(
                        embed=nextcord.Embed(
                            title="Error",
                            description=str(e),
                            color=nextcord.Color.red(),
                        )
                    )

            else:
                await noperms(message, "Du brauchst Botowner")
        elif message.content == "T!quit":
            if message.author.id == redbuggamer:
                await message.channel.send("@everyone ")
                await message.channel.send("Bye Bye! Hab kein bock mehr auf euch")
                await message.channel.send("*Leaves Server*")
                await message.guild.leave()
            else:
                await noperms(message, "Du brauchst Botowner")

        elif message.content.startswith("T!code "):
            a = message.content.split("```")
            if len(a) == 3:
                code = a[1]
                code = code.strip("python")
                response = PistonAPI().execute("python", "3.10.0", code)
            else:
                response = "Sorry, aber du must code angeben"
            embed = nextcord.Embed(
                color=nextcord.Color.blue(),
                title="Code execution",
                description=f"```{response}```",
            )
            embed.set_footer(
                text="Powered by https://github.com/engineer-man/piston")
            await message.channel.send(embed=embed)
        elif message.content.startswith("T!get"):
            match message.content.split()[1]:
                case "id":
                    user = message.content.split(" ", 1)[1]
                    for guild in client.guilds:
                        user = guild.get_member_named(user)
                        if user != None:
                            try:
                                id = user.id
                                break
                            except Exception:
                                pass
                    await message.channel.send(embed=nextcord.Embed(description=f"Die id von {user} ist `{id}`"))
                case "name":
                    id_str = message.content.split(" ")[2]
                    id: nextcord.User = client.get_user(int(message.content.split(" ")[2]))
                    name = id
                    await message.channel.send(embed=nextcord.Embed(description=f"Der name von {id_str} ist {id}"))
            # other essential stuff here:
        elif message.content.startswith("T!"):
            await message.channel.send(
                embed=nextcord.Embed(
                    description="Der Command `" + message.content + "` existiert nicht"
                )
            )
    elif message.content.startswith("T!"):
        await message.reply(
            embed=nextcord.Embed(
                description="Acces denied - You have been blocked", color=0xE74C3C
            )
        )
    if message.content.startswith("T!") and delete:
        if not message.guild == None:
            await message.delete()


@client.event
async def on_member_join(member: nextcord.Member):
    if member.dm_channel == None:
        await member.create_dm()
    await member.dm_channel.send(
        embed=nextcord.Embed(
            description="Hey "
            + member.mention
            + "! Willkommen auf "
            + str(member.guild)
            + "!",
            color=0x206694,
        ).set_thumbnail(url=member.guild.icon.url)
    )
    print(str(member.name) + " joined " + str(member.guild))


@client.event
async def on_guild_join(guild: nextcord.Guild):
    if guild.owner.dm_channel == None:
        await guild.owner.create_dm()
    await guild.owner.dm_channel.send(
        embed=nextcord.Embed(
            description="Hi also ich bin ein bot mach einfach mal `T!help` für eine Liste der commands",
            color=0x3498DB,
        )
    )


@client.event
async def on_message_delete(message: nextcord.Message):
    if message.author == client.user:
        cursor.execute("DELETE FROM polls WHERE id = ?", (message.id,))
        connection.commit()


# run the bot
client.run(TOKEN)
