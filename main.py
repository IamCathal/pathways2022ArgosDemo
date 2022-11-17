from extractArgos import *
from selenium import webdriver

def searchArgos():
    printIntro()
    xboxesFromArgos = getItemFromArgos("xbox series x console")
    playStationsFromArgos = getItemFromArgos("playstation 5 console")
    football = getItemFromArgos("size 5 fifa football")
    tableTennisTable = getItemFromArgos("9ft Indoor Table Tennis Table")
    getTotalPrice([xboxesFromArgos, playStationsFromArgos, football, tableTennisTable])

def getItemFromArgos(console):
    webpage = webdriver.Firefox()
    webpage.get("https://www.argos.ie")
    acceptCookieBannerArgos(webpage)
    searchForProduct(console, webpage)
    consoles = extractItemsFromPage(console, webpage.page_source)
    webpage.close()
    return consoles


searchArgos()