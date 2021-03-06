#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
from gi.repository import Gdk

from Izquierda import Izquierda


class BasePanel(Gtk.Paned):

    def __init__(self):

        Gtk.Paned.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        self.modify_bg(0, Gdk.color_parse("#ffffff"))

        self.izquierda = Izquierda()

        self.pack1(self.izquierda, resize=False, shrink=False)

        self.show_all()

    def salir(self):
        self.izquierda.salir()
