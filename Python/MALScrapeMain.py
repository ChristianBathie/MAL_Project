import requests, re, json, sys, time, random, maldb, malscraper
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


# MyList -> anime/characters -> scrape characters/people 
# -> for each character: insert character, 
#   -> for each person in character: check if person exists in DB, if no add them, then add VoiceRole connection
# -> for each person in staff, check if person exists in DB, if no add them, then add Staff connection

# LET EXCEPTIONS HAPPEN MAYBE INSTEAD OF CHECK: IS MORE EFFICIENT

scraper = MALScraper()
db = MALDb()
# Scrape user's anime list for urls
username = 'TrashPandaButts'
animeURLList = scraper.listScrape(username)
# Scrape any anime page that isn't already in database
for url in animeURLList:
    if db.selectSingle(table='Anime', column='url', value=url) is None:
        anime = scraper.animeScrape(url)
        db.insertAnime(*anime.values()[:-1])
        for studio in anime['StudioList']:
            db.insertStudio(**studio)
            db.insertAnimeStudio(anime['ID'], studio['ID'])

# for all anime in the database
animeList = db.selectAllColumn('Anime', 'id, title, url')
for anime in animeList:
    ## print('\n--------------------------------------------------------------------------------')
    ## print('  ' + str(i))
    ## printUnicode('  ' + anime[1])
    ## print('--------------------------------------------------------------------------------\n')
    staffTuple = scraper.staffScrape(anime['URL']+'/characters')
    for character in staffTuple['CharacterList']:
        db.insertCharacter(*character.values()[:-1])
        for person in character['VoiceActorList']:
            if db.selectSingle('Person', 'id', person['ID']) is None:
                p = scraper.personScrape(person['URL'])
                db.insertPerson(**p)
            db.insertVoiceRole(person['ID'], character['ID'], person['Language'])
    for staff in staffTuple['StaffList']:
        if db.selectSingle(table='Person', column='id', value=staff['ID']) is None:
            p = scraper.personScrape(staff['URL'])
            db.insertPerson(**p)
        db.insertStaff(anime['ID'], staff['ID'], staff['Positions'])
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
