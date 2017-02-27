import pymysql

class MALDb:
    
    def __init__(self):
        self.connection = pymysql.connect(host='localhost', port=3306, user='root', password='admin1234', db='mal_project', charset='utf8')
        self.cursor = self.connection.cursor()
    
    def reconnect(self):
        self.closeConnection()
        self.connection =  pymysql.connect(host='localhost', port=3306, user='root', password='admin1234', db='mal_project', charset='utf8')
        self.cursor = self.connection.cursor()
        
    def closeConnection(self):
        self.cursor.close()
        self.connection.close()
        self.cursor = None
        self.connection = None
    
    def printUnicode(self, output):
        try:
            print(output)
        except UnicodeEncodeError:
            for c in output:
                try:
                    print(c, end='')
                except UnicodeEncodeError:
                    print('[unicode]', end='')
            print()

    def insertAnime(self, id, title, releaseDate, titleEnglish, titleSynonyms, memberCount, scoreValue, scoreCount, favouriteCount, url, image):
        anime = (id, title, releaseDate, titleEnglish, titleSynonyms, memberCount, scoreValue, scoreCount, favouriteCount, url, image) + (title, releaseDate, titleEnglish, titleSynonyms, memberCount, scoreValue, scoreCount, favouriteCount, url, image)
        sql = '''
            INSERT INTO Anime 
                (id, title, releaseDate, titleEnglish, titleSynonyms, memberCount, scoreValue, scoreCount, favouriteCount, url, image)
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                title=%s, releaseDate=%s, titleEnglish=%s, titleSynonyms=%s, memberCount=%s, scoreValue=%s, scoreCount=%s, favouriteCount=%s, url=%s, image=%s;
        '''
        return self.insertGeneral(sql, anime, tableName='Anime')    
    
    def insertAnimeCharacter(self, animeID, characterID, main):
        animeCharacter = (animeID, characterID, main)
        sql ='''
            INSERT INTO AnimeStudio
                (idAnime, idCharacter, main) 
            VALUES 
                (%s, %s, %s)
        '''
        self.insertGeneral(sql, animeCharacter, tableName='AnimeCharacter')
    
    def insertAnimeGenre(self, animeID, genreID):
        animeGenre = (animeID, genreID)
        sql ='''
            INSERT INTO AnimeGenre
                (idAnime, idGenre) 
            VALUES 
                (%s, %s)
        '''
        self.insertGeneral(sql, animeGenre, tableName='AnimeGenre')
        
    def insertAnimeStaff(self, animeID, position):
        animeStaff = (animeID, position)
        sql ='''
            INSERT INTO AnimeStaff
                (idAnime, position) 
            VALUES 
                (%s, %s)
        '''
        self.insertGeneral(sql, animeStaff, tableName='AnimeStaff')

    def insertAnimeStudio(self, animeID, studioID):
        animeStudio = (animeID, studioID)
        sql ='''
            INSERT INTO AnimeStudio
                (idAnime, idStudio) 
            VALUES 
                (%s, %s)
        '''
        self.insertGeneral(sql, animeStudio, tableName='AnimeStudio')

    def insertCharacter(self, id, fullname, favouriteCount, image):
        character = (id, fullname, favouriteCount,image) + (fullname, favouriteCount, image)
        sql = '''
            INSERT INTO mal_project.CharacterProfile
                (id, fullname, favouriteCount, image)
            VALUES
                (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                fullname=%s, favouriteCount=%s, image=%s;
        '''
        self.insertGeneral(sql, character, tableName='CharacterProfile')
        
    def insertGenre(self, genreID, title):
        genre = (genreID, title)
        sql = '''
            INSERT INTO mal_project.Genre 
                (genreID, title)
            VALUES 
                (%s, %s)
        '''
        self.insertGeneral(sql, genre, tableName='Genre')

    def insertPerson(self, id, fullname, birthday, favouriteCount, image):
        person = (id, fullname, birthday, favouriteCount, image) + (fullname, birthday, favouriteCount, image)
        sql = '''
            INSERT INTO mal_project.Person 
                (id, fullname, birthday, favouriteCount, image) 
            VALUES 
                (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                fullname=%s, birthday=%s, favouriteCount=%s, image=%s;
        '''
        self.insertGeneral(sql, person, tableName='Person')

    def insertStaff(self, personID, animeStaffID):
        staff = (personID, animeStaffID)
        sql = '''
            INSERT INTO mal_project.Staff 
                (idPerson, idAnimeStaff)
            VALUES 
                (%s, %s)
        '''
        self.insertGeneral(sql, staff, tableName='Staff')

    def insertStudio(self, id, name):
        studio = (id, name) + (name,)
        sql = '''
            INSERT INTO mal_project.Studio 
                (id, studioName)
            VALUES 
                (%s, %s)
            ON DUPLICATE KEY UPDATE
                studioName=%s;
        '''
        self.insertGeneral(sql, studio, tableName='Studio')

    def insertVoiceRole(self, idPerson, idAnimeCharacter, language):
        role = (idPerson, idAnimeCharacter, language)
        sql = '''
            INSERT INTO mal_project.VoiceRole 
                (idPerson, idAnimeCharacter, language)
            VALUES 
                (%s, %s, %s)
        '''
        self.insertGeneral(sql, role, tableName='VoiceRole')
       
    # Used to insert new information into the database. Returns true if update is successful, false otherwise
    def insertGeneral(self, sql, values, tableName='table name not given'):
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

    def updateAnime(self, animeID, memberCount, scoreValue, scoreCount, favouriteCount):
        newAnimeValues = (memberCount, scoreValue, scoreCount, favouriteCount) + (animeID,)
        sql = '''
            UPDATE mal_project.Anime
            SET memberCount=%s, scoreValue=%s, scoreCount=%s, favouriteCount=%s
            WHERE id=%s
        '''
        executeGeneral(sql, newAnimeValues, tableName='Anime')
    
    def selectAnime(self, url):
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
            
    def selectAllColumn(self, table, column):
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

    def selectSingle(self, table, column, value):
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