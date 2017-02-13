import requests, re, json, sys, time, maldb, random
from lxml import html,etree
from datetime import datetime

def printUnicode(output):
    try:
        print(output)
    except UnicodeEncodeError:
        for c in output:
            try:
                print(c, end='')
            except UnicodeEncodeError:
                print('[unicode]', end='')
        print()

def animeScrape(session, url):
    # url in form '/anime/[show id]/[show name]'
    
    animeID = 0
    animeTitle = ''
    animeTitleEnglish = ''
    animeTitleSynonyms = ''
    animeAirDate = None
    animeURL = url
    animeStudios = []
    
    aIDPattern = '/anime/(\d+)/'
    aTitlePath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[1]/h1/span/text()'
    sideBarPath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[@id="content"]/table/tr/td[1]/div'
    aTitleEnglishPath = './div[span/text()="English:"]/text()'  # relative to sideBarPath
    aTitleSynonymsPath = './div[span/text()="Synonyms:"]/text()'# relative to sideBarPath
    aAirDatePath = './div[span/text()="Aired:"]/text()'         # relative to sideBarPath
    aStudiosPath = './div[span/text()="Studios:"]/a'            # relative to sideBarPath
    studioIDRegex = re.compile('/anime/producer/(\d+)/')        # for matching url from link in side bar
    
    attempt = 0
    while(attempt < 7):
        time.sleep(attempt)
        animePage = session.get('https://myanimelist.net' + url)
        
        if (animePage.status_code == 200):
            htmlTree = html.fromstring(animePage.text)
            animeID = int(re.match(aIDPattern, url).group(1))                                           # ID
            animeTitle = htmlTree.xpath(aTitlePath, smart_strings=False)[0]                             # Title
            sideBarTree = htmlTree.xpath(sideBarPath)[0]                                                # - side bar subtree
            try:
                airDateStr = sideBarTree.xpath(aAirDatePath, smart_strings=False)[1]                    # - raw date string
                tempList = airDateStr.split()
                airDateStr = tempList[0] + tempList[1] + tempList[2]
                animeAirDate = datetime.strptime(airDateStr, '%b%d,%Y').date().isoformat()              # Date Aired
            except:
                animeAirDate = None
                
            engList = sideBarTree.xpath(aTitleEnglishPath, smart_strings=False)
            if len(engList)>1: animeTitleEnglish = engList[1].strip()   # Title: English
            synList = sideBarTree.xpath(aTitleSynonymsPath, smart_strings=False)
            if len(synList)>1: animeTitleSynonyms = synList[1].strip()  # Title: Synonyms
            
            for studioLink in sideBarTree.xpath(aStudiosPath):
                studioURL = studioLink.xpath('./@href', smart_strings=False)[0]
                studioID = studioIDRegex.match(studioURL).group(1)                                      # Studio ID
                studioName = studioLink.xpath('./text()', smart_strings=False)[0]                       # Studio Name
                animeStudios.append((studioID, studioName, studioURL))                                  # - add studio tuple to list
            #animePageResult = [str for str in [s.strip() for s in animePageResult] if str != '']
            break
        else:
            print(str(animePage.status_code) +': '+ animePage.reason)       
            if (animePage.status_code != 404):
                attempt += 1
            else:
                return None
    if (attempt == 7):
        print('Something went wrong scraping character page. Character: ' + url)
        sys.exit()
    
    return (animeID, animeTitle, animeAirDate, animeTitleEnglish, animeTitleSynonyms, url, animeStudios) # change to dictionary?

