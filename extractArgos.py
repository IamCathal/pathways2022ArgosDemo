from selenium.webdriver.common.keys import Keys
from datetime import datetime
from termcolor import colored
from colorama import init
from bs4 import BeautifulSoup
import time
import re

def extractIndividualConsoles(console, soup):
    consoleList = []
    potentialConsoles = []
    count = 1

    for item in soup.find_all("li", class_="product"):
        noDelivery = item.find("li", class_="nodelivery")
        available = False
        if noDelivery is None:
            available = True
        else:
            available = False

        potentialConsoles.append({
            "link": soup.find("a", id=re.compile(f"(href_{count})"))["href"].strip(),
            "name": soup.find("a", id=re.compile(f"(href_{count})")).get_text().strip(),
            "price": item.find("li", class_="price").get_text().strip(),
            "available": available
        })
        count += 1

    for item in potentialConsoles:
        if "console".lower() in item["name"].lower():
            consoleList.append(item)

    print(f"{colored(f'{getCurrTime()} [Argos: {console.upper()}]', getColor(console))} Found {str(count)} products")
    return consoleList

def extractConsolesFromPage(console, pageSource):
    init()
    soup = BeautifulSoup(pageSource, 'html.parser')
    results = extractIndividualConsoles(console, soup)
    print(f"{colored(f'{getCurrTime()} [Argos: {console.upper()}]', getColor(console))} Found {str(len(results))} {console}")
    for console in results:
        print(f"{getCurrTime()} Product: \t{console['name']}\n\t Price:\t\t{console['price']}\n\t Available:\t{console['available']}")
    return results

def acceptCookieBannerArgos(driver):
    print(f"{colored(f'{getCurrTime()} [Argos]', 'white')} Accepting cookie banner")
    time.sleep(1)
    cookieBanner = driver.find_element("id", "onetrust-accept-btn-handler")
    cookieBanner.click()
    time.sleep(2)

def searchForProduct(word, driver):
    print(f"{colored(f'{getCurrTime()} [Argos: {word.upper()}]', getColor(word))} Searching for " + word)
    element = driver.find_element("id", "search")
    for letter in word:
        element.send_keys(letter)
        time.sleep(0.1)
    element.send_keys(Keys.RETURN)

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