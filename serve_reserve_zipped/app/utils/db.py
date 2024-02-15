import psycopg2
from app import app

class DBHANDLER:
    def __init__(self):
        pass

    def connect_to_database(self):
        ''' Provides connection to the database '''
        try:
            self.conn = psycopg2.connect(app.config['DB_URL'])
            self.cursor = self.conn.cursor()
        except:
            return {"error":"No connection to the database established"}

    def close_connection(self):
        ''' Closes connection to the database '''
        try:
            self.conn.commit()
            self.conn.close()
            self.conn = ""
            self.cursror = ""
        except:
            return {"error":"Unable to close database connection"}
        
    def search_return_one(self, statement, search_value):
        ''' Returns one tuple from the database matchin a search value '''
        self.connect_to_database()
        self.cursor.execute(statement, (search_value,))
        data = self.cursor.fetchone()
        self.close_connection()
        return data

    def insert_into(self, statement, values):
        ''' Inserts data into the database using a singular search value '''
        self.connect_to_database()
        self.cursor.execute(statement, (values))
        self.close_connection()

    def search_return_all(self, statement, search_value):
        ''' Returns all tuples from the database matching a search value '''
        self.connect_to_database()
        self.cursor.execute(statement, (search_value,))
        data = self.cursor.fetchall()
        self.close_connection()
        return data

    def return_all(self, statement):
        ''' Returns all data from a table '''
        self.connect_to_database()
        self.cursor.execute(statement)
        data = self.cursor.fetchall()
        self.close_connection()
        return data

db = DBHANDLER()



