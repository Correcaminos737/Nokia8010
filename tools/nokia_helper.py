"""Nokia 8010 Android TV Retro Manager & Automation Suite
Single entry-point CLI for controller configuration, playlist generation,
anti-duplicate ROM checking, and RetroArch maintenance over ADB.
"""

import os
import sys
import re
import json
import zipfile
import shutil
import subprocess

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def get_adb_path():
    which_adb = shutil.which("adb")
    if which_adb and os.path.exists(which_adb):
        return which_adb
    sdk_adb = os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe")
    if os.path.exists(sdk_adb):
        return sdk_adb
    for p in [r"C:\platform-tools\adb.exe", r"C:\Android\platform-tools\adb.exe"]:
        if os.path.exists(p):
            return p
    return "adb"

ADB_PATH = get_adb_path()
DEVICE_IP = os.environ.get("NOKIA_IP", "192.168.1.128:5555")

def set_device_ip(ip_str):
    global DEVICE_IP
    if not ip_str:
        return
    ip_str = ip_str.strip()
    if ":" not in ip_str:
        ip_str = f"{ip_str}:5555"
    DEVICE_IP = ip_str

SYSTEMS_META = [
    ("arcade", "FBNeo - Arcade Games.lpl", "FBNeo - Arcade Games", "fbneo", "Arcade (FinalBurn Neo)"),
    ("snes", "Nintendo - Super Nintendo Entertainment System.lpl", "Nintendo - Super Nintendo Entertainment System", "snes9x", "Nintendo - SNES / SFC (Snes9x)"),
    ("nes", "Nintendo - Nintendo Entertainment System.lpl", "Nintendo - Nintendo Entertainment System", "fceumm", "Nintendo - NES / Famicom (FCEUmm)"),
    ("megadrive", "Sega - Mega Drive - Genesis.lpl", "Sega - Mega Drive - Genesis", "genesis_plus_gx", "Sega - MS/MD/CD/32X (Genesis Plus GX)"),
    ("gba", "Nintendo - Game Boy Advance.lpl", "Nintendo - Game Boy Advance", "mgba", "Nintendo - Game Boy Advance (mGBA)"),
    ("gb", "Nintendo - Game Boy.lpl", "Nintendo - Game Boy", "gambatte", "Nintendo - Game Boy / Color (Gambatte)"),
    ("gbc", "Nintendo - Game Boy Color.lpl", "Nintendo - Game Boy Color", "gambatte", "Nintendo - Game Boy / Color (Gambatte)"),
    ("neogeo", "SNK - Neo Geo.lpl", "SNK - Neo Geo", "fbneo", "Arcade (FinalBurn Neo)"),
    ("pce", "NEC - PC Engine - TurboGrafx 16.lpl", "NEC - PC Engine - TurboGrafx 16", "mednafen_pce_fast", "NEC - PC Engine / CD (Beetle PCE FAST)"),
    ("atari", "Atari - 2600.lpl", "Atari - 2600", "stella", "Atari - 2600 (Stella)"),
    ("mastersys", "Sega - Master System - Mark III.lpl", "Sega - Master System - Mark III", "genesis_plus_gx", "Sega - MS/MD/CD/32X (Genesis Plus GX)"),
    ("gamegear", "Sega - Game Gear.lpl", "Sega - Game Gear", "genesis_plus_gx", "Sega - MS/MD/CD/32X (Genesis Plus GX)")
]

def ensure_connected():
    try:
        res = subprocess.run([ADB_PATH, "devices"], capture_output=True, text=True, timeout=5)
        if f"{DEVICE_IP}\tdevice" not in res.stdout:
            subprocess.run([ADB_PATH, "connect", DEVICE_IP], capture_output=True, text=True, timeout=5)
    except Exception as e:
        return False
    return True

def run_adb(cmd, capture=True):
    ensure_connected()
    if isinstance(cmd, list):
        full_cmd = [ADB_PATH, "-s", DEVICE_IP] + cmd
        res = subprocess.run(full_cmd, capture_output=capture, text=True, encoding="utf-8", errors="ignore")
    else:
        full_cmd = f'"{ADB_PATH}" -s {DEVICE_IP} {cmd}'
        res = subprocess.run(full_cmd, capture_output=capture, text=True, shell=True, encoding="utf-8", errors="ignore")
    return res.stdout.strip() if capture else ""

