from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# method to get number of works from text full of unnecessary information
def getNumber(text):
    currChar = 'x'
    sb = ""

    # based on format in the html, the number of works starts at index max - 4
    index = len(text) - 4

    # for works whose works count isn't given
    if text[index+2] != ")":
        return "N/A"
    else:
        while currChar != "(":
            currChar = text[index]
            sb = sb + currChar
            index = index - 1
            currChar = text[index]

    return sb[::-1]

# list to store all info
media_types = []
fandom_names = []
works = []
link_to_fandom = []
link_to_media = []

# Downloading ao3 info
headers = {'Accept-Language': 'en-US,en;q=0.8'}
url = 'https://archiveofourown.org/media'
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# get boxes that encapsulate information
listbox = soup.find_all('li', class_="medium listbox group")
print(f'number of elements: {len(listbox)}')

for order in range(len(listbox)):
    # get number of fandoms per box
    ordered_list = listbox[order].find('ol', class_="index group")
    num_fandoms = len(ordered_list.find_all('li'))
    list_fandomNames = ordered_list.find_all('li')

    for i in range(num_fandoms):
        # getting media type
        media_types.append(listbox[order].find('h3', class_="heading").text)
        # fandom name
        fandom_names.append(list_fandomNames[i].a.text)
        # fandom link
        link_to_fandom.append(list_fandomNames[i].a.attrs.get('href'))
        # fandom works
        works.append(getNumber(list_fandomNames[i].text))
        # getting media link
        link_to_media.append(listbox[order].find('h3', class_="heading").a.attrs.get('href'))

df = pd.DataFrame(
    {"Media Type": media_types,
     "Fandom Names": fandom_names,
     "Number of Works": works,
     "Fandom Link": link_to_fandom,
     "Media Link": link_to_media}
    )

print (df.head())

df.to_csv('archiveofourown.csv', index=False)
# what to get from the ao3 all fandoms page:
# media | fandom name | works | link to fandom | link to works of the same media
