"""
Modulo principal que se encarga de gestionar el programa, desde aqui se invocan las
otras clases (Modeloy Vista), y se realiza toda la logica de la aplicacion.
"""
from sqlite3 import IntegrityError, OperationalError
from datetime import datetime
from random import randint
from re import fullmatch
from os import getlogin
from openpyxl import Workbook
from vista import App
from modelo import Modelo

abs_path = str(__file__)[:-(len(__name__)+3)]
database = f"{abs_path}src\datos\main.db"
tabla = "DEPOSITO"

class Controlador():
    """
    La clase Controlador va a ser la que se encargue, con sus
    instancia, de llevar este control de la aplicacion. Desde su constructor va a
    utilizar a las otras dos clases (Vista y Modelo), y mediante sus instancias generara
    la logica para poder operar la aplicaion.
    """
    def __init__(self):
        """
        Como se dijo anteriormenete, desde el constructor se invocaran a las otras dos clases
        y se inicializarade forma correcta la aplicacion.
        """
        self.modelo = Modelo(database, tabla)
        self.vista = App(self)
        self.limpiar()
        self.refresh_table()

    def alta(
            self
    ):
        """
        Se da de alta los datos que proporciona el ususario hacia
        la base de datos.
        """
        try:
            if fullmatch(r"[A-Z]{2}-\d{6}", self.vista.valor_item_id.get()):
                fecha_hoy = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                datos = [
                    self.vista.valor_item_id.get(),
                    self.vista.valor_nombre.get(),
                    self.vista.valor_precio.get(),
                    self.vista.valor_stock.get(),
                    self.vista.valor_categoria.get(),
                    fecha_hoy
                ]

                self.modelo.insert_row(datos)
                self.refresh_table()
                self.limpiar()
            else:
                self.vista.error("ERROR.ALTA.ITEMID")
        except IntegrityError:
            self.vista.error("ERROR.ALTA.2ITEMID")

    def baja(
            self
    ):
        """
        Se dan de baja los datos que el usuario seleccione de la base de datos.
        """
        try:
            iid = self.vista.tabla_principal.item(self.vista.tabla_principal.focus())["text"]
            self.modelo.delete_row(iid)
            self.refresh_table()
        except OperationalError:
            self.vista.error("ERROR.BAJA")

    def refresh_table(
            self
    ):
        """
        Se actualiza la tabla. Es una instancia interna para poder visualizar los
        cambios cadavez que se realizan.
        """
        self.vista.tabla_principal.delete(*self.vista.tabla_principal.get_children())

        datos = self.modelo.leer_tabla()

        for dato in datos:

            iid = dato[0]
            lista_aux = []
            for i in range(1, 7):
                lista_aux.append(dato[i])
            valores = tuple(lista_aux)

            self.vista.tabla_principal.insert("", "end", text=iid, values=valores)
        
        self.vista.combo_categoria.config(values=self.modelo.extract_categoria())

    def actualizar(
            self
    ):
        """
        Se actualizan los datos en la base de datos que el usuario haya modificado.
        """
        if self.vista.estado_consulta.get():
            iid = self.vista.tabla_principal.item(self.vista.tabla_principal.focus())["text"]

            fecha_hoy = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            datos = (
                self.vista.valor_item_id.get(),
                self.vista.valor_nombre.get(),
                self.vista.valor_precio.get(),
                self.vista.valor_stock.get(),
                self.vista.valor_categoria.get(),
                fecha_hoy,
                iid
            )

            self.modelo.update(datos)
            self.refresh_table()
            self.limpiar()
        else:
            self.vista.error("ERROR.ACTUALIZAR")

    def limpiar(
            self
    ):
        """
        Pone todos los valores de los campos de toma de datos en un valor de *default*.
        """
        self.vista.valor_item_id.set("")
        self.vista.valor_nombre.set("")
        self.vista.valor_precio.set(0)
        self.vista.valor_stock.set(0)
        self.vista.valor_categoria.set("")
        self.vista.estado_consulta.set(False)
    
    def consulta(
            self
    ):
        """
        Setea los valores de los campos de entrada segun el valor de la tabla seleccionado.
        """
        try:
            iid = self.vista.tabla_principal.item(self.vista.tabla_principal.focus())["text"]
            datos = self.modelo.leer_fila(iid)

            self.vista.valor_item_id.set(datos[0][1])
            self.vista.valor_nombre.set(datos[0][2])
            self.vista.valor_precio.set(datos[0][3])
            self.vista.valor_stock.set(datos[0][4])
            self.vista.valor_categoria.set(datos[0][5])

            self.vista.estado_consulta.set(True)
        except IndexError:
            self.vista.error("ERROR.CONSULTA")

    def buscar(
            self
    ):
        """
        Actualiza la tabla segun los valores que coincidan con los ingresados en los
        campos de entrada.
        """
        datos = (
            self.vista.valor_item_id.get(),
            self.vista.valor_nombre.get(),
            self.vista.valor_precio.get(),
            self.vista.valor_stock.get(),
            self.vista.valor_categoria.get()
        )
        
        if datos == ("", "", 0.0, 0, ""):
            self.refresh_table()
        else:
            self.vista.tabla_principal.delete(*self.vista.tabla_principal.get_children())

            datos = self.modelo.buscar(datos)

            for dato in datos:

                iid = dato[0]
                lista_aux = []
                for i in range(1, 7):
                    lista_aux.append(dato[i])
                valores = tuple(lista_aux)

                self.vista.tabla_principal.insert("", "end", text=iid, values=valores)

    def genid(
            self
    ):
        """
        Proporciona un valor de *Item-ID* con un valor aleatoreo teniendo en cuenta el
        resto de valores ingresado por el usuario. 
        """
        try:
            self.modelo.cursor.execute(f"SELECT itemid FROM {tabla}")

            lista_ids = []
            for i in self.modelo.cursor.fetchall():
                lista_ids.append(i[0])
            self.modelo.con.commit()

            a = self.vista.valor_categoria.get()[0].upper()
            b = self.vista.valor_nombre.get()[0].upper()

            while True:
                c = str(randint(1, 100000)).zfill(6)
                new_id = f"{a}{b}-{c}"
                if new_id not in lista_ids:
                    break

            self.vista.valor_item_id.set(new_id)
        except IndexError:
            self.vista.error("ERROR.GENID")

    def exportar(
            self
    ):
        """
        Exporta la tabla principal a un formato *.xlsx*
        hacia alguna de las siguientes ubicaicones:

          * **Documentos**
          
          * **Escritorio**

          * **Ubicacion del programa**

        Este es el orden que intentara de manera predeterminada.
        """
        wb = Workbook()
        ws = wb.active
        ws.title = f"{self.modelo.tabla}"

        ws.append(["ID", "Item ID", "Nombre", "Precio", "Stock", "Categoria", "Fecha de modificaicon"])
        for i in self.modelo.leer_tabla():
            ws.append(i)

        fecha_hoy = datetime.now().strftime("%d.%m.%Y - %H h %M m %S s")

        nombre_archivo_excel = f"{self.modelo.tabla} - {fecha_hoy}.xlsx"

        directorios = [
            f"C:\\Users\\{getlogin()}\\Documents\\{nombre_archivo_excel}",
            f"C:\\Users\\{getlogin()}\\Desktop\\{nombre_archivo_excel}",
            nombre_archivo_excel
        ]

        for i in directorios:
            try:
                wb.save(i)
                self.vista.aviso_exportacion(directorios.index(i))
                break
            except FileNotFoundError:
                pass

def _main():
    mi_programa = Controlador()
    mi_programa.vista.mainloop()
    mi_programa.modelo.con.close()

if __name__ == "__main__":
    _main()
