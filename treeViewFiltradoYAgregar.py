import time

import gi
import sqlite3 as dbapi


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

"""

columnas = ("Nombre", "Apellido", "Numero de teléfono")
agendaTelefonica = (
                    ("Pepe", "Pérez", "986 444 555"),
                    ("Ana", "Yañéz", "985 333 777"),
                    ("Roque", "Díz", "987 222 889"),
                    )
"""


class FestraPrincipal(Gtk.Window):
    global handlerConnectionAceptar
    handlerConnectionAceptar = None
    handlerConnectionCancelar = None
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo Treeview Filtrado")

        self.set_default_size(250, 100)
        self.set_border_width(10)
        caja = Gtk.Box (orientation=Gtk.Orientation.VERTICAL, spacing=4)

        """
        - Boton borrar  con confirmacion
        - ToolTips 
        - confirmacion de la operacion realizada
        -- etiqueta
        -- limpiar campos
        -- Sonido
        -- Progrres bar
        - Campo Fallecido en el treeview
        - Informar de los 
        - Teclas de acceso rapido
        - Iconos
        - Dar opcion a cambiar el tamaño de letra
        - Opcion de cambio de idioma
        - Verificar que los datos ingresados son correctos, el formato ese tipo, que el dni tenga los caracteres correctos, que la edad sea un numero
        - Edicion en las celdas
        
        """

        # caja general
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path('estilo.css')

        self.contexto = Gtk.StyleContext()
        self.screen = Gdk.Screen.get_default()
        self.contexto.add_provider_for_screen(self.screen, self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


        self.filtradoGenero = "None"

        self.modelo = Gtk.ListStore(str,str,int,str,bool)
        self.modelo_filtrado = self.modelo.filter_new()
        print(type(self.modelo_filtrado))
        self.modelo_filtrado.set_visible_func(self.filtro_usuarios_genero)
        print(self.modelo_filtrado)
        try:
            bbdd = dbapi.connect("baseDatos.dat")
            cursor = bbdd.cursor()
            cursor.execute("select * from usuarios")
            for fila in cursor:
                self.modelo.append(fila)
        except dbapi.DatabaseError as e:
            print("Error al cargar el ListStores")
        finally:
            cursor.close()
            bbdd.close()

        #vistaVerdista = Gtk.TreeView(model=modelo)
        self.vistaVerdista = Gtk.TreeView(model=self.modelo_filtrado)
        ventanaScroll  = Gtk.ScrolledWindow()
        ventanaScroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        ventanaScroll.set_size_request(200, 132)
        ventanaScroll.add(self.vistaVerdista)
        self.objetoSeleccion = self.vistaVerdista.get_selection()
        self.objetoSeleccion.connect("changed",self.on_objetoSeleccion_changed)

        for i, tituloColumna in enumerate  (["Dni", "Nombre"]):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(tituloColumna, celda, text=i)
            self.vistaVerdista.append_column(columna)

        celda = Gtk.CellRendererProgress()
        columna = Gtk.TreeViewColumn("Edad", celda, value=2)
        self.vistaVerdista.append_column(columna)


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
        celda.connect("edited", self.on_celdaCombo_edited, self.modelo_filtrado, 3)
        columna = Gtk.TreeViewColumn("Genero", celda, text=3)
        self.vistaVerdista.append_column(columna)
        caja.pack_start(ventanaScroll, True, True, 2)

        cajaH = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        caja.pack_start(cajaH, True, True, 0)

        rbtHombre = Gtk.RadioButton.new_with_label(None,"Hombre")
        rbtMujer = Gtk.RadioButton.new_with_label_from_widget(rbtHombre, label="Mujer")
        rbtOtros = Gtk.RadioButton.new_with_label_from_widget(rbtHombre, label="Otros")
        cajaH.pack_start(rbtHombre, True, True, 2)
        cajaH.pack_start(rbtMujer, True, True, 2)
        cajaH.pack_start(rbtOtros, True, True, 2)


        rbtHombre.connect("toggled", self.on_genero_toggled, "Hombre", self.modelo_filtrado)
        rbtMujer.connect("toggled", self.on_genero_toggled, "Mujer", self.modelo_filtrado)
        rbtOtros.connect("toggled", self.on_genero_toggled, "Otros", self.modelo_filtrado)

        cajaHGrande = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)

        cajaHGrande.pack_start(caja, True, True, 2)

        cajaVSegunda = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)

        self.lblNombre = Gtk.Label(label="Nombre:")
        self.lblDNI = Gtk.Label(label="DNI:")
        self.lblEdad = Gtk.Label(label="Edad:")
        self.lblGenero = Gtk.Label(label="Genero:")
        self.campoNombre = Gtk.Entry()
        self.campoNombre.set_tooltip_text("Nombre de la persona a crear o insertar")
        self.campoDNI = Gtk.Entry()
        self.campoEdad = Gtk.Entry()
        self.cmbGenero = Gtk.ComboBox()
        self.chkFallecido = Gtk.CheckButton(label="Fallecido")


        generos = [
            "Hombre",
            "Mujer",
            "Otros",
        ]
        self.cmbGenero = Gtk.ComboBoxText()
        self.cmbGenero.set_entry_text_column(0)
        # currency_combo.connect("changed", self.on_currency_combo_changed)
        for genero in generos:
            self.cmbGenero.append_text(genero)

        self.cmbGenero.set_active(0)

        cajaHPequenaPrimera = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        cajaHPequenaPrimera.pack_start(self.lblNombre,True, True, 0)
        cajaHPequenaPrimera.pack_start(self.campoNombre, True, True, 0)
        cajaHPequenaPrimera.pack_start(self.lblDNI,True, True, 0)
        cajaHPequenaPrimera.pack_start(self.campoDNI, True, True, 0)
        cajaHPequenaPrimera.set_size_request(40,15)


        cajaHPequenaSegunda = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        cajaHPequenaSegunda.pack_start(self.lblEdad,True, True, 0)
        cajaHPequenaSegunda.pack_start(self.campoEdad, True, True, 0)
        cajaHPequenaSegunda.pack_start(self.lblGenero,True, True, 0)
        cajaHPequenaSegunda.pack_start(self.cmbGenero, True, True, 0)
        cajaHPequenaSegunda.pack_start(self.chkFallecido, True, True, 0)
        cajaHPequenaSegunda.set_size_request(40,15)

        self.barraProgreso = Gtk.ProgressBar()
        cajaHPequenaSegunda.pack_start(self.barraProgreso, True, True,0)
        self.contadorActividad = 100
        self.temporizador = GLib.timeout_add(50, self.on_contador, None)

        self.spinner = Gtk.Spinner()
        self.spinner.hide()
        cajaHPequenaSegunda.pack_start(self.spinner, True, True,0)



        cajaVSegunda.pack_start(cajaHPequenaPrimera,True, True, 0)
        cajaVSegunda.pack_start(cajaHPequenaSegunda,True, True, 0)


        cajaHPequenaTercera = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)


        self.btnNuevo = Gtk.Button.new_with_mnemonic(label="_Nuevo")
        self.btnNuevo.connect("clicked", self.on_btnNuevo_clicked)
        self.btnEditar = Gtk.Button(label="Editar")
        self.btnEditar.connect("clicked", self.on_btnEditar_clicked)
        self.btnAceptar = Gtk.Button(label="Aceptar")
        self.btnCancelar = Gtk.Button(label="Cancelar")
        self.btnCancelar.connect("clicked", self.on_btnCancelar_clicked)

        cajaHPequenaTercera.pack_start(self.btnNuevo,True, True, 0)
        cajaHPequenaTercera.pack_start(self.btnEditar,True, True, 0)
        cajaHPequenaTercera.pack_start(self.btnAceptar,True, True, 0)
        cajaHPequenaTercera.pack_start(self.btnCancelar,True, True, 0)
        cajaVSegunda.pack_start(cajaHPequenaTercera, True, True, 0)


        txvConsola = Gtk.TextView()
        self.bufferTexto = Gtk.TextBuffer()
        txvConsola.set_buffer(self.bufferTexto)

        cajaVSegunda.pack_start(txvConsola, True, True, 0)

        self.deshabilitarControles()
        cajaHGrande.pack_start(cajaVSegunda, True, True, 0)
        self.add(cajaHGrande)

        self.connect("delete-event", Gtk.main_quit)  ## la el segundo argumento no debe tener el parentesis de funcion, ya que en ese caso la ejecutaria

        self.show_all()

        self.btnAceptar.hide()
        self.btnCancelar.hide()
    def deshabilitarControles(self):
        self.lblNombre.set_sensitive(False)
        self.lblDNI.set_sensitive(False)
        self.lblEdad.set_sensitive(False)
        self.lblGenero.set_sensitive(False)

        self.campoNombre.set_sensitive(False)
        self.campoDNI.set_sensitive(False)
        self.campoEdad.set_sensitive(False)
        self.cmbGenero.set_sensitive(False)
        self.chkFallecido.set_sensitive(False)
    def habilitarControles(self):
        self.lblNombre.set_sensitive(True)
        self.lblDNI.set_sensitive(True)
        self.lblEdad.set_sensitive(True)
        self.lblGenero.set_sensitive(True)

        self.campoNombre.set_sensitive(True)
        self.campoDNI.set_sensitive(True)
        self.campoEdad.set_sensitive(True)
        self.cmbGenero.set_sensitive(True)
        self.chkFallecido.set_sensitive(True)

    def on_contador(self, datosExtras):
        if self.contadorActividad<100:
            self.contadorActividad +=1
            self.barraProgreso.set_fraction(self.contadorActividad/100)
        else:
            self.barraProgreso.hide()
            self.spinner.stop()
        return True
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
    def on_btnNuevo_clicked(self, algo):
        self.btnNuevo.hide()
        self.btnEditar.hide()
        global handlerConnectionAceptar
        handlerConnectionAceptar = self.btnAceptar.connect("clicked", self.on_btnAceptarNuevo_clicked)
        self.btnAceptar.show()
        self.btnCancelar.show()

        self.habilitarControles()
    def on_btnEditar_clicked(self, algo):
        self.btnNuevo.hide()
        self.btnEditar.hide()
        global handlerConnectionAceptar
        handlerConnectionAceptar = self.btnAceptar.connect("clicked", self.on_btnAceptarEditar_clicked)
        self.btnAceptar.show()
        self.btnCancelar.show()


        (modelo,fila) = self.objetoSeleccion.get_selected()
        dni = modelo[fila][0] if modelo[fila][0] is not None else ""
        nombre = modelo[fila][1] if modelo[fila][1] is not None else ""
        edad = str(modelo[fila][2]) if modelo[fila][2] is not None else ""

        self.campoNombre.set_text(nombre)
        self.campoDNI.set_text(dni)
        self.campoEdad.set_text(edad)

        if modelo[fila][3] == "Hombre":
            self.cmbGenero.set_active(0)
        elif modelo[fila][3] == "Mujer":
            self.cmbGenero.set_active(1)
        elif modelo[fila][3] == "Otros":
            self.cmbGenero.set_active(2)

        if modelo[fila][4] == True:
            self.chkFallecido.set_active(True)
        else:
            self.chkFallecido.set_active(False)

        self.habilitarControles()
    def on_btnCancelar_clicked(self, algo):
        self.btnAceptar.hide()
        global handlerConnectionAceptar
        self.btnAceptar.disconnect(handlerConnectionAceptar)
        handlerConnectionAceptar = None
        self.btnCancelar.hide()
        self.btnNuevo.show()
        self.btnEditar.show()


        self.lblNombre.set_name("normal")
        self.lblDNI.set_name("normal")
        self.lblEdad.set_name("normal")
        self.contexto.add_provider_for_screen(self.screen, self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


        self.deshabilitarControles()

        self.campoNombre.set_text("")
        self.campoEdad.set_text("")
        self.campoDNI.set_text("")
        self.chkFallecido.set_active(False)
    def on_btnAceptarNuevo_clicked(self, algo):
        self.btnAceptar.hide()
        global handlerConnectionAceptar
        self.btnAceptar.disconnect(handlerConnectionAceptar)
        handlerConnectionAceptar = None
        self.btnCancelar.hide()
        self.btnNuevo.show()
        self.btnEditar.show()

        self.deshabilitarControles()


        print("aceptar nuevo")


        if self.comprobar_dni_formato() and self.comprobar_edad():
            try:
                bbdd = dbapi.connect("baseDatos.dat")
                cursor = bbdd.cursor()
                # cursor.execute("""insert into usuarios values ( '3333-a',"Ana Perez",19, "Mujer", True)""")
                datos = (
                        (self.campoDNI.get_text(), self.campoNombre.get_text(),self.campoEdad.get_text(), self.cmbGenero.get_active_text(),self.chkFallecido.get_active())
                        )
                cursor.execute("""insert into usuarios values ( ?,?,?,?,?)""",datos)
                print("Insertado con Exito")
                mensageInsertado = "\nNuevo usuario guardado"
                self.bufferTexto.insert_at_cursor(mensageInsertado,len(mensageInsertado))
                bbdd.commit()

                # Obtén el modelo subyacente desde el modelo filtrado
                model_filter = self.vistaVerdista.get_model()
                model = model_filter.get_model()


                datos = (
                        (self.campoDNI.get_text(), self.campoNombre.get_text(),int(self.campoEdad.get_text()), self.cmbGenero.get_active_text(),self.chkFallecido.get_active())
                        )

                # Agrega los datos directamente al modelo conectado al Gtk.TreeView
                model.append(datos)
                """
                modelito = self.modelo_filtrado.get_model()
                modelito.append(datos)
                self.modelo_filtrado = modelito.filter_new()
                """
            except dbapi.DatabaseError as e:
                print("Error al insertar")

            self.campoNombre.set_text("")
            self.campoEdad.set_text("")
            self.campoDNI.set_text("")
            self.chkFallecido.set_active(False)

            self.barraProgreso.show()
            self.contadorActividad = 0

            self.spinner.show()
            self.spinner.start()

        else:
            print("Error en el dni o edad")


    def on_btnAceptarEditar_clicked(self, fila,):
        self.btnAceptar.hide()
        self.btnAceptar.disconnect(handlerConnectionAceptar)
        self.btnCancelar.hide()
        self.btnNuevo.show()
        self.btnEditar.show()

        self.spinner.show()
        self.spinner.start()

        self.deshabilitarControles()

        datos = (
            (self.campoDNI.get_text(), self.campoNombre.get_text(), self.campoEdad.get_text(),
             self.cmbGenero.get_active_text(), self.chkFallecido.get_active())
        )
        if self.comprobar_dni_formato() and self.comprobar_edad():
            try:
                bbdd = dbapi.connect("baseDatos.dat")
                cursor = bbdd.cursor()
                # cursor.execute("""insert into usuarios values ( '3333-a',"Ana Perez",19, "Mujer", True)""")
                datos = (
                        (self.campoNombre.get_text(),int(self.campoEdad.get_text()), self.cmbGenero.get_active_text(),self.chkFallecido.get_active(), self.campoDNI.get_text())
                        )
                print(datos)
                cursor.execute("update usuarios set nombre=?, edad = ?, genero=?, fallecido = ? where dni=?", datos)
                print("Actualizado con Exito")
                mensageActualizado = "Usuario Modificado"
                self.bufferTexto.insert_at_cursor(mensageActualizado, len(mensageActualizado))
                bbdd.commit()


                # Obtén el modelo subyacente desde el modelo filtrado
                model_filter = self.vistaVerdista.get_model()
                model = model_filter.get_model()
                datos = (
                        (self.campoDNI.get_text(), self.campoNombre.get_text(),int(self.campoEdad.get_text()), self.cmbGenero.get_active_text(),self.chkFallecido.get_active())
                        )

                # Agrega los datos directamente al modelo conectado al Gtk.TreeView
                # Recordar que funciona como un pequeño mutable

                (modelo, fila) = self.objetoSeleccion.get_selected()

                modelo[fila][0] = self.campoDNI.get_text()
                modelo[fila][1] = self.campoNombre.get_text()
                modelo[fila][2] = int(self.campoEdad.get_text())


            except dbapi.DatabaseError as e:
                print("Error al actualizar")
        else:
            print("valor de edad o dni incorrecto")
    def comprobar_dni_formato(self):
        dni = self.campoDNI.get_text()
        if len(dni)==10:
            if dni[0:7].isdigit() and dni[8] == "-" and dni[9].isupper():
                self.campoDNI.set_name("normal")
                print("Dni Valido")
                return True
            else:
                print("Error, el Dni debe de tener 8 digitos, un guion y una letra en mayuscula")
                self.campoDNI.set_name("error")
                self.contexto.add_provider_for_screen(self.screen, self.css_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
                return False
        else:
            self.campoDNI.set_name("error")
            self.contexto.add_provider_for_screen(self.screen, self.css_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            print("Error: el dni debe tener 10 elementos")
    def comprobar_edad(self):
        edad= self.campoEdad.get_text()
        if edad.isdigit():
            if int(edad)>0:
                self.campoEdad.set_name("normal")
                return True
            else:
                self.campoEdad.set_name("error")
                print("Edad debe ser mayor de 0")
                return False
        else:
            self.campoEdad.set_name("error")
            print("Edad debe ser un numero")

    def on_objetoSeleccion_changed(self, objetoSeleccion):
        (modelo,fila) = objetoSeleccion.get_selected()
        global handlerConnectionAceptar

        if handlerConnectionAceptar is not None:
            if fila is not None:
                if modelo[fila] is not None:
                    # Verificar cada campo antes de asignarlo al Entry
                    # Leerlo de forma natural, es raro si se usa la vista entrenada de nuestro enseñador java
                    dni = modelo[fila][0] if modelo[fila][0] is not None else ""
                    nombre = modelo[fila][1] if modelo[fila][1] is not None else ""
                    edad = str(modelo[fila][2]) if modelo[fila][2] is not None else ""

                    self.campoNombre.set_text(nombre)
                    self.campoDNI.set_text(dni)
                    self.campoEdad.set_text(edad)

                    if modelo[fila][3] == "Hombre":
                        self.cmbGenero.set_active(0)
                    elif modelo[fila][3] == "Mujer":
                        self.cmbGenero.set_active(1)
                    elif modelo[fila][3] == "Otros":
                        self.cmbGenero.set_active(2)

                    if modelo[fila][4] == True:
                        self.chkFallecido.set_active(True)
                    else:
                        self.chkFallecido.set_active(False)
                else:
                    # Limpiar los Entry si el modelo[fila] es None
                    self.campoNombre.set_text("")
                    self.campoDNI.set_text("")
                    self.campoEdad.set_text("")
                    # Desactivar los botones de opción
                    self.cmbGenero.set_active(False)
                    self.cmbGenero.set_active(False)
                    self.cmbGenero.set_active(False)
            else:
                # Limpiar los Entry si fila es None
                self.campoNombre.set_text("")
                self.campoDNI.set_text("")
                self.campoEdad.set_text("")
                # Desactivar los botones de opción
                self.cmbGenero.set_active(False)
                self.cmbGenero.set_active(False)
                self.cmbGenero.set_active(False)



if __name__ == "__main__":
    FestraPrincipal()
    Gtk.main()

