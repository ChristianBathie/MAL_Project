import pymysql

class MALDb:
    
    def __init__(self, connection = None):
        if connection is None:  
            self.connection = pymysql.connect(host='localhost', port=3306, user='root', password='admin1234', db='mal_project', charset='utf8')
        self.cursor = connection.cursor()
    
    def reconnect():
        self.connection =  pymysql.connect(host='localhost', port=3306, user='root', password='admin1234', db='mal_project', charset='utf8')
        self.cursor = connection.cursor()
        
    def closeConnection():
        self.cursor.close()
        self.connection.close()
        self.cursor = None
        self.connection = None
    
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

    def insertAnime(id, title, releaseDate, titleEnglish, titleSynonyms, memberCount, scoreValue, scoreCount, favouriteCount, url):
        anime = (id, title, releaseDate, titleEnglish, titleSynonyms, memberCount, scoreValue, scoreCount, favouriteCount, url) + 
        (title, releaseDate, titleEnglish, titleSynonyms, memberCount, scoreValue, scoreCount, favouriteCount, url)
        sql = '''
            INSERT INTO Anime 
                (id, title, releaseDate, titleEnglish, titleSynonyms, memberCount, scoreValue, scoreCount, favouriteCount, url)
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                title=%s, releaseDate=%s, titleEnglish=%s, titleSynonyms=%s, memberCount=%s, scoreValue=%s, scoreCount=%s, favouriteCount=%s, url=%s;
        '''
        insertGeneral(sql, anime, tableName='Anime')    
    
    def insertAnimeCharacter(animeID, characterID, main):
        animeCharacter = (animeID, characterID, main)
        sql ='''
            INSERT INTO AnimeStudio
                (idAnime, idCharacter, main) 
            VALUES 
                (%s, %s, %s)
        '''
        insertGeneral(sql, animeCharacter, tableName='AnimeCharacter')
    
    def insertAnimeGenre(animeID, genreID):
        animeGenre = (animeID, genreID)
        sql ='''
            INSERT INTO AnimeGenre
                (idAnime, idGenre) 
            VALUES 
                (%s, %s)
        '''
        insertGeneral(sql, animeGenre, tableName='AnimeGenre')
        
    def insertAnimeStaff(animeID, position):
        animeStaff = (animeID, position)
        sql ='''
            INSERT INTO AnimeStaff
                (idAnime, position) 
            VALUES 
                (%s, %s)
        '''
        insertGeneral(sql, animeStaff, tableName='AnimeStaff')

    def insertAnimeStudio(animeID, studioID):
        animeStudio = (animeID, studioID)
        sql ='''
            INSERT INTO AnimeStudio
                (idAnime, idStudio) 
            VALUES 
                (%s, %s)
        '''
        insertGeneral(sql, animeStudio, tableName='AnimeStudio')

    def insertCharacter(id, fullname, favouriteCount, url, image):
        character = (id, fullname, favouriteCount, url, image) + (fullname, favouriteCount, url, image)
        sql = '''
            INSERT INTO mal_project.CharacterProfile
                (id, fullname, favouriteCount, url, image)
            VALUES
                (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                fullname=%s, favouriteCount=%s, image=%s;
        '''
        insertGeneral(sql, character, tableName='CharacterProfile')
        
    def insertGenre(genreID, title):
        genre = (genreID, title)
        sql = '''
            INSERT INTO mal_project.Genre 
                (genreID, title)
            VALUES 
                (%s, %s)
        '''
        insertGeneral(sql, genre, tableName='Genre')

    def insertPerson(id, fullname, birthday, favouriteCount, url, image):
        person = (id, fullname, birthday, favouriteCount, url, image) + (fullname, birthday, favouriteCount, url, image)
        sql = '''
            INSERT INTO mal_project.Person 
                (id, fullname, birthday, favouriteCount, url, image) 
            VALUES 
                (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                fullname=%s, birthday=%s, favouriteCount=%s, image=%s;
        '''
        insertGeneral(sql, person, tableName='Person')

    def insertStaff(personID, animeStaffID):
        staff = (personID, animeStaffID)
        sql = '''
            INSERT INTO mal_project.Staff 
                (idPerson, idAnimeStaff)
            VALUES 
                (%s, %s)
        '''
        insertGeneral(sql, staff, tableName='Staff')

    def insertStudio(id, name, url):
        studio = (id, name, url) + (name, url)
        sql = '''
            INSERT INTO mal_project.Studio 
                (id, studioName, url)
            VALUES 
                (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                studioName=%s, url=%s;
        '''
        insertGeneral(sql, studio, tableName='Studio')

    def insertVoiceRole(idPerson, idAnimeCharacter, language):
        role = (idPerson, idAnimeCharacter, language)
        sql = '''
            INSERT INTO mal_project.VoiceRole 
                (idPerson, idAnimeCharacter, language)
            VALUES 
                (%s, %s, %s)
        '''
        insertGeneral(sql, role, tableName='VoiceRole')
       
    # Used to insert new information into the database. Returns true if update is successful, false otherwise
    def executeGeneral(sql, values, tableName='table name not given'):
        # print(values)
        try:
            # Execute the SQL command
            self.cursor.execute(sql, values)
            # Commit your changes in the database
            ## output = 'Insert made into '+tableName+' table\n'
            ## output += ' -> ' + str(values[0:2])
            ## printUnicode(output=output)
            self.connection.commit()
            return True
        except Exception as e:
            # Rollback in case there is any error
            print('Error inserting into database, rolling back changes')
            print (str(e))
            self.connection.rollback()
            return False

    def updateAnime(animeID, memberCount, scoreValue, scoreCount, favouriteCount):
        newAnimeValues = (memberCount, scoreValue, scoreCount, favouriteCount) + (animeID,)
        sql = '''
            UPDATE mal_project.Anime
            SET memberCount=%s, scoreValue=%s, scoreCount=%s, favouriteCount=%s
            WHERE id=%s
        '''
        executeGeneral(sql, newAnimeValues, tableName='Anime')
    
    def selectAnime(url):
        sql = 'SELECT * FROM mal_project.Anime WHERE url = %s'
        try:
            # Execute the SQL command
            self.cursor.execute(sql, tuple(url))
            # Fetch all the rows in a list of lists.
            row = self.cursor.fetchone()
            return row
        except Exception as e:
            print(e)
            return None
            
    def selectAllColumn(table, column):
        sql = 'SELECT %s FROM mal_project.%s' % (column, table)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            animeList = self.cursor.fetchall()
            return animeList
        except Exception as e:
            print(e)
            return None

    def selectSingle(table, column, value):
        sql = 'SELECT * FROM mal_project.%s WHERE %s = ' % (table, column)
        sql += '%s'
        try:
            # Execute the SQL command
            self.cursor.execute(sql, value)
            # Fetch all the rows in a list of lists.
            anime = self.cursor.fetchone()
            return anime
        except Exception as e:
            print(e)
            return None