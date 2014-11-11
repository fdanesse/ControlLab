#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands

PATH = os.path.dirname(__file__)

# SERVIDOR
desktop = os.path.join(PATH, 'ControlLabServer.desktop')
run = os.path.join(PATH, 'ControlLabServer')
server = os.path.join(PATH, 'ControlLabServer.py')

dir_path = "/usr/local/share/ControlLab"
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

print commands.getoutput('cp %s /etc/xdg/autostart/' % (desktop))
print commands.getoutput('cp %s /usr/bin/' % (run))
print commands.getoutput('cp %s %s' % (server, dir_path))

desktop = os.path.join('/etc/xdg/autostart/', 'ControlLabServer.desktop')
run = os.path.join('/usr/bin/', 'ControlLabServer')
server = os.path.join(dir_path, 'ControlLabServer.py')

#print commands.getoutput('chown root:root %s' % (desktop))
#print commands.getoutput('chown root:root %s' % (run))
#print commands.getoutput('chown root:root %s' % (server))

print commands.getoutput('chmod 755 %s' % (desktop))
print commands.getoutput('chmod 755 %s' % (run))
print commands.getoutput('chmod 755 %s' % (server))

#sudo su
user = raw_input("Ingresa el usuario a controlar: ")
comand = "%s ALL=NOPASSWD:/sbin/shutdown" % user
arch = open('/etc/sudoers', 'r')
text = arch.read()
arch.close()
if not comand in text:
    text = '%s\n%s\n' % (text, comand)
    arch = open('/etc/sudoers', 'w')
    text = arch.write(text)
    arch.close()

# CONTROL
desktop = os.path.join(PATH, 'ControlLab.desktop')
run = os.path.join(PATH, 'ControlLab')
server = os.path.join(PATH, 'ControlLab.py')

print commands.getoutput('cp %s /etc/xdg/autostart/' % (desktop))
print commands.getoutput('cp %s /usr/bin/' % (run))
print commands.getoutput('cp %s %s' % (server, dir_path))

desktop = os.path.join('/etc/xdg/autostart/', 'ControlLab.desktop')
run = os.path.join('/usr/bin/', 'ControlLab')
server = os.path.join(dir_path, 'ControlLab.py')

#print commands.getoutput('chown root:root %s' % (desktop))
#print commands.getoutput('chown root:root %s' % (run))
#print commands.getoutput('chown root:root %s' % (server))

print commands.getoutput('chmod 755 %s' % (desktop))
print commands.getoutput('chmod 755 %s' % (run))
print commands.getoutput('chmod 755 %s' % (server))