def staffScrape(session, url):
    # url in form '/anime/[show id]/[show name]/characters'
    characterList = []
    staffList = []
    
    animeID = int(re.match('/anime/(\d+)/', url).group(1))
    characterPath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[@id="content"]/table/tr/td[2]/div[1]/h2[2]/preceding-sibling::table'
    characterURLPath = './tr/td[2]/a/@href'             # relative to characterPath
    characterIDRegex = re.compile('/character/(\d+)/')  # regex that matches id in url from the Character link
    characterNamePath = './tr/td[2]/a/text()'           # relative to characterPath
    characterRolePath = './tr/td[2]/div/small/text()'   # relative to characterPath
    cVAPath = './tr/td[3]/table/tr/td[1]'               # relative to characterPath
    cVALinkPath = './a/@href'                           # relative to VAPath
    personIDRegex = re.compile('/people/(\d+)/')        # regex that matches id in url from the VA link
    cVANamePath = './a/text()'                          # relative to VAPath
    cVALangPath = './small/text()'                      # relative to VAPath
    
    staffPath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[@id="content"]/table/tr/td[2]/div[1]/h2[2]/following-sibling::table/tr'
    staffURLPath = './td[2]/a/@href'
    staffNamePath = './td[2]/a/text()'
    staffPositionsPath = './td[2]/small/text()'
    
    attempt = 0
    while(attempt < 8):
        randSleep = float(random.randrange(1,100))/float(25)
        time.sleep(randSleep)
        characterPage = session.get('https://myanimelist.net' + url)
        
        if (characterPage.status_code == 200):
            htmlTree = html.fromstring(characterPage.text)
            
            for characterTree in htmlTree.xpath(characterPath):
                cURL = characterTree.xpath(characterURLPath, smart_strings=False)[0]
                cID = int(characterIDRegex.match(cURL).group(1))                        # Character ID
                cNameSplit = characterTree.xpath(characterNamePath, smart_strings=False)[0].strip().split(', ') # Character Name
                cName = ' '.join(reversed(cNameSplit))
                cRole = characterTree.xpath(characterRolePath, smart_strings=False)[0]  # Character Role
                cVAList = []
                for VA in characterTree.xpath(cVAPath):
                    cVAURL = VA.xpath(cVALinkPath, smart_strings=False)[0]              # VA URL
                    cVAID = int(personIDRegex.match(cVAURL).group(1))                   # VA ID
                    cVAName = VA.xpath(cVANamePath, smart_strings=False)[0]             # VA Name
                    cVALang = VA.xpath(cVALangPath, smart_strings=False)[0]             # VA Language
                    cVAList.append((cVAID, cVAName, cVAURL, cVALang))
                characterList.append((cID, animeID, cName, cRole, cURL, cVAList))
                
            for staffTree in htmlTree.xpath(staffPath):
                staffURL = staffTree.xpath(staffURLPath, smart_strings=False)[0]
                staffID = int(personIDRegex.match(staffURL).group(1))
                staffName = staffTree.xpath(staffNamePath, smart_strings=False)[0]
                staffPositions = staffTree.xpath(staffPositionsPath, smart_strings=False)[0]
                staffList.append((staffID, staffName, staffURL, staffPositions))
                
            break
            
        else:
            print(str(characterPage.status_code) +': '+ characterPage.reason)       
            if (characterPage.status_code != 404):
                attempt += 1
            else:
                return None
    if (attempt == 8):
        print('Something went wrong scraping character page. Character: ' + url)
        sys.exit()
    return (characterList, staffList)
    
def personScrape(session, url):
    # url in form '/people/[person id]/[person name]'
    personID = 0
    personName = ''
    personBirthday = ''
    
    personIDPattern = '/people/(\d+)/'
    personNamePath = '/html/head/meta[@property="og:title"]/@content'
    personBirthdayPath = '/html/body/div[@id="myanimelist"]/div[3]/div[@id="contentWrapper"]/div[@id="content"]/table/tr/td[1]/div[span/text()="Birthday:"]/text()'
    
    attempt = 0
    success = False
    while(success == False):
        randSleep = float(random.randrange(1,100))/float(25)
        time.sleep(randSleep)
        personPage = session.get('https://myanimelist.net' +  url)
        if (personPage.status_code == 200):
            personTree = html.fromstring(personPage.text)
            
            personID = int(re.match(personIDPattern, url).group(1))                                 # ID
            personName = personTree.xpath(personNamePath, smart_strings=False)[0].strip()           # Name
            birthdayStr = personTree.xpath(personBirthdayPath, smart_strings=False)[0]              # - raw birthday string
            try:
                tempList = birthdayStr.split()
                birthdayStr = tempList[0] + tempList[1] + tempList[2]
                personBirthday = datetime.strptime(birthdayStr, '%b%d,%Y').date().isoformat()        # Birthday
            except:
                personBirthday = None
            success == True
        else:
            printUnicode('   Error: ' + url)
            print('    -> '+ str(personPage.status_code) +': '+ personPage.reason)
            if (personPage.status_code != 404):
                attempt += 1
            else:
                return None
        if (attempt == 10 && success == False):
            attempt = 0
            print('Something went wrong scraping person page. Person: ' + url)
            print('Sleeping for 30 seconds')
            for i in range(30):
               time.sleep(1)
               if i%5 == 0: print(i, end='', flush=True)
               else: print('.', end='', flush=True)
            print('30')
    return (personID, personName, personBirthday, url)

 
def listScrape(session, username):
    
    resultList = []
    attempt = 0
    success = False
    while(success == False):
        time.sleep(0.3)
        listPage = session.get('https://myanimelist.net/animelist/' + username + '?status=7')
        if (listPage.status_code == 200):
            success = True
            
            htmlTree = html.fromstring(listPage.text)
            listClass = htmlTree.xpath('/html/body/@class', smart_strings=False)[0]

            if (listClass == 'ownlist'):
                resultList = htmlTree.xpath('/html/body/div[@id="list_surround"]/table[position() > 3]/tr/td[2 and @class!="table_header"]/a/@href')# checkout http://lxml.de/xpathxslt.html if not enough
            elif (listClass == 'ownlist anime'):
                # get json string from data-items attribute from anime list table
                unparsed_jsonData = htmlTree.xpath('/html/body/div[@id="list-container"]/div[3]/div/table/@data-items')
                # parse the json data (a long string) into a python list of dictionaries
                data = json.loads(unparsed_jsonData[0]) # data.sort(key=lambda k: k['anime_title'])
                # create list of url's from their dictionary entries
                resultList = [anime['anime_url'] for anime in data]
            else:
                print('Error: private list or something')
                resultList = None
        else:
            print('   Error: ' + url)
            print('    -> '+ str(personPage.status_code) +': '+ personPage.reason)
            if (listPage.status_code != 404):
                attempt += 1
            else:
                print('   Private list or invalid username')
                return None
    return resultList
    # 49 61 72
