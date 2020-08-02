import os
import discord
import pandas as pd
import youtube_api.youtube_api_utils
from youtube_api import YouTubeDataAPI
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord.ext import commands
from HololiveStreamer import hololiveStreamer
from HololiveStream import HololiveStream
from JikanClient import JikanClient

load_dotenv()   

#Load in discord token and youtube API key from environment variables
TOKEN = os.getenv('MANGO_TOKEN')
YT_KEY = os.getenv('YOUTUBE_KEY')

#Variables used with hololive commands
selectedGen = None
holoStreamers = []

#setup bot
mango = commands.Bot(command_prefix='m!')

#create youtube data api client
yt = YouTubeDataAPI(YT_KEY)

#Create jikanClient to interact with JikanAPI
jikan = JikanClient()

@mango.event
async def on_ready():   
    print(f'{mango.user} is online!')
    #Change status

#Command to let user search for a livestream
@mango.command(name = "holoStream")
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
            embed.url='https://www.youtube.com/watch?v='+stream.streamID
            embed.add_field(name = "\u200b",value = "**Total viewers: **" + stream.totalViews + "\n**Likes: **" + stream.likes  ,inline = True)

            await ctx.send(embed=embed)

        #If there are no livestreams, check if there is an upcoming stream or not
        else: 
            #Send a second search to see if there are any upcoming streams for the selected hololive streamer
            secondSearch = yt.search(channel_id=stream.channelID, search_type='video', event_type='upcoming',)
            #If there is an upcoming stream scheduled, proceed to parse for data
            if len(secondSearch)>0:
                stream.streamID = secondSearch[0]['video_id']
                stream.streamTitle = secondSearch[0]['video_title']
                stream.streamThumbnail = secondSearch[0]['video_thumbnail']
                stream.streamDesc = secondSearch[0]['video_description']
                
                #Send another request to get info on view and like count of the upcoming stream
                #print(stream.streamID)
                videoData = yt.get_video_metadata(stream.streamID)
                stream.totalViews = videoData['video_view_count']
                stream.likes = videoData['video_like_count']
                print("data sucesfully obtained")

                #Check if we actually got an upcoming stream (This is due to youtube's data api returning streams that have just finished as "upcoming" for some reason)
                #We can only check this by sending a second request to VideoData - the upcoming stream will have 0 views because it has not premeried yet
                if stream.totalViews == '0':
                    #Let user know that there are no current live streams, but that there is an upcoming one
                    await ctx.send(stream.channelTitle + " has no current livestreams, but does have an upcoming stream in the near future:")
                    #create the embed
                    embed = discord.Embed(title = stream.streamTitle,description = stream.streamDesc,colour = discord.Colour(0x2abdb5))
                    
                    #Modify some attributes 
                    embed.set_thumbnail(url=stream.streamThumbnail)
                    embed.set_author(name = stream.channelTitle,icon_url=stream.channelImage)
                    embed.url='https://www.youtube.com/watch?v='+stream.streamID
                    embed.set_footer(text='If the channel displayed is not the hololive streamer you are looking for, try using m!hologen and m!holoselect to directly check their channel')

                    embed.add_field(name = "\u200b",value = "**Total viewers: **" + stream.totalViews + "\n**Likes: **" + stream.likes  ,inline = True)
                        
                    await ctx.send(embed=embed)
                
                elif stream.totalViews != '0':
                    await ctx.send(stream.channelTitle + ' is not currently streaming live nor has any upcoming livestreams\n' 
                    +'If the channel displayed is not the hololive streamer you are looking for, try using m!hologen and m!holoselect to directly check their channel')

            #If no upcoming stream, let users know that channel is not live nor are there are any upcoming stream
            else:
                await ctx.send(stream.channelTitle + ' is not currently streaming live nor has any upcoming livestreams\n' 
                +'If the channel displayed is not the hololive streamer you are looking for, try using m!hologen and m!holoselect to directly check their channel')

