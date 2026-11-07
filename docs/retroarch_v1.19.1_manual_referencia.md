# 🕹️ Manual de Referencia Técnica: RetroArch v1.19.1 (Nokia Streaming Box 8010 - Android 14)

Este documento sirve como guía oficial y referencia estricta para la configuración de controles, teclas rápidas, rutas y estructura en la Nokia Box 8010.

---

## 🎮 1. Arquitectura de Entrada y Mando Virtual (RetroPad)

RetroArch traduce los mandos físicos a una abstracción llamada **RetroPad** (basada en el diseño de Super Nintendo / SNES).

### Mapeo Físico (Xbox / PC Gamepad -> RetroPad)
| RetroPad (SNES) | Mando Físico (Xbox Layout) | Función Estándar Arcade | Función Consola |
| :--- | :--- | :--- | :--- |
| **Botón B (abajo)** | **Botón A** (verde) | Disparo principal / Acción 1 | Botón B / Cancelar |
| **Botón A (derecha)** | **Botón B** (rojo) | Salto / Bomba / Acción 2 | Botón A / Aceptar |
| **Botón Y (izquierda)** | **Botón X** (azul) | Acción 3 / Fuego secundario | Botón Y |
| **Botón X (arriba)** | **Botón Y** (amarillo) | Acción 4 / Especial | Botón X |
| **Select** | **Botón Back** | **INSERT COIN (Moneda)** | Select |
| **Start** | **Botón Start** | **Player Start (Empezar)** | Start / Pausa |
| **L1 / R1** | **LB / RB (Bumpers)** | Gatillos superiores / Armas | L / R |
| **L2 / R2** | **LT / RT (Gatillos)** | Gatillos analógicos | ZL / ZR |
| **L3 / R3** | **Pulsar Palancas** | **Menú Rápido (Combo)** | L3 / R3 |
| **Cruceta / Stick L**| **D-Pad / Analógico** | Movimiento de 8 direcciones | Direcciones |

> [!NOTE]  
> En la interfaz aparece una doble asignación (ej: `A (Auto), Tecla z`). La columna de teclado (`Tecla z`, `Tecla rshift`) es un valor residual de PC y queda **completamente inactiva** en Android TV. No requiere ningún teclado conectado.

---

## ⚡ 2. Teclas Rápidas y Atajos del Menú (Hotkeys)

### 🚨 Regla Crítica de Arcade: Inserción de Monedas Limpia
- **Variable:** `input_enable_hotkey_btn = "nul"`
- **En la Interfaz:** `Ajustes > Entrada > Teclas rápidas > Tecla para activar teclas rápidas = ---`
- **Por qué:** Si se asigna cualquier botón aquí (especialmente `Select`), RetroArch secuestra ese botón para esperar un segundo botón, bloqueando la inserción de monedas en recreativas. Al dejarlo en `---`, pulsar `SELECT` / `BACK` es 100% Moneda directa.

### 🔘 Combinación para Abrir el Menú Rápido (`input_menu_toggle_gamepad_combo`)
Ubicación: `Ajustes > Entrada > Teclas rápidas` (o `Controles del menú`).

Valores oficiales del enum en RetroArch:
- `0`: Ninguna (Desactivado)
- `1`: Abajo + Y + L1 + R1
- `2`: **L3 + R3 (Recomendada: pulsar ambos joysticks hacia adentro)**
- `3`: L1 + R1 + Start + Select
- `4`: Start + Select *(¡PROHIBIDO en arcade! Causa Coin Error / Sound Error)*
- `5`: L3 + R1
- `6`: L1 + R1
- `7`: **Mantener Start durante 2 segundos**
- `8`: Mantener Select durante 2 segundos
- `9`: Abajo + Select
- `10`: L2 + R2

---

## 👥 3. Configuración Multijugador (2 Jugadores)

1. **Número de Usuarios:**
   - `Ajustes > Entrada > Número máximo de usuarios = 2`
2. **Control de Menú Universal:**
   - `Ajustes > Entrada > Controles del menú > Todos los usuarios pueden controlar el menú = Sí`
   - Permite que tanto el Jugador 1 (Khensu) como el Jugador 2 (EasySMX) puedan pausar, navegar y seleccionar juegos.
3. **Asignación de Puertos:**
   - `Puerto 1`: Índice de dispositivo -> Primer mando USB (`ControllerNumber: 4` o `ControllerNumber: 3`).
   - `Puerto 2`: Índice de dispositivo -> Segundo mando USB.

---

## 📂 4. Rutas Críticas y Estructura en Memoria Interna

- **Configuración Maestra:** `/sdcard/RetroArch/retroarch.cfg`
- **Listas de Reproducción (.lpl):** `/sdcard/RetroArch/playlists/`
- **Miniaturas y Carátulas:** `/sdcard/RetroArch/thumbnails/<Nombre_Playlist>/Named_Boxarts/<Nombre_Juego>.png`
- **BIOS de Sistemas:** `/sdcard/RetroArch/system/`
- **ROMs:** `/sdcard/ROMs/<sistema>/`
- **Modo Carátulas en Playlists:** `"right_thumbnail_mode": 1`

---

## 💾 5. Flujo Obligatorio para Guardar Cambios

RetroArch **NO recarga configuraciones en caliente** y sobreescribe archivos al salir si no se guardan manualmente:
1. Siempre guardar desde la interfaz: `Menú principal > Archivo de configuración > Guardar configuración actual`.
2. Si se inyectan cambios por ADB, cerrar la app con `am force-stop com.retroarch` **antes** de modificar el archivo en disco.
