#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands

PATH = os.path.dirname(__file__)

desktop = os.path.join(PATH, 'ControlLabServer.desktop')
run = os.path.join(PATH, 'ControlLabServer')
server = os.path.join(PATH, 'ControlLabServer.py')

print commands.getoutput('cp %s /etc/xdg/autostart/' % (desktop))
print commands.getoutput('cp %s /usr/bin/' % (run))
print commands.getoutput('cp %s /usr/local/share/' % (server))

desktop = os.path.join('/etc/xdg/autostart/', 'ControlLabServer.desktop')
run = os.path.join('/usr/bin/', 'ControlLabServer')
server = os.path.join('/usr/local/share/', 'ControlLabServer.py')

print commands.getoutput('chown root:root %s' % (desktop))
print commands.getoutput('chown root:root %s' % (run))
print commands.getoutput('chown root:root %s' % (server))

print commands.getoutput('chmod 755 %s' % (desktop))
print commands.getoutput('chmod 755 %s' % (run))
print commands.getoutput('chmod 755 %s' % (server))
