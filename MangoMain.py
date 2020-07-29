import os
import discord
from HololiveStream import HololiveStream
from HololiveStreamer import hololiveStreamer
import pandas as pd
import youtube_api.youtube_api_utils
from youtube_api import YouTubeDataAPI
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord.ext import commands

load_dotenv()   

#Load in discord token and youtube API key from environment variables
TOKEN = os.getenv('MANGO_TOKEN')
YT_KEY = os.getenv('YOUTUBE_KEY')

#Variable used with hololive commands
selectedGen = -1

#setup bot
mango = commands.Bot(command_prefix='m!')

#create youtube data api client
yt = YouTubeDataAPI(YT_KEY)

@mango.event
async def on_ready():   
    print(f'{mango.user} is online!')
    #Change status

@mango.command(name = "holostream")
async def Hololive(ctx,arg):
    initialSearch = yt.search(q=arg, search_type='channel')
    #ID's we will be using for the channel and livestream to send requests
    stream = HololiveStream()
    
    #If we get a matching channel, we get the id and title. Otherwise, we tell the user that no matching channel was found in the search 
    #(Hololive streamers will usually be at the top of the list due to their distinct names, no need to check) - m!hologen and m!holoselect will be used for 
    #direct selection anyways
    if len(initialSearch)>0:
        stream.channelID = initialSearch[0]['channel_id']
        stream.channelTitle = initialSearch[0]['channel_title']
        stream.channelImage = initialSearch[0]['video_thumbnail']
        print(stream.channelID) 
    else:
        await ctx.send('No channel was found, please double check spelling and search again~')
    
    #If the channelID exists, proceed to see if they are live
    if(hasattr(stream,'channelID')):
        channelState = yt.search(channel_id=stream.channelID, search_type='video', event_type='live',)
        
        #If we get a response (meaning that the channel is live), proceed to grab the details of the stream and send it as an embed
        if len(channelState)>0:
            stream.streamID = channelState[0]['video_id']
            stream.streamTitle = channelState[0]['video_title']
            stream.streamThumbnail = channelState[0]['video_thumbnail']
            stream.streamDesc = channelState[0]['video_description']
            
            #Send another request to get info on view and like count of the stream
            videoData = yt.get_video_metadata(stream.streamID)
            stream.totalViews = videoData['video_view_count']
            stream.likes = videoData['video_like_count']
            print("data sucesfully obtained")

            #create the embed
            embed = discord.Embed(title = stream.streamTitle,description = stream.streamDesc,colour = discord.Colour(0x2abdb5))
            
            #Modify some attributes 
            embed.set_thumbnail(url=stream.streamThumbnail)
            embed.set_author(name = stream.channelTitle,icon_url=stream.channelImage)

            embed.add_field(name = "\u200b",value = "**Total viewers: **" + stream.totalViews + "\n**Likes: **" + stream.likes  ,inline = True)

            await ctx.send(embed=embed)

        else: 
            await ctx.send(stream.channelTitle + ' is not currently streaming live, upcoming stream info will be added in a future patch~ \n' 
            +'If the channel displayed is not the hololive streamer you are looking for, try using m!hologen and m!holoselect to directly check their channel')

@mango.command(name='hololist')
async def hololist(ctx):
    embed = discord.Embed(title = "List of supported Hololive generations",description = '**0.** Hololive Gen 0\n' + '**1.** Hololive Gen 1\n' + '**2.** Hololive Gen 2\n'
    + '**3.** Hololive Gen 3\n' + '**4.** Hololive Gen 4\n'+ '**5.** Hololive gamers',
    colour = discord.Colour(0x42b9f5))
    embed.set_footer(text = 'use m!hologen <list number> to get more details on each generation')
    
    await ctx.send(embed = embed)

@mango.command(name='hologen')
async def hologen(ctx,arg):
    selectedGen = int(arg)
    memberNum = os.getenv(arg + '_SIZE')
    displayString = ""
    for i in range(int(memberNum)):
        currentID = os.getenv(arg+'.'+f'{i}')
        nameSearch = yt.get_channel_metadata(currentID)
        channelName = nameSearch['title']
        displayString = displayString + "**"+f'{i+1}'+ '.** ' + channelName +"\n"
    
    embed = discord.Embed(title = 'Members of ' + os.getenv(arg) +':',description = displayString, colour = discord.Colour(0x42b9f5))
    embed.set_footer(text = 'use m!holoselect <list number> to get more details on each generation')
    await ctx.send(embed = embed)
    

@mango.command(name='holoselect')
async def holoselect(ctx,arg):
    pass

mango.run(TOKEN)