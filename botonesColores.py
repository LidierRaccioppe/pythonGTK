import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk




class FestraPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Primera ventana con Gtk")


        cajaH = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)

        cajaV1 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 4)
        cajaV1.pack_start(self.boton_con_color("red"), True, True, 2)
        cajaV1.pack_start(self.boton_con_color("yellow"), True, True, 2)
        cajaV1.pack_start(self.boton_con_color("purple"), True, True, 2)
        cajaH.pack_start(cajaV1, True, True, 2)

        cajaH.pack_start(self.boton_con_color("green"), True, True, 2)

        cajaV2 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        cajaV2.pack_start(self.boton_con_color("blue"), True, True, 2)
        cajaV2.pack_start(self.boton_con_color("orange"), True, True, 2)
        cajaH.pack_start(cajaV2, True, True, 2)



        lblEtiqueta = Gtk.Label(label="NOS MATARAN A TODOS NOS MATARAN A TODOS NOS MATARAN A TODOS ")

        ## btnBoton = Gtk.Button().override_background_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(20050))



        self.add(cajaH)

        self.connect("delete-event", Gtk.main_quit) ## la el segundo argumento no debe tener el parentesis de funcion, ya que en ese caso la ejecutaria

        self.show_all()

    def on_dibuja(self, control, cr, datos):
        contexto = control.get_style_context()
        ancho = control.get_allocated_width()
        alto = control.get_allocated_height()
        Gtk.render_background(contexto, cr, 0 , 0, ancho, alto)

        r,g,b,a = datos ["color"]
        cr.set_source_rgba(r,g,b,a)
        cr.rectangle (0,0, ancho, alto)
        cr.fill()


    def boton_con_color(self,  color):
        rgba = Gdk.RGBA()
        rgba.parse(color)

        boton = Gtk.Button()
        area=Gtk.DrawingArea()
        area.set_size_request(32,24)
        area.connect("draw", self.on_dibuja, {"color":rgba})
        boton.add(area)
        return boton

if __name__ == "__main__":
    FestraPrincipal()
    Gtk.main()

