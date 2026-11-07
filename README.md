# Nokia 8010 Android TV Retro Manager & Hub

Modern retro-gaming hub and management suite for the **Nokia Streaming Box 8010** (SEI Robotics SEI800 / Android 14 TV, API 34).

## 🚀 Overview
This repository contains the complete automation toolset, configurations, and anti-duplication engine designed specifically for Android TV gaming setups:
* **RetroArch Integration:** Zero-conflict controller mappings and automated playlist generator.
* **Dual Gamepad Engine:** Automated input-port binding solving Android TV Remote conflicts (RC212) and enabling simultaneous 2-Player gaming.
* **Arcade Protection Filter:** Prevents Toaplan/Capcom arcade PCB lockouts (*Coin Error / Sound Error*) through safe hotkey design and LB -> Coin remap.
* **Anti-Duplication Database (`configs/catalog_games.json`):** Curated catalog of 1,904 titles across 12 systems to audit incoming games before adding them.

---

## 📁 Repository Structure
```
Nokia8010/
├── .agent/
│   └── skills/nokia-retro-manager/     # AI Agent skill for Antigravity / LLM
├── configs/
│   ├── catalog_games.json              # Master database of 1,904 games (anti-duplication)
│   └── retroarch/                      # Clean, versioned RetroArch master configs and remaps
├── docs/
│   └── retroarch_v1.19.1_manual_referencia.md
├── tools/
│   ├── arcade_coin_lb.rmp              # Arcade Remap (Left Bumper -> Coin)
│   └── nokia_helper.py                 # Unified CLI toolkit (ADB automation)
├── JUEGOS/                             # Directory for ROM zip packages (ignored in Git)
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🛠️ CLI Toolkit (`tools/nokia_helper.py`)
All routine maintenance and deployment tasks are automated through a single, token-efficient Python CLI:

```bash
# 1. Check connection and gamepads (concise JSON output):
python tools/nokia_helper.py status

# 2. Configure Player 1 and Player 2 USB gamepads with safe hotkeys:
python tools/nokia_helper.py pads

# 3. Deploy arcade remap (LB = Insert Coin):
python tools/nokia_helper.py remap

# 4. Generate and push clean RetroArch playlists (.lpl):
python tools/nokia_helper.py playlists

# 5. Check any new ROMs or folder against the catalog to avoid duplicates:
python tools/nokia_helper.py check-roms "ruta/al/nuevo_paquete.zip"

# 6. Synchronize and deduplicate 1,900+ ROMs directly to Nokia 8010 internal storage:
python tools/nokia_helper.py sync

# 7. Complete setup in one command (pads + remap + playlists):
python tools/nokia_helper.py all
```

---

## 👥 Guía Rápida para Amigos (Instalación Plug & Play)

> [!TIP]
> Si vas a realizar la instalación utilizando **Google Antigravity**, consulta la guía completa:
> 👉 [docs/guia_antigravity_amigos.md](file:///s:/Proyectos/Nokia8010/docs/guia_antigravity_amigos.md). ¡Simplemente dile a tu asistente en el chat *"Ayúdame a configurar mi Nokia Box"* y él se encargará de todo!

1. **Clonar este repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd Nokia8010
   ```
2. **Descargar el pack de ROMs (SwissTransfer):**
   * Descarga el archivo `tiny-best-set-go-games.zip` (5,3 GB) proporcionado por enlace directo.
   * Colócalo dentro de la carpeta `JUEGOS/`.
3. **Conectar la Nokia Box por Wi-Fi:**
   * En la Nokia Box: activa *Opciones de Desarrollador* y *Depuración por red / ADB*.
4. **Ejecutar el instalador:**
   ```bash
   python tools/nokia_helper.py sync
   python tools/nokia_helper.py all
   ```
   ¡Listo! Los juegos y controles quedarán 100% configurados sin tocar menús complejos.

---

## 🎮 Controller Layout (Universal RetroPad)
* **Action 1 (Shoot):** Button `A`
* **Action 2 (Jump):** Button `B`
* **Action 3 / Secondary:** Button `X`
* **Action 4:** Button `Y`
* **Insert Coin:** Button `LB` o `BACK` (single tap)
* **Game Start:** Button `START`
* **Menu Toggle / Exit to Menu:** Hold `START` for 2 seconds (safe from coin error)
* **D-Pad & Analog Thumbstick:** Fully enabled for all classic 8-bit, 16-bit, and Arcade systems.

---

## 📄 License
MIT License.
