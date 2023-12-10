"""
El modulo Vista es el encargado de armar la ventana interactiva e
interactuar con el usuario para poder brindar al controlador los comandos
que este quiere realizar
"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from widgets import Ventana, Boton, Texto, Entrada, Combobox, Tabla

class App(Tk):
    """
    La clase Vista se contruye heredando de la libreria
    `Tkinter <https://docs.python.org/es/3/library/tkinter.html>`_
    el moudlo `Tk <https://docs.python.org/es/3/library/tk.html>`_.
    El controlador llama a la clase Vista y cuando se crea el objeto de
    la clase Controlador se genera el mainloop de la aplicacion.
    """
    def __init__(self, controlador):
        """
        En el constructor de la clase se pide como parametro la clase Controlador,
        para poder linkear las instancias de la clase Controlador, con las acciones de los
        botones de la aplicacion.

        Como primer paso se utiliza la intancia *super()* para invocar al constructor de
        la clase `Tk <https://docs.python.org/es/3/library/tk.html>`_.

        Luego se configura el estilo y atributos de la ventana principal, se definen las
        variables de la aplicacion y se invoca al metodo  *_insertar_widgets()*, que se
        encarga de incertar todos los widgets en la ventana.

        Args:
            controlador (clase): Clase Controlador que se cruza con la de Vista para poder utilizar las instancias de Controlador
        """
        super().__init__()
        self.controlador = controlador

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.configure(background="#DCDAD5")
        self.resizable(False, False)
        self.title("Gestor de Deposito")
        self.iconbitmap(r"src\img\icono.ico")

        self.valor_item_id = StringVar()
        self.valor_nombre = StringVar()
        self.valor_precio = DoubleVar()
        self.valor_stock = IntVar()
        self.valor_categoria = StringVar()

        self.estado_consulta = BooleanVar()
        self.estado_consulta.set(False)

        #   (id_de_elemento, heading, ancho, justificacion)
        self.contenido_tabla = [
            ("itemid", "Item ID", 70, CENTER),
            ("nombre", "Nombre", 220, W),
            ("precio", "Precio", 150, W),
            ("stock", "Stock", 150, W),
            ("categoria", "Categoria", 200, W),
            ("fecha", "Fecha", 150, W),
        ]

        self.lista_categoria = self.controlador.modelo.extract_categoria()

        self._insertar_widgets()

    def _insertar_widgets(
            self
    ):
        """
        Instancia interna que se encarga del diseño y colocacion de los widgets en la
        ventana. 
        """

        # ventana(master, col.num, row.num, columspan, rowspan, texto_de_cuadro)
        self.ventana_datos = Ventana(self, 0, 0, 1, 1, "Datos")
        self.ventana_botones = Ventana(self, 1, 0, 1, 1, "Acciones")
        self.ventana_tabla = Ventana(self, 0, 1, 2, 1, "Tabla")

        # label(master, col.num, row.num, columspan, rowspan, texto_de_label)
        # entry(master, col.num, row.num, columspan, rowspan, variable_de_entry)

        self.texto_itemid = Texto(self.ventana_datos, 0, 0, 1, 1, "Item ID")
        self.entry_itemid = Entrada(self.ventana_datos, 1, 0, 2, 1, self.valor_item_id)

        self.texto_nombre = Texto(self.ventana_datos, 0, 1, 1, 1, "Nombre")
        self.entry_nombre = Entrada(self.ventana_datos, 1, 1, 2, 1, self.valor_nombre)

        self.texto_precio = Texto(self.ventana_datos, 0, 2, 1, 1, "Precio")
        self.entry_precio = Entrada(self.ventana_datos, 1, 2, 2, 1, self.valor_precio)

        self.texto_stock = Texto(self.ventana_datos, 0, 3, 1, 1, "Stock")
        self.entry_stock = Entrada(self.ventana_datos, 1, 3, 2, 1, self.valor_stock)

        # combobox(master, col.num, row.num, columspan, rowspan, lista_de_cbox, variable_de_entry)

        self.texto_categoria = Texto(self.ventana_datos, 0, 4, 1, 1, "Categoria")
        self.entry_categoria = Entrada(self.ventana_datos, 1, 4, 1, 1, self.valor_categoria)
        self.combo_categoria = Combobox(self.ventana_datos, 2, 4, 1, 1, self.lista_categoria, self.valor_categoria)

        # boton(master, col.num, row.num, columspan, rowspan, texto_de_boton, funcion_linkeada)

        self.boton_alta = Boton(self.ventana_botones, 0, 0, 1, 1, "ALTA", self.controlador.alta)
        self.boton_baja = Boton(self.ventana_botones, 1, 0, 1, 1, "ELIMINAR", self.controlador.baja)
        self.boton_actualizar = Boton(self.ventana_botones, 0, 1, 1, 1, "ACTUALIZAR", self.controlador.actualizar)
        self.boton_consulta = Boton(self.ventana_botones, 1, 1, 1, 1, "CONSULTA", self.controlador.consulta)
        self.boton_buscar = Boton(self.ventana_botones, 0, 2, 1, 1, "BUSCAR", self.controlador.buscar)
        self.boton_limpiar = Boton(self.ventana_botones, 1, 2, 1, 1, "LIMPIAR", self.controlador.limpiar)
        self.boton_generar_id = Boton(self.ventana_botones, 0, 3, 1, 1, "GENERAR ID", self.controlador.genid)
        self.boton_exportar = Boton(self.ventana_botones, 1, 3, 1, 1, "EXPORTAR", self.controlador.exportar)

        # (master, contenido_de_tabla)

        self.tabla_principal = Tabla(self.ventana_tabla, self.contenido_tabla)

    def error(
            self, codigo
    ):
        """
        En este metodo el controlador envia un codigo de error predeterminado y segun cual sea el
        codigo se displaya un mensaje de error puntual para cada caso.

        Args:
            codigo (str): Codigo predefinido en el controlador que se envia en el caso de que ocurra algun errot en la aplicacion.
        """

        mensajes = {
            "ERROR.ACTUALIZAR": ["Error de Actualizar", "Realice previamente una consulta de algun dato"],
            "ERROR.GENID": ["Error en Generar ID", "Completar los campos para generar un id automaticamente"],
            "ERROR.CONSULTA": ["Error de Consulta", "Seleccione un elemento para consultar"],
            "ERROR.BAJA": ["Error en Eliminar", "Seleccione un elemento para eliminar"],
            "ERROR.ALTA.2ITEMID": ["Error en Item-ID", "Valor duplicado"],
            "ERROR.ALTA.ITEMID": ["Error en Item-ID",
                                  "Ingrese un valor correcto de Item-ID.\
                                   Utilice el fomrato de dos mayusculas y 6 digitos. Ej: AA-123456"],
        }

        mb.showerror(mensajes[codigo][0], mensajes[codigo][1])

    def aviso_exportacion(
            self, codigo
    ):
        """
        Metodo que displaya un mensaje hacia donde se exporto la tabla.

        Args:
            codigo (int): Codigo predefinido en el controlador que se envia para informar donde se realizo la exportacion de la tabla.
        """
        
        mensajes = {
            0: "Se exporto con exito la tabla hacia la carpeta Documentos",
            1: "Se exporto con exito la tabal hacia el Escritorio",
            2: "Se exporto con exito la tabla hacia la ubicacion del programa"
        }

        mb.showinfo("Exportacion de tabla", mensajes[codigo])

def main():
    pass

if __name__ == "__main__":
    main()
