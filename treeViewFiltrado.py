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
        self.set_title("Ejemplo Treeview Filtrado")

        self.set_default_size(250, 100)
        self.set_border_width(10)
        caja = Gtk.Box (orientation=Gtk.Orientation.VERTICAL, spacing=4)

        self.filtradoGenero = "None"

        modelo = Gtk.ListStore(str,str,int,str,bool)
        modelo_filtrado = modelo.filter_new()
        modelo_filtrado.set_visible_func(self.filtro_usuarios_genero)
        try:
            bbdd = dbapi.connect("baseDatos.dat")
            cursor = bbdd.cursor()
            cursor.execute("select * from usuarios")
            for fila in cursor:
                modelo.append(fila)
        except dbapi.DatabaseError as e:
            print("Error al cargar el ListStores")
        finally:
            cursor.close()
            bbdd.close()

        #vistaVerdista = Gtk.TreeView(model=modelo)
        vistaVerdista = Gtk.TreeView(model=modelo_filtrado)
        objetoSeleccion = vistaVerdista.get_selection()

        for i, tituloColumna in enumerate  (["Dni", "Nombre"]):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(tituloColumna, celda, text=i)
            vistaVerdista.append_column(columna)

        celda = Gtk.CellRendererProgress()
        columna = Gtk.TreeViewColumn("Edad", celda, value=2)
        vistaVerdista.append_column(columna)


        modeloCombo = Gtk.ListStore(str)
        modeloCombo.append(("Hombre",))
        modeloCombo.append(("Mujer",))
        modeloCombo.append(("Otros",))
        celda = Gtk.CellRendererCombo()
        celda.set_property("editable", True)
        celda.props.model = modeloCombo
        # celda.set_property("model", modeloCombo)
        celda.set_property("text-column", 0)
        celda.set_property("has-entry", False)
        celda.connect("edited", self.on_celdaCombo_edited, modelo_filtrado, 3)
        columna = Gtk.TreeViewColumn("Genero", celda, text=3)
        vistaVerdista.append_column(columna)
        caja.pack_start(vistaVerdista, True, True, 2)

        cajaH = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        caja.pack_start(cajaH, True, True, 0)

        rbtHombre = Gtk.RadioButton.new_with_label(None,"Hombre")
        rbtMujer = Gtk.RadioButton.new_with_label_from_widget(rbtHombre, label="Mujer")
        rbtOtros = Gtk.RadioButton.new_with_label_from_widget(rbtHombre, label="Otros")
        cajaH.pack_start(rbtHombre, True, True, 2)
        cajaH.pack_start(rbtMujer, True, True, 2)
        cajaH.pack_start(rbtOtros, True, True, 2)

        rbtHombre.connect("toggled", self.on_genero_toggled, "Hombre", modelo_filtrado)
        rbtMujer.connect("toggled", self.on_genero_toggled, "Mujer", modelo_filtrado)
        rbtOtros.connect("toggled", self.on_genero_toggled, "Otros", modelo_filtrado)

        self.add(caja)

        self.connect("delete-event", Gtk.main_quit)  ## la el segundo argumento no debe tener el parentesis de funcion, ya que en ese caso la ejecutaria

        self.show_all()
    def on_celdaCombo_edited(self, control, fila, texto, modelo, columna):
        try:
            bbdd = dbapi.connect("baseDatos.dat")
            cursor = bbdd.cursor()
            cursor.execute("update usuarios set genero=? where dni=?", (texto, modelo[fila][0]))
            bbdd.commit()
        except dbapi.DatabaseError as e:
            print("Error al actualizar el genero")
        modelo[fila][columna] = texto
        modelo.refilter()
    def on_genero_toggled(self, botonSeleccionado, genero, modelo):
        if botonSeleccionado.get_active():
            self.filtradoGenero = genero
            modelo.refilter()
    def filtro_usuarios_genero(self, modelo, fila, datos):
        if self.filtradoGenero == "None" or self.filtradoGenero is None:
            return True
        else:
            return modelo[fila][3] == self.filtradoGenero

if __name__ == "__main__":
    FestraPrincipal()
    Gtk.main()