#Command that lists all the supported hololive groups
@mango.command(name='holoList')
async def hololist(ctx):
    embed = discord.Embed(title = "List of supported Hololive generations",description = '**0.** Hololive Gen 0\n' + '**1.** Hololive Gen 1\n' + '**2.** Hololive Gen 2\n'
    + '**3.** Hololive Gen 3\n' + '**4.** Hololive Gen 4\n'+ '**5.** Hololive gamers',
    colour = discord.Colour(0x42b9f5))
    embed.set_footer(text = 'use m!hologen <list number> to get more details on each generation')
    
    await ctx.send(embed = embed)

#Command that brings up the members of a hololive group/generation
@mango.command(name='holoGen')
async def hologen(ctx,arg):
    global holoStreamers
    global selectedGen
    holoStreamers.clear()
    try:
        selectedGen = int(arg)
        memberNum = os.getenv(arg + '_SIZE')
        displayString = ""
        
        for i in range(int(memberNum)):
            currentID = os.getenv(arg+'.'+f'{i}')
            nameSearch = yt.search(channel_id=currentID,search_type='channel')
            channelName = nameSearch[0]['channel_title']
            channelProfile = nameSearch[0]['video_thumbnail']
            streamer = hololiveStreamer(group = arg, title = channelName, profile = channelProfile)
            holoStreamers.append(streamer)
            displayString = displayString + "**"+f'{i+1}'+ '.** ' + channelName +"\n"
        
        embed = discord.Embed(title = 'Members of ' + os.getenv(arg) +':',description = displayString, colour = discord.Colour(0x42b9f5))
        embed.set_footer(text = 'use m!holoselect <list number> to get the status on each member')
        await ctx.send(embed = embed)
    
    except (TypeError, ValueError):
        await ctx.send('Please select a valid number from the displayed list!')
    
#Command used to selelct a hololiveStreamers for more details on if they're livestreaming or not
@mango.command(name='holoSelect')
async def holoselect(ctx,arg):
    global selectedGen
    #Makes sure the user has actually selected a generation/group to select a member from
    #print(selectedGen)
    if selectedGen != None:
        try:
            #The ID of the hololive streamer we want to search for
            searchID = os.getenv(f'{selectedGen}'+'.'+f'{int(arg)-1}')
            
            #Create hololive stream object and set some attributes
            stream = HololiveStream()
            stream.channelID = searchID
            stream.channelTitle = holoStreamers[int(arg)-1].channel_title
            stream.channelImage = holoStreamers[int(arg)-1].channel_profile

            #Send search to api to see if channel is live
            search = yt.search(channel_id=searchID, search_type='video', event_type='live',)
            #If we get a response (meaning that the channel is live), proceed to grab the details of the stream and send it as an embed
            if len(search)>0:
                stream.streamID = search[0]['video_id']
                stream.streamTitle = search[0]['video_title']
                stream.streamThumbnail = search[0]['video_thumbnail']
                stream.streamDesc = search[0]['video_description']
                
                #Send another request to get info on view and like count of the stream
                #print(stream.streamID)
                videoData = yt.get_video_metadata(stream.streamID)
                stream.totalViews = videoData['video_view_count']
                stream.likes = videoData['video_like_count']
                print("data sucesfully obtained")

                #create the embed
                embed = discord.Embed(title = stream.streamTitle,description = stream.streamDesc,colour = discord.Colour(0x2abdb5))
                
                #Modify some attributes 
                embed.set_thumbnail(url=stream.streamThumbnail)
                embed.set_author(name = stream.channelTitle,icon_url=stream.channelImage)
                embed.url='https://www.youtube.com/watch?v='+stream.streamID

                embed.add_field(name = "\u200b",value = "**Total viewers: **" + stream.totalViews + "\n**Likes: **" + stream.likes  ,inline = True)

                await ctx.send(embed=embed)
            
            #If no current livestreams, see if there is an upcoming stream or not
            else:
                #Send a second search to see if there are any upcoming streams for the selected hololive streamer
                secondSearch = yt.search(channel_id=searchID, search_type='video', event_type='upcoming',)
                #If there is an upcoming stream scheduled, proceed to parse for data
                if len(secondSearch)>0:
                    stream.streamID = secondSearch[0]['video_id']
                    stream.streamTitle = secondSearch[0]['video_title']
                    stream.streamThumbnail = secondSearch[0]['video_thumbnail']
                    stream.streamDesc = secondSearch[0]['video_description']
                    
                    #Send another request to get info on view and like count of the upcoming stream
                    #print(stream.streamID)
                    videoData = yt.get_video_metadata(stream.streamID)
                    stream.totalViews = videoData['video_view_count']
                    stream.likes = videoData['video_like_count']
                    print("data sucesfully obtained")

                    #Check if we actually got an upcoming livestream - youtube data api will sometimes give us a livestream that just ended recently
                    #We can only check this by sending a second request for video metadata and seeing if total views = 0 or not
                    if stream.totalViews == '0':
                        #Let user know that there are no current live streams, but that there is an upcoming one
                        await ctx.send(holoStreamers[int(arg)-1].channel_title + " has no current livestreams, but does have an upcoming stream in the near future:")
                        #create the embed
                        embed = discord.Embed(title = stream.streamTitle,description = stream.streamDesc,colour = discord.Colour(0x2abdb5))
                        
                        #Modify some attributes 
                        embed.set_thumbnail(url = stream.streamThumbnail)
                        embed.set_author(name = stream.channelTitle,icon_url=stream.channelImage)
                        embed.url='https://www.youtube.com/watch?v='+stream.streamID

                        embed.add_field(name = "\u200b",value = "**Total viewers: **" + stream.totalViews + "\n**Likes: **" + stream.likes  ,inline = True)

                        await ctx.send(embed=embed)

                    elif stream.totalViews != '0':
                        await ctx.send(holoStreamers[int(arg)-1].channel_title + ' is not currently streaming live nor has any upcoming livestreams~')

                #If no upcoming stream, let users know that channel is not live nor are there are any upcoming stream
                else:
                    await ctx.send(holoStreamers[int(arg)-1].channel_title + ' is not currently streaming live nor has any upcoming livestreams~')

        except(ValueError,IndexError):
            await ctx.send('Please select a valid member number from the generation/group!')
    
    elif selectedGen == None:
        await ctx.send('Please select a generation first!')

