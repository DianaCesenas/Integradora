import mysql.connector

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",      
                password="",      
                database="bd_reservaciones"
            )
        except mysql.connector.Error as err:
            print(f"Error de Conexión: {err}")
            raise err

    def get_cursor(self):
        return self.connection.cursor() if self.connection else None

    def close(self):
        if self.connection:
            self.connection.close()