def get_gamepad_indices():
    ensure_connected()
    out = run_adb(["shell", "dumpsys", "input"])
    matches = re.findall(r'Device\s+\d+:\s+([^\n]+).*?ControllerNum:\s*(\d+)', out, re.DOTALL)
    gamepads = []
    for name, cnum in matches:
        if any(k in name.lower() for k in ("box", "pad", "easysmx", "controller", "joystick")):
            val = int(cnum)
            if val not in gamepads:
                gamepads.append(val)
    if not gamepads:
        gamepads = [3, 4]
    elif len(gamepads) == 1:
        gamepads.append(gamepads[0] + 1)
    return gamepads

def cmd_status():
    """Outputs compact JSON for token efficiency."""
    conn = ensure_connected()
    pads = get_gamepad_indices() if conn else []
    status = {
        "device": DEVICE_IP,
        "connected": conn,
        "gamepads": pads,
        "player1": pads[0] if len(pads) > 0 else None,
        "player2": pads[1] if len(pads) > 1 else None
    }
    print(json.dumps(status))

def setup_dual_pads():
    pads = get_gamepad_indices()
    p1 = str(pads[0])
    p2 = str(pads[1])
    
    master_cfg = f"""# Clean Master RetroArch Config for Nokia 8010
input_driver = "android"
input_joypad_driver = "android"
input_autodetect_enable = "true"
input_remap_binds_enable = "true"
all_users_control_menu = "true"

# Safe Hotkeys: Hold START 2 seconds to toggle menu (no coin conflict)
input_menu_toggle_gamepad_combo = "5"
input_enable_hotkey_btn = "nul"
input_menu_toggle_btn = "nul"

# Map to physical USB Gamepad devices
input_player1_joypad_index = "{p1}"
input_player2_joypad_index = "{p2}"

# Analog Stick to D-Pad mode (both work)
input_player1_analog_dpad_mode = "1"
input_player2_analog_dpad_mode = "1"

# Disable diagnostic freeze in FBNeo
fbneo-diagnostic-input = "None"
"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    configs_dir = os.path.join(base_dir, "configs", "retroarch")
    os.makedirs(configs_dir, exist_ok=True)
    master_path = os.path.join(configs_dir, "retroarch_master.cfg")
    with open(master_path, "w", encoding="utf-8") as f:
        f.write(master_cfg)

    run_adb(["push", master_path, "/sdcard/RetroArch/retroarch.cfg"])
    print(f"[OK] Master config deployed (P1: {p1}, P2: {p2}, Hold START=Menu).")

def deploy_remap():
    rmp_content = """input_remap_port_p1 = "0"
input_player1_btn_l = "2"
input_remap_port_p2 = "1"
input_player2_btn_l = "2"
"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    remap_path = os.path.join(base_dir, "configs", "retroarch", "arcade_coin_lb.rmp")
    os.makedirs(os.path.dirname(remap_path), exist_ok=True)
    with open(remap_path, "w", encoding="utf-8") as f:
        f.write(rmp_content)

    cores = [
        "FinalBurn Neo",
        "FinalBurn_Neo",
        "Arcade (FinalBurn Neo)",
        "FB Alpha 2012",
        "MAME 2003-Plus"
    ]
    ensure_connected()
    for c in cores:
        run_adb(["shell", f"mkdir -p '/sdcard/RetroArch/config/remaps/{c}'"])
        run_adb(["push", remap_path, f"/sdcard/RetroArch/config/remaps/{c}/{c}.rmp"])

    print("[OK] Arcade Remap deployed: LB (Left Bumper) -> Coin for 1P & 2P.")

