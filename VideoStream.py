#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gst
from gi.repository import GstVideo  # necesario
from gi.repository import GdkX11

GObject.threads_init()
Gst.init([])


class VideoStream(GObject.GObject):

    def __init__(self, ventana_id):

        GObject.GObject.__init__(self)

        self.ventana_id = ventana_id

        self.pipeline = Gst.Pipeline()

        udpsrc = Gst.ElementFactory.make('udpsrc', "udpsrc")
        udpsrc.set_property("port", 5001)

        avdec_png = Gst.ElementFactory.make('avdec_png', "avdec_png")

        videoconvert = Gst.ElementFactory.make(
            'videoconvert', "videoconvert")
        videorate = Gst.ElementFactory.make('videorate', "videorate")

        xvimagesink = Gst.ElementFactory.make('xvimagesink', "xvimagesink")
        xvimagesink.set_property("force-aspect-ratio", True)
        xvimagesink.set_property("synchronous", False)

        try:
            videorate.set_property("max-rate", 30)

        except:
            pass

        self.pipeline.add(udpsrc)
        self.pipeline.add(avdec_png)
        self.pipeline.add(videoconvert)
        self.pipeline.add(videorate)
        self.pipeline.add(xvimagesink)

        udpsrc.link(avdec_png)
        avdec_png.link(videoconvert)
        videoconvert.link(videorate)
        videorate.link(xvimagesink)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

        self.pipeline.set_state(Gst.State.PLAYING)
        print "OK"
    def __sync_message(self, bus, mensaje):
        """
        Captura los mensajes en el bus del pipe Gst.
        """

        try:
            if mensaje.get_structure().get_name() == 'prepare-window-handle':
                mensaje.src.set_window_handle(self.ventana_id)
                return

        except:
            pass

    def __on_mensaje(self, bus, mensaje):
        """
        Captura los mensajes en el bus del pipe Gst.
        """

        if mensaje.type == Gst.MessageType.ERROR:
            err, debug = mensaje.parse_error()
            print "###", err, debug
