#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pprint

#imports the minidom library
import xml.dom.minidom
from xml.dom import minidom
docs = xml.dom.minidom.parse("/Users/Shrit/Downloads/MyAnimeList.xml")

#imports the ElementTree library
import xml.etree.ElementTree as ET            
malDoc = ET.parse("/Users/Shrit/Downloads/MyAnimeList.xml")
malRoot = malDoc.getroot()

#imports HTML Reader
import urllib.request
import urllib.error
import re

#imports HTMLParser
from bs4 import BeautifulSoup
import lxml

#prompts user to input a .xml file of their anime list from MyAnimeList
print("Please input your MyAnimeList Anime List here (.xml file): ")
animeList = input()
#parsing the XML file

xmldoc = minidom.parse(animeList)

#aggregating lists
myAnimeList = docs.getElementsByTagName('myanimelist')
anime = docs.getElementsByTagName('anime')
title = docs.getElementsByTagName('series_title')

#Creates a dictionary containing anime IDs as keys and their respective scores as values
def getIDAndScore():
    animeInfo = {}
    for info in malRoot.findall("anime"):
        if (info.find("my_status").text == "Completed"):
            animeID = info.find("series_animedb_id").text
            animeScore = info.find("my_score").text
            animeInfo[animeID] = animeScore
    return animeInfo

#prints a list for each title containing its ID and score
IDAndScore = getIDAndScore()

#functions to get the scores of studios, genres, themes, and demographics of each anime
def getName(soup):
    animeName = soup.find("title").string.replace(" - MyAnimeList.net", "")
    animeName.replace("\n", "")
    return animeName

def getStudioScores(studioScore):
    studio = soup.find("span", string="Studios:")
    studioName = studio.next_sibling.next_sibling.text
    score = int(IDAndScore[ID])
    if studioName in studioScore:
        studioScore[studioName][0] += 1
    else:
        studioScore[studioName] = [1]
    if studioName in studioScore and len(studioScore[studioName]) > 1:
        score = score + int(studioScore[studioName][1])
    if len(studioScore[studioName]) == 1:
        studioScore[studioName].append(score)
    else:
        studioScore[studioName][1] = score
    return studioScore

def getGenreScores(genreScore):
    if soup.find(string=re.compile("Genres:")):
        genre = soup.find("span", string="Genres:")
    elif soup.find(string=re.compile("Genre:")):
        genre = soup.find("span", string="Genre:")
    else:
        return genreScore
    genreName = genre.next_sibling.next_sibling.text
    score = int(IDAndScore[ID])
    if genreName in genreScore:
        genreScore[genreName][0] += 1
    else:
        genreScore[genreName] = [1]
    if genreName in genreScore and len(genreScore[genreName]) > 1:
        score = score + int(genreScore[genreName][1])
    if len(genreScore[genreName]) == 1:    
        genreScore[genreName].append(score)
    else:
        genreScore[genreName][1] = score
    return genreScore

def getThemeScores(themeScore):
    if soup.find(string=re.compile("Themes:")):
        theme = soup.find("span", string="Themes:")
    elif soup.find(string=re.compile("Theme:")):
        theme = soup.find("span", string="Theme:")
    else:
        return themeScore
    themeName = theme.next_sibling.next_sibling.text
    score = int(IDAndScore[ID])
    if themeName in themeScore:
        themeScore[themeName][0] += 1
    else:
        themeScore[themeName] = [1]
    if themeName in themeScore and len(themeScore[themeName]) > 1:
        score = score + int(themeScore[themeName][1])
    if len(themeScore[themeName]) == 1:
        themeScore[themeName].append(score)
    else:
        themeScore[themeName][1] = score
    return themeScore

def getDemographicScores(demoScore):
    if soup.find(string=re.compile("Demographics:")):
        demo = soup.find("span", string="Demographics:")
    elif soup.find(string=re.compile("Demographic:")):
        demo = soup.find("span", string="Demographic:")
    else:
        return demoScore
    demoName = demo.next_sibling.next_sibling.text
    score = int(IDAndScore[ID])
    if demoName in demoScore:
        demoScore[demoName][0] += 1
    else:
        demoScore[demoName] = [1]
    if demoName in demoScore and len(demoScore[demoName]) > 1:
        score = score + int(demoScore[demoName][1])
    if len(demoScore[demoName]) == 1:
        demoScore[demoName].append(score)
    else:
        demoScore[demoName][1] = score
    return demoScore

#function to print the total summed scores for each descriptor of each anime
studioScore = {}
genreScore = {}
themeScore = {}
demoScore = {}
for ID in IDAndScore:
    webUrl = urllib.request.urlopen("https://myanimelist.net/anime/" + str(ID) + "/")
    data = webUrl.read()
    soup = BeautifulSoup(data, "html.parser")
    getStudioScores(studioScore)
    getGenreScores(genreScore)
    getThemeScores(themeScore)
    getDemographicScores(demoScore)

studioScore = getStudioScores(studioScore)
genreScore = getGenreScores(genreScore)
themeScore = getThemeScores(themeScore)
demoScore = getDemographicScores(demoScore) 
    
