from sqlite3 import connect

class Modelo():
    def __init__(self, mi_database, nombre_tabla):

        self.con = connect(mi_database)
        self.cursor = self.con.cursor()
        self.tabla = nombre_tabla
        self._crear_tabla()

    # Se crea la tabla
    def _crear_tabla(
            self
    ):
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
        querry = f"""INSERT INTO '{self.tabla}'
                (itemid, nombre, precio, stock, categoria, fecha)
                VALUES (?, ?, ?, ?, ?, ?)"""

        self.cursor.execute(querry, data_querry)
        self.con.commit()

    # elimina una fila en la tabla seleccionada y con el id que corresponda
    def delete_row(
            self, iid
    ):
        self.cursor.execute(f"DELETE FROM '{self.tabla}' WHERE id = {iid}")
        self.con.commit()

    # devuelve los datos de la tabla que coincidan con la tupla pasada
    def buscar(
            self, data_querry
    ):
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
        querry = f"""SELECT * FROM '{self.tabla}' ORDER BY fecha DESC"""

        self.cursor.execute(querry)

        datos = self.cursor.fetchall()

        self.con.commit()

        return datos

    # entrega los datos especificos de una fila por medio de su id
    def leer_fila(
            self, iid
    ):
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

def main():
    pass

if __name__ == "__main__":
    main()
