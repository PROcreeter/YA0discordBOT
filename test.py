import discord
from discord.ext import commands
#from core.classes import Cog_Extension
import json,asyncio
from datetime import datetime,timedelta

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%m/%d")
tomorrow= now+ timedelta(1)
print(tomorrow.strftime("%m/%d"))