def make_all_playlists():
    ensure_connected()
    base_dir = os.path.dirname(os.path.dirname(__file__))
    temp_dir = os.path.join(base_dir, "configs", "playlists")
    os.makedirs(temp_dir, exist_ok=True)
    
    arcade_titles = {}
    titles_path = os.path.join(base_dir, "configs", "arcade_titles.json")
    if os.path.exists(titles_path):
        try:
            with open(titles_path, "r", encoding="utf-8") as tf:
                arcade_titles = json.load(tf)
        except Exception:
            arcade_titles = {}

    run_adb(["shell", "mkdir", "-p", "/sdcard/RetroArch/playlists/"])
    
    total = 0
    for subfolder, lpl_name, db_name, core_id, core_full_name in SYSTEMS_META:
        raw_files = run_adb(f"shell ls /sdcard/ROMs/{subfolder}").splitlines()
        files = [f.strip() for f in raw_files if f.strip().endswith((".zip", ".7z", ".nes", ".sfc", ".md", ".bin", ".pce"))]
        
        items = []
        for f in sorted(files):
            stem = os.path.splitext(f)[0]
            if subfolder in ("arcade", "neogeo") and stem.lower() in arcade_titles:
                display_name = arcade_titles[stem.lower()]
            else:
                display_name = stem

            items.append({
                "path": f"/sdcard/ROMs/{subfolder}/{f}",
                "label": display_name,
                "core_path": "DETECT",
                "core_name": core_full_name,
                "crc32": "DETECT",
                "db_name": lpl_name
            })
            
        playlist = {
            "version": "1.5",
            "default_core_path": "DETECT",
            "default_core_name": core_full_name,
            "label_display_mode": 0,
            "right_thumbnail_mode": 1,
            "left_thumbnail_mode": 0,
            "sort_mode": 0,
            "items": items
        }
        
        local_lpl = os.path.join(temp_dir, lpl_name)
        with open(local_lpl, "w", encoding="utf-8") as out:
            json.dump(playlist, out, indent=2, ensure_ascii=False)
            
        run_adb(["push", local_lpl, f"/sdcard/RetroArch/playlists/{lpl_name}"])
        print(f"  + {lpl_name:<46}: {len(items):>4} items")
        total += len(items)
        
    print(f"[OK] All playlists synced: {total} total titles.")

def check_roms(incoming_path):
    """Anti-duplication engine comparing new files against catalog_games.json."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    catalog_path = os.path.join(base_dir, "configs", "catalog_games.json")
    if not os.path.exists(catalog_path):
        print(f"[ERROR] Catalog not found at {catalog_path}")
        return

    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    existing_titles = set()
    existing_files = set()
    existing_crcs = set()

    for sys_code, sys_data in catalog.get("systems", {}).items():
        for g in sys_data.get("games", []):
            existing_titles.add(g["title"].lower())
            existing_files.add(g["filename"].lower())
            if g.get("crc32"):
                existing_crcs.add(g["crc32"].upper())

    if not os.path.exists(incoming_path):
        print(f"[ERROR] Target path does not exist: {incoming_path}")
        return

    duplicates = []
    new_games = []

    # If it's a zip file
    if zipfile.is_zipfile(incoming_path):
        with zipfile.ZipFile(incoming_path, "r") as z:
            for info in z.infolist():
                if info.filename.endswith("/") or info.filename.lower().startswith("bios/"):
                    continue
                fname = os.path.basename(info.filename)
                title = os.path.splitext(fname)[0]
                crc = f"{info.CRC:08X}"
                
                is_dup = (fname.lower() in existing_files) or (title.lower() in existing_titles) or (crc in existing_crcs)
                if is_dup:
                    duplicates.append(fname)
                else:
                    new_games.append(fname)
    # If it's a folder
    elif os.path.isdir(incoming_path):
        for root, _, files in os.walk(incoming_path):
            for f in files:
                title = os.path.splitext(f)[0]
                if f.lower() in existing_files or title.lower() in existing_titles:
                    duplicates.append(f)
                else:
                    new_games.append(f)
    else:
        fname = os.path.basename(incoming_path)
        title = os.path.splitext(fname)[0]
        if fname.lower() in existing_files or title.lower() in existing_titles:
            duplicates.append(fname)
        else:
            new_games.append(fname)

    print("=" * 60)
    print(" 🔍 REPORTE DE CONTROL DE DUPLICADOS")
    print("=" * 60)
    print(f"  Total juegos analizados: {len(duplicates) + len(new_games)}")
    print(f"  ❌ Ya existentes (duplicados omitidos): {len(duplicates)}")
    print(f"  ✨ Nuevos juegos únicos para agregar : {len(new_games)}")
    if new_games:
        print("\n  Primeros juegos nuevos detectados:")
        for n in new_games[:10]:
            print(f"    + {n}")
        if len(new_games) > 10:
            print(f"    ... y {len(new_games) - 10} más.")
    print("=" * 60)

def sync_from_zip():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    zip_path = os.path.join(base_dir, "JUEGOS", "tiny-best-set-go-games.zip")
    if not os.path.exists(zip_path):
        print(f"[ERROR] Zip file not found at {zip_path}")
        return

    extract_temp = os.path.join(base_dir, "temp_extracted")
    os.makedirs(extract_temp, exist_ok=True)

    folder_map = {
        "arcade": "arcade", "sfc": "snes", "fc": "nes", "md": "megadrive",
        "gba": "gba", "gb": "gb", "gbc": "gbc", "neogeo": "neogeo",
        "pce": "pce", "atari": "atari", "ms": "mastersys", "gg": "gamegear", "bios": "bios"
    }

    # Query device files to avoid re-uploading
    out = run_adb(["shell", "find", "/sdcard/ROMs/", "-type", "f"])
    existing = set()
    for line in out.splitlines():
        line = line.strip()
        if line:
            parts = line.split("/")
            if len(parts) >= 2:
                existing.add((parts[-2].lower(), parts[-1].lower()))

    to_push = {}
    with zipfile.ZipFile(zip_path, "r") as z:
        for entry in z.namelist():
            if entry.endswith("/"):
                continue
            parts = entry.split("/")
            if len(parts) >= 3 and parts[0].lower() == "roms":
                sys_key = parts[1].lower()
                target_folder = folder_map.get(sys_key, sys_key)
                fname = parts[-1]
                if (target_folder, fname.lower()) in existing:
                    continue
                if target_folder not in to_push:
                    to_push[target_folder] = []
                to_push[target_folder].append((entry, fname))

    total_new = sum(len(items) for items in to_push.values())
    print(f"[OK] Deduplication check: {total_new} new items to sync.")

    for target_folder, files in sorted(to_push.items()):
        if not files:
            continue
        local_staging = os.path.join(extract_temp, target_folder)
        os.makedirs(local_staging, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as z:
            for zip_entry, fname in files:
                dest = os.path.join(local_staging, fname)
                with z.open(zip_entry) as src, open(dest, "wb") as dst:
                    shutil.copyfileobj(src, dst)
        
        remote_path = f"/sdcard/ROMs/{target_folder}/"
        run_adb(["shell", f"mkdir -p '{remote_path}'"])
        print(f"  Transferring {len(files)} files to {remote_path}...")
        run_adb(["push", local_staging + "/.", remote_path])
        shutil.rmtree(local_staging)

    shutil.rmtree(extract_temp, ignore_errors=True)
    print("[OK] ROM synchronization complete.")

def print_help():
    print("""Uso: python tools/nokia_helper.py [--ip <IP_NOKIA>] <comando>

