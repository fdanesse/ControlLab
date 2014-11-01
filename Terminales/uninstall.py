#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands

desktop = os.path.join('/etc/xdg/autostart/', 'ControlLabServer.desktop')
run = os.path.join('/usr/bin/', 'ControlLabServer')
path = os.path.join('/usr/local/share/ControlLab')

print commands.getoutput('rm %s' % (desktop))
print commands.getoutput('rm %s' % (run))
print commands.getoutput('rm -r %s' % (path))
