import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk




class FestraPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo de Stack Layout")



        cajaV = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)

        tarjetas = Gtk.Stack()
        tarjetas.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        tarjetas.set_transition_duration(1000)


        chkPulsame = Gtk.CheckButton(label = "Apretame")
        tarjetas.add_titled(chkPulsame, "apretame", "Check apretame")

        lblEtiqueta = Gtk.Label()
        lblEtiqueta.set_markup("<big>Esta es una etiqueta grande</big>")
        tarjetas.add_titled(lblEtiqueta, "etiqueta", "Una etiqueta")

        botonesTarjetas = Gtk.StackSwitcher()
        botonesTarjetas.set_stack(tarjetas)
        cajaV.pack_start(botonesTarjetas, True, True, 0)
        cajaV.pack_start(tarjetas, True, True, 0)





        self.add(cajaV)
        self.connect("delete-event", Gtk.main_quit) ## la el segundo argumento no debe tener el parentesis de funcion, ya que en ese caso la ejecutaria
        self.show_all()


if __name__ == "__main__":
    FestraPrincipal()
    Gtk.main()
