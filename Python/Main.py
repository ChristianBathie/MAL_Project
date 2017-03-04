import sys
import time
import random
from MALDb import MALDb 
from MALScraper import MALScraper
from MyPrint import MyPrint

# MyList -> anime/characters -> scrape characters/people 
# -> for each character: insert character, 
#   -> for each person in character: check if person exists in DB, if no add them, then add VoiceRole connection
# -> for each person in staff, check if person exists in DB, if no add them, then add Staff connection

# LET EXCEPTIONS HAPPEN MAYBE INSTEAD OF CHECK: IS MORE EFFICIENT

# Anime MainPage
# -> Anime 
# -> Genre -> AnimeGenre    #Sidebar
# -> Studio -> AnimeStudio  #Sidebar
# Anime CharacterPage
# -> Character ->  AnimeCharacter -> Person -> VoiceRole
# -> AnimeStaff -> Person -> Staff

# anime, genre, studio, character, person
# AnimeGenre, AnimeStudio, AnimeCharacter, AnimeStaff
# VoiceRole, Staff

# Anime
# - AnimeStudio - Role - Staff
# Studio Person


def main():
    scraper = MALScraper()
    db = MALDb()
    # Scrape user's anime list for urls
    username = 'TrashPandaButts'
    animeURLList = scraper.scrape_list(username)
    # Scrape any anime page that isn't already in database
    for url in animeURLList:
        if db.select_single(table='Anime', column='url', value=url) is None:
            anime = scraper.scrape_anime(url)
            db.insert_anime(*anime.values()[:-1])
            for studio in anime['StudioList']:
                db.insert_studio(**studio)
                db.insert_animestudio(anime['ID'], studio['ID'])
    # for all anime in the database
    animeList = db.select_all_column('Anime', 'id, title, url')
    scrapeCycles = 0
    for anime in animeList:
        ## print('\n--------------------------------------------------------------------------------')
        ## print('  ' + str(i))
        ## printUnicode('  ' + anime[1])
        ## print('--------------------------------------------------------------------------------\n')
        dictAnimeStaff = scraper.scrape_animestaff(anime['url']+'/characters')
        for character in dictAnimeStaff['CharacterList']:
            db.insert_character(*character.values()[:-1])
            for person in character['VoiceActorList']:
                if db.select_single('Person', 'id', person['ID']) is None:
                    p = scraper.scrape_person(person['URL'])
                    db.insert_person(**p)
                db.insert_voicerole(person['ID'], character['ID'], person['Language'])
        for staff in dictAnimeStaff['StaffList']:
            if db.select_single(table='Person', column='id', value=staff['ID']) is None:
                p = scraper.scrape_person(staff['URL'])
                db.insert_person(**p)
            #db.insert_staff(anime['idAnime'], staff['idStaff'], staff['positions'])
        scrapeCycles += 1
        if scrapeCycles % 8 == 0:
            scraper.session_reset(5)


def complete_collection():
    return


def anime_collection(scraper, db, animeurllist):
    for animeurl in animeurllist:
        dictAnime = scraper.scrape_anime(animeurl)
        db.insert_anime(**dictAnime['anime'])
        for studio in dictAnime['studioList']:
            db.insert_studio(**studio)
            db.insert_animestudio(dictAnime['anime']['idAnime'], studio['idStudio'])
        for genre in dictAnime['genreList']:
            db.insert_genre(**genre)
            db.insert_animegenre(dictAnime['anime']['idAnime'], genre['idGenre'])
    return


def character_collection():
    return
    # get list of all characters in database
    # for each character in database
    #   - scrape character page (name, favourites, image, anime(id, name?))


def person_collection():
    return
    # get list of people in database
    # for each person in database
    # - scrape person page (birthday, favourites, image)


def test():
    dictAnime = scraper.scrape_anime('/anime/1/Cowboy_Bebop')
    db.insert_anime(**dictAnime['anime'])
    for studio in dictAnime['studioList']:
        db.insert_studio(**studio)
        db.insert_animestudio(dictAnime['anime']['idAnime'], studio['idStudio'])
        # insert Studio
        # insert AnimeStudio (FK: anime, studio)
    for genre in dictAnime['genreList']:
        db.insert_genre(**genre)
        db.insert_animegenre(dictAnime['anime']['idAnime'], genre['idGenre'])
        # insert Genre
        # insert AnimeGenre (FK: anime, genre)
    # Scrape character page
    # staffTuple = scraper.scrape_animestaff('/anime/1/Cowboy_Bebop'+'/characters')
    # for character in staffTuple['CharacterList']:
    #     print(character)
    #     # insert Character
    #     # insert AnimeCharacter (FK: anime, character)
    #     # insert Person
    #     # insert Voicerole (FK: person, animecharacter)
    # # Scrape person
    # for staff in staffTuple['StaffList']:
    #     print(staff)
    #     # insert Person
    #     # insert Person (FK: anime)
    #     # insert Staff (FK: person, animestaff)
    # if db.insert_anime(**dictAnime['anime']):
    #     print('Insert successful')
    # else:
    #     print('Insert failed')

scraper = MALScraper()
db = MALDb()
animeurllist = scraper.scrape_list('TrashPandaButts')
anime_collection(scraper, db, animeurllist)
