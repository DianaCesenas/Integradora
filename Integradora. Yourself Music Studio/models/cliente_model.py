import mysql.connector

class ModeloBase:
    def __init__(self, db):
        self.db = db


class ClienteModel(ModeloBase):
    
    
    def validar(self, nombre, apellido, telefono, email, calle, numero, colonia):
        # 1. Validar vacíos
        if (not nombre.strip() or not apellido.strip() or 
            not telefono.strip() or not calle.strip() or 
            not numero.strip() or not colonia.strip()):
            return "⚠️ Todos los campos son obligatorios."

        # 2. Validar Email
        if not email.strip() or "@" not in email:
            return "⚠️ El correo debe tener un '@' válido."
            
        return None # Todo correcto

    def get_all(self):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM clientes")
        datos = cursor.fetchall()
        cursor.close()
        return datos
    
    def crear(self, nombre, apellido, telefono, email, calle, numero, colonia):
        cursor = self.db.get_cursor()
        sql = """INSERT INTO clientes 
                 (Nombre, Apellido, Telefono, Email, Calle, Numero, Colonia) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (nombre, apellido, telefono, email, calle, numero, colonia))
        self.db.connection.commit()
        cursor.close()

    def actualizar(self, id_cliente, nombre, apellido, telefono, email, calle, numero, colonia):
        cursor = self.db.get_cursor()
        sql = """UPDATE clientes 
                 SET Nombre=%s, Apellido=%s, Telefono=%s, Email=%s, Calle=%s, Numero=%s, Colonia=%s 
                 WHERE ID=%s"""
        cursor.execute(sql, (nombre, apellido, telefono, email, calle, numero, colonia, id_cliente))
        self.db.connection.commit()
        cursor.close()

    def eliminar(self, id_cliente):
        cursor = self.db.get_cursor()
        cursor.execute("DELETE FROM clientes WHERE ID=%s", (id_cliente,))
        self.db.connection.commit()
        cursor.close()

    def buscar(self, texto_busqueda):
        cursor = self.db.get_cursor()
        
        parametro = f"%{texto_busqueda}%"
        
       
        sql = """
            SELECT * FROM clientes 
            WHERE Nombre LIKE %s 
            OR Apellido LIKE %s 
            OR Telefono LIKE %s
            OR Email LIKE %s
        """

        cursor.execute(sql, (parametro, parametro, parametro, parametro))
        
        datos = cursor.fetchall()
        cursor.close()
        return datos