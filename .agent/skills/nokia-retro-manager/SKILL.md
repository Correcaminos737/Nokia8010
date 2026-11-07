---
name: nokia-retro-manager
description: >-
  Manage the Nokia Streaming Box 8010 Android TV retro-gaming environment.
  Use when diagnosing, installing, configuring RetroArch, mapping controllers,
  verifying game duplicates, or synchronizing arcade and console ROMs via ADB.
---

# Nokia Retro Manager Skill

Comprehensive runbook for managing the Nokia Streaming Box 8010 (Android 14 TV) connected via ADB over Wi-Fi (`192.168.1.128:5555`).

## Architecture & Tools
* **Master Automation Tool:** `s:\Proyectos\Nokia8010\tools\nokia_helper.py`
  * Single entry-point CLI providing token-efficient, compact JSON outputs.
  * Verified subcommands:
    * `python tools/nokia_helper.py status`: Returns instant JSON with connection state and P1/P2 controller indices. **Always prefer this over raw `dumpsys input`**.
    * `python tools/nokia_helper.py pads`: Binds active physical controllers to Player 1 & 2 with safe menu toggle (Hold START 2s).
    * `python tools/nokia_helper.py remap`: Deploys LB (Left Bumper) -> Coin remap for all arcade cores.
    * `python tools/nokia_helper.py playlists`: Generates clean RetroArch playlists with thumbnail boxart mode enabled.
    * `python tools/nokia_helper.py sync`: Deduplicates and pushes ROMs from `JUEGOS/tiny-best-set-go-games.zip`.
    * `python tools/nokia_helper.py check-roms <path>`: Anti-duplication engine comparing new ROMs/zips against `configs/catalog_games.json`.
    * `python tools/nokia_helper.py all`: Executes complete configuration pipeline in a single step.

## Master Games Catalog
* **Database Location:** `s:\Proyectos\Nokia8010\configs\catalog_games.json`
* **Coverage:** 1,904 curated titles across 12 systems (Tiny Best Set: GO base set).
* **Properties per Game:** `title`, `filename`, `crc32`, `size_bytes`, `system_name`, `target_folder`, `recommended_core`.

## Key Directories on Nokia 8010
* **Internal ROMs Root:** `/sdcard/ROMs/`
  * `arcade/`: FBNeo arcade games.
  * `snes/`, `nes/`, `megadrive/`, `gba/`, `gb/`, `gbc/`, `neogeo/`, `pce/`, `atari/`, `mastersys/`, `gamegear/`
* **RetroArch System / BIOS:** `/sdcard/RetroArch/system/`
* **RetroArch Configurations:**
  * Master configuration: `/sdcard/RetroArch/retroarch.cfg`
  * Remaps: `/sdcard/RetroArch/config/remaps/<Core Name>/<Core Name>.rmp`
  * Playlists: `/sdcard/RetroArch/playlists/`
  * Thumbnails: `/sdcard/RetroArch/thumbnails/<System Name>/Named_Boxarts/`

## Rules & Safety Constraints
1. **Never trigger Arcade Coin Error:** Do not map `Start + Select` as menu toggle; use `input_menu_toggle_gamepad_combo = "5"` (Hold Start 2 seconds) or L3+R3.
2. **Prevent Virtual Device Override:** Always assign active gamepad `joypad_index` to Player 1 and Player 2 so Android TV remote / virtual devices do not steal Port 1.
3. **No Uncompressed ROMs:** Keep arcade ROMs intact as `.zip`.
4. **Token Optimization Rule:** Never dump raw ADB system traces into conversation context. Use the helper CLI methods.
