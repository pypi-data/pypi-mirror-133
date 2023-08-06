from discord.ext import commands
from itertools import cycle
import time
import discord
import warnings
import aiohttp
import datetime
warnings.filterwarnings("ignore", category=DeprecationWarning)




#set activity
async def set_activity(bot, stuff):
    #checking if stuff is list or not
    check = isinstance(stuff, list)
    all_activity = ["watching", "listening", "playing", "competing", "competing in"]
    
    if check == False:
        print("""You have to insert a list as argument. For Example - ["Watching", "People type !help"]""")
        return
        
    if check == True:
        #checking if the lenght of the items inside the list is 2 or not
        if len(stuff) != 2:
            print("""The list must have atleast 2 items inside. First item will be discord.ActivityType and second item will be the activity name! For Example - ["Watching", "People type !help"]""")
        
        if len(stuff) == 2:
            #everything is fine! lets start coding
            status_activity = stuff[0]
            status_name = stuff[1]
            
            status_activity = status_activity.lower().strip()
            
            #checking if activity exists or not
            if status_activity not in all_activity:
                print("""Inserted activity is invalid. Valid activities are Watching/Playing/Listening/Competing""")
                return
            
            #if else starts here
            #watching
            if status_activity == "watching":
                await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = status_name))
            
            #Listening
            if status_activity == "listening":
                await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = status_name))
            
            #Playing
            if status_activity == "playing":
                await bot.change_presence(activity = discord.Game(name = status_name))
            
            #Competing
            if status_activity == "competing" or status_activity == "competing in":
                await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.competing, name = status_name))





# set status
async def set_status(bot, stuff):
    #checking if stuff is list or not
    all_status = ["online", "idle", "dnd", "offline"]
    check = isinstance(stuff, str)
    
    if check == False:
        print("""You have to insert a string as argument. For Example -  "Idle" """)
        return
        
    if check == True:
        #checking if the string is in all_status or not
        stuff = stuff.lower().strip()
        
        if stuff not in all_status:
            print("""Your status must be  -  Online/Idle/DND/Offline""")
            return
        
        if stuff in all_status:
            #everyting is fine! lets start coding
            #online
            if stuff == "online":
                await bot.change_presence(status = discord.Status.online)
            
            #idle
            if stuff == "idle":
                await bot.change_presence(status = discord.Status.idle)
            
            #do not disturb
            if stuff == "dnd":
                await bot.change_presence(status = discord.Status.dnd)
            
            #offline
            if stuff == "offline":
                await bot.change_presence(status = discord.Status.offline)




#get all server icon link
def get_all_guild_icon(bot):
    icon_list = []
    for guild in bot.guilds:
        icon_list.append(guild.icon_url)
    return icon_list





#get all server name
def get_all_guild_name(bot):
    name_list = []
    for guild in bot.guilds:
        name_list.append(guild.name)
    return name_list




#get all server id
def get_all_guild_id(bot):
    id_list = []
    for guild in bot.guilds:
        id_list.append(int(guild.id))
    return id_list



#get all owner name
def get_all_owner_name(bot):
    name_list = []
    for guild in bot.guilds:
        name_list.append(guild.owner.name)
    return name_list





#get all owner id
def get_all_owner_id(bot):
    id_list = []
    for guild in bot.guilds:
        id_list.append(int(guild.owner_id))
    return id_list



#generate invite link
def generate_invite_link(bot):
    invite_link = discord.utils.oauth_url(bot.user.id)
    return invite_link


#timeout someone
async def timeout_user(*, token, user_id: int, guild_id: int, until):
    headers = {"Authorization": f"Bot {token}"}
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
    timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
    json = {'communication_disabled_until': timeout}
    async with aiohttp.ClientSession().patch(url, json=json, headers=headers) as session:
        print(session.status)
        if session.status in range(200, 299):
           return True
        return False

#@client.command()
#async def timeout(ctx: commands.Context, member: discord.Member, until: int):
#    handshake = await timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=until)
#    if handshake:
    #     return await ctx.send(f"Successfully timed out user for {until} minutes.")
   # await ctx.send("Something went wrong")