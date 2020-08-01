#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:50:00 2020

@author: skylarronkihn
"""


import requests
from bs4 import BeautifulSoup

def imdb() :
    
    # gets the url for the IMDB top 250
    main_url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    req = requests.get(main_url)
    
    
    if req.status_code==200:
        soup = BeautifulSoup(req.text, 'html.parser')
        movies = soup.find_all('tr')
        movies.pop(0)
        
        years = []
        ratings = []
        min_year = 2050
        max_year = 0
        
        # gathers information about each movie
        for movie in movies:
            year = movie.find('span', class_='secondaryInfo').text.strip()
            num = int(year[1: 5])
            years.append(num)
            
            if num < min_year:
                min_year = num
                
            if num > max_year:
                max_year = num
                
            rate = movie.find('td', class_='ratingColumn imdbRating').text
            rating = float(rate.strip())
            ratings.append(rating)
            
        
        print("Some statistics about the 250 Top Rated Movies:\n")
        print("Average year: " + str(average(years)))
        print("Movie years: " + str(min_year) + " - " + str(max_year))
        print("Average rating: " + str(average(ratings)))
        print("\n")
        
    else:
        print("Error")
    
    # user can choose a movie to learn more about
    val = int(input("Choose a ranking to learn more about that movie (Between"
                    + " 1 and 250):\n"))
    
    # if the number is not valid, the url goes to the first movie
    if val > 0 and val < 251:
        movie = movies[val - 1]
        title = movie.find('td', class_='titleColumn')
        url = "https://www.imdb.com" + title.find('a').get('href')
    else: 
        movie = movies[0]
        title = movie.find('td', class_='titleColumn')
        url = "https://www.imdb.com" + title.find('a').get('href')
    
    resp = requests.get(url)
    
    if resp.status_code==200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        description = soup.title.string
        index = description.find(" (")
        title = description[0: index]
        date = description[(index + 2): description.find(')')]
        
        director = soup.find(class_="credit_summary_item").a.text
        
        stats = soup.find('div', class_='subtext').text.strip()
        r = stats[0: stats.find("|")].strip()
        time = stats[stats.find("|") + 1: findNum(stats, "|", 2)].strip()
        genre = stats[findNum(stats, "|", 2) + 1: findNum(stats, "|", 3)]
        
        
        print("\nMovie: " + title)
        print("Year released: " + date)
        print("Director: " + director)
        print("Rating: " + r)
        print("Running time: " + time)
        print("Genre: " + genre.strip())
        
        
    else:
        print("Error")
    
def average(l) :
    return sum(l) / len(l)  

# finds the nth instance of a substring
def findNum(text, char, index):
    count = -1
    for i in range(0, index):
        count = text.find(char, count + 1)
        
    return count

        
imdb()