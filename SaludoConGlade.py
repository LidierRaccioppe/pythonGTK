import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class FestraPrincipal():
    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file("SaludoGlade.glade")

        wndFestraPrincipal = builder.get_object("wndFiestraPrincipal")
        self.lblEtiqueta = builder.get_object("lblEtiqueta")
        self.txtName = builder.get_object("txtName")
        self.btnSaludo = builder.get_object("btnSaludo")

        sennales = {
            "on_btnSaludo_clicked" : self.on_btnBoton_clicked,
            "on_txtName_activate" : self.on_txtName_activate,
            "krakatoa" : Gtk.main_quit
        }
        ## para conectar con el glade
        builder.connect_signals(sennales)


    def on_btnBoton_clicked(self, boton):
        print("tocadito")
        self.lblEtiqueta.set_text("muestro que tocaste al boton")
    def on_txtName_activate(self,  entrada):
        print("presionadito")
        self.lblEtiqueta.set_text(entrada.get_text())

if __name__ == "__main__":
    FestraPrincipal()
    Gtk.main()

