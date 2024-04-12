from itertools import chain

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class FestraPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo con check y radio botton")

        ## Box almacena los objetos que puedan haber en el entorno grafico
        caja = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        # Caja para los datos del alumno (nombre, apellido) en horizontal
        cajaAlumnoBasico = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
        etiquetaNombre = Gtk.Label(label="Nombre")
        cajaAlumnoBasico.pack_start(etiquetaNombre, True, True, 2)
        campoTextoNombre = Gtk.Entry(name = "Nombre")
        cajaAlumnoBasico.pack_start(campoTextoNombre, True, True, 2)
        etiquetaApellido = Gtk.Label(label="Apellido")
        cajaAlumnoBasico.pack_start(etiquetaApellido, True, True, 2)
        caja.pack_start(cajaAlumnoBasico, True, True, 2)
        campoTextoApellido = Gtk.Entry(name = "Apellido")
        cajaAlumnoBasico.pack_start(campoTextoApellido, True, True, 2)

        # Caja para los datos del alumno (Modulo, Nota, un check box de si la curso en ingles o no) en horizontal
        cajaAlumnoModulo = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=10)
        etiquetaModulo = Gtk.Label(label="SI")
        cajaAlumnoModulo.pack_start(etiquetaModulo, True, True, 0)
        etiquetaNota = Gtk.Label(label="Nota")
        cajaAlumnoModulo.pack_start(etiquetaNota, True, True, 0)
        campoTextoNotaSI = Gtk.Entry(name = "SI")
        cajaAlumnoModulo.pack_start(campoTextoNotaSI, True, True, 0)
        checkInglesSI = Gtk.CheckButton()
        checkInglesSI.set_label("Ingles")
        cajaAlumnoModulo.pack_start(checkInglesSI, True, True, 0)
        caja.pack_start(cajaAlumnoModulo, True, True, 2)

        # Caja para los datos del alumno (Modulo, Nota, un check box de si la curso en ingles o no) en horizontal
        cajaAlumnoModulo = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=10)
        etiquetaModulo = Gtk.Label(label="COD")
        cajaAlumnoModulo.pack_start(etiquetaModulo, True, True, 0)
        etiquetaNota = Gtk.Label(label="Nota")
        cajaAlumnoModulo.pack_start(etiquetaNota, True, True, 0)
        campoTextoNotaCOD = Gtk.Entry(name="COD")
        cajaAlumnoModulo.pack_start(campoTextoNotaCOD, True, True, 0)
        checkInglesCOD = Gtk.CheckButton()
        checkInglesCOD.set_label("Ingles")
        cajaAlumnoModulo.pack_start(checkInglesCOD, True, True, 0)
        caja.pack_start(cajaAlumnoModulo, True, True, 2)

        # Caja para los datos del alumno (Modulo, Nota, un check box de si la curso en ingles o no) en horizontal
        cajaAlumnoModulo = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=10)
        etiquetaModulo = Gtk.Label(label="Prog")
        cajaAlumnoModulo.pack_start(etiquetaModulo, True, True, 0)
        etiquetaNota = Gtk.Label(label="Nota")
        cajaAlumnoModulo.pack_start(etiquetaNota, True, True, 0)
        campoTextoNotaProg = Gtk.Entry(name="Prog")
        cajaAlumnoModulo.pack_start(campoTextoNotaProg, True, True, 0)
        checkInglesProg = Gtk.CheckButton()
        checkInglesProg.set_label("Ingles")
        cajaAlumnoModulo.pack_start(checkInglesProg, True, True, 0)
        caja.pack_start(cajaAlumnoModulo, True, True, 2)

        # Boton que tome los datos metidos en todos los entrys anteriores asi como el resultado del check box y los meta en una lista
        botonGuardar = Gtk.Button(label="Guardar")
        botonGuardar.connect("clicked", self.on_btnGuardar_clicked, [campoTextoNombre, campoTextoApellido, campoTextoNotaSI , checkInglesSI, checkInglesCOD, campoTextoNotaCOD, campoTextoNotaProg, checkInglesProg])
        caja.pack_start(botonGuardar, True, True, 2)


        self.add(caja)

        self.connect("delete-event", Gtk.main_quit) ## la el segundo argumento no debe tener el parentesis de funcion, ya que en ese caso la ejecutaria

        self.show_all()
    def on_btnGuardar_clicked(self, referenciaSeñalBoton, listaDeCampos):
        for campo in listaDeCampos:
            # Por si el campo es el check box
            if isinstance(campo, Gtk.CheckButton):
                if campo.get_active():
                    print(campo.get_label()+" esta activado")
                else:
                    print(campo.get_label()+" esta desactivado")
            else:
                # Mostrar el texto de la etiqueta que acompaña al entry
                print(campo.get_name())
                # Mostrar el texto del entry
                print(campo.get_text())

    def on_entrada_activate(self, entrada, etiqueta):
        print("presionadito")
        etiqueta.set_text(entrada.get_text())
    def buttonWithColor(self, color):
        rgba = Gdk.RGBA()
        rgba.parse(color)

        boton = Gtk.Button()
        area = Gtk.DrawingArea()
        area.set_size_request(32,24)
        area.connect("draw",self.on_debuxa, {"color": rgba})

        boton.add(area)
        return boton

if __name__ == "__main__":
    FestraPrincipal()
    Gtk.main()

