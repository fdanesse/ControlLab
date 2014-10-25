#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands

desktop = os.path.join('/etc/xdg/autostart/', 'ControlLabServer.desktop')
run = os.path.join('/usr/bin/', 'ControlLabServer')
server = os.path.join('/usr/local/share/', 'ControlLabServer.py')

print commands.getoutput('rm %s' % (desktop))
print commands.getoutput('rm %s' % (run))
print commands.getoutput('rm %s' % (server))
