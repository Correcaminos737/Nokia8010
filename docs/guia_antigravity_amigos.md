# 🚀 Guía de Bienvenida y Configuración con Antigravity (Para Amigos)

¡Bienvenido/a al gestor retro para tu **Nokia Streaming Box 8010**!

Este proyecto está diseñado para funcionar de forma **100% automatizada** utilizando tu asistente de IA **Google Antigravity**. No necesitas saber de comandos de terminal, ADB ni editar ficheros de configuración complejos: **Antigravity lo hará todo por ti.**

---

## 💬 Cómo empezar en Antigravity (En 1 solo mensaje)

Abre este proyecto en tu Antigravity y escribe en el chat:

> *"Hola Antigravity, ayúdame a configurar mi Nokia Box 8010"*

El asistente leerá automáticamente las reglas del proyecto (`.agent/rules.md`), te pedirá los datos que necesita y ejecutará la instalación paso a paso.

---

## 📋 Preparativos Previos (Solo 3 cosas)

Antes de pedirle a Antigravity que empiece, asegúrate de tener estos 3 puntos listos:

### 1. Activar la Depuración en tu Nokia Box
1. En tu Nokia Box 8010, entra a **Ajustes** (icono de rueda dentada) > **Preferencias del dispositivo** > **Información**.
2. Baja hasta **Compilación del SO de Android TV** y pulsa el botón central del mando **7 veces seguidas** (aparecerá un mensaje diciendo *"¡Ya eres desarrollador!"*).
3. Vuelve atrás y entra en el nuevo menú **Opciones para desarrolladores**.
4. Activa la opción **Depuración por USB** (o **Depuración por red**).

### 2. Conocer la Dirección IP de tu Nokia Box
En la televisión, ve a:
* **Ajustes** > **Red e Internet** > Selecciona tu red Wi-Fi > **Dirección IP** (ejemplo: `192.168.1.45`).
*(Ten a mano este número, Antigravity te lo pedirá en el chat)*.

### 3. Colocar el Pack de Juegos
1. Descarga el archivo `tiny-best-set-go-games.zip` (5,3 GB) desde el enlace de **SwissTransfer** que te envió tu amigo.
2. Cópialo tal cual (sin descomprimir) dentro de la carpeta:
   ```
   Nokia8010/JUEGOS/tiny-best-set-go-games.zip
   ```
3. Conecta tus mandos USB (Xbox, EasySMX, etc.) a los puertos USB de la Nokia Box.

---

## 🕹️ ¿Qué hará Antigravity automáticamente?

Cuando le des tu IP a Antigravity, ejecutará las siguientes tareas en segundo plano:

1. **Conexión y Chequeo:** Se conecta por Wi-Fi a tu Nokia Box y detecta tus mandos físicos.
2. **Transferencia de ROMs:** Extrae las más de 1.900 ROMs y BIOS y las copia organizadas a `/sdcard/ROMs/`.
3. **Calibración de Mandos (2 Jugadores):** Configura el Jugador 1 y Jugador 2 para que el mando a distancia de la tele no interfiera en tus partidas.
4. **Protección Arcade (Coin Lockout):** Asigna el gatillo **LB** para insertar monedas limpiamente y fija la combinación para abrir el menú de pausa manteniendo **START durante 2 segundos** (así nunca se colgará un juego arcade por pulsar Select + Start).
5. **Listas de Reproducción:** Crea las 12 listas de consolas con miniaturas oficiales habilitadas.

---

## 🎮 Controles de Referencia una vez Instalado

| Acción | Botón en Mando (Xbox Layout) | Función |
| :--- | :--- | :--- |
| **Acción 1 / Disparo** | **Botón A** (verde) | Fuego principal / Aceptar |
| **Acción 2 / Salto** | **Botón B** (rojo) | Salto / Atrás / Cancelar |
| **Insertar Moneda (Arcade)** | **Botón LB** (gatillo sup. izquierdo) o **BACK** | Insert Coin sin errores |
| **Empezar Partida** | **Botón START** | Player 1 Start / Pausa |
| **Menú de RetroArch (Guardar/Salir)**| **Mantener START durante 2 segundos** | Abre el Menú Rápido |
| **Movimiento** | **Cruceta (D-Pad) o Joystick Analógico** | Ambos habilitados |

---

## ➕ ¿Quieres añadir más juegos en el futuro sin duplicados?
El proyecto incluye un catálogo con los 1.904 juegos ya cargados. Si te descargas una nueva carpeta o archivo de ROMs, simplemente dile a Antigravity:

> *"Antigravity, comprueba si este paquete de juegos tiene duplicados: C:\Descargas\NuevosJuegos.zip"*

Antigravity analizará el paquete y te dirá exactamente qué juegos son nuevos y cuáles ya tenías para no malgastar espacio en tu Nokia Box.
