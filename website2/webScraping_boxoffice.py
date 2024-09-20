from types import NoneType

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from numpy.matlib import empty
from pandas.plotting import table
from six import class_types

# initializing lists to store all information
movie_titles = []
genre = []
actor = []
movie_length = []
movie_releaseDate = []
ccc_info = []

# downloading info from the website
htmlLink =  'https://www.boxofficemojo.com/calendar/?ref_=bo_nb_ydw_tab'
header = {'Accept-Language': 'en-US,en;q=0.8'}
response = requests.get(htmlLink, headers = header)
soup = BeautifulSoup(response.text, 'html.parser')

# getting movie name
movieInfo = soup.find_all('div', class_="a-section a-spacing-none mojo-schedule-release-details")

# function to remove new lines for the genres
def line_remover(list):
    tempList = []
    for ele in list:
        tempList.append(re.sub('\n', '', ele))
    return tempList


# split into smaller segments to get actor and movie length
for i in range(len(movieInfo)):
    moviePeople = movieInfo[i].find_all('div', class_="a-section a-spacing-none")
    if not moviePeople:
        actor.append("N/A")
        movie_length.append("N/A")
    else:
        if len(moviePeople) == 3:
            if len(moviePeople[1].text) > 1:
                actor.append(re.sub("^With: ", '', moviePeople[1].text))
            else:
                actor.append("N/A")
            if len(moviePeople[2].text) > 1:
                movie_length.append(moviePeople[2].text)
            else:
                print("meoweeeerrrr")
                movie_length.append("N/A")
        else:
            if len(moviePeople[0].text) > 1:
                actor.append(re.sub("^With: ", '', moviePeople[0].text))
            else:
                actor.append("N/A")
            if len(moviePeople[1].text) > 1:
                movie_length.append(moviePeople[1].text)
            else:
                print("meow")
                movie_length.append("N/A")

# returns div
# refer to movie info when trying to get info about the movie e.g., movieInfo[0].find('h3') etc.

# getting headers (movie names)
for i in range(len(movieInfo)):
    # appending movie name onto list
    movie_name = movieInfo[i].find('h3').text
    movie_titles.append(movie_name)

# getting release dates
tableInfo = soup.find("div", id="table")
tableBody = tableInfo.find_all("tr")
dateRows = tableInfo.find_all("tr", class_="mojo-group-label")

for i in range(len(dateRows)):

    if i < len(dateRows) - 1:
        currentDate = dateRows[i]
        nextDate =  tableBody.index(dateRows[i+1])
    else:
        currentDate = dateRows[i]
        nextDate = tableBody.index(tableBody[-1]) + 1

    for j in range(tableBody.index(currentDate) + 1, nextDate):
        movie_releaseDate.append(dateRows[i].text)

# getting genre
# movie_genre = tableInfo.find_all("div", class_="a-section a-spacing-none mojo-schedule-genres")
newList = []
for i in range(len(movieInfo)):
    # movie genre
    movie_genre = movieInfo[i].find("div", class_="a-section a-spacing-none mojo-schedule-genres")
    newList.append(movie_genre)

    # actor
    movie_actor = movieInfo[i]

for indiv in newList:
    if isinstance(indiv, NoneType):
        genre.append("N/A")
    else:
        genre.append(indiv.text)

genre = line_remover(genre)

# print(f'genres: {genre} ({len(genre)})')
print(f'dates: {movie_releaseDate}')
print(f'movies: {(movie_titles)}')

df = pd.DataFrame(
    {"Movie Name": movie_titles,
     "Genres": genre,
     "Actor(s)": actor,
     "Movie Run Time": movie_length,
     "Release Date": movie_releaseDate}
    )

print (df.head())

df.to_csv('boxoffice.csv', index=False)

# find table body > find_all table row > loop through list, if tr.class = "mojo-group-label" extract date
# >> append date x amount of times | x is number of tr(table row) until next "mojo-group-label"
# >>> if end of list && no more "mojo-group-label", the number is the last number

# information to scrape:
# movie name | genre | actor(s) | movie length | movie release date
