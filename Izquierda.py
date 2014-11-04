#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import threading

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib

from Widgets import WidgetPC

DICT = {
    "base": "192.168.1",
    "rango": range(10, 11),
    }


class ConnectionControl(GObject.Object):

    __gsignals__ = {
    "connected": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, GObject.TYPE_BOOLEAN))}

    def __init__(self):

        GObject.Object.__init__(self)

        self.rango = []
        self.indice = 0

        for addr in DICT["rango"]:
            self.rango.append("%s.%s" % (DICT["base"], addr))

    def check_on(self):
        print "Checkeando:", self.rango[self.indice]
        ret = commands.getoutput("nmap -sP %s" % self.rango[self.indice])
        if "Host is up" in ret:
            self.emit("connected", self.rango[self.indice], True)
        else:
            self.emit("connected", self.rango[self.indice], False)
        if self.indice < len(self.rango) - 1:
            self.indice += 1
        else:
            self.indice = 0
        GLib.timeout_add(5000, self.check_on)
        return False


class Izquierda(Gtk.EventBox):

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.modify_bg(0, Gdk.color_parse("#ffffff"))

        self.set_border_width(5)

        self.handlers = {}
        self.control = False
        self.thread = False

        self.base_box = Gtk.VBox()
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.base_box)
        self.add(scroll)

        todas = WidgetPC("Todas")
        todas.connect("activar", self.__activar_todas)
        self.base_box.pack_start(todas, False, False, 0)

        for addr in DICT["rango"]:
            widget = WidgetPC("%s.%s" % (DICT["base"], addr))
            widget.connect("activar", self.__activar)
            self.base_box.pack_start(widget, False, False, 0)

        self.show_all()

        self.control = ConnectionControl()
        self.control.connect("connected", self.__control_update)
        self.thread = threading.Thread(target=self.control.check_on)
        self.thread.start()

    def __control_update(self, control, ip, connected):
        """
        El widget se activa o desactiva segun esté o no
        conectado a su terminal.
        """
        for widget in self.base_box.get_children()[1:]:
            if widget.ip == ip:
                widget.set_color_active(connected)
                break

    def __activar_todas(self, widget, ip, aplicacion, valor):
        for widget in self.base_box.get_children()[1:]:
            widget.set_valor(aplicacion, valor)

    def __activar(self, widget, ip, aplicacion, valor):
        self.__new_handler(widget, ip, aplicacion, valor)

    def __new_handler(self, widget, ip, aplicacion, valor):
        key = "%s-%s" % (ip, aplicacion)
        if self.handlers.get(key, False):
            GLib.source_remove(self.handlers[key])
            del(self.handlers[key])
        if valor:
            self.handlers[key] = GLib.timeout_add(5000,
                self.__down, widget, aplicacion)
        else:
            self.handlers[key] = GLib.timeout_add(5000,
                self.__up, widget, aplicacion)

    def __down(self, widget, aplicacion):
        widget.bloquear(aplicacion)
        return True

    def __up(self, widget, aplicacion):
        widget.desbloquear(aplicacion)
        return True

    def salir(self):
        for widget in self.base_box.get_children()[1:]:
            widget.salir()
