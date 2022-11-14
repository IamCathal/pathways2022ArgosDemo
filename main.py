from extractArgos import *
from selenium import webdriver

def searchArgos():
    xboxesFromArgos = getConsoleFromArgos("xbox series x console")
    playStationsFromArgos = getConsoleFromArgos("playstation 5 console")

def getConsoleFromArgos(console):
    webpage = webdriver.Chrome()
    webpage.get("https://www.argos.ie")
    acceptCookieBannerArgos(webpage)
    searchForProduct(console, webpage)
    return(extractConsolesFromPage(console, webpage.page_source))

searchArgos()