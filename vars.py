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
