#導入 Discord.py
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import asyncio,json,datetime
import os
import threading

with open('settings.json','r',encoding='utf8') as jFile:
    jdata = json.load(jFile)
    
#bot 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='%',intents=intents)
channel = bot.get_channel(jdata['event_channel'])

# 頻道通知
#調用 event 函式庫
@bot.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', bot.user, 'online!')
    
    
    
@bot.event
#當有訊息時
async def on_message(message): #bot online test
    #排除自己的訊息，避免陷入無限循環
    if message.author == bot.user:
        return
    #如果包含 0，機器人回傳 1
    if message.content == '0':
       await message.channel.send('1')
    await bot.process_commands(message)

@bot.command() 
async def reload(ctx,extension): #reload extension
    path=jdata['cmd_files']+'\\'+extension+'.py'
    if os.path.exists(path):
        await bot.reload_extension(F'cmds.{extension}')
        await ctx.send(f'reloaded {extension} done.')
    else:
        await ctx.send(f'{extension} not found :({path})')

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

async def load_extensions():
    for Filename in os.listdir(jdata['cmd_files']):
        if Filename.endswith('.py'):
            await bot.load_extension(F'cmds.{Filename[:-3]}')
            print(Filename)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(jdata['token'])

        
if __name__ == '__main__':
    asyncio.run(main())
#TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面