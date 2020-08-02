import asyncio
import discord
from jikanpy import Jikan
from anime import anime

class JikanClient:
    'Class used to handle requests related to the jikan.moe API and provide anime and manga information using Jikan API wrapper'

    def __init__(self):
        pass
        self.jikan = Jikan()
        self.animeList = []

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

    #Method used to search for a manga
    def mangaSearch(self, mangaName):
        pass

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

if __name__ == '__main__':
    client = JikanClient()
    client.animeSearch("Gundam 00")
    #client.animeListDisplay("Gundam 00")
  

