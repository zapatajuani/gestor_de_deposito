from tkinter import *
from tkinter import ttk
from atributos import *

class Ventana(ttk.Labelframe):
    def __init__(self, master, col, row, cspan, rspan, titulo):
        super().__init__(master)
        self.config(text=titulo)
        self.grid(column=col,
                  row=row,
                  columnspan=cspan,
                  rowspan=rspan,
                  padx=att_ventanas["padx"],
                  pady=att_ventanas["pady"],
                  sticky=att_ventanas["sticky"])

class Texto(ttk.Label):
    def __init__(self, master, col, row, cspan, rspan, texto):
        super().__init__(master, text=texto)
        self.config(width=att_labels["width"])
        self.grid(column=col,
                  row=row,
                  columnspan=cspan,
                  rowspan=rspan,
                  ipadx=att_labels["ipadx"],
                  ipady=att_labels["ipady"],
                  padx=att_labels["padx"],
                  pady=att_labels["pady"],
                  sticky=att_labels["sticky"])

class Boton(ttk.Button):
    def __init__(self, master, col, row, cspan, rspan, texto, funcion):
        super().__init__(master, text=texto, command=funcion)
        self.config(width=att_buttons["width"])
        self.grid(column=col,
                  row=row,
                  columnspan=cspan,
                  rowspan=rspan,
                  ipadx=att_buttons["ipadx"],
                  ipady=att_buttons["ipady"],
                  padx=att_buttons["padx"],
                  pady=att_buttons["pady"],
                  sticky=att_buttons["sticky"])

class Entrada(ttk.Entry):
    def __init__(self, master, col, row, cspan, rspan, variable):
        super().__init__(master, textvariable=variable)
        self.config(width=att_entry["width"])
        self.grid(column=col,
                  row=row,
                  columnspan=cspan,
                  rowspan=rspan,
                  ipadx=att_entry["ipadx"],
                  ipady=att_entry["ipady"],
                  padx=att_entry["padx"],
                  pady=att_entry["pady"],
                  sticky=att_entry["sticky"])

class Combobox(ttk.Combobox):
    def __init__(self, master, col, row, cspan, rspan, lista, variable):
        super().__init__(master, textvariable=variable)
        self["values"] = lista
        self.config(state="readonly", width=att_combobox["width"])
        self.grid(column=col,
                  row=row,
                  columnspan=cspan,
                  rowspan=rspan,
                  ipadx=att_combobox["ipadx"],
                  ipady=att_combobox["ipady"],
                  padx=att_combobox["padx"],
                  pady=att_combobox["pady"],
                  sticky=att_combobox["sticky"])

class Tabla(ttk.Treeview):
    def __init__(self, master, contenido):

        tabla_scroll = ttk.Scrollbar(master)
        tabla_scroll.pack(fill=Y, side=RIGHT, padx=5, pady=5)

        aux = []
        for i in contenido:
            aux.append(i[0])

        super().__init__(master, columns=aux, show="headings",
                         yscrollcommand=tabla_scroll.set,
                         height=25)

        tabla_scroll.config(command=self.yview)

        for a in contenido:
            self.heading(a[0], text=a[1])
            self.column(a[0], width=a[2], anchor=a[3])

        self.pack(fill=X, side=RIGHT, padx=5, pady=5)

def main():
    pass

if __name__ == "__main__":
    main()
