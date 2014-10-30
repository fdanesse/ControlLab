#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time

from gi.repository import GObject

#15 19 24


class Client(GObject.Object):

    __gsignals__ = {
    "error": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_INT,)),
    "connected": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,))}

    def __init__(self, ip):

        GObject.Object.__init__(self)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dir = (ip, 5555)

        print "Encendiendo Cliente para: %s . . ." % ip

    def conectarse(self):
        try:
            self.socket.connect(self.dir)
            self.socket.setblocking(0)
            time.sleep(0.5)
            self.emit("connected", True)
        except socket.error, err:
            # FIXME: socket.error:
            # [Errno 111] Conexión rehusada
            # [Errno 113] No existe ninguna ruta hasta el «host»
            self.emit("error", err.errno)
            self.emit("connected", False)

    def desconectarse(self):
        self.socket.close()
        time.sleep(0.5)

    def enviar(self, datos):
        datos = "%s\n" % datos
        enviado = False
        while not enviado:
            try:
                self.socket.sendall(datos)
                enviado = True
            except socket.error, err:
                # FIXME: socket.error
                # [Errno 32] Tubería rota
                self.emit("error", err.errno)
                return False
            time.sleep(0.02)

    def recibir(self):
        entrada = ""
        while not entrada:
            try:
                entrada = self.socket.recv(200)
                entrada = entrada.replace("*", "").strip()
            except socket.error, err:
                print "Error Recibir:", err
                # FIXME: socket.error
                # [Errno 107] El otro extremo de la conexión no está conectado
                # [Errno 11] Recurso no disponible temporalmente
                self.emit("error", err.errno)
                return False
        return entrada
