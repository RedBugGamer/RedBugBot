import datetime
import math
from dotenv import load_dotenv
import nextcord
import sqlite3
import os
from vars import client
import secretlib
import utilitie

load_dotenv()
developer_mode = os.environ["developer_mode"] == "True"
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
redbuggamer = 772386889817784340

async def check_developer_mode_msg(message:nextcord.Message):
    if developer_mode and not message.author.id == redbuggamer:
        await message.reply("Sorry, aber der command ist während developing nicht enabled")
        return True
    return False
async def check_developer_mode_interaction(interaction:nextcord.Interaction):
    if developer_mode and not interaction.user.id == redbuggamer:
        await interaction.response.send_message("Sorry, aber dieses Feature ist während developing nicht enabled",ephemeral=True)
        return True
    return False
def get_dc_timestamp(datetime:datetime.datetime,type:str="F"):
    time = math.floor(datetime.timestamp())
    return f"<t:{time}:{type}>"
async def noperms(obj: nextcord.Message, neededpermission=""):
    await obj.reply(
        embed=nextcord.Embed(
            title="Du hast keine Berechtigung dazu",
            description=neededpermission,
            color=0xE74C3C,
        )
    )

async def log_in_channel(description:str,color:nextcord.Color=nextcord.Color.green()):
    c = client.get_channel(secretlib.log_channel)
    t = get_dc_timestamp(datetime.datetime.now(), "f")
    await c.send(embed=nextcord.Embed(color=color,title=f"[{t}] Log",description=description))
