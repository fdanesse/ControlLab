#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import socket
import SocketServer
import commands
import json
import codecs

CONFIG = os.path.join(os.environ["HOME"], ".ControlLabServer.json")


class RequestHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        while 1:
            try:
                entrada = str(self.rfile.readline()).strip()
                if not entrada:
                    self.request.close()
                    return

                respuesta = self.__procesar(entrada,
                    str(self.client_address[0]))

                if respuesta:
                    while len(respuesta) < 200:
                        respuesta = "%s*" % respuesta
                    self.wfile.write(respuesta)
                else:
                    self.request.close()

            except socket.error, err:
                self.request.close()

    def __procesar(self, entrada, ip):
        datos = entrada.split(",")
        if datos:
            if datos[0] == "Apagar":
                commands.getoutput('sudo shutdown -h now')
                return "OK"
            elif datos[0] == "Down":
                for dat in datos[1:]:
                    self.server.bloquear(dat)
                return "OK"
            elif datos[0] == "Up":
                for dat in datos[1:]:
                    self.server.desbloquear(dat)
                return "OK"
            else:
                return "OK"
        else:
            return "NO"


class Server(SocketServer.ThreadingMixIn, SocketServer.ThreadingTCPServer):

    def __init__(self, logger=None, host='localhost',
        port=5555, handler=RequestHandler):
        SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler)

        self.allow_reuse_address = True
        self.socket.setblocking(0)
        print "Server ON . . ."

    def bloquear(self, dat):
        _dict = get_dict()
        _dict[dat] = True
        set_dict(_dict)
        commands.getoutput("killall %s" % dat)

    def desbloquear(self, dat):
        _dict = get_dict()
        if _dict.get(dat, False):
            del(_dict[dat])
            set_dict(_dict)

    def shutdown(self):
        print "Server OFF"
        SocketServer.ThreadingTCPServer.shutdown(self)


def make_config_file():
    _dict = {}
    archivo = open(CONFIG, "w")

    archivo.write(
        json.dumps(
            _dict,
            indent=4,
            separators=(", ", ":"),
            sort_keys=True
            )
        )

    archivo.close()


def get_dict():
    archivo = codecs.open(CONFIG, "r", "utf-8")
    _dict = json.JSONDecoder(encoding="utf-8").decode(archivo.read())
    archivo.close()
    return _dict


def set_dict(_dict):
    archivo = open(CONFIG, "w")
    archivo.write(
        json.dumps(
            _dict,
            indent=4,
            separators=(", ", ":"),
            sort_keys=True))
    archivo.close()


def __return_ip(interfaz):
    import commands
    import platform
    sistema = platform.platform()
    text = commands.getoutput('ifconfig %s' % interfaz).splitlines()
    datos = ''
    for linea in text:
        if 'olpc' in sistema:
            if 'inet ' in linea and 'netmask ' in linea and 'broadcast ' in linea:
                datos = linea
                break
        else:
            if 'Direc. inet:' in linea and 'Difus.:' in linea and 'Másc:' in linea:
                datos = linea
                break
    ip = ''
    if datos:
        if 'olpc' in sistema:
            ip = datos.split('inet ')[1].split('netmask ')[0].strip()
        else:
            ip = datos.split('Direc. inet:')[1].split('Difus.:')[0].strip()
    return ip


def get_ip():
    ip = __return_ip("wlan0")
    if not ip:
        ip = __return_ip("eth0")
    if not ip:
        ip = False
    return ip


if __name__ == "__main__":
    make_config_file()
    ip = get_ip()
    while not ip:
        time.sleep(2)
        ip = get_ip()
    server = Server(host=ip, port=5555, handler=RequestHandler)
    server.serve_forever()
    server.shutdown()
    del(server)
    server = False
