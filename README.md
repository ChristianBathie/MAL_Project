This is a personal project for learning purposes with the aim of being able to provide 
MyAnimeList.net (MAL) users with statistics and recommendations based on the their anime list.
The main focus is intended to be on voice actors and staff over other data.

#####Basic Operatation:
- Users will enter their MAL username on the home page
- Server side will read/scrape their MAL anime list page
- Relevent anime data will be retrieved from the MySQL DB
  * any anime data that isn't already in the DB will be scraped from the website 
- User will be directed to a page showing their list on anime with a number of options
- The page will be updated mostly asynchonously with Javascript where possible
  * larger features may be given their own page if appropriate 

#####Potential Features:
- Sortable/Filterable table of anime, staff, studios, characters with relevent links and stats
- Table of favourite voice actors and staff based on shows in their anime list
- Anything else that feels appropriate once I'm further along in the project
	
#####Recommendations to be produced based on things like:
- Personal scoring of shows on their list
- Sitewide average scores of shows
- Show recency
- Common voice actors and production staff among ther watched shows
  - eg a voice actor of a main character in a show they rated an 8 may be given a higher weighting than a voice actor of a supporting character from a show they rated a 9 
- Other typical things like studio, genre, etc
- Weightings based on recency, personal and overall scores

#####This project consists of:
- Webscraper (Python) [working: needs revision]
- Relational database (MySQL) [complete]
- Server side (NodeJS) [learning/early stages]
- Client side (HTML,CSS etc...) [not started]

####TODO
1. Python websraper and MySQL DB: adding more data
  * extend scraper to collect this additional data
2. Node.js server: serving content from database
  * learn more about Node.js 
  * get server class working with basic functionality (serving content from MySQL DB) 
  * see what needs to be done from there (eg figuring out how to handle more processor heavy queries/operations) 
3. Webpage: HTML/CSS/JS
  * display all the information nicely 
	
