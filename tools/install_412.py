import subprocess
import os
import urllib.request
import time

ADB = os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe")
DEV = "192.168.1.128:5555"
URL = "https://github.com/TapiocaFox/Daijishou/releases/download/v1.4.80/412.apk"
DEST = os.path.join(os.path.dirname(__file__), "daijisho_412.apk")

if not os.path.exists(DEST):
    print("Descargando 412.apk...")
    urllib.request.urlretrieve(URL, DEST)
    print("Descarga lista.")

print("Conectando e instalando...")
subprocess.run([ADB, "connect", DEV])
subprocess.run([ADB, "-s", DEV, "uninstall", "com.magneticchen.daijishou"])
res = subprocess.run([ADB, "-s", DEV, "install", DEST], capture_output=True, text=True)
print("Install:", res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)

subprocess.run([ADB, "-s", DEV, "shell", "appops", "set", "com.magneticchen.daijishou", "MANAGE_EXTERNAL_STORAGE", "allow"])
subprocess.run([ADB, "-s", DEV, "shell", "am", "start", "-n", "com.magneticchen.daijishou/.activities.MainActivity"])
time.sleep(3)
subprocess.run([ADB, "-s", DEV, "shell", "screencap", "-p", "/sdcard/daijisho_screen.png"])
subprocess.run([ADB, "-s", DEV, "pull", "/sdcard/daijisho_screen.png", "daijisho_screen.png"])
print("Listo!")
