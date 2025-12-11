from conexionBD import *
from datetime import date
fecha_hoy = date.today()
class ReservasModel:
    @staticmethod
    def agregar(fecha,id_sala,id_cliente,hi,hf,p):
        try:
            estatus="activo"
            cursor.execute("INSERT INTO reservaciones VALUES (NULL,%s,%s,%s,%s,%s,%s,%s)",
            (id_sala,fecha,hi,hf,p,id_cliente,estatus)
            ) 
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def datosSala1():
        try:
            cursor.execute("SELECT salas.capacidad, CONCAT(TIME_FORMAT(reservaciones.hora_inicio, '%H:%i'), '-', TIME_FORMAT(reservaciones.hora_termino, '%H:%i')),reservaciones.hora_inicio,reservaciones.hora_termino FROM salas LEFT JOIN reservaciones ON salas.ID = reservaciones.ID_salas AND reservaciones.estatus_Reserva = 'activo' AND reservaciones.fecha = CURDATE() WHERE salas.nombre = 'AZUL'")
            return cursor.fetchall()
        except:
            return []
        
    @staticmethod
    def datosSala2():
        try:
            cursor.execute("SELECT salas.capacidad, CONCAT(TIME_FORMAT(reservaciones.hora_inicio, '%H:%i'), '-', TIME_FORMAT(reservaciones.hora_termino, '%H:%i')),reservaciones.hora_inicio,reservaciones.hora_termino FROM salas LEFT JOIN reservaciones ON salas.ID = reservaciones.ID_salas AND reservaciones.estatus_Reserva = 'activo' AND reservaciones.fecha = CURDATE() WHERE salas.nombre = 'ROJA'")
            return cursor.fetchall()
        except:
            return []
        
    @staticmethod
    def datosSala3():
        try:
            cursor.execute("SELECT salas.capacidad, CONCAT(TIME_FORMAT(reservaciones.hora_inicio, '%H:%i'), '-', TIME_FORMAT(reservaciones.hora_termino, '%H:%i')),reservaciones.hora_inicio,reservaciones.hora_termino FROM salas LEFT JOIN reservaciones ON salas.ID = reservaciones.ID_salas AND reservaciones.estatus_Reserva = 'activo' AND reservaciones.fecha = CURDATE() WHERE salas.nombre = 'NARANJA'")
            return cursor.fetchall()
        except:
            return []
    
    @staticmethod
    def datosSala4():
        try:
            cursor.execute("SELECT salas.capacidad, CONCAT(TIME_FORMAT(reservaciones.hora_inicio, '%H:%i'), '-', TIME_FORMAT(reservaciones.hora_termino, '%H:%i')),reservaciones.hora_inicio,reservaciones.hora_termino FROM salas LEFT JOIN reservaciones ON salas.ID = reservaciones.ID_salas AND reservaciones.estatus_Reserva = 'activo' AND reservaciones.fecha = CURDATE() WHERE salas.nombre = 'BLANCA'")
            return cursor.fetchall()
        except:
            return []
        
        


        
    @staticmethod
    def mostrar(texto_busqueda, orden):
        try:
            sql = "SELECT reservaciones.id ,salas.nombre,reservaciones.fecha,CONCAT(TIME_FORMAT(reservaciones.hora_inicio, '%H:%i'),'-', TIME_FORMAT(reservaciones.hora_termino, '%H:%i')),CONCAT(clientes.Nombre, ' ', clientes.Apellido),reservaciones.personas FROM reservaciones INNER JOIN salas ON reservaciones.ID_salas = salas.ID INNER JOIN clientes ON reservaciones.ID_cliente = clientes.ID WHERE estatus_Reserva='activo'"
            params = []
            
            if texto_busqueda:
                sql += " AND (clientes.Nombre LIKE %s OR salas.nombre LIKE %s)"
        
                # El parámetro se repite porque hay dos signos de interrogación (?)
                busqueda_formateada = f"%{texto_busqueda}%"
                params.append(busqueda_formateada)
                params.append(busqueda_formateada)
            
            if orden == "nombre_asc":
                sql += " ORDER BY nombre ASC"
            else:
                # Orden por defecto (por ejemplo, fecha más reciente)
                sql += " ORDER BY reservaciones.fecha DESC"
            
            cursor.execute(sql, tuple(params))
            return cursor.fetchall()
        except Exception as e:
            return []
        
        

    @staticmethod
    def modificar(id,nump):
        try:
            cursor.execute("UPDATE reservaciones SET personas=%s WHERE id=%s",(nump,id))
            conexion.commit()
            return True
        except:
            return False
        

    @staticmethod
    def desactivar(id):
        try:
            cursor.execute("UPDATE reservaciones SET estatus_Reserva='inactivo' WHERE id=%s",(id,))
            conexion.commit()
            return True
        except:
            return False
        
        
    @staticmethod
    def salas():
        try:
            cursor.execute("SELECT ID,nombre FROM salas WHERE estatus = 1")
            return cursor.fetchall()        
        except:
            return []
    
    @staticmethod
    def mostrar_fechas(date,id):
       
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
        
    @staticmethod
    def agregarCliente(campo_nombre,campo_apellido,campo_telefono,campo_email,campo_calle,campo_numero,campo_colonia):
        try:
            cursor.execute("INSERT INTO clientes VALUES(NULL, %s, %s, %s, %s, %s, %s, %s)",(campo_nombre,campo_apellido,campo_telefono,campo_email,campo_calle,campo_numero,campo_colonia))
            conexion.commit()
            return True
        except:
            return False
       
    @staticmethod
    def buscarCliente(campo_nombre,campo_apellido,campo_telefono):
        try:
            cursor.execute("SELECT * FROM clientes WHERE Nombre=%s AND Apellido=%s AND Telefono=%s",(campo_nombre,campo_apellido,campo_telefono))
            return cursor.fetchall()
        except:
            return []
        
