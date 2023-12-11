from controlador import Controlador

def _main():
    mi_programa = Controlador()
    mi_programa.vista.mainloop()
    mi_programa.modelo.con.close()

if __name__ == "__main__":
    _main()
