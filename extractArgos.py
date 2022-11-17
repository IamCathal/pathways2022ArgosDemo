from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
from termcolor import colored
from colorama import init
from bs4 import BeautifulSoup
import time
import re
import os

def extractIndividualItem(itemName, soup):
    itemList = []
    potentialItems = []
    count = 1

    for item in soup.find_all("li", class_="product"):
        noDelivery = item.find("li", class_="nodelivery")
        available = False
        if noDelivery is None:
            available = True
        else:
            available = False

        potentialItems.append({
            "link": soup.find("a", id=re.compile(f"(href_{count})"))["href"].strip(),
            "name": soup.find("a", id=re.compile(f"(href_{count})")).get_text().strip(),
            "price": item.find("li", class_="price").get_text().strip(),
            "available": available
        })
        count += 1

    for item in potentialItems:
        if "console".lower() in item["name"].lower() or "e-move hydro" in item["name"].lower() or "9ft indoor table" in item["name"].lower() or "- burgandy" in item["name"].lower():
            itemList.append(item)

    print(f"{colored(f'{getCurrTime()} [Argos: {itemName.upper()}]', getColor(itemName))} Found {str(count)} products")
    return itemList

def extractItemsFromPage(console, pageSource):
    init()
    soup = BeautifulSoup(pageSource, 'html.parser')
    results = extractIndividualItem(console, soup)
    print(f"{colored(f'{getCurrTime()} [Argos: {console.upper()}]', getColor(console))} Found {str(len(results))} {console}")
    for console in results:
        print(f"{getCurrTime()} Product: \t{console['name']}\n\t Price:\t\t{console['price']}\n\t Available:\t{console['available']}")
    time.sleep(2)
    return results

def printIntro():
    print("""
                                                     _                        _            
     /\                           /\        | |                      | |           
    /  \   _ __ __ _  ___  ___   /  \  _   _| |_ ___  _ __ ___   __ _| |_ ___ _ __ 
   / /\ \ | '__/ _` |/ _ \/ __| / /\ \| | | | __/ _ \| '_ ` _ \ / _` | __/ _ \ '__|
  / ____ \| | | (_| | (_) \__ \/ ____ \ |_| | || (_) | | | | | | (_| | ||  __/ |   
 /_/    \_\_|  \__, |\___/|___/_/    \_\__,_|\__\___/|_| |_| |_|\__,_|\__\___|_|   
                __/ |                                                              
               |___/                                                               
    
    """)
    print("======   Automatically find out if your presents are in stock in argos    =====")
    print("===============================================================================")

def acceptCookieBannerArgos(driver):
    win = driver.find_element(By.TAG_NAME,"html")
    #for zoom out this will change to 90% if you need more copy and paste it again. Or you can change - to + for zoom in.    
    win.send_keys(Keys.CONTROL + "+")
    win.send_keys(Keys.CONTROL + "+")
    win.send_keys(Keys.CONTROL + "+")
        
    print(f"{colored(f'{getCurrTime()} [Argos]', 'white')} Accepting cookie banner")
    time.sleep(2)
    
    try:
        cookieBanner = driver.find_element("id", "onetrust-accept-btn-handler")
        cookieBanner.click()
    except Exception as e:
        print(f"CRASHED: {e}")
        driver.close()
        quit()
    time.sleep(3)

def searchForProduct(word, driver):
    print(f"{colored(f'{getCurrTime()} [Argos: {word.upper()}]', getColor(word))} Searching for " + word)
    element = driver.find_element("id", "search")
    for letter in word:
        element.send_keys(letter)
        time.sleep(0.04)
    element.send_keys(Keys.RETURN)
    time.sleep(3)

def getColor(console):
    console = console.lower()
    if console == "playstation 5 console":
        return "blue"
    elif console == "xbox series x console":
        return "green"
    else:
        return "white"

def getCurrTime():
    now = datetime.now()
    return  now.strftime("%H:%M:%S")

def getIntPrice(stringPrice):
    return float(stringPrice.replace("€",""))

def getTotalPrice(items):
    totalPrice = 0
    if len(items) != 0:
        for item in items:
            if item != []:
                totalPrice += getIntPrice(item[0]["price"])
    
    totalItemsAvailable = 0
    if len(items) != 0:
        for item in items:
            if item != []:
                if item[0]["available"] == True:
                    totalItemsAvailable += 1
                
    extraMessage = ""
    if totalPrice == 0:
        extraMessage += ". Looks like its going to be a rough Christmas!"
    print(f"All {totalItemsAvailable} in-stock items cost €{totalPrice}{extraMessage}")
    print("===============================================================================")
