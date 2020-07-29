import os
import discord
from HololiveStream import HololiveStream
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

#setup bot
mango = commands.Bot(command_prefix='m!')

#create youtube data api client
yt = YouTubeDataAPI(YT_KEY)

@mango.event
async def on_ready():   
    print(f'{mango.user} is online!')
    #Change status

#,pass_context=True
@mango.command(name="embed")
async def embed (ctx):
    
    #create the embed
    embed = discord.Embed(title = "Livestream Title:",description = "Livestream Description",colour = discord.Colour(0x2abdb5))
    
    #Modify some attributes 
    embed.set_thumbnail(url="https://pbs.twimg.com/media/DU2xgrpU0AEeTai.jpg")
    embed.set_author(name = "Channel name")

    embed.add_field(name = "\u200b",value = "**Total viewers: **" + "Number of viewers" + "\n**Likes: **" + " Number of likes",inline = True)

    await ctx.send(embed=embed)

@mango.command(name="test")
async def test(ctx,arg):
    await ctx.send(arg)

@mango.command(name = "hololive")
async def Hololive(ctx,arg):
    initialSearch = yt.search(q=arg, search_type='channel')
    #ID's we will be using for the channel and livestream to send requests
    stream = HololiveStream()
    
    #If we get a matching channel, we get the id. Otherwise, we tell the user that no matching channel was found in the search
    if len(initialSearch)>0:
        stream.channelID = initialSearch[0]['channel_id']
        
    else:
        await ctx.send('No channel was found, please double check spelling and search again~')

    #If the channelID exists, proceed to see if they are live
    print(stream.channelID)
    channelState = yt.search(channel_id=stream.channelID, search_type='video', event_type='live')
    
    #If we get a response (meaning that the channel is live), proceed to grab the details of the stream and send it as an embed
    if len(channelState)>0:
        stream.streamID = channelState[0]['video_id']
        stream.streamTitle = channelState[0]['video_title']
        stream.streamThumbnail = channelState[0]['video_thumbnail']
        stream.streamDesc = channelState[0]['video_description']
        stream.channelTitle = channelState[0]['channel_title']
        
        #Send another request to get info on view and like count of the stream
        videoData = yt.get_video_metadata(stream.streamID)
        stream.totalViews = videoData['video_view_count']
        stream.likes = videoData['video_like_count']
        print("data sucesfully obtained")

        #create the embed
        embed = discord.Embed(title = stream.streamTitle,description = stream.streamDesc,colour = discord.Colour(0x2abdb5))
        
        #Modify some attributes 
        embed.set_thumbnail(url=stream.streamThumbnail)
        embed.set_author(name = stream.channelTitle)

        embed.add_field(name = "\u200b",value = "**Total viewers: **" + stream.totalViews + "\n**Likes: **" + stream.likes  ,inline = True)

        await ctx.send(embed=embed)

    else: 
        await ctx.send('The channel is not currently streaming live, upcoming stream info will be added in a future patch~')
        

mango.run(TOKEN)