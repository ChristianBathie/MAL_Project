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
    # if url[0] is None:
        # person = personScrape(session, url[1])
        # maldb.insertPerson(*person, db)
# sys.exit()

# LET EXCEPTIONS HAPPEN MAYBE INSTEAD OF CHECK: IS MORE EFFICIENT

session = requests.Session()
db = MALDb()

username = 'TrashPandaButts'
animeURLList = listScrape(session, username)
for url in animeURLList:
    if db.selectSingle(table='Anime', column='url', value=url) is None:
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
            if db.selectSingle('Person', 'id', person[0]) is None:
                p = personScrape(session, person[2])
                db.insertPerson(*p)
            db.insertVoiceRole(person[0], character[0], person[3])
    for staff in staffList:
        if db.selectSingle(table='Person', column='id', value=staff[0]) is None:
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
