import gi
import sqlite3 as dbapi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

"""

columnas = ("Nombre", "Apellido", "Numero de teléfono")
agendaTelefonica = (
                    ("Pepe", "Pérez", "986 444 555"),
                    ("Ana", "Yañéz", "985 333 777"),
                    ("Roque", "Díz", "987 222 889"),
                    )
"""
class FestraPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo listin telefonico con Treeview")

        self.set_default_size(250,100)
        self.set_border_width(10)

        # Establecemos el tipo que tendra en cada columna
        modelo = Gtk.ListStore(str,str,str)

        try:
            bbdd = dbapi.connect ("baseTelefonica.dat")
            cursor = bbdd.cursor()
            cursor.execute("select * from listaTelefonos")
            for usuarioListin in cursor:
                modelo.append(usuarioListin)
            cursor.close()
            bbdd.close()
        except dbapi.Error as e:
            print(e)
        except dbapi.DatabaseError as e:
            print(e)


        vistaVerdista = Gtk.TreeView(model=modelo)
        objetoSeleccion = vistaVerdista.get_selection()
        objetoSeleccion.connect("changed", self.on_objetoSeleccion_changed)
        columnas = ("Nombre", "Apellido", "Numero de teléfono")
        for i, nombreColumna in enumerate(columnas):
            celda = Gtk.CellRendererText()
            if i==0:
                celda.props.weight_set = True
                celda.props.weight = Pango.Weight.BOLD
            if i==2:
                celda.props.editable = True
                celda.connect("edited", self.on_celdaTelefono_edited, modelo, i)
            col = Gtk.TreeViewColumn(nombreColumna, celda, text=i)
            vistaVerdista.append_column(col)

        """
        El tema es que esto tiene varias cosas que darle.
        
        Darle un modelo, luego el treeview, luego un Gtk.TreeviewColumn, y luego los celdas
        """


        ## Box almacena los objetos que puedan haber en el entorno grafico
        caja = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        caja.pack_start(vistaVerdista, True, True, 0)
        grid = Gtk.Grid()
        caja.pack_start(grid, True, True, 0)

        lblNombre = Gtk.Label(label="Nombre")
        lblApellido = Gtk.Label(label="Apellido")
        lblTelefono = Gtk.Label(label="Telefono")
        self.txtNombre = Gtk.Entry()
        self.txtApellido = Gtk.Entry()
        self.txtTelefono = Gtk.Entry()

        btnAnadir = Gtk.Button(label="Añadir")
        btnBorrar = Gtk.Button(label="Borrar")

        grid.add(lblNombre)
        grid.attach_next_to(self.txtNombre,lblNombre, Gtk.PositionType.RIGHT,1, 1)
        grid.attach_next_to(lblApellido,self.txtNombre, Gtk.PositionType.RIGHT,1, 1)
        grid.attach_next_to(self.txtApellido,lblApellido, Gtk.PositionType.RIGHT,1, 1)
        grid.attach_next_to(lblTelefono,lblNombre, Gtk.PositionType.BOTTOM,1, 1)
        grid.attach_next_to(self.txtTelefono,lblTelefono, Gtk.PositionType.RIGHT,1, 1)
        grid.attach_next_to(btnAnadir,self.txtTelefono, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(btnBorrar,self.txtTelefono, Gtk.PositionType.BOTTOM, 2, 1)
        btnAnadir.connect("clicked", self.on_btnAnadir_clicked, modelo)
        btnBorrar.connect("clicked", self.on_btnBorrar_clicked, objetoSeleccion )

        self.add(caja)

        self.connect("delete-event", Gtk.main_quit) ## la el segundo argumento no debe tener el parentesis de funcion, ya que en ese caso la ejecutaria

        self.show_all()
    def on_objetoSeleccion_changed(self, seleccion):
        (modelo, fila) = seleccion.get_selected()
        print(modelo[fila][0], modelo[fila][1], modelo[fila][2])
    def on_celdaTelefono_edited(self, celda , fila, texto, modelo, columna):
        try:
            bbdd = dbapi.connect ("baseTelefonica.dat")
            cursor = bbdd.cursor()
            cursor.execute("update listaTeleofonos set telefono = ? where telefono = ?", (texto, modelo[fila][2]))
            bbdd.commit()
            cursor.close()
            bbdd.close()
        except dbapi.Error as e:
            print(e)
        except dbapi.DatabaseError as e:
            print(e)
        modelo[fila][columna] = texto
    def on_btnBorrar_clicked(self, boton, seleccion):
        (modelo, fila) = seleccion.get_selected()
        print(modelo[fila][2])
        try:
            bbdd = dbapi.connect("baseTelefonica.dat")
            cursor = bbdd.cursor()
            cursor.execute("delete from listaTelefonos where  telefono = ?", (modelo[fila][2],))

            bbdd.commit()
            cursor.close()
            bbdd.close()
        except dbapi.Error as e:
            print(e)
        except dbapi.DatabaseError as e:
            print(e)

        modelo.remove(fila)
    def on_btnAnadir_clicked(self, boton, modelo):

        if self.txtNombre.get_text() !="" and self.txtApellido.get_text() !="" and self.txtTelefono.get_text() !="":
            elemento = (self.txtNombre.get_text(),self.txtApellido.get_text(),self.txtTelefono.get_text())
        modelo.append (elemento)
        self.txtNombre.set_text("")
        self.txtApellido.set_text("")
        self.txtTelefono.set_text("")
        try:
            bbdd = dbapi.connect("baseTelefonica.dat")
            cursor = bbdd.cursor()
            cursor.execute("insert into listaTelefonos values (?,?,?)", elemento)
            for usuarioListin in cursor:
                modelo.append(usuarioListin)
            bbdd.commit()
            cursor.close()
            bbdd.close()
        except dbapi.Error as e:
            print(e)
        except dbapi.DatabaseError as e:
            print(e)


if __name__ == "__main__":
    FestraPrincipal()
    Gtk.main()

