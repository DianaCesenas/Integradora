from conexionBD import *

class ReservasModel:
    @staticmethod
    def agregar(cliente,id_salas,fecha,hi,ht,personas,id_cliente):
        try:
            cursor.execute("INSERT INTO reservas VALUES (NULL,%s,%s,%s,%s,%s,%s,%s)",
            (cliente,id_salas,fecha,hi,ht,personas,id_cliente)
            ) 
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def mostrar():
        try:
            cursor.execute("SELECT id,nombre_cliente,ID_salas,fecha,hora_inicio,hora_termino,personas,ID_cliente WHERE estatus_reserva='activo'")
            return cursor.fetchall()
        except:
            return []

    @staticmethod
    def modificar(id,cliente,id_salas,fecha,hi,ht,personas,id_cliente):
        try:
            cursor.execute("UPDATE Reservas SET nombre_cliente=%s,ID_salas=%s,fecha=%s,hora_inicio=%s,hora_termino=%s,personas=%s,ID_cliente, WHERE id=%s"),(cliente,id_salas,fecha,hi,ht,personas,id_cliente,id)
            return True
        except:
            return False

    @staticmethod
    def desactivar(id):
        try:
            cursor.execute("UPDATE Reservas SET estatus_reserva='inactivo' WHERE id=%s"),(id,)
            return True
        except:
            return 
        
    @staticmethod
    def salas():
        try:
            cursor.execute("SELECT ID,nombre FROM salas")
            return cursor.fetchall()        
        except:
            return []
    
    @staticmethod
    def mostrar_fechas(date,id):
        try:
            cursor.execute(
            "SELECT hora_inicio,hora_termino FROM reservaciones where fecha=%s and ID_salas=%s",(date,id))
            return cursor.fetchall()
        except:
            return[]
        
        
    @staticmethod
    def mostrar_clientes():
        try:
            cursor.execute(
            "SELECT ID,CONCAT(Nombre,' ',Apellido) FROM clientes")
            return cursor.fetchall()
        except:
            return[]
       
        
