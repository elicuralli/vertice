from service.entities.control import Control
from database.db import get_connection


class ControlModel(): 

    @classmethod
    def get_todo_control(self):
        
        try:

            conection = get_connection()
            control_es = []

            with conection.cursor() as cursor:
                cursor.execute("SELECT *FROM control")
                result = cursor.fetchall()

                if result is not None:
                    for row in result:
                            control = Control(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[3],password= row[4])
                            control_es.append(control.to_JSON())

                conection.close()
                return control_es
            
        except  Exception as ex:
                raise Exception(ex)
        
    @classmethod
    def get_control(self,cedula: str):

        try:
            conection = get_connection()
            control_es =  None

            with conection.cursor() as cursor:
                cursor.execute("SELECT *FROM control WHERE cedula= %s",(cedula,))
                row = cursor.fetchone()

                if row is not None:
                    control = Control(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[3],password= row[4])
                    control_es= control.to_JSON()

            conection.close()
            return control_es


        except  Exception as ex:
            print(ex)
            raise Exception(ex)
        
    @classmethod
    def add_control(self,control):

        try:
            conection = get_connection()
            
            with conection.cursor() as cursor:
               
                cursor.execute("SELECT * from control WHERE cedula =%s",(control.cedula,))
                result = cursor.fetchone()
                if result is not None: 
                    return 'usuario ya existe'
                cursor.execute("""INSERT INTO control(cedula,fullname,correo,telefono,password)VALUES (%s,%s,%s,%s,%s)""",(control.cedula,control.fullname,control.correo,control.telefono,control.password))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows
        
        except  Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_control(self,control):

        try:
            conection = get_connection()

            with conection.cursor() as cursor:
                cursor.execute("UPDATE control SET fullname =%s,correo =%s,telefono=%s WHERE cedula =%s",(control.fullname,control.correo,control.telefono,control.cedula))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows
        
        except  Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_control(self,control):
        try:
            conection = get_connection()                                      
            
            with conection.cursor() as cursor:
                cursor.execute("DELETE FROM control WHERE cedula = %s", (control.cedula,))
                affected_rows = cursor.rowcount
                conection.commit()

            conection.close()
            return affected_rows

        except  Exception as ex:
            raise Exception(ex)

    @classmethod
    def login(self,control: Control):
        try:

            conection = get_connection()
            cont: Control
            with conection.cursor() as cursor:
                cursor.execute("SELECT * from control WHERE correo =%s",(control.correo,))
                row = cursor.fetchone()

                if row is not None:
                    cont = Control(cedula=row[0],fullname=row[1],correo=row[2],telefono=row[3],password= row[4])
                else:
                    return None

            conection.close()
            return cont
        
        except Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def update_password(cls, correo, new_password):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("UPDATE control SET password=%s WHERE correo=%s", (new_password, correo))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_control_by_correo(cls, correo):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM control WHERE correo=%s", (correo,))
                row = cursor.fetchone()
                if row:
                    control = Control(
                        cedula=row[0],
                        fullname=row[1],
                        correo=row[2],
                        telefono=row[3],
                        password=row[4]
                    )
                    return control
                else:
                    return None
            connection.close()
        except Exception as ex:
            raise Exception(ex)