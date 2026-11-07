# Antigravity Agent Rules - Nokia 8010 Retro Suite

Bienvenido/a. Este espacio de trabajo gestiona la configuración automática de retro-gaming para la **Nokia Streaming Box 8010** (Android 14 TV) con RetroArch.

---

## 🤖 1. Protocolo de Bienvenida y Onboarding (Para el Amigo del Usuario)
Cuando el usuario abra este workspace y pida configurar su consola, la IA debe seguir este flujo interactivo paso a paso:

1. **Pedir la IP de la Nokia Box:**
   * Indicar cómo mirarla en la TV: `Ajustes (rueda dentada) > Red e Internet > [Tu Wi-Fi] > Dirección IP` (ejemplo: `192.168.1.50`).
   * Recordar activar la depuración si no lo han hecho: `Ajustes > Preferencias del dispositivo > Información > pulsar 7 veces en 'Compilación'` para activar Opciones de desarrollador, y luego activar **Depuración por USB / Depuración por red**.
2. **Verificar el pack de juegos:**
   * Preguntar si ya han colocado el archivo `tiny-best-set-go-games.zip` (descargado de SwissTransfer) dentro de la carpeta `JUEGOS/`.
3. **Comprobar los mandos conectados:**
   * Pedir que conecten sus mandos USB a la Nokia Box.

---

## ⚡ 2. Protocolo de Ejecución Automatizado (Token-Optimized)
El agente **NUNCA debe ejecutar comandos ADB extensos** (`dumpsys input`, `logcat`, `ls` recursivos) directamente en el contexto para ahorrar tokens. Debe usar exclusivamente el CLI maestro:

```bash
# Paso A: Verificar conectividad y mandos físicos detectados
python tools/nokia_helper.py --ip <IP> status

# Paso B: Sincronizar y desduplicar las 1.900+ ROMs y BIOS
python tools/nokia_helper.py --ip <IP> sync

# Paso C: Calibrar mandos (P1/P2), remap de monedas (LB) y listas de reproducción
python tools/nokia_helper.py --ip <IP> all
```

---

## 🎮 3. Explicación de Controles y Uso para el Usuario
Una vez terminada la instalación, el agente debe explicar brevemente al usuario cómo jugar:
* **Entrar/Salir del Menú de RetroArch:** Mantener pulsado el botón **START durante 2 segundos**. *(Protege contra bloqueos de monedas en arcade)*.
* **Insertar Moneda (Arcade):** Pulsar **LB** (Gatillo superior izquierdo) o botón **BACK**.
* **Empezar partida:** Pulsar **START**.
* **Disparo / Acción principal:** Botón **A** (verde).
* **Salto / Acción secundaria:** Botón **B** (rojo).
* **Multijugador:** El Jugador 1 y el Jugador 2 están asignados automáticamente sin conflicto con el mando de la tele.
* **Evitar duplicados al añadir juegos:** Explicar que pueden usar `python tools/nokia_helper.py check-roms <ruta_o_zip>` antes de meter juegos nuevos.
