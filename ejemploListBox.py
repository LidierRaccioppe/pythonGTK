import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class FilaListBoxConDatos(Gtk.ListBoxRow):
    def __init__(self, palabra):
        super().__init__()
        self.palabra = palabra
        self.add(Gtk.Label(label=palabra))

class FestraPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo ListBox de Gtk")

        caja = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)

        listBox = Gtk.ListBox()
        caja.pack_start(listBox, True, True, 0)

        elementoListBox = "Esta es una cadena para ordenar con el ListBox, para el ListBox".split()
        for palabra in elementoListBox:
            listBox.add(FilaListBoxConDatos(palabra=palabra))

        def funcionOrdenacion(fila1, fila2):
            return fila1.palabra.lower() > fila2.palabra.lower()
        # Documentacion: https://lazka.github.io/pgi-docs/Gtk-3.0/classes/ListBox.html#Gtk.ListBox.set_sort_func
        def funcionFiltracion(fila):
            return False if fila.palabra == "ListBox" else True
        # Documentacion: https://lazka.github.io/pgi-docs/Gtk-3.0/classes/ListBox.html#Gtk.ListBox.set_filter_func
        listBox.set_sort_func(funcionOrdenacion)
        listBox.set_filter_func(funcionFiltracion)
        listBox.connect("row-activated", self.on_row_activated)


        self.add(caja)

        self.connect("delete-event", Gtk.main_quit) ## la el segundo argumento no debe tener el parentesis de funcion, ya que en ese caso la ejecutaria

        self.show_all()

    def on_row_activated(self, listBox, fila):
        print(fila.palabra)
if __name__ == "__main__":
    FestraPrincipal()
    Gtk.main()