# for animeURL in resultList[83:]:
    # print(i)
    # # animeURL = resultList[i]
    # # animeStaffURL = resultList[i] + '/characters'
    # anime = animeScrape(session, animeURL)
    # maldb.insertAnime(*anime)
    # # characterList = staffScrape(session, animeStaffURL)
    # # for character in characterList:
        # # print(str(character[0])+': '+character[1])
        # # for VA in character[4]:
            # # print('    '+str(VA[0]).ljust(7)+'- '+VA[1].ljust(22)+': '+VA[2])
        # # print()
    # i += 1
    # if (i%10 == 0): 
        # time.sleep(4)
    # elif (i%50 == 0):
        # session.close()
        # time.sleep(6)
        # session = requests.Session()


# MyList -> anime/characters -> scrape characters/people 
# -> for each character: insert character, 
#   -> for each person in character: check if person exists in DB, if no add them, then add VoiceRole connection
# -> for each person in staff, check if person exists in DB, if no add them, then add Staff connection


# personList = maldb.selectAllColumn('Person', 'birthday, url')
# for url in personList:
    # print(url[1])
    # print('Birthday: '+str(url[0]))
    # if url[0] == None:
        # person = personScrape(session, url[1])
        # maldb.insertPerson(*person, db)
# sys.exit()

# LET EXCEPTIONS HAPPEN MAYBE INSTEAD OF CHECK: IS MORE EFFICIENT

session = requests.Session()
db = MALDb()

username = 'TrashPandaButts'
animeURLList = listScrape(session, username)
for url in animeURLList:
    if db.selectSingle(table='Anime', column='url', value=url) == None:
        anime = animeScrape(session, url)
        db.insertAnime(*anime[:-1])
        for studio in anime[6]:
            db.insertStudio(*studio)
            db.insertAnimeStudio(anime[0], studio[0])
        
animeList = db.selectAllColumn('Anime', 'id, title, url')
for anime in animeList:
    print('\n--------------------------------------------------------------------------------')
    print('  ' + str(i))
    printUnicode('  ' + anime[1])
    print('--------------------------------------------------------------------------------\n')
    staffTuple = staffScrape(session, anime[2]+'/characters')
    characterList = staffTuple[0]
    staffList = staffTuple[1]
    for character in characterList:
        db.insertCharacter(*character[:-1])
        for person in character[5]:
            if db.selectSingle('Person', 'id', person[0]) == None:
                p = personScrape(session, person[2])
                db.insertPerson(*p)
            db.insertVoiceRole(person[0], character[0], person[3])
    for staff in staffList:
        if db.selectSingle(table='Person', column='id', value=staff[0]) == None:
            p = personScrape(session, staff[2])
            db.insertPerson(*p)
        db.insertStaff(anime[0], staff[0], staff[3])
    i += 1
    if (i%8 == 0):
        session.close()
        print('sleeping then refreshing session every 8 anime')
        print('Sleeping for 1 min')
        for j in range(60):
           time.sleep(1)
           if j%5 == 0: print(j, end='', flush=True)
           else: print('.', end='', flush=True)
        print('60')
        session = requests.Session()

session.close()
        
# result = maldb.selectSingle('person', 'url', resultList[i])
# if result != None: print(result)
# else: print('No result found')
        
    # sys.exit()
    # i = 1
    # for anime in resultList:
        # try:
            # print(str(i) + '.', end=' ')
            # print(anime)
        # except UnicodeEncodeError:
            # for c in anime:
                # try:
                    # print(c, end='')
                # except UnicodeEncodeError:
                    # print('[unicode]', end='')
            # print()
        # finally:
            # i += 1

# # get data-items attribute from anime list table
# unformattedResultList = htmlTree.xpath('//*[@id="list-container"]/div[3]/div/table/@data-items')
# # concatenate list items into a single string so they can be "cleaned"
# unformattedResultStr = ''.join(unformattedResultList)
# # "clean" results string by replacing escape characters
# unformattedResultStr = bytes(unformattedResultStr.replace('\\/', '/'), 'ascii').decode('unicode-escape')# maybe don't need url, will unicode have additional \ in front of them?

# mypattern = r'''
    # "anime_title":"(.*?)".*?
    # "anime_id":(\d+).*?
    # "anime_url":"(.*?)"         
# '''
# titleRegex = re.compile(mypattern, re.M|re.I|re.X)
# resultList = titleRegex.findall(unformattedResultStr)
# resultList.sort()
# i = 1
# for tuple in resultList:
    # try:
        # print(str(i) + '.', end=' ')
        # print(str(tuple))
    # except UnicodeEncodeError:
        # for c in str(tuple):
            # try:
                # print(c, end='')
            # except UnicodeEncodeError:
                # print('[unicode]', end='')
        # print()
    # finally:
        # i += 1
        
#listClass = tree.xpath('/html/body/@class')
#if (listClass == 'ownlist'):
#elif (listClass == 'ownlist anime'):
#else:
