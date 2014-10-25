#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

from Widgets import WidgetPC


class Izquierda(Gtk.EventBox):

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.modify_bg(0, Gdk.color_parse("#ffffff"))

        self.set_border_width(5)

        self.handlers = {}

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

        for addr in range(8, 9):
            widget = WidgetPC("192.168.1.%s" % addr)
            widget.connect("activar", self.__activar)
            self.base_box.pack_start(widget, False, False, 0)

        #for addr in range(10, 25):
        #    widget = WidgetPC("192.168.5.%s" % addr)
        #    widget.connect("activar", self.__activar)
        #    self.base_box.pack_start(widget, False, False, 0)

        self.show_all()

    def __activar_todas(self, widget, ip, aplicacion, valor):
        """
        Cualquier cambio en el Widget General debe afectar a cada uno de los
        Widgets particulares.
        """
        for widget in self.base_box.get_children()[1:]:
            widget.set_valor(aplicacion, valor)

    def __activar(self, widget, ip, aplicacion, valor):
        """
        Activa y desactiva Handlers.
        """
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
            print "Se vuelve a permitir:", aplicacion, "en:", ip

    def __down(self, widget, aplicacion):
        """
        Manda desactivar aplicaciones en las terminales.
        """
        widget.bloquear(aplicacion)
        return True
