import pymysql

class MALDb:
    
    def __init__(self, connection = None):
        if connection == None:  
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

    def insertAnime(id, title, releaseDate, englishTitle, synonymsTitle, url):
        anime = (id, title, releaseDate, englishTitle, synonymsTitle, url) + (title, releaseDate, englishTitle, synonymsTitle, url)
        sql = '''
            INSERT INTO Anime 
                (id, title, releaseDate, titleEnglish, titleSynonyms, url) 
            VALUES 
                (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                title=%s, releaseDate=%s, titleEnglish=%s, titleSynonyms=%s, url=%s;
        '''
        insertGeneral(sql, anime, tableName='Anime')

    def insertAnimeStudio(animeID, studioID):
        animeStudio = (animeID, studioID)
        sql ='''
            INSERT INTO AnimeStudio
                (idAnime, idStudio) 
            VALUES 
                (%s, %s)
        '''
        insertGeneral(sql, animeStudio, tableName='AnimeStudio')

    def insertCharacter(id, idAnime, name, role, url):
        character = (id, idAnime, name, role, url) + (name, role, url)
        sql = '''
            INSERT INTO mal_project.Character
                (id, idAnime, name, role, url)
            VALUES
                (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name=%s, role=%s, url=%s
        '''
        insertGeneral(sql, character, tableName='Character')

    def insertPerson(id, name, birthday, url):
        person = (id, name, birthday, url) + (name, birthday)
        sql = '''
            INSERT INTO mal_project.Person 
                (id, name, birthday, url) 
            VALUES 
                (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name=%s, birthday=%s
        '''
        insertGeneral(sql, person, tableName='Person')

    def insertStaff(animeID, personID, position):
        staff = (animeID, personID, position) + (position,)
        sql = '''
            INSERT INTO mal_project.Staff 
                (idAnime, idPerson, position)
            VALUES 
                (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                position=%s;
        '''
        insertGeneral(sql, staff, tableName='Staff')

    def insertStudio(id, name, url):
        studio = (id, name, url) + (url,)
        sql = '''
            INSERT INTO mal_project.Studio 
                (id, name, url)
            VALUES 
                (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                url=%s;
        '''
        insertGeneral(sql, studio, tableName='Studio')

    def insertVoiceRole(idPerson, idCharacter, language):
        role = (idPerson, idCharacter, language)
        sql = '''
            INSERT INTO mal_project.VoiceRole 
                (idPerson, idCharacter, language)
            VALUES 
                (%s, %s, %s)
        '''
        insertGeneral(sql, role, tableName='VoiceRole')
       
    def insertGeneral(sql, values, tableName='some'):
        # print(values)
        try:
            # Execute the SQL command
            self.cursor.execute(sql, values)
            # Commit your changes in the database
            output = 'Insert made into '+tableName+' table\n'
            output += ' -> ' + str(values[0:2])
            printUnicode(output=output)
            self.connection.commit()
            return True
        except Exception as e:
            # Rollback in case there is any error
            print('Error inserting into database, rolling back changes')
            print (str(e))
            self.connection.rollback()
            return False

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