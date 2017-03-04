import requests
import re
import json
import sys
import time
import random
from MyPrint import MyPrint
from lxml import html  # , etree
from datetime import datetime


class MALScraper:
    attemptsAllowed = 10

    def __init__(self, session=None):
        if session is None:
            session = requests.Session()
        self.session = session

    def session_reset(self, sleepPeriod=0):
        print('Scraper: resetting session')
        self.session.close()
        self.session = None
        if sleepPeriod > 0:
            self.sleep_printed(sleepPeriod)
        self.session = requests.Session()

    def session_close(self):
        if self.session is not None:
            self.session.close()

    @staticmethod
    def sleep_printed(period=30):
        print('Sleeping for ' + str(period) + ' seconds')
        for i in range(period):
            time.sleep(1)
            if (i % 5) == 0:
                print(i, end='', flush=True)
            else:
                print('.', end='', flush=True)
        print(str(period))

    # sleep for some random amount of time between 0.2 and 4 seconds; to avoid http error 429 (too many requests)
    @staticmethod
    def sleep_random():
        randPeriod = float(random.randrange(5, 100)) / float(25)
        time.sleep(randPeriod)

    # returns a tuple containing the attributes of a single anime
    def scrape_anime(self, url):
        # url in form '/anime/[show id]/[show name]'
        # returned anime attributes
        animeID = 0
        animeTitle = ''
        animeTitleEnglish = ''
        animeTitleSynonyms = ''
        animeReleaseDate = None
        animeScoreValue = 0.0
        animeScoreCount = 0
        animeMemberCount = 0
        animeFavouriteCount = 0
        animeImage = ''
        animeStudioList = []
        animeGenreList = []
        # attribute paths/patterns
        aIDPattern = '/anime/(\d+)/'
        aTitlePath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[1]/h1/span/text()'
        sideBarPath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[@id="content"]/table/tr/td[1]/div'
        # - relative to sideBarPath
        aTitleEnglishPath = './div[span/text()="English:"]/text()'
        aTitleSynonymsPath = './div[span/text()="Synonyms:"]/text()'
        aAirDatePath = './div[span/text()="Aired:"]/text()'
        aStudioPath = './div[span/text()="Studios:"]/a'
        studioIDRegex = re.compile('/anime/producer/(\d+)/')  # for match using url from link in side bar
        aGenrePath = './div[span/text()="Genres:"]/a'
        aGenreIDPattern = '/anime/genre/(\d+)/'
        aScoreValuePath = './div[@itemprop="aggregateRating"]/span[@itemprop="ratingValue"]/text()'
        aScoreCountPath = './div[@itemprop="aggregateRating"]/span[@itemprop="ratingCount"]/text()'
        aMemberCountPath = './div[span/text()="Members:"]/text()'
        aFavouriteCountPath = './div[span/text()="Favorites:"]/text()'
        aImageURLPath = './div[1]/a/img/@src'
        aImagePattern = 'https://myanimelist.cdn-dena.com/images/anime/(.*)'  # eg https://myanimelist.cdn-dena.com/images/anime/5/73199.jpg

        success = False
        attempt = 0
        while attempt < MALScraper.attemptsAllowed:
            self.sleep_random()
            animePage = self.session.get('https://myanimelist.net' + url)
            if animePage.status_code == 200:
                htmlTree = html.fromstring(animePage.text)
                # ID
                animeID = int(re.match(aIDPattern, url).group(1))
                # Title
                animeTitle = htmlTree.xpath(aTitlePath, smart_strings=False)[0]
                sideBarTree = htmlTree.xpath(sideBarPath)[0]  # side bar subtree
                # Air Date
                try:
                    airDateStr = sideBarTree.xpath(aAirDatePath, smart_strings=False)[1]  # raw date string
                    tempList = airDateStr.split()
                    airDateStr = tempList[0] + tempList[1] + tempList[2]
                    animeReleaseDate = datetime.strptime(airDateStr, '%b%d,%Y').date().isoformat()
                except:
                    animeReleaseDate = None
                # Title: English
                engList = sideBarTree.xpath(aTitleEnglishPath, smart_strings=False)
                if len(engList) > 1:
                    animeTitleEnglish = engList[1].strip()
                # Title: Synonyms
                synList = sideBarTree.xpath(aTitleSynonymsPath, smart_strings=False)
                if len(synList) > 1:
                    animeTitleSynonyms = synList[1].strip()
                # Score
                animeScoreValue = float(sideBarTree.xpath(aScoreValuePath, smart_strings=False)[0])
                animeScoreCount = int(sideBarTree.xpath(aScoreCountPath, smart_strings=False)[0].replace(',', ''))
                # Members
                animeMemberCount = int(sideBarTree.xpath(aMemberCountPath, smart_strings=False)[1].strip().replace(',', ''))
                # Favourites
                animeFavouriteCount = int(sideBarTree.xpath(aFavouriteCountPath, smart_strings=False)[1].strip().replace(',', ''))
                # Image
                animeImage = re.match(aImagePattern, sideBarTree.xpath(aImageURLPath, smart_strings=False)[0]).group(1)
                # Studios
                for studioLink in sideBarTree.xpath(aStudioPath):
                    studioURL = studioLink.xpath('./@href', smart_strings=False)[0]
                    studioID = studioIDRegex.match(studioURL).group(1)
                    studioName = studioLink.xpath('./text()', smart_strings=False)[0]
                    print(studioID, ':', studioName)
                    animeStudioList.append({
                        'idStudio': studioID,
                        'name': studioName
                    })
                # Genres
                for genreLink in sideBarTree.xpath(aGenrePath):
                    genreURL = genreLink.xpath('./@href', smart_strings=False)[0]
                    genreID = int(re.match(aGenreIDPattern, genreURL).group(1))
                    genreTitle = genreLink.xpath('./text()', smart_strings=False)[0]
                    animeGenreList.append({
                        'idGenre': genreID,
                        'title': genreTitle
                    })
                # animePageResult = [str for str in [s.strip() for s in animePageResult] if str != '']
                success = True
                break
            else:
                print(str(animePage.status_code) + ': ' + animePage.reason)
                if animePage.status_code == 404:
                    success = False
                    break
                else:
                    attempt += 1

        if success:
            return {
                'anime': {
                    'idAnime': animeID,
                    'title': animeTitle,
                    'releaseDate': animeReleaseDate,
                    'titleEnglish': animeTitleEnglish,
                    'titleSynonyms': animeTitleSynonyms,
                    'scoreValue': animeScoreValue,
                    'scoreCount': animeScoreCount,
                    'memberCount': animeMemberCount,
                    'favouriteCount': animeFavouriteCount,
                    'url': url,
                    'image': animeImage,
                },
                'studioList': animeStudioList,
                'genreList': animeGenreList
            }
        elif attempt < MALScraper.attemptsAllowed:  # 404
            return None
        else:
            print('Something went wrong scraping character page. Character: ' + url)
            sys.exit()

    # returns a dictionary containing list of character tuples and a list of staff tuples. each character tuple will contain a list of voice actors tuples.
    def scrape_animestaff(self, url):
        # url in form '/anime/[show id]/[show name]/characters'
        # returned lists
        characterList = []
        staffList = []
        # character attribute paths/patterns
        animeID = int(re.match('/anime/(\d+)/', url).group(1))
        characterPath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[@id="content"]/table/tr/td[2]/div[1]/h2[2]/preceding-sibling::table'
        characterURLPath = './tr/td[2]/a/@href'  # relative to characterPath
        characterIDRegex = re.compile('/character/(\d+)/')  # regex that matches id in url from the Character link
        ## characterNamePath = './tr/td[2]/a/text()'  # relative to characterPath
        characterRolePath = './tr/td[2]/div/small/text()'  # relative to characterPath
        # voice actor attribute paths/patterns
        cVAPath = './tr/td[3]/table/tr/td[1]'  # relative to characterPath
        cVALinkPath = './a/@href'  # relative to VAPath
        personIDRegex = re.compile('/people/(\d+)/')  # regex that matches id in url from the VA link
        ## cVANamePath = './a/text()'  # relative to VAPath
        cVALangPath = './small/text()'  # relative to VAPath
        # staff attribute paths/patterns
        staffPath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[@id="content"]/table/tr/td[2]/div[1]/h2[2]/following-sibling::table/tr'
        staffURLPath = './td[2]/a/@href'
        staffNamePath = './td[2]/a/text()'
        staffPositionsPath = './td[2]/small/text()'

        attempt = 0
        success = False
        while attempt < MALScraper.attemptsAllowed:
            self.sleep_random()
            characterPage = self.session.get('https://myanimelist.net' + url)
            if characterPage.status_code == 200:
                htmlTree = html.fromstring(characterPage.text)
                # Characters
                for characterTree in htmlTree.xpath(characterPath):
                    cURL = characterTree.xpath(characterURLPath, smart_strings=False)[0]
                    cID = int(characterIDRegex.match(cURL).group(1))
                    ## cNameSplit = characterTree.xpath(characterNamePath, smart_strings=False)[0].strip().split(', ')  # character name as a list with whitespace stripped
                    ## cName = ' '.join(reversed(cNameSplit))  # Character Name
                    cRole = characterTree.xpath(characterRolePath, smart_strings=False)[0]
                    cVAList = []
                    # Voice Actors
                    for VA in characterTree.xpath(cVAPath):
                        cVAURL = VA.xpath(cVALinkPath, smart_strings=False)[0]
                        cVAID = int(personIDRegex.match(cVAURL).group(1))
                        cVALang = VA.xpath(cVALangPath, smart_strings=False)[0]
                        cVAList.append({
                            'idPerson': cVAID,
                            'language': cVALang
                        })
                    characterList.append({
                        'idCharacter': cID,
                        'idAnime': animeID,
                        'role': cRole,
                        'voiceActorList': cVAList
                    })
                # Staff
                for staffTree in htmlTree.xpath(staffPath):
                    staffURL = staffTree.xpath(staffURLPath, smart_strings=False)[0]
                    staffID = int(personIDRegex.match(staffURL).group(1))
                    staffName = staffTree.xpath(staffNamePath, smart_strings=False)[0]
                    staffPositions = staffTree.xpath(staffPositionsPath, smart_strings=False)[0].split(", ")
                    staffList.append({
                        'idPerson': staffID,
                        'fullname': staffName,
                        'positions': staffPositions
                    })
                success = True
                break
            else:
                print(str(characterPage.status_code) + ': ' + characterPage.reason)
                if characterPage.status_code == 404:
                    success = False
                    break
                else:
                    attempt += 1

        if success:
            return {
                'CharacterList': characterList,
                'StaffList': staffList
            }
        elif attempt < MALScraper.attemptsAllowed:  # 404
            return None
        else:  # stop scrape so that problem can be found
            print('Something went wrong scraping character page. Character: ' + url)
            sys.exit()

    # returns a dictionary of attributes of a single person from the given url of that person's webpage
    def scrape_person(self, url):
        # url in form '/people/[person id]/[person name]'
        # returned person attributes
        personID = 0
        personName = ''
        personBirthday = ''
        personFavouriteCount = 0
        personImage = ''
        # attribute paths/patterns
        personIDPattern = '/people/(\d+)/'
        personNamePath = '/html/head/meta[@property="og:title"]/@content'
        personBirthdayPath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[@id="content"]/table/tr/td[1]/div[span/text()="Birthday:"]/text()'
        personFavouriteCountPath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[@id="content"]/table/tr/td[1]/div[span/text()="Member Favourites:"]/text()'
        personImageURLPath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[@id="content"]/table/tr/td[1]/div[1]/a/img/@src'
        personImagePattern = 'https://myanimelist.cdn-dena.com/images/voiceactors/(.*)'  # https://myanimelist.cdn-dena.com/images/anime/5/73199.jpg

        success = False
        attempt = 0
        while attempt < MALScraper.attemptsAllowed:
            # errors continually occurring while trying to load page
            if attempt < 10:
                self.sleep_random()
            else:
                attempt = 0
                print('Something went wrong scraping person page. Person: ' + url)
                self.session_reset(30)
            personPage = self.session.get('https://myanimelist.net' + url)
            if personPage.status_code == 200:
                personTree = html.fromstring(personPage.text)
                # ID
                personID = int(re.match(personIDPattern, url).group(1))
                # Name
                personName = personTree.xpath(personNamePath, smart_strings=False)[0].strip()
                # Birthday
                birthdayStr = personTree.xpath(personBirthdayPath, smart_strings=False)[0]  # raw birthday string
                try:
                    tempList = birthdayStr.split()
                    birthdayStr = tempList[0] + tempList[1] + tempList[2]
                    personBirthday = datetime.strptime(birthdayStr, '%b%d,%Y').date().isoformat()
                except:  # if birthday is missing or in odd format
                    personBirthday = None
                # Favourites
                personFavouriteCount = int(personTree.xpath(personFavouriteCountPath, smart_strings=False)[1].strip().replace(',', ''))
                # Image
                personImage = re.match(personImagePattern, personTree.xpath(personImageURLPath, smart_strings=False)[0]).group(1)
                success = True
                break
            else:
                MyPrint.unicode('   Error: ' + url)
                print('    -> ' + str(personPage.status_code) + ': ' + personPage.reason)
                if personPage.status_code == 404:
                    success = False
                    break
                else:
                    attempt += 1

        if success:
            return {
                'idPerson': personID,
                'fullname': personName,
                'birthday': personBirthday,
                'favouriteCount': personFavouriteCount,
                'image': personImage
            }
        elif attempt < MALScraper.attemptsAllowed:  # 404
            return None
        else:  # stop scrape so that problem can be found
            print('Something went wrong scraping character page. Character: ' + url)
            sys.exit()

    # returns a dictionary of attributes of a single person from the given url of that person's webpage
    def scrape_character(self, url):
        # url in form '/people/[person id]/[person name]'
        # returned person attributes
        characterID = 0
        characterName = ''
        characterFavouriteCount = 0
        characterImage = ''
        # attribute paths/patterns
        characterIDPattern = '/character/(\d+)/'
        characterNamePath = '/html/head/meta[@property="og:title"]/@content'
        characterFavouriteCountPath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[@id="content"]/table/tr/td[1]/text()'
        characterImageURLPath = '/html/head/meta[@property="og:image"]/@content'
        characterImagePattern = 'https://myanimelist.cdn-dena.com/images/voiceactors/(.*)'  # https://myanimelist.cdn-dena.com/images/anime/5/73199.jpg

        success = False
        attempt = 0
        while attempt < MALScraper.attemptsAllowed:
            # errors continually occurring while trying to load page
            if attempt < 10:
                self.sleep_random()
            else:
                attempt = 0
                print('Something went wrong scraping person page. Character: ' + url)
                self.session_reset(30)
            characterPage = self.session.get('https://myanimelist.net' + url)
            if characterPage.status_code == 200:
                characterTree = html.fromstring(characterPage.text)
                # ID
                characterID = int(re.match(characterIDPattern, url).group(1))
                # Name
                characterName = characterTree.xpath(characterNamePath, smart_strings=False)[0].strip()
                # Favourites
                characterFavouriteCount = int(re.sub(r'[^\d+]', '', characterTree.xpath(characterFavouriteCountPath, smart_strings=False)[1]))
                # Image
                characterImage = re.match(characterImagePattern, characterTree.xpath(characterImageURLPath, smart_strings=False)[0]).group(1)
                success = True
                break
            else:
                MyPrint.unicode('   Error: ' + url)
                print('    -> ' + str(characterPage.status_code) + ': ' + characterPage.reason)
                if characterPage.status_code == 404:
                    success = False
                    break
                else:
                    attempt += 1

        if success:
            return {
                'idCharacter': characterID,
                'fullname': characterName,
                'favouriteCount': characterFavouriteCount,
                'image': characterImage
            }
        elif attempt < MALScraper.attemptsAllowed:  # 404
            return None
        else:  # stop scrape so that problem can be found
            print('Something went wrong scraping character page. Character: ' + url)
            sys.exit()

    # returns the list of urls from the anime in a given users list
    def scrape_list(self, username):
        # username is a valid MAL username
        # returned list
        animeURLList = []
        # list paths
        oldListPath = '/html/body/div[@id="list_surround"]/table[position() > 3]/tr/td[2 and @class!="table_header"]/a/@href'
        newListJSONPath = '/html/body/div[@id="list-container"]/div[3]/div/table/@data-items'

        attempt = 0
        success = False
        while attempt < MALScraper.attemptsAllowed:
            self.sleep_random()
            listPage = self.session.get('https://myanimelist.net/animelist/' + username + '?status=7')
            if listPage.status_code == 200:
                htmlTree = html.fromstring(listPage.text)
                listClass = htmlTree.xpath('/html/body/@class', smart_strings=False)[0]
                if listClass == 'ownlist':  # older style lists
                    animeURLList = htmlTree.xpath(oldListPath)  # checkout http://lxml.de/xpathxslt.html if not enough
                elif listClass == 'ownlist anime':  # new style lists
                    unparsed_jsonData = htmlTree.xpath(newListJSONPath)  # get json string from data-items attribute from anime list table
                    data = json.loads(unparsed_jsonData[0])  # parse the json data (a long string) into a python list of dictionaries ## data.sort(key=lambda k: k['anime_title'])
                    animeURLList = [anime['anime_url'] for anime in data]  # create list of url's from their dictionary entries
                else:
                    print('Error: private list? (page loaded successfully but unable to retrieve list class)')
                    animeURLList = None
                success = True
                break
            else:
                print('   List Error: ' + username)
                print('    -> ' + str(listPage.status_code) + ': ' + listPage.reason)
                if listPage.status_code == 404:
                    success = False
                    break
                else:
                    attempt += 1

        if success:
            return animeURLList
        elif attempt < MALScraper.attemptsAllowed:
            print('   Private list or invalid username')
            return None
        else:
            print('Something went wrong when scraping list for user: ' + username)
            sys.exit()
