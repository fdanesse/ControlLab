#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

from BasePanel import BasePanel

PATH = os.path.dirname(__file__)

GObject.threads_init()


class Control(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_title("Control")

        archivo = os.path.join(PATH, "Iconos", 'compu.png')
        self.set_icon_from_file(archivo)
        self.modify_bg(0, Gdk.color_parse("#ffffff"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(5)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.panel = BasePanel()

        self.add(self.panel)

        self.show_all()

        self.connect("delete-event", self.__salir)

    def __salir(self, widget=None, event=None):
        Gtk.main_quit()
        sys.exit(0)


if __name__ == "__main__":
    Control()
    Gtk.main()
