import datetime
from dotenv import load_dotenv
import os
import nextcord

redbuggamer = 772386889817784340

load_dotenv()
developer_mode = os.environ["developer_mode"] == "True"
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
    " ": "",
}

zen = "https://zenquotes.io/api/random"
sadwords = ["demotivatet", "traurig", "demotiviert", "sad"]
Hicooldown = 0
startuptime = datetime.datetime.now()
githubcooldown = 180
chatboton = False
