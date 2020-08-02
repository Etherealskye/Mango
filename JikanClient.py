import asyncio
import discord
from jikanpy import Jikan
from anime import anime
from manga import manga

class JikanClient:
    'Class used to handle requests related to the jikan.moe API and provide anime and manga information using Jikan API wrapper'

    def __init__(self):
        pass
        self.jikan = Jikan()
        self.animeList = []
        self.mangaList = []

    #Method used to sesarch for an anime and add the first 25 anime received to our search results
    def animeSearch(self, animeName):
        self.animeList.clear()
        animeResults = self.jikan.search(query = animeName, search_type = 'anime')
        if(len(animeResults['results'])<25):
            for i in animeResults['results']:
                currentAnime = (anime(
                    i['mal_id'],
                    i['title'],
                    i['score'],
                    i['airing'],
                    i['synopsis'],
                    i['image_url'],
                    i['episodes']))
                self.animeList.append(currentAnime)
        else:
            for i in range(25):
                currentAnime = (anime(
                    animeResults['results'][i]['mal_id'],
                    animeResults['results'][i]['title'],
                    animeResults['results'][i]['score'],
                    animeResults['results'][i]['airing'],
                    animeResults['results'][i]['synopsis'],
                    animeResults['results'][i]['image_url'],
                    animeResults['results'][i]['episodes']))
                self.animeList.append(currentAnime)

    #Return an embed to be sent for a specific anime
    def animeEmbed(self, animeIndex):
            embed = discord.Embed(
                title = self.animeList[animeIndex].title,
                description = self.animeList[animeIndex].synopsis,
                colour = discord.Colour(0x8d32e3)
            )
            
            embed.set_thumbnail(url = self.animeList[animeIndex].image)
            embed.add_field(name = "Rating:",value = f'{self.animeList[animeIndex].rating}'+'/10',inline = True)
            embed.add_field(name = "Status:",value = f'{self.animeList[animeIndex].status}',inline = True)
            embed.add_field(name = "Episodes:",value = f'{self.animeList[animeIndex].episodes}',inline = True)
            return embed
    
    #Return an embed that displasy all the anime search resutls
    def animeListDisplay(self, animeName):
        descString = ''
        for i in range(len(self.animeList)):
            descString = descString + "**"+f'{i+1}'+"**. " + self.animeList[i].title
            if i != len(self.animeList)-1:
                descString = descString + "\n"

        embed = discord.Embed(
            title = "List of anime found for '" + animeName + "':",
            description = descString,
            colour = discord.Colour(0x8d32e3)
        )
        #print(descString)
        return embed

    #Method used to search for a manga and add the first 25 results to our list
    def mangaSearch(self, mangaName):
        self.mangaList.clear()
        mangaResults = self.jikan.search(query = mangaName, search_type = 'manga')
        if(len(mangaResults['results'])<25):
            for i in mangaResults['results']:
                currentManga = (manga(
                    i['mal_id'],
                    i['title'],
                    i['score'],
                    i['publishing'],
                    i['synopsis'],
                    i['image_url'],
                    i['chapters'],
                    i['volumes']))
                self.mangaList.append(currentManga)
        else:
            for i in range(25):
                currentManga = (manga(
                    mangaResults['results'][i]['mal_id'],
                    mangaResults['results'][i]['title'],
                    mangaResults['results'][i]['score'],
                    mangaResults['results'][i]['publishing'],
                    mangaResults['results'][i]['synopsis'],
                    mangaResults['results'][i]['image_url'],
                    mangaResults['results'][i]['chapters'],
                    mangaResults['results'][i]['volumes']))
                self.mangaList.append(currentManga)

    #Return an embed that displasy all the manga search resutls
    def mangaListDisplay(self, mangaName):
        descString = ''
        for i in range(len(self.mangaList)):
            descString = descString + "**"+f'{i+1}'+"**. " + self.mangaList[i].title
            if i != len(self.mangaList)-1:
                descString = descString + "\n"

        embed = discord.Embed(
            title = "List of anime found for '" + mangaName + "':",
            description = descString,
            colour = discord.Colour(0x8d32e3)
        )
        #print(descString)
        return embed

    #Return an embed to be sent for a specific manga
    def mangaEmbed(self, mangaIndex):
        embed = discord.Embed(
            title = self.mangaList[mangaIndex].title,
            description = self.mangaList[mangaIndex].synopsis,
            colour = discord.Colour(0x8d32e3)
        )

        embed.set_thumbnail(url = self.mangaList[mangaIndex].image)
        embed.add_field(name = "Rating:",value = f'{self.mangaList[mangaIndex].rating}'+'/10',inline = True)
        embed.add_field(name = "Status:",value = f'{self.mangaList[mangaIndex].status}',inline = True)
        embed.add_field(name = "Chapters:",value = f'{self.mangaList[mangaIndex].chapters}',inline = True)
        embed.add_field(name = "Volumes:",value = f'{self.mangaList[mangaIndex].volumes}',inline = True)
        return embed

if __name__ == '__main__':
    client = JikanClient()
    client.mangaSearch("Spy X Family")
    for i in client.mangaList:
        print(i)
    #client.animeListDisplay("Gundam 00")
  