#function to use a mathematical function to take all those inputs with the user score, and come out with 
#the user's statistically most favorite sections
studioScores = {}
genreScores = {}
themeScores = {}
demoScores = {}
for k, v in studioScore.items():
        studioScores[k] = studioScore[k]
        studioScores[k] = v[1] / v[0]
for k, v in genreScore.items():
        genreScores[k] = genreScore[k]
        genreScores[k] = v[1] / v[0]
for k, v in themeScore.items():
        themeScores[k] = themeScore[k]
        themeScores[k] = v[1] / v[0]
for k, v in demoScore.items():
        demoScores[k] = demoScore[k]
        demoScores[k] = v[1] / v[0]

getName(soup)
studioScores
genreScores
themeScores
demoScores 

##Go through each anime on MyAnimeList and based on its studio, genres, themes, and demographics
##and give it a recommendation score based on its similarity to the user's favorites.
##Recommend the top n number of anime to user.
def getStudio(soup):
    studio = soup.find("span", string="Studios:")
    studioName = studio.next_sibling.next_sibling.text
    return studioName

def getGenres(soup):
    genreList = []
    flag = True
    if soup.find(string="Genres:"):
        c = 0
    elif soup.find(string="Genre:"):
        c = 1
    else:
        genreList.append("None")
        return genreList
    if c == 0:
        for genre in soup.find("span", text="Genres:").parent.find_all("span"):
            if genre.text != "Themes:" or genre.text != "Theme:" or genre.text != "Demographics:" or genre.text != "Demographic:" or genre.text != "Duration:":
                if flag == False:
                    genreList.append(genre.text)
                flag = False
            else:
                return genreList
    else:
        genre = soup.find("span", string="Genre:")
        genreName = genre.next_sibling.next_sibling.text
        genreList.append(genreName)
    return genreList

def getThemes(soup):
    themeList = []
    flag = True
    if soup.find(string="Themes:"):
        c = 0
    elif soup.find(string="Theme:"):
        c = 1
    else:
        themeList.append("None")
        return themeList
    if c == 0:
        for theme in soup.find("span", text="Themes:").parent.find_all("span"):
            if theme.text != "Demographics:" or genre.text != "Demographic:" or genre.text != "Duration:":
                if flag == False:
                    themeList.append(theme.text)
                flag = False
            else:
                return themeList
    else:
        theme = soup.find("span", string="Theme:")
        themeName = theme.next_sibling.next_sibling.text
        themeList.append(themeName)
    return themeList
    
def getDemos(soup):
    demoList = []
    flag = True
    if soup.find(string="Demographics:"):
        c = 0
    elif soup.find(string="Demographic:"):
        c = 1
    else:
        demoList.append("None")
        return demoList
    if c == 0:
        for demo in soup.find("span", text="Demographics:").parent.find_all('span'):
            if demo.text != "Duration:":
                if flag == False:
                    demoList.append(demo.text)
                flag = False
            else:
                return demoList
    else:
        demo = soup.find("span", string="Demographic:")
        demoName = demo.next_sibling.next_sibling.text
        demoList.append(demoName)
    return demoList


def getRecommendations(): 
    recommendedAnime = {}
    sortedRecommendedAnime = {}
    sortedAnimeList = []
    sortedList = []
    for num in range(1, 50000):
        count = 0
        try:
            webUrl = urllib.request.urlopen("https://myanimelist.net/anime/" + str(num) + "/")
            data = webUrl.read()
            soup = BeautifulSoup(data, "html.parser")
            studioName = getStudio(soup)
            genreList = getGenres(soup)
            themeList = getThemes(soup)
            demoList = getDemos(soup)
            if soup.find("a", string="TV") or soup.find("a", string="Movie"):
                if str(num) not in IDAndScore:
                    animeScore = 0

                    if studioName in studioScores:
                        animeScore += studioScores[studioName]
                    if genreList[0] in genreScores:
                        for num in range(len(genreList)):
                            if genreList[num - 1] in genreScores:
                                animeScore += genreScores[genreList[num - 1]]
                                count += 1
                    if themeList[0] in themeScores:
                        for num in range(len(themeList)):
                            if themeList[num - 1] in themeScores:
                                animeScore += themeScores[themeList[num - 1]]
                                count += 1
                    if demoList[0] in demoScores:
                        for num in range(len(demoList)):
                            if demoList[num - 1] in demoScores:
                                animeScore += demoScores[demoList[num - 1]]
                                count += 1
                    if len(recommendedAnime) < 11:
                        recommendedAnime[getName(soup)] = animeScore / count
                        if len(recommendedAnime) == 10:
                            sortedAnimeList = sorted(recommendedAnime.items(), key=lambda kv: kv[1])
                            sortedRecommendedAnime = dict(sortedAnimeList)
                    else:
                        for name in sortedRecommendedAnime:
                            if (animeScore > sortedRecommendedAnime[name]):
                                del sortedRecommendedAnime[name]
                                sortedRecommendedAnime[getName(soup)] = animeScore
                                sortedAnimeList = sorted(sortedRecommendedAnime.items(), key=lambda kv: kv[1])
                                sortedRecommendedAnime = dict(sortedAnimeList)
                                break
        except urllib.error.HTTPError:
            pass
    return sortedRecommendedAnime

animeRecommendations = sorted(getRecommendations())
pprint.pprint(animeRecommendations)


# In[ ]:




