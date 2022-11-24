#!/usr/bin/env python3

browser_desktop_file = '/usr/share/applications/firedragon.desktop'

with open(browser_desktop_file, "rt") as file:
    data = file.read()
    data = data.replace('Exec=', 'Exec=env MOZ_USE_XINPUT2=1 ')

with open( browser_desktop_file,"wt") as file:
    file.write(data)
