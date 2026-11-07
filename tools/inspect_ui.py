import subprocess
import os
import re

ADB = os.path.expandvars(r'%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe')
DEV = '192.168.1.128:5555'

subprocess.run([ADB, 'connect', DEV])
subprocess.run([ADB, '-s', DEV, 'shell', 'uiautomator', 'dump', '/sdcard/window_dump.xml'])
subprocess.run([ADB, '-s', DEV, 'pull', '/sdcard/window_dump.xml', 'window_dump.xml'])

if os.path.exists('window_dump.xml'):
    with open('window_dump.xml', 'r', encoding='utf-8', errors='ignore') as f:
        xml = f.read()
    texts = re.findall(r'text="([^"]+)"', xml)
    print('Textos en pantalla:', [t.encode('ascii', 'ignore').decode() for t in texts])
    descs = re.findall(r'content-desc="([^"]+)"', xml)
    print('Descripciones:', [d.encode('ascii', 'ignore').decode() for d in descs])
