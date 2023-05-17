import discord
from discord.ext import commands,tasks
from core.classes import Cog_Extension
import json,asyncio,datetime
import getData
import asyncpg

# class testcmd(Cog_Extension):
#     started_tasks = []
    
#     async def task_loop(self ,ctx, something):  # the function that will "loop"
#         await ctx.send(something)

#     @commands.command()
#     async def start(self ,ctx, something):
#         t = tasks.loop(seconds=10)(self.task_loop)
#         self.started_tasks.append(t)
#         t.start(ctx, something)


#     @commands.command()
#     async def stop(self):
#         for t in self.started_tasks:
#             t.cancel()
class testcmd(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot
        self.data = []
        #self.batch_update.add_exception_type(asyncpg.PostgresConnectionError)
        self.batch_update1.start()
        self.batch_update2.start()

    def cog_unload(self):
        self.batch_update1.cancel()

    @tasks.loop(minutes=1)
    async def batch_update1(self):
        now=datetime.datetime.now().strftime("%H:%M")
        if now == "00:00":
            print("autoYA0_List")
        
    @tasks.loop(seconds=10)
    async def batch_update2(self):
        print("hi10")
async def setup(bot):
    await bot.add_cog(testcmd(bot))