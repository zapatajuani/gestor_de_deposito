from controlador import Controlador

mi_programa = Controlador()
mi_programa.vista.mainloop()
mi_programa.modelo.con.close()
