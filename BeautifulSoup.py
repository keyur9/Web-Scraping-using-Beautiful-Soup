# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 12:01:12 2015
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
#Importing libraries
import sys,time,socket
from bs4 import BeautifulSoup
import mechanize
from urllib2 import *
import urllib2

#Setting socket timeout
socket.setdefaulttimeout(20)

#Capturing the start time of this program
start_time = time.clock()

#Mechanize the browser
br = mechanize.Browser()


browser=urllib2.build_opener()
browser.addheaders=[('User-agent', 'Mozilla/5.0')]

#create a new file and open a connection to it.
#fileWriter=open('reviewk3.txt','w')
fileWriter=open('reviews.txt','a')
fileReader=open('in.txt')

#Creating the list to store all the records 
nameList = list()
DateList = list()
ReviewList = list()
RatingList = list()

#Site used for parsing
sitename = 'www.flipkart.com'

#Setting the read timeout
read_timeout = 1.0

for line in fileReader:
    #Fetch the url from file in.txt    
    page = 0
    reviewlink = line.strip()    
    url = reviewlink + str(page)
    
    #Opening the url    
    try: 
        br.set_handle_refresh(False)
        response=br.open(url,timeout=(5.0)) 
    except Exception as e:
        error_type, error_obj, error_info = sys.exc_info()
        print 'ERROR FOR URL:',url
        print error_type, 'Line:', error_info.tb_lineno
        continue
    except urllib2.URLError, e:
        print "Oops, timed out?"
        pass
    except socket.timeout:
        print "Timed out!"
        pass
    except:
        myresponse = []
        pass
    
    html = response.read()
    bsObj = BeautifulSoup(html)
    
    del ReviewList[:]
    del DateList[:]
    del RatingList[:]
    
    #Will parse the Dates and append it to the list
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
    
    #Calculating the lenghts
    lenDate = len(DateList)
    lenReview = len(ReviewList)
    lenRating = len(RatingList)

    #Comparing length and writing data to file.
    if lenDate == lenReview == lenRating:
        index = 0
        while (index < lenReview):
            fileWriter.write(sitename + '\t' + ReviewList[index].encode('utf8') +'\t'+ RatingList[index].encode('utf8') + '\t' + DateList[index].encode('utf8')+'\n')
            index+=1
    else:
        print 'Some issue while writing data to file as records all records are not fetched.'

    nextpage = 10
    while True:
        newlink = 'http://www.flipkart.com/micromax-32b200hdi-81-cm-32-led-tv/product-reviews/ITMDTZ6NN78YHSZY?pid=TVSDTZ6NN78YHSZY&rating=1,2,3,4,5&reviewers=all&type=top&sort=most_helpful&start=' + str(nextpage)
        newlink = reviewlink + str(nextpage)    
            
        #Opening the url          
        try:
            br.set_handle_refresh(False)            
            myresponse=br.open(newlink,timeout=(10.0))
        except Exception as e:
            error_type, error_obj, error_info = sys.exc_info()
            print 'ERROR FOR URL:',newlink
            print error_type, 'Line:', error_info.tb_lineno
            continue
        except urllib2.URLError, e:
            print "Oops, timed out?"
            pass
        except socket.timeout:
            print "Timed out!"
            pass
        except:
            myresponse = []
            pass
        
        myhtml = myresponse.read()
        bsObj = BeautifulSoup(myhtml)
        
        del ReviewList[:]
        del DateList[:]
        del RatingList[:]

        #Will parse the Dates and append it to the list
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
       
        nextpage = nextpage + 10
        print 'Next Page', nextpage

        #Calculating the lenghts
        lenDate = len(DateList)
        lenReview = len(ReviewList)
        lenRating = len(RatingList)
        
        #Comparing length and writing data to file.        
        if lenDate == lenReview == lenRating:
            index = 0
            while (index < lenReview):
                fileWriter.write(sitename + '\t' + ReviewList[index].encode('utf8') +'\t'+ RatingList[index].encode('utf8') + '\t' + DateList[index].encode('utf8')+'\n')
                index+=1
        else:
            print 'Some issue while writing data to file as records all records are not fetched.'
    
#Printing the running time   
print time.clock() - start_time, "seconds"

#Closing the FileReader    
fileReader.close()

#Closing the File Writer
fileWriter.close()
