import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk




class FestraPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Primera ventana con Gtk")

        lblEtiqueta = Gtk.Label(label="NOS MATARAN A TODOS NOS MATARAN A TODOS NOS MATARAN A TODOS ")

        btnBoton = Gtk.Button()

        imagen = Gtk.Image()
        imagen.set_from_file("giu.jpeg")
        ## self.add(imagen)

        entrada = Gtk.Entry()





        ## Box almacena los objetos que puedan haber en el entorno grafico
        caja = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)

        caja.pack_start(btnBoton, True, True, 5)


        ## Segun lo que se rellene puede quedar mal
        ## Segun las palabras de Manuel, los que quedan bien son casi todos los de texto
        caja.pack_start(lblEtiqueta, True, True, 5)

        entrada.connect("activate", self.on_entrada_activate, lblEtiqueta)

        caja.pack_start(entrada, True, True, 5)
        caja.pack_start(imagen, True, True, 5)
        btnBoton = Gtk.Button(label = "You touch my tralala")

        btnBoton.connect("clicked" ,  self.on_btnBoton_clicked, lblEtiqueta)

        caja.pack_start(btnBoton, False, False, 5)

        self.add(caja)

        self.connect("delete-event", Gtk.main_quit) ## la el segundo argumento no debe tener el parentesis de funcion, ya que en ese caso la ejecutaria

        self.show_all()

    def on_btnBoton_clicked(self, referenciaSeñalBoton, etiqueta):
        print("tocadito")
        etiqueta.set_text("muestro que tocaste al boton")
    def on_entrada_activate(self,  entrada, etiqueta):
        print("presionadito")
        etiqueta.set_text(entrada.get_text())

if __name__ == "__main__":
    FestraPrincipal()
    Gtk.main()

