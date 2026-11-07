import os
import sys
import json

sys.path.append(r"s:\Proyectos\Nokia8010\tools")
import nokia_helper

SYSTEMS = [
    ("arcade", "FBNeo - Arcade Games.lpl", "FBNeo - Arcade Games"),
    ("snes", "Nintendo - Super Nintendo Entertainment System.lpl", "Nintendo - Super Nintendo Entertainment System"),
    ("nes", "Nintendo - Nintendo Entertainment System.lpl", "Nintendo - Nintendo Entertainment System"),
    ("megadrive", "Sega - Mega Drive - Genesis.lpl", "Sega - Mega Drive - Genesis"),
    ("gba", "Nintendo - Game Boy Advance.lpl", "Nintendo - Game Boy Advance"),
    ("gb", "Nintendo - Game Boy.lpl", "Nintendo - Game Boy"),
    ("gbc", "Nintendo - Game Boy Color.lpl", "Nintendo - Game Boy Color"),
    ("neogeo", "SNK - Neo Geo.lpl", "SNK - Neo Geo"),
    ("pce", "NEC - PC Engine - TurboGrafx 16.lpl", "NEC - PC Engine - TurboGrafx 16"),
    ("atari", "Atari - 2600.lpl", "Atari - 2600"),
    ("mastersys", "Sega - Master System - Mark III.lpl", "Sega - Master System - Mark III"),
    ("gamegear", "Sega - Game Gear.lpl", "Sega - Game Gear")
]

def make_all_playlists():
    nokia_helper.ensure_connected()
    base_dir = r"s:\Proyectos\Nokia8010\temp_playlists"
    os.makedirs(base_dir, exist_ok=True)
    
    nokia_helper.run_adb(["shell", "mkdir", "-p", "/sdcard/RetroArch/playlists/"])
    
    total_items = 0
    for subfolder, lpl_name, db_name in SYSTEMS:
        raw_files = nokia_helper.run_adb(f"shell ls /sdcard/ROMs/{subfolder}").splitlines()
        files = [f.strip() for f in raw_files if f.strip().endswith((".zip", ".7z", ".nes", ".sfc", ".md", ".bin"))]
        
        items = []
        for f in sorted(files):
            # Clean display label (remove extension)
            display_name = os.path.splitext(f)[0]
            items.append({
                "path": f"/sdcard/ROMs/{subfolder}/{f}",
                "label": display_name,
                "core_path": "DETECT",
                "core_name": "DETECT",
                "crc32": "DETECT",
                "db_name": lpl_name
            })
            
        playlist = {
            "version": "1.5",
            "default_core_path": "",
            "default_core_name": "",
            "label_display_mode": 0,
            "right_thumbnail_mode": 0,
            "left_thumbnail_mode": 0,
            "sort_mode": 0,
            "items": items
        }
        
        local_lpl = os.path.join(base_dir, lpl_name)
        with open(local_lpl, "w", encoding="utf-8") as out:
            json.dump(playlist, out, indent=2, ensure_ascii=False)
            
        nokia_helper.run_adb(["push", local_lpl, f"/sdcard/RetroArch/playlists/{lpl_name}"])
        print(f"[OK] Generated {lpl_name:<45}: {len(items):>4} items")
        total_items += len(items)
        
    print(f"\n[OK] All playlists pushed! Total across all systems: {total_items} games.")

if __name__ == "__main__":
    make_all_playlists()
