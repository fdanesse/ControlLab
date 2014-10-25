#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
from gi.repository import Gdk

from Izquierda import Izquierda


class BasePanel(Gtk.Paned):

    def __init__(self):

        Gtk.Paned.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        self.modify_bg(0, Gdk.color_parse("#ffffff"))

        self.pack1(Izquierda(), resize=False, shrink=False)

        self.show_all()
