import subprocess
import re
import os
import sys
import zipfile
import shutil

ADB_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe")
DEVICE_IP = "192.168.1.128:5555"

def ensure_connected():
    res = subprocess.run([ADB_PATH, "devices"], capture_output=True, text=True)
    if "192.168.1.128:5555\tdevice" not in res.stdout:
        subprocess.run([ADB_PATH, "connect", DEVICE_IP], capture_output=True, text=True)

def run_adb(cmd, capture=True):
    ensure_connected()
    if isinstance(cmd, list):
        full_cmd = [ADB_PATH, "-s", DEVICE_IP] + cmd
        res = subprocess.run(full_cmd, capture_output=capture, text=True, encoding='utf-8', errors='ignore')
    else:
        full_cmd = f'"{ADB_PATH}" -s {DEVICE_IP} {cmd}'
        res = subprocess.run(full_cmd, capture_output=capture, text=True, shell=True, encoding='utf-8', errors='ignore')
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

def setup_dual_pads():
    p1_idx, p2_idx = get_gamepad_indices()[:2]
    print(f"[OK] Mapping gamepads -> Player 1 (Index #{p1_idx}), Player 2 (Index #{p2_idx})")

    master_cfg = f"""# Master RetroArch Config for Nokia 8010 Dual Gamepads
input_driver = "android"
all_users_control_menu = "true"
input_menu_toggle_gamepad_combo = "5"
input_enable_hotkey_btn = "nul"
input_menu_toggle_btn = "nul"

# Player 1
input_player1_joypad_index = "{p1_idx}"
input_player1_analog_dpad_mode = "1"
input_player1_b_btn = "0"
input_player1_a_btn = "1"
input_player1_y_btn = "2"
input_player1_x_btn = "3"
input_player1_l_btn = "4"
input_player1_r_btn = "5"
input_player1_select_btn = "6"
input_player1_start_btn = "7"
input_player1_l3_btn = "9"
input_player1_r3_btn = "10"
input_player1_up_btn = "h0up"
input_player1_down_btn = "h0down"
input_player1_left_btn = "h0left"
input_player1_right_btn = "h0right"
input_player1_l_x_plus_axis = "+0"
input_player1_l_x_minus_axis = "-0"
input_player1_l_y_plus_axis = "+1"
input_player1_l_y_minus_axis = "-1"

# Player 2
input_player2_joypad_index = "{p2_idx}"
input_player2_analog_dpad_mode = "1"
input_player2_b_btn = "0"
input_player2_a_btn = "1"
input_player2_y_btn = "2"
input_player2_x_btn = "3"
input_player2_l_btn = "4"
input_player2_r_btn = "5"
input_player2_select_btn = "6"
input_player2_start_btn = "7"
input_player2_l3_btn = "9"
input_player2_r3_btn = "10"
input_player2_up_btn = "h0up"
input_player2_down_btn = "h0down"
input_player2_left_btn = "h0left"
input_player2_right_btn = "h0right"
input_player2_l_x_plus_axis = "+0"
input_player2_l_x_minus_axis = "-0"
input_player2_l_y_plus_axis = "+1"
input_player2_l_y_minus_axis = "-1"

fbneo-diagnostic-input = "None"
"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    configs_dir = os.path.join(base_dir, "configs", "retroarch")
    os.makedirs(configs_dir, exist_ok=True)
    master_path = os.path.join(configs_dir, "retroarch_master.cfg")
    with open(master_path, "w", encoding="utf-8") as f:
        f.write(master_cfg)

    # Push to device
    run_adb(["push", master_path, "/sdcard/RetroArch/retroarch.cfg"])
    for core in ["FinalBurn Neo", "FB Alpha 2012", "Snes9x", "Genesis Plus GX Wide"]:
        run_adb(["shell", f"mkdir -p '/sdcard/RetroArch/config/{core}'"])
        run_adb(["push", master_path, f"/sdcard/RetroArch/config/{core}/{core}.cfg"])
    print("[OK] Universal 2-Player configuration deployed to RetroArch.")

def get_existing_device_roms():
    out = run_adb(["shell", "find", "/sdcard/ROMs/", "-type", "f"])
    existing = set()
    for line in out.splitlines():
        line = line.strip()
        if line:
            parts = line.split("/")
            if len(parts) >= 2:
                # Store (subfolder, filename) in lowercase
                existing.add((parts[-2].lower(), parts[-1].lower()))
    return existing

def sync_all_roms_and_bios():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    zip_path = os.path.join(base_dir, "JUEGOS", "tiny-best-set-go-games.zip")
    if not os.path.exists(zip_path):
        print(f"[ERROR] Zip file not found at {zip_path}")
        return

    extract_temp = os.path.join(base_dir, "temp_extracted")
    os.makedirs(extract_temp, exist_ok=True)

    print("[1/3] Reading existing ROMs on Nokia 8010 to avoid duplicates...")
    existing_roms = get_existing_device_roms()
    print(f"      Found {len(existing_roms)} existing items on device.")

    folder_map = {
        "arcade": "arcade",
        "sfc": "snes",
        "fc": "nes",
        "md": "megadrive",
        "gba": "gba",
        "gb": "gb",
        "gbc": "gbc",
        "neogeo": "neogeo",
        "pce": "pce",
        "atari": "atari",
        "ms": "mastersys",
        "gg": "gamegear",
        "bios": "bios"
    }

    print("[2/3] Extracting and preparing ROMs by console...")
    to_push_by_folder = {}
    with zipfile.ZipFile(zip_path, "r") as z:
        for entry in z.namelist():
            if entry.endswith("/"):
                continue
            parts = entry.split("/")
            if len(parts) >= 3 and parts[0].lower() == "roms":
                sys_key = parts[1].lower()
                target_folder = folder_map.get(sys_key, sys_key)
                fname = parts[-1]
                
                # Deduplication check:
                if (target_folder, fname.lower()) in existing_roms:
                    continue
                
                if target_folder not in to_push_by_folder:
                    to_push_by_folder[target_folder] = []
                to_push_by_folder[target_folder].append((entry, fname))

    total_new = sum(len(items) for items in to_push_by_folder.values())
    print(f"      Total new items to transfer: {total_new} (skipping already existing duplicates).")

    print("[3/3] Transferring organized ROMs to Nokia 8010 internal storage...")
    for target_folder, files in sorted(to_push_by_folder.items()):
        if not files:
            continue
        
        local_staging = os.path.join(extract_temp, target_folder)
        os.makedirs(local_staging, exist_ok=True)
        
        # Extract batch locally
        with zipfile.ZipFile(zip_path, "r") as z:
            for zip_entry, fname in files:
                dest = os.path.join(local_staging, fname)
                with z.open(zip_entry) as src, open(dest, "wb") as dst:
                    shutil.copyfileobj(src, dst)
        
        # Push batch to device via ADB
        if target_folder == "bios":
            remote_path = "/sdcard/RetroArch/system/"
        else:
            remote_path = f"/sdcard/ROMs/{target_folder}/"
            run_adb(["shell", f"mkdir -p '{remote_path}'"])
        
        print(f"      Pushing {len(files)} files to {remote_path}...")
        run_adb(["push", local_staging + "/.", remote_path])
        
        # Clean local staging to conserve PC disk
        shutil.rmtree(local_staging)

    # Cleanup temp
    shutil.rmtree(extract_temp, ignore_errors=True)
    print("[OK] Complete ROM set and BIOS deployed organized and deduplicated!")

def clean_project_for_git():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    print(f"[OK] Cleaning project at {base_dir} for Git...")
    
    # 1. Configs folder
    configs_dir = os.path.join(base_dir, "configs", "retroarch")
    os.makedirs(configs_dir, exist_ok=True)
    
    # Move loose configs
    for f in os.listdir(base_dir):
        if f.endswith((".cfg", ".rmp")) and os.path.isfile(os.path.join(base_dir, f)):
            src = os.path.join(base_dir, f)
            dst = os.path.join(configs_dir, f)
            shutil.move(src, dst)
            
    # Remove obsolete test/debug files
    obsolete_files = [
        "CALLUS95.ZIP", "goldnaxe.zip", "test_dino.zip", "test_mslug.zip", "test_snowbros.zip",
        "dumpsys_input.txt", "window_dump.xml", "current_screen.png", "menu_screen.png",
        "quick_menu.png", "f1_screen.png", "menu_btn.png", "menu_check.png", "snowbros_test.png",
        "snowbros_loaded.png", "snowbros_fixed.png", "snowbros_running.png", "user_screen.png",
        "nav1.png", "nav2.png", "ready.png", "coin_err.png", "fresh_boot.png", "fresh_boot2.png"
    ]
    for obs in obsolete_files:
        p = os.path.join(base_dir, obs)
        if os.path.exists(p):
            os.remove(p)

    # Remove temporary directories
    for d in ["arcade_pack", "callus_extracted", "hf_arcade", "roms_arcade", "temp_extracted"]:
        dp = os.path.join(base_dir, d)
        if os.path.exists(dp):
            shutil.rmtree(dp, ignore_errors=True)

    print("[OK] Project cleaned and structured.")

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "pads"
    if action == "pads":
        setup_dual_pads()
    elif action == "sync":
        sync_all_roms_and_bios()
    elif action == "clean":
        clean_project_for_git()
    elif action == "all":
        clean_project_for_git()
        setup_dual_pads()
        sync_all_roms_and_bios()
