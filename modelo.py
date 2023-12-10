"""
El modulo Modelo es el encargado de interactuar con la
base de datos, generar la conexion y las request que pida el
controlador.
"""
from sqlite3 import connect

class Modelo():
    """
    La clase Modelo se construye pasandole dos parametros, la ruta de la base
    de datos y el nombre de la tabla (este se puede crear o cargar si ya existe).
    Esta clase se llama desde el controlador, en el constructor de su clase, para que
    pueda ejecutar las instacias del modelo y asi interactuar con la base de datos.

    Args:
        mi_database (str): Ruta de acceso a la base de datos

        nombre_tabla (str): Nombre de la tabla a la cual acceder o crear
    """
    def __init__(self, mi_database, nombre_tabla):
        """
        En el conructor de la clase generaremos la conexion con la base de datos y
        con la instancia _crear_tabla crearemos la tabla si es que esta no existe. Ademas
        asignaremos las variables de clase:
        
          * **self.con**: La conexion a la base de datos.

          * **self.cursor**: El cursor para actuar sobre la abse de datos.
          
          * **self.tabla**: El nombre de la tabla asignado a una variable de clase.
        """

        self.con = connect(mi_database)
        self.cursor = self.con.cursor()
        self.tabla = nombre_tabla
        self._crear_tabla()

    # Se crea la tabla
    def _crear_tabla(
            self
    ):
        """
        Metodo de instancia interno del modulo que se utiliza para crear la
        tabla en el caso de que esta no exista.
        """
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS '{self.tabla}' (
            id integer PRIMARY KEY,
            itemid text UNIQUE,
            nombre text,
            precio float,
            stock integer,
            categoria text,
            fecha text
            )"""
        )
        self.con.commit()

    # incerta una nueva fila en la tabal seleccionada
    def insert_row(
            self, data_querry
    ):
        """
        Inserta una fila completa en la tabla con los datos proporcionados.
        
        Args:
            data_querry (tuple): Tupla que contiene en orden los datos de cada fila de la tabla que se quieren ingresar.
        """

        querry = f"""INSERT INTO '{self.tabla}'
                (itemid, nombre, precio, stock, categoria, fecha)
                VALUES (?, ?, ?, ?, ?, ?)"""

        self.cursor.execute(querry, data_querry)
        self.con.commit()

    # elimina una fila en la tabla seleccionada y con el id que corresponda
    def delete_row(
            self, iid
    ):
        """
        Se elimina la fila indicada con el *iid* correspondiente.

        Args:
            iid (int): Valor clave de la fila que se desea eliminar. 
        """

        self.cursor.execute(f"DELETE FROM '{self.tabla}' WHERE id = {iid}")
        self.con.commit()

    # devuelve los datos de la tabla que coincidan con la tupla pasada
    def buscar(
            self, data_querry
    ):
        """
        Funcion que devuelve los valores de la tabla que coincidan con los elementos pasados
        como argumentos.

        Args:
            data_querry (tuple): Tupla que contiene en orden los datos de busqueda.

        Returns:
            Todos los datos que coincidan con los pasados en el *data_querry*
        """

        querry = f"""SELECT * FROM '{self.tabla}'
                     WHERE itemid = ? OR nombre = ? OR precio = ? OR stock = ? OR categoria = ?
                     ORDER BY fecha DESC"""

        self.cursor.execute(querry, data_querry)

        datos = self.cursor.fetchall()

        self.con.commit()

        return datos
    
    # lee todos los datos de la tabla seleccionada
    def leer_tabla(
            self
    ):
        """
        Selecciona todos los elementos de la tabla y los devuelve ordenados de manera descendente
        por la ultima fecha de modificacicon de cada uno. 
        """

        querry = f"""SELECT * FROM '{self.tabla}' ORDER BY fecha DESC"""

        self.cursor.execute(querry)

        datos = self.cursor.fetchall()

        self.con.commit()

        return datos

    # entrega los datos especificos de una fila por medio de su id
    def leer_fila(
            self, iid
    ):
        """
        Retorna los datos de la fila que coincida con el id proporcionado.

        Args:
            iid (int): Valor clave de la fila que se desea extraer los datos.

        Returns:
            Se devuelve una tupla con los datos de la fila solicitada 
        """

        querry = f"SELECT * FROM '{self.tabla}' WHERE id = ?"

        data_querry = (iid,)

        self.cursor.execute(querry, data_querry)

        datos = self.cursor.fetchall()

        self.con.commit()

        return datos

    # actualiza los datos de una cierta fila con los datos pasados
    def update(
            self, data_querry
    ):
        """
        Actualiza toda una fila de la tabla.

        Args:
            data_querry (tuple): Tupla que contiene los datos de la fila que se quiere modificar
        """

        querry = f"""UPDATE '{self.tabla}' SET
                itemid = ?,
                nombre = ?,
                precio = ?,
                stock = ?,
                categoria = ?,
                fecha = ?

                WHERE id = ?
                """

        self.cursor.execute(querry, data_querry)
        self.con.commit()

    # extraer array con elementos de la categoria
    def extract_categoria(
            self
    ):
        """
        Extrae de los elementos de la columna CATEGORIA sin repertir.

        Returns:
            Devuele una **lista** con las categorias que la tabla posee, sin repetir.
        """
        
        querry = "SELECT categoria FROM DEPOSITO"

        self.cursor.execute(querry)

        datos = []

        for a in self.cursor.fetchall():
            if a[0] in datos:
                pass
            else:
                datos.append(a[0])

        self.con.commit()

        return datos

def _main():
    pass

if __name__ == "__main__":
    _main()
