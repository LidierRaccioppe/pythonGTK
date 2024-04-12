from itertools import chain

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class FestraPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo con check y radio botton")

        ## Box almacena los objetos que puedan haber en el entorno grafico
        caja = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)

        rbtBoton1 = Gtk.RadioButton.new_with_label_from_widget(None, "Boton 1")
        rbtBoton1.connect("toggled", self.on_rbtBoton_toggled, "1")
        caja.pack_start(rbtBoton1, False, False, 2)

        rbtBoton2 = Gtk.RadioButton.new_from_widget(rbtBoton1)
        rbtBoton2.set_label("Boton 2")
        rbtBoton2.connect("toggled", self.on_rbtBoton_toggled, "2")
        caja.pack_start(rbtBoton2, False, False, 2)

        rbtBoton3 = Gtk.RadioButton.new_with_mnemonic_from_widget(rbtBoton1, "_Boton 3")
        rbtBoton3.connect("toggled", self.on_rbtBoton_toggled, "3")
        caja.pack_start(rbtBoton3, False, False, 2)


        chkCheqcheqcheqcheq = Gtk.CheckButton()
        chkCheqcheqcheqcheq.set_label("Chec 1")
        chkCheqcheqcheqcheq.connect("toggled", self.on_chkCheq_toggled)
        caja.pack_start(chkCheqcheqcheqcheq, False, False, 0)

        chkCheq5 = Gtk.CheckButton.new_with_label( "Check 5")
        chkCheq5.connect("toggled", self.on_chkCheq_toggled)
        caja.pack_start(chkCheq5, False, False, 2)


        self.add(caja)

        self.connect("delete-event", Gtk.main_quit) ## la el segundo argumento no debe tener el parentesis de funcion, ya que en ese caso la ejecutaria

        self.show_all()

    def on_chkCheq_toggled(self, chkBoton):
        if chkBoton.get_active():
            print("Boton Cheq activado fue "+chkBoton.get_label())
        else:
            print("Check Boton desactivado: "+ chkBoton.get_label())





    def on_rbtBoton_toggled(self, boton, numeroDelBotonPulsado):
        if boton.get_active():
            print("Boton "+numeroDelBotonPulsado+" fue activado")
        else:
            print("Boton "+numeroDelBotonPulsado+" fue desactivado")

    def on_btnBoton_clicked(self, referenciaSeñalBoton, etiqueta):
        print("tocadito")
        etiqueta.set_text("muestro que tocaste al boton")
    def on_entrada_activate(self,  entrada, etiqueta):
        print("presionadito")
        etiqueta.set_text(entrada.get_text())

if __name__ == "__main__":
    FestraPrincipal()
    Gtk.main()

