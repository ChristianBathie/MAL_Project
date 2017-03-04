import pymysql
# import MyPrint


class MALDb:
    
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='admin1234',
            charset='utf8'
        )
        self.cursor = self.connection.cursor()
    
    def reconnect(self):
        self.closeconnection()
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='admin1234',
            charset='utf8'
        )
        self.cursor = self.connection.cursor()
        
    def closeconnection(self):
        self.cursor.close()
        self.connection.close()
        self.cursor = None
        self.connection = None

    def insert_anime(self, idAnime, title, releaseDate, titleEnglish, titleSynonyms, memberCount, scoreValue, scoreCount, favouriteCount, url, image):
        anime = (idAnime, title, releaseDate, titleEnglish, titleSynonyms, memberCount, scoreValue, scoreCount, favouriteCount, url, image) + (title, releaseDate, titleEnglish, titleSynonyms, memberCount, scoreValue, scoreCount, favouriteCount, url, image)
        sql = '''
            INSERT INTO mal_project.Anime
                (id, title, releaseDate, titleEnglish, titleSynonyms, memberCount, scoreValue, scoreCount, favouriteCount, url, image)
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                title=%s, releaseDate=%s, titleEnglish=%s, titleSynonyms=%s, memberCount=%s, scoreValue=%s, scoreCount=%s, favouriteCount=%s, url=%s, image=%s;
        '''
        return self.insert(sql, anime, tableName='Anime')
    
    def insert_animecharacter(self, idAnime, idCharacter, main):
        animeCharacter = (idAnime, idCharacter, main)
        sql = '''
            INSERT IGNORE mal_project.AnimeStudio
                (idAnime, idCharacter, main) 
            VALUES 
                (%s, %s, %s)
        '''
        self.insert(sql, animeCharacter, tableName='AnimeCharacter')
    
    def insert_animegenre(self, idAnime, idGenre):
        animeGenre = (idAnime, idGenre)
        sql = '''
            INSERT IGNORE INTO  mal_project.AnimeGenre
                (idAnime, idGenre) 
            VALUES 
                (%s, %s)
        '''
        self.insert(sql, animeGenre, tableName='AnimeGenre')
        
    def insert_animestaff(self, idAnime, position):
        animeStaff = (idAnime, position)
        sql = '''
            INSERT IGNORE INTO  mal_project.AnimeStaff
                (idAnime, position) 
            VALUES
                (%s, %s)
        '''
        self.insert(sql, animeStaff, tableName='AnimeStaff')

    def insert_animestudio(self, idAnime, idStudio):
        animeStudio = (idAnime, idStudio)
        sql = '''
            INSERT IGNORE INTO  mal_project.AnimeStudio
                (idAnime, idStudio) 
            VALUES 
                (%s, %s)
        '''
        self.insert(sql, animeStudio, tableName='AnimeStudio')

    def insert_character(self, idCharacter, fullname, favouriteCount, image):
        character = (idCharacter, fullname, favouriteCount, image) + (fullname, favouriteCount, image)
        sql = '''
            INSERT INTO mal_project.CharacterProfile
                (id, fullname, favouriteCount, image)
            VALUES
                (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                fullname=%s, favouriteCount=%s, image=%s;
        '''
        self.insert(sql, character, tableName='CharacterProfile')
        
    def insert_genre(self, idGenre, title):
        genre = (idGenre, title)
        sql = '''
            INSERT IGNORE INTO mal_project.Genre
                (id, title)
            VALUES 
                (%s, %s)
        '''
        self.insert(sql, genre, tableName='Genre')

    def insert_person(self, idPerson, fullname, birthday, favouriteCount, image):
        person = (idPerson, fullname, birthday, favouriteCount, image) + (fullname, birthday, favouriteCount, image)
        sql = '''
            INSERT INTO mal_project.Person
                (id, fullname, birthday, favouriteCount, image) 
            VALUES 
                (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                fullname=%s, birthday=%s, favouriteCount=%s, image=%s;
        '''
        self.insert(sql, person, tableName='Person')

    def insert_staff(self, idPerson, idAnimeStaff):
        staff = (idPerson, idAnimeStaff)
        sql = '''
            INSERT IGNORE INTO mal_project.Staff
                (idPerson, idAnimeStaff)
            VALUES 
                (%s, %s)
        '''
        self.insert(sql, staff, tableName='Staff')

    def insert_studio(self, idStudio, name):
        studio = (idStudio, name)
        sql = '''
            INSERT IGNORE INTO mal_project.Studio
                (id, studioName)
            VALUES 
                (%s, %s)
        '''
        self.insert(sql, studio, tableName='Studio')

    def insert_voicerole(self, idPerson, idAnimeCharacter, language):
        role = (idPerson, idAnimeCharacter, language)
        sql = '''
            INSERT IGNORE INTO mal_project.VoiceRole
                (idPerson, idAnimeCharacter, language)
            VALUES 
                (%s, %s, %s)
        '''
        self.insert(sql, role, tableName='VoiceRole')
       
    # Used to insert new information into the database. Returns true if update is successful, false otherwise
    def insert(self, sql, values, tableName='table name not given'):
        # print(values)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            print('insert made into table:', tableName)
            return True
        except Exception as e:
            # Rollback in case there is any error
            print('Error inserting into database, rolling back changes')
            print(str(e))
            self.connection.rollback()
            return False

    def update_anime(self, animeID, memberCount, scoreValue, scoreCount, favouriteCount):
        newAnimeValues = (memberCount, scoreValue, scoreCount, favouriteCount) + (animeID,)
        sql = '''
            UPDATE mal_project.Anime
            SET memberCount=%s, scoreValue=%s, scoreCount=%s, favouriteCount=%s
            WHERE id=%s
        '''
        self.insert(sql, newAnimeValues, tableName='Anime')
    
    def select_anime(self, url):
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
            
    def select_all_column(self, table, column):
        sql = 'SELECT %s FROM mal_project.%s' % (column, table)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            resultList = self.cursor.fetchall()
            return resultList
        except Exception as e:
            print(e)
            return None

    def select_single(self, table, column, value):
        sql = 'SELECT * FROM mal_project.%s WHERE %s = ' % (table, column)
        sql += '%s'
        try:
            # Execute the SQL command
            self.cursor.execute(sql, value)
            # Fetch all the rows in a list of lists.
            resultSingle = self.cursor.fetchone()
            return resultSingle
        except Exception as e:
            print(e)
            return None
