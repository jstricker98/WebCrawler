
import urllib.request
from bs4 import BeautifulSoup
from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls') #windows OS
    else:
        _ = system('clear') #other OS

def getLinks(url):
    try:
        encodedSite = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        return []
    except urllib.error.URLError as e:
        return []
    else:
        siteBytes = encodedSite.read()
        webSite = siteBytes.decode()
        encodedSite.close()

        soup = BeautifulSoup(webSite, "html.parser")

        listOfLinks = []

        for a in soup.find_all('a', href=True):
            link = a['href']
            if "https://" in link:
                if ".edu" in link and ".edu/" not in link:
                    listOfLinks.append(link)
                elif ".org" in link and ".org/" not in link:
                    listOfLinks.append(link)
                elif ".gov" in link and ".gov/" not in link:
                    listOfLinks.append(link)
            elif link[0] == '/':
                listURL = url.split('/')
                listOfLinks.append(listURL[0] + "//" + listURL[2] + link)
        return listOfLinks

clear()

url = input("Enter URL: ")
numOfHops = int(input("Enter number of hops (0 will only grab links from the given url): "))

clear()

links = getLinks(url)

checkedLinks = [url]

print("Number of hops left: " + str(numOfHops))
print("Links found: " + str(links.__len__()))

while (numOfHops != 0):
    newLinks = []
    linksToAdd = []
    for link in links:
        if link not in checkedLinks:
            newLinks = getLinks(link)
            checkedLinks.append(link)
            for newLink in newLinks:
                if newLink not in checkedLinks:
                    linksToAdd.append(newLink)
            clear()
            print("Number of hops left: " + str(numOfHops))
            print("Links found: " + str(links.__len__() + linksToAdd.__len__()))
            print("Current link: " + link)
    links = links + linksToAdd
    numOfHops = numOfHops -1
    clear()
    print("Number of hops left: " + str(numOfHops))
    print("Links found: " + str(links.__len__()))
    print("Current link: ")

if input(str(links.__len__()) + " link(s) were found.\n\
Would you like to view them? (yes or no): ") == "yes":
    print(links)