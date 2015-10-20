# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 00:48:45 2015
@author: keyur

### Name: Keyur Doshi
### Student ID: 10405923
### BIA 660B Mid Term Project

Description:

Mid Term project which will perform the following:

Step 1: Select 4 different websites that include reviews on TVs. The reviews should include text, a date of submission, and a star rating.

Step 2: Collect at least 1000 TV reviews from each of the 4 websites. Use a different python script for each website.

Step 3: Store all the reviews from all 4 websites in a single file called "reviews.txt". The file should include the following TAB-separated columns:

: website where the review came from (e.g. amazon.com).
: the FULL review text, exactly as it appears on the website.
: the review's rating 
: the review's date of submission, as it appears on the website.
"""

#Importing library
import sys,time,urllib2
from bs4 import BeautifulSoup

#Capturing the start time of this program
start_time = time.clock()

#Website used for parsing
website = str('flipkart.com')

#Initializing browser
browser=urllib2.build_opener()
browser.addheaders=[('User-agent', 'Mozilla/5.0')]

#create a new file and open a connection to it.
fileWriter=open('reviews.txt','w')
fileReader=open('in.txt')

#Initializing index
index=0

#Creating the list to store all the records 
ReviewList = []
RatingList=[]
DateList=[]

for line in fileReader:
    #Fetch the url from file in.txt    
    reviewlink = line.strip()   
    print reviewlink

    if reviewlink:
        page=0    
        while True:
            url = reviewlink + str(page)
            #Opening the url    
            try:
                response=browser.open(url,timeout=(5.0))
                time.sleep(2) 
            except Exception as e:
                error_type, error_obj, error_info = sys.exc_info()
                print 'ERROR FOR URL:',url
                print error_type, 'Line:', error_info.tb_lineno
                continue
            
            #Initializing Beautifulsoup object
            html = response.read()
            bsObj = BeautifulSoup(html)
            
            for date in bsObj.findAll("div",{"class":"date line fk-font-small"}):
                DateList.append(date.text.strip())
        
            #Will parse the Reviews and append it to the list
            for review in bsObj.findAll("span",{"class":"review-text"}):
                ReviewList.append(review.text.replace('\n', ' ').strip())
    
            #Will parse the Ratings and append it to the list
            for rating in bsObj.findAll("div",{"class":"fk-stars"}):
                RatingList.append(rating['title'].strip())
    
            #Will check if reviews are available 
            stop = bsObj.find("div",{"class":"fk-text-center fk-font-big"})
            if stop:
                print 'Exiting..No more reviews for this product'
                break
            
            page+=10
            print 'Reviews Collected',len(ReviewList)
            
            #Comparing length and writing data to file.            
            if len(DateList) == len(ReviewList) == len(RatingList):
                index = 0
                while (index < len(ReviewList)):
                    fileWriter.write(website + '\t' + ReviewList[index].encode('utf8') +'\t'+ RatingList[index].encode('utf8') + '\t' + DateList[index].encode('utf8')+'\n')
                    index+=1
            else:
                print 'Some issue while writing data to file as records all records are not fetched.'
                
    else:
        print 'Parsing completed'

print 'Total Reviews Collected',len(ReviewList)

#Printing the running time   
print time.clock() - start_time, "seconds"

#Closing the FileReader    
fileReader.close()

#Closing the File Writer
fileWriter.close()