#Command used to search for anime and display a list of results
@mango.command(name = 'animeSearch')
async def animeSearch(ctx, arg):
    jikan.animeSearch(arg)
    #Only proceed to send the embed if we actually have any anime to display. Else, let the user know that no anime were found.
    #This prevents the bot from sending an empty embed.
    if len(jikan.animeList)>0:
        embed = jikan.animeListDisplay(arg)
        await ctx.send(embed = embed)

    else:
        await ctx.send("No anime found for: '" + arg + "'")

#Commnand used to select an anime from the displayed list of results
@mango.command(name = 'animeSelect')
async def animeSelect(ctx,arg):
    try:
        #Make sure that we have succesfully gotten a displayed list of anime
        if len(jikan.animeList)>0:
            await ctx.send(embed=jikan.animeEmbed(int(arg)-1))

        else:
            await ctx.send("Please use m!animeSearch <anime name> first!")

    except (ValueError,IndexError):
        await ctx.send("Please enter a number from the displayed list!")

#Command used to search for manga and display the results
@mango.command(name = 'mangaSearch')
async def mangaSearch (ctx, arg):
    jikan.mangaSearch(arg)
    #Only proceed to send the embed if we actually have any manga to display. Else, let the user know that no manga were found.
    #This prevents the bot from sending an empty embed.
    if len(jikan.mangaList)>0:
        embed = jikan.mangaListDisplay(arg)
        await ctx.send(embed = embed)

    else:
        await ctx.send("No manga found for: '" + arg + "'")

#Command used to select manga from the displayed list of results
@mango.command(name = 'mangaSelect')
async def mangaSelect(ctx, arg):
    try:
        #Make sure that we have successfully gotten a displayed list of manga
        if len(jikan.mangaList)>>0:
            await ctx.send(embed = jikan.mangaEmbed(int(arg)-1))
        
        else:
            await ctx.send("Please use m!mangaSearch <manga name> first!")
    
    except(ValueError,IndexError):
        await ctx.send("Please enter a number from the displayed list")

mango.run(TOKEN)