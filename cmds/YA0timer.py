import discord
from discord.ext import commands,tasks
from core.classes import Cog_Extension
import json,asyncio,datetime
import getData

with open('settings.json','r',encoding='utf8') as s:
    settings = json.load(s)
event_channel = settings['event_channel']
p2035=1
timeron= 1
started_tasks = []
class YA0timer(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot
        self.data = []
        #self.batch_update.add_exception_type(asyncpg.PostgresConnectionError)
        self.Time_List_Autosend.start()
        self.Ya0TimerMain.start()
        self.mention2035.start()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("YA0timer ok!")

    #----------------------------------------------------------------------
    @commands.command()
    async def TimerON(self,ctx):
        global timeron
        timeron=1
        await ctx.channel.send(f'TimerON!')
    
    @commands.command()
    async def TimerOFF(self,ctx):
        global timeron
        timeron=0
        await ctx.channel.send(f'TimerOFF!')
        
    @commands.command() ##command
    async def Time_List(self,ctx):#show today and tomorrow's all nights
        discr=self.ListFormat()
        timeList = discord.Embed(title="西圖斯夜晚時間",description=discr,colour=0x00f5b8)
        
        global event_channel
        #print(event_channel)
        #channel = await self.bot.fetch_channel(event_channel)
        await ctx.channel.send(embed=timeList)
        
    @tasks.loop(minutes=1)
    async def Time_List_Autosend(self):#Update at 00:00 everyday
        now=datetime.datetime.now().strftime("%H:%M")
        if now == "00:00":
            await getData.get_Data()
            with open('time.json','r',encoding='utf8') as jfile:
                timedata = json.load(jfile)
            jfile.close()
            
            today=timedata["today"]
            tomorrow=timedata["tomorrow"]

            discr=f"今天:{today}\n"
            for i in range(len(timedata[today])):
                discr+=f"> {timedata[today][str(i)]}\n"
                                
            discr+=f"\n明天:{tomorrow}\n"
            for i in range(len(timedata[tomorrow])):
                discr+=f"> {timedata[tomorrow][str(i)]}\n"
            
            timeList = discord.Embed(title="西圖斯夜晚時間",description=discr,colour=0x00f5b8)
            
            global event_channel
            #print(event_channel)
            channel = await self.bot.fetch_channel(event_channel)
            await channel.send(embed=timeList)
            
    
    @tasks.loop(minutes=1)
    async def Ya0TimerMain(self): 
        if timeron:
            
            global channel
            channel = await self.bot.fetch_channel(event_channel)
            now_time = datetime.datetime.now().strftime('%H:%M')
            #print('nowtime=',now_time)
            with open('time.json','r',encoding='utf8') as jfile:
                jdata = json.load(jfile)
                #print('from YA0TimerMain(os): jdata[nextcall]=',jdata['nextcall'])
            if now_time == jdata['nextcall']:
                getData.get_nextcall()
                print('from YA0TimerMain(update): jdata[nextcall]=',jdata['nextcall'])
                await channel.send('都看看現在幾點了!(拿起狙擊槍)')
            #print('---------------')
    
    @tasks.loop(seconds=1)
    async def mention2035(self):
        global p2035
        channel = await self.bot.fetch_channel(event_channel)
        now_time = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
        #print(now_time)
        if now_time == "35/01/01 00:00:00" and p2035:
            await channel.send('天哪。。。我不知道我31歲還會不會玩這半成品集合體 By PROcreeter At 03/27/2023 11:35 AM')
            self.mention2035().cancel()
    
    def getNextcall(self):
        getData.get_nextcall()
        
    def ListFormat(self):
        with open('time.json','r',encoding='utf8') as jfile:
            timedata = json.load(jfile)
        jfile.close()
        
        today=timedata["today"]
        tomorrow=timedata["tomorrow"]

        discr=f"今天:{today}\n"
        for i in range(len(timedata[today])):
            discr+=f"> {timedata[today][str(i)]}\n"
                            
        discr+=f"\n明天:{tomorrow}\n"
        for i in range(len(timedata[tomorrow])):
            discr+=f"> {timedata[tomorrow][str(i)]}\n"
        
        return discr 

async def setup(bot):
    await bot.add_cog(YA0timer(bot))