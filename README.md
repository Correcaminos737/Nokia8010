# Nokia 8010 Android TV Retro Manager & Hub

Modern retro-gaming hub and management suite for the **Nokia Streaming Box 8010** (SEI Robotics SEI800 / Android 14 TV, API 34).

## 🚀 Overview
This repository contains the full hybrid application (Vite / Capacitor / Android Native Java) and ADB automation toolset designed specifically for Android TV gaming setups:
* **TV Frontend App (`com.nokia8010.manager`):** Leanback-optimized interface for browsing and launching emulators and media apps.
* **RetroArch Integration:** Native Intent bridge launching games with explicit `CONFIGFILE`, `ROM`, and `LIBRETRO` parameters.
* **Dual Gamepad Engine:** Automated input-port binding solving Android TV Remote conflicts (RC212) and enabling simultaneous 2-Player gaming.
* **Arcade Protection Filter:** Prevents Toaplan/Capcom arcade PCB lockouts (*Coin Error / Sound Error*) through safe hotkey design.

---

## 📁 Repository Structure
```
├── .agent/                  # Antigravity agent skills and runbooks
│   └── skills/nokia-retro-manager/
├── android/                 # Native Android Studio Project (Gradle / Java)
│   └── app/src/main/java/com/nokia8010/manager/
│       └── Tv8010BridgePlugin.java
├── configs/                 # Clean, versioned RetroArch configurations
│   └── retroarch/
│       └── retroarch_master.cfg
├── src/                     # Web / JS Frontend for Android TV
├── tools/                   # Automation and maintenance tools
│   └── nokia_helper.py
├── capacitor.config.json    # Capacitor configuration
├── package.json             # NPM dependencies
└── vite.config.js           # Vite bundler configuration
```

---

## 🛠️ CLI Toolkit (`tools/nokia_helper.py`)
All routine maintenance and deployment tasks are automated through a lightweight Python CLI:
```bash
# Calibrate and map 2 gamepads (Player 1 & Player 2):
python tools/nokia_helper.py pads

# Sync, categorize, and deduplicate 1,900+ ROMs directly to internal storage:
python tools/nokia_helper.py sync

# Clean repository of temporary logs and dumps:
python tools/nokia_helper.py clean
```

---

## 🎮 Controller Layout (Universal RetroPad)
* **Action 1 (Shoot):** Button `A`
* **Action 2 (Jump):** Button `B`
* **Action 3 / Secondary:** Button `X`
* **Action 4:** Button `Y`
* **Insert Coin:** Button `BACK` (single tap)
* **Game Start:** Button `START`
* **Menu Toggle / Exit to Menu:** Hold `START` for 2 seconds (safe from coin error)
* **D-Pad & Analog Thumbstick:** Fully enabled for all classic 8-bit, 16-bit, and Arcade systems.

---

## 📄 License
MIT License.
