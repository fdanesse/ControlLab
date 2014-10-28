#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf
from gi.repository import GLib

from JAMediaTerminal.Terminal import Terminal

base = os.path.dirname(__file__)

APLICACIONES = {
    "Internet": ["chrome", "firefox", "chromium-browser"],
    "Juegos": ["java", "ioquake3", "openarena"],
    }


class WidgetPC(Gtk.EventBox):

    __gsignals__ = {
    "activar": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING, GObject.TYPE_BOOLEAN))}

    def __init__(self, ip):

        Gtk.EventBox.__init__(self)

        self.modify_bg(0, Gdk.color_parse("#ffffff"))

        self.ip = ip
        self.client = False
        self.connected = False
        self.videostream = False
        self.terminal = Terminal()

        frame = Gtk.Frame()
        frame.set_label(self.ip)
        event = Gtk.EventBox()
        event.modify_bg(0, Gdk.color_parse("#ffffff"))
        event.set_border_width(5)
        hbox = Gtk.HBox()
        event.add(hbox)
        frame.add(event)

        drawing = Gtk.DrawingArea()  #gst-launch-0.10 udpsrc port=5001 ! smokedec ! ffmpegcolorspace ! autovideosink
        drawing.connect("realize", self.__realize)
        drawing.modify_bg(0, Gdk.color_parse("#000000"))
        drawing.set_size_request(200, -1)
        hbox.pack_start(drawing, False, False, 5)

        self.vbox = Gtk.VBox()
        boton = Gtk.ToggleButton("Internet")
        boton.connect("toggled", self.__do_toggled)
        self.vbox.pack_start(boton, False, False, 0)

        boton = Gtk.ToggleButton("Juegos")
        boton.connect("toggled", self.__do_toggled)
        self.vbox.pack_start(boton, False, False, 0)

        control = Gtk.ToggleButton("Controlar")
        self.vbox.pack_start(control, False, False, 0)
        control.set_sensitive(False)

        guiar = Gtk.ToggleButton("Guiar")
        self.vbox.pack_start(guiar, False, False, 0)
        guiar.set_sensitive(False)

        hbox2 = Gtk.HBox()
        volumen = ControlVolumen()
        volumen.set_sensitive(False)
        terminal = Gtk.ToggleButton()
        image = Gtk.Image()
        archivo = os.path.join(base, "JAMediaTerminal/Iconos/bash.svg")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, 16, 16)
        image.set_from_pixbuf(pixbuf)
        terminal.set_image(image)
        terminal.connect("toggled", self.__show_terminal)
        hbox2.pack_start(volumen, True, True, 0)
        hbox2.pack_start(terminal, True, True, 0)
        self.vbox.pack_start(hbox2, False, False, 0)

        hbox.pack_start(self.vbox, False, False, 0)
        hbox.pack_start(self.terminal, True, True, 5)

        # Widgets para status
        vbox = Gtk.VBox()
        self.info = Gtk.Label()
        self.info.modify_fg(0, Gdk.color_parse("#00ff00"))
        vbox.pack_start(self.info, False, False, 5)
        self.info1 = Gtk.Label()
        self.info1.modify_fg(0, Gdk.color_parse("#00ff00"))
        vbox.pack_start(self.info1, False, False, 5)
        hbox.pack_start(vbox, False, False, 5)

        self.add(frame)
        self.show_all()

        if self.ip != "Todas":
            self.set_sensitive(False)
            GLib.timeout_add(3000, self.__check_on)

    def __realize(self, drawing):
        self.terminal.hide()
        #if self.ip != "Todas":
        #    from gi.repository import GdkX11
        #    from VideoStream import VideoStream
        #    xid = drawing.get_property('window').get_xid()
        #    self.videostream = VideoStream(xid)

    def __check_on(self):
        ret = commands.getoutput("nmap -sP %s" % self.ip)
        if "Host is up" in ret:
            self.connected = True
            self.info.set_text("Terminal en Linea")
            self.info.modify_fg(0, Gdk.color_parse("#00ff00"))
            if not self.client:
                self.__connect_client()
        else:
            self.connected = False
            self.info.set_text("Terminal Fuera de Linea")
            self.info.modify_fg(0, Gdk.color_parse("#ff0000"))
            self.__desconectarse()
        GLib.timeout_add(3000, self.__check_on)
        return False

    def __desconectarse(self):
        if self.client:
            self.client.desconectarse()
        del(self.client)
        self.client = False
        self.info1.set_text("Cliente Desconectado")
        self.info1.modify_fg(0, Gdk.color_parse("#ff0000"))
        self.set_sensitive(False)

    def __connect_client(self):
        """
        El widget se activa o desactiva segun esté o no
        conectado a su terminal.
        """
        from Client import Client
        self.client = Client(self.ip)
        conectado = self.client.conectarse()
        self.set_sensitive(conectado)
        if conectado:
            self.info1.set_text("Cliente Conectado")
            self.info1.modify_fg(0, Gdk.color_parse("#00ff00"))
            self.client.connect("error", self.__client_error)
        else:
            self.__desconectarse()
        return False

    def __client_error(self, client, error):
        if error == 113:
            # No debiera producirse nunca ya que este error se produce al
            # intentar conectarse y estas se;ales se conectan luego de que se
            # establece la conexion.
            #self.info1.set_text("[Errno 113] No existe ninguna ruta hasta el «host»")
            pass
        elif error == 111:
            # Es casi imposible que se produzca debido a
            # la dinamica de la aplicacion
            #self.info.set_text("[Errno 111] Conexión rehusada")
            pass
        elif error == 107:
            # Es casi imposible que se produzca debido a
            # la dinamica de la aplicacion
            #self.info1.set_text("[Errno 107] El otro extremo de la conexión no está conectado")
            pass
        elif error == 11:
            # Es casi imposible que se produzca debido a
            # la dinamica de la aplicacion
            #self.info1.set_text("[Errno 11] Recurso no disponible temporalmente")
            pass
        elif error == 32:
            # La terminal se conecto y se apago el server, la tuberia se rompe
            #self.info1.set_text("[Errno 32] Tubería rota")
            pass
        self.__desconectarse()

    def __do_toggled(self, widget):
        self.emit("activar", self.ip, widget.get_label(), widget.get_active())

    def __show_terminal(self, widget):
        if widget.get_active():
            self.terminal.show()
        else:
            self.terminal.hide()

    def set_valor(self, aplicacion, valor):
        """
        Activación externa de opciones.
        """
        for boton in self.vbox.get_children():
            if boton.get_label() == aplicacion:
                boton.set_active(valor)
                return

    def bloquear(self, aplicacion):
        """
        Le dice a la terminal que bloquee determinadas aplicaciones.
        """
        if self.client:
            items = list(APLICACIONES[aplicacion])
            text = "Down"
            for item in items:
                text = "%s,%s" % (text, item)
            self.client.enviar(text)


class ControlVolumen(Gtk.VolumeButton):

    __gsignals__ = {
    "volumen": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT,))}

    def __init__(self):

        Gtk.VolumeButton.__init__(self)
        self.show_all()

    def do_value_changed(self, valor):
        self.emit('volumen', valor)
