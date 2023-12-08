from sqlite3 import IntegrityError, OperationalError
from datetime import datetime
from random import randint
from re import fullmatch
from os import getlogin
from openpyxl import Workbook
from vista import App
from modelo import Modelo

database = "src\datos\main.db"
tabla = "DEPOSITO"

class Controlador():
    def __init__(self):
        self.modelo = Modelo(database, tabla)
        self.vista = App(self)
        self.limpiar()
        self.refresh_table()

    def alta(
            self
    ):
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
        try:
            iid = self.vista.tabla_principal.item(self.vista.tabla_principal.focus())["text"]
            self.modelo.delete_row(iid)
            self.refresh_table()
        except OperationalError:
            self.vista.error("ERROR.BAJA")

    def refresh_table(
            self
    ):
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
        self.vista.valor_item_id.set("")
        self.vista.valor_nombre.set("")
        self.vista.valor_precio.set(0)
        self.vista.valor_stock.set(0)
        self.vista.valor_categoria.set("")
        self.vista.estado_consulta.set(False)
    
    def consulta(
            self
    ):
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

def main():
    mi_programa = Controlador()
    mi_programa.vista.mainloop()
    mi_programa.modelo.con.close()

if __name__ == "__main__":
    main()
