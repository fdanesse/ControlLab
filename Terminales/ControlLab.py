#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands
import json
import codecs

from gi.repository import GObject
from gi.repository import GLib

CONFIG = os.path.join(os.environ["HOME"], ".ControlLabServer.json")


def get_dict():
    _dict = {}
    if os.path.exists(CONFIG):
        archivo = codecs.open(CONFIG, "r", "utf-8")
        _dict = json.JSONDecoder(encoding="utf-8").decode(archivo.read())
        archivo.close()
    return _dict


class ControlLab(GObject.GObject):

    def __init__(self):

        GObject.GObject.__init__(self)

        GLib.timeout_add(5000, self.__handle)

    def __handle(self):
        _dict = get_dict()
        map(self.__bloquear, _dict.keys())
        GLib.timeout_add(5000, self.__handle)
        return False

    def __bloquear(self, aplicacion):
        print aplicacion
        commands.getoutput("killall %s" % aplicacion)


if __name__ == "__main__":
    control = ControlLab()
    GObject.MainLoop().run()