Opciones globales:
  --ip <IP>            Especifica la IP de la Nokia Box (ej: 192.168.1.50).

Comandos disponibles:
  status               Muestra estado de conexión y mandos en JSON conciso.
  pads                 Configura mandos USB (P1 & P2) y menú seguro (Hold START 2s).
  remap                Despliega remap LB -> Coin para todos los núcleos Arcade.
  playlists            Genera y sube las listas de reproducción a RetroArch.
  sync                 Sincroniza y desduplica ROMs desde JUEGOS/ hacia la Nokia 8010.
  check-roms <ruta>    Compara una carpeta o zip contra el catálogo para evitar duplicados.
  all                  Ejecuta configuración completa (pads + remap + playlists).
""")

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--ip" in args:
        idx = args.index("--ip")
        if idx + 1 < len(args):
            set_device_ip(args[idx + 1])
            del args[idx:idx + 2]

    if not args:
        print_help()
        sys.exit(0)

    cmd = args[0].lower()
    if cmd == "status":
        cmd_status()
    elif cmd == "pads":
        setup_dual_pads()
    elif cmd == "remap":
        deploy_remap()
    elif cmd == "playlists":
        make_all_playlists()
    elif cmd == "sync":
        sync_from_zip()
    elif cmd == "check-roms":
        if len(args) > 1:
            check_roms(args[1])
        else:
            print("[ERROR] Debes especificar la ruta de la ROM o carpeta: python tools/nokia_helper.py check-roms <ruta>")
    elif cmd == "all":
        setup_dual_pads()
        deploy_remap()
        make_all_playlists()
    else:
        print(f"[ERROR] Comando desconocido: {cmd}")
        print_help()
