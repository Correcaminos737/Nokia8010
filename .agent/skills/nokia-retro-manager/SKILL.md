---
name: nokia-retro-manager
description: >-
  Manage the Nokia Streaming Box 8010 Android TV retro-gaming environment.
  Use when diagnosing, installing, configuring RetroArch, mapping controllers,
  or synchronizing arcade and console ROMs via ADB.
---

# Nokia Retro Manager Skill

Comprehensive runbook for managing the Nokia Streaming Box 8010 (Android 14 TV) connected via ADB over Wi-Fi (`192.168.1.128:5555`).

## Architecture & Tools
* **Master Automation Tool:** `s:\Proyectos\Nokia8010\tools\nokia_helper.py`
  * Automatically verifies ADB connection.
  * Dynamically queries input device numbers to avoid hardcoded controller ports.
  * Manages RetroArch configuration and deployments in single, token-efficient executions.

## Key Directories on Nokia 8010
* **Internal ROMs Root:** `/sdcard/ROMs/`
  * `arcade/`: FBNeo & MAME arcade games.
  * `snes/`, `nes/`, `megadrive/`, `gba/`, `gb/`, `gbc/`, `neogeo/`, `pce/`, `atari/`
* **RetroArch System / BIOS:** `/sdcard/RetroArch/system/`
* **RetroArch Configurations:**
  * Master configuration: `/sdcard/RetroArch/retroarch.cfg`
  * Autoconfig profiles: `/sdcard/RetroArch/autoconfig/android/`
  * Core overrides: `/sdcard/RetroArch/config/<Core Name>/<Core Name>.cfg`

## Rules & Safety Constraints
1. **Never trigger Arcade Coin Error:** Do not map `Start + Select` as menu toggle; use `input_menu_toggle_gamepad_combo = "5"` (Hold Start 2 seconds) or L3+R3.
2. **Prevent Virtual Device Override:** Always assign active gamepad `joypad_index` to Player 1 and Player 2 so Android TV remote / virtual devices do not steal Port 1.
3. **No Uncompressed ROMs:** Keep arcade ROMs intact as `.zip`.
