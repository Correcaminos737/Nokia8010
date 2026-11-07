import subprocess
import os
import urllib.request

ADB_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe")
DEVICE_IP = "192.168.1.128:5555"
APK_URL = "https://github.com/TapiocaFox/Daijishou/releases/download/v1.5.0/416.apk"
APK_LOCAL = os.path.join(os.path.dirname(__file__), "daijisho.apk")

print(f"Descargando Daijishou APK desde {APK_URL}...")
urllib.request.urlretrieve(APK_URL, APK_LOCAL)
print(f"Descargado con exito en {APK_LOCAL} ({os.path.getsize(APK_LOCAL)} bytes).")

print("Conectando al Nokia 8010...")
subprocess.run([ADB_PATH, "connect", DEVICE_IP], check=True)

print("Instalando APK en el Nokia 8010...")
res = subprocess.run([ADB_PATH, "-s", DEVICE_IP, "install", "-r", APK_LOCAL], capture_output=True, text=True)
print("Resultado:", res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)

# Comprobar instalacion
res_pkg = subprocess.run([ADB_PATH, "-s", DEVICE_IP, "shell", "pm", "list", "packages", "daijishou"], capture_output=True, text=True)
print("Verificacion paquete:", res_pkg.stdout.strip())
