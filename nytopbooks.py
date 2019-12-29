# -*- coding: utf-8 -*-
"""
@author: Samip
"""

"""This scripts aims to get all book names on historic New York Time Best Sellers (Business section). The purpose is to:
1. help to compile my reading list in 2020
2. serve as reference to use Python for simple web analytics"""

#One interesting finding: No best seller list for 2015-08, maybe a bug in New York Times system

"""For the web element, the top 10 list for each month is organized inside an ordered list (“ol”) with class name “css-12yzwg4”. 
The contents are saved inside the division (“div”) with class name “css-xe4cfy”, and each book is one item of the contents. 
The book title has “h3” tag with class name “css-5pe77f”, and book author has “p” tag with class name “css-hjukut”."""


#Import libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup

#Create a DataFrame to store result
df = pd.DataFrame()

d = {1 : 'audio-fiction', 2 : 'audio-nonfiction', 3 : 'business-books', 4 : 'science', 5 : 'sports'}

choice = int(input("Enter 1 for Audio Fiction, 2 for Audio NonFiction, 3 for Business Books, 4 for Science and 5 for Sports: "))

"""The list on website starts from November 2013, hence the starting year is 2013.
URL pattern is https://www.nytimes.com/books/best-sellers/2019/08/01/business-books/, where only year and month changes """
try:
    for year in range(2013, 2020):
        for month in range(1, 13):
           
            
            url = "https://www.nytimes.com/books/best-sellers/{0}/{1}/01/{2}/".format(year, str(month).zfill(2), d[choice])
            page = requests.get(url)
            
            #Ensure the proper result is obtained
            if page.status_code != 200:
                continue
            
            #Use Beautifulsoup to parse right elements 
            soup = BeautifulSoup(page.text, 'html.parser')
            top_books = soup.findAll("ol", {"class" : "css-12yzwg4"})[0].findAll("div", {"class" : "css-xe4cfy"})
    
            #Loop through each year and month and get the best seller, and append that in dataframe
            for i in range(len(top_books)):
                book = top_books[i].contents[0]
                title = book.findAll("h3", {"class" : "css-5pe77f"})[0].text
                author = book.findAll("p", {"class" : "css-hjukut"})[0].text
                author = author[3:]
                review = book.get("href")
                
                #Save each result in Pandas Series and append to dataFrame           
                item = pd.Series([year, month, title, author, i + 1, review], index = ['Year', 'Month', 'Title', 'Author', 'Rank', 'Review'])
                df = df.append(item, ignore_index = True, sort = False)
                
    #Save the result to a pickle file for analysis
    df.to_pickle("nytopbooks.pkl")
    df.to_csv('NewYork Top Books.csv', index = False)

except KeyError:
    print("Incorrect choice")          