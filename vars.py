import datetime
from dotenv import load_dotenv
import os
import nextcord
import sqlite3

redbuggamer = 772386889817784340

load_dotenv()
developer_mode = os.environ["developer_mode"] == "True"
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

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
cursor.execute(
    "CREATE TABLE if not exists errors (id int PRIMARY KEY, message String, errormsg String, user String, expires DATE)"
)

intents = nextcord.Intents.default()
intents.members = True
intents.all()
client = nextcord.Client(intents=intents)
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
    " ": " ",
}

zen = "https://zenquotes.io/api/random"
sadwords = ["demotivatet", "traurig", "demotiviert", "sad"]
Hicooldown = 0
startuptime = datetime.datetime.now()
githubcooldown = 180
chatboton = False

temp = []
for user in cursor.execute("SELECT * FROM userdata WHERE blocked = true"):
    temp.append(user[1])
blockedusers = temp
del temp