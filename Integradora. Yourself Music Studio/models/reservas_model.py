from conexionBD import *

class ReservasModel:
    @staticmethod
    def agregar(fecha,id_sala,id_cliente,hi,hf,p):
        print("entro 1")
        estatus="activo"
        cursor.execute("INSERT INTO reservaciones VALUES (NULL,%s,%s,%s,%s,%s,%s,%s)",
        (id_sala,fecha,hi,hf,p,id_cliente,estatus)
        ) 
        conexion.commit()


    @staticmethod
    def mostrar():
        try:
            cursor.execute(
            "SELECT reservaciones.id ,salas.nombre,CONCAT(TIME_FORMAT(reservaciones.hora_inicio, '%H:%i'),'-', TIME_FORMAT(reservaciones.hora_termino, '%H:%i')),CONCAT(clientes.Nombre, ' ', clientes.Apellido),reservaciones.personas FROM reservaciones INNER JOIN salas ON reservaciones.ID_salas = salas.ID INNER JOIN clientes ON reservaciones.ID_cliente = clientes.ID")
            return cursor.fetchall()
        except:
            return []
        

    @staticmethod
    def modificar(id,id_salas,fecha,hi,ht,personas,id_cliente):
        try:
            cursor.execute("UPDATE Reservas SET ID_salas=%s,fecha=%s,hora_inicio=%s,hora_termino=%s,personas=%s,ID_cliente, WHERE id=%s"),(id_salas,fecha,hi,ht,personas,id_cliente,id)
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
    def mostrar_horas(date,id):
       
        cursor.execute(
        "SELECT hora_inicio,hora_termino FROM reservaciones where fecha=%s and ID_salas=%s",(date,id))
        return cursor.fetchall()
    
        
        
    @staticmethod
    def mostrar_clientes():
        try:
            cursor.execute(
            "SELECT ID,CONCAT(Nombre,' ',Apellido) FROM clientes")
            return cursor.fetchall()
        except:
            return[]
       
        
