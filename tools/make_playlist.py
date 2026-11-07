import subprocess
import os
import json

ADB = os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe")
DEV = "192.168.1.128:5555"

# Clean names mapping
NAMES = {
    "1941.zip": "1941: Counter Attack",
    "1942.zip": "1942",
    "1943.zip": "1943: The Battle of Midway",
    "19xx.zip": "19XX: The War Against Destiny",
    "3wonders.zip": "Three Wonders (Wonder 3)",
    "altbeast.zip": "Altered Beast",
    "area88.zip": "Area 88 (U.N. Squadron)",
    "bublbobl.zip": "Bubble Bobble",
    "captcomm.zip": "Captain Commando",
    "cawing.zip": "Carrier Air Wing",
    "dino.zip": "Cadillacs and Dinosaurs",
    "ffight.zip": "Final Fight",
    "forgottn.zip": "Forgotten Worlds",
    "galaga.zip": "Galaga",
    "ghouls.zip": "Ghouls'n Ghosts",
    "gng.zip": "Ghosts'n Goblins",
    "goldnaxe.zip": "Golden Axe",
    "knights.zip": "Knights of the Round",
    "kod.zip": "The King of Dragons",
    "kof98.zip": "The King of Fighters '98",
    "mbomber.zip": "Mega Man: The Power Battle",
    "megaman.zip": "Mega Man 2: The Power Fighters",
    "mercs.zip": "Mercs",
    "mslug.zip": "Metal Slug: Super Vehicle-001",
    "mslug3.zip": "Metal Slug 3",
    "mslugx.zip": "Metal Slug X",
    "msword.zip": "Magic Sword",
    "nemo.zip": "Nemo",
    "pang.zip": "Pang / Buster Bros",
    "pang3.zip": "Pang! 3",
    "punish.zip": "The Punisher",
    "punisher.zip": "The Punisher (World)",
    "sf2.zip": "Street Fighter II: The World Warrior",
    "sf2ce.zip": "Street Fighter II': Champion Edition",
    "sf2t.zip": "Street Fighter II' Turbo: Hyper Fighting",
    "sfzch.zip": "Street Fighter Alpha (CPS Changer)",
    "simpsons.zip": "The Simpsons (4 Players)",
    "slammast.zip": "Saturday Night Slam Masters",
    "snowbros.zip": "Snow Bros. - Nick & Tom",
    "spang.zip": "Super Pang",
    "ssriders.zip": "Sunset Riders (4 Players)",
    "strider.zip": "Strider",
    "tetris.zip": "Tetris (Sega)",
    "tmnt.zip": "Teenage Mutant Ninja Turtles (4 Players)",
    "tmnt2.zip": "TMNT: Turtles in Time (4 Players)",
    "unsquad.zip": "U.N. Squadron",
    "varth.zip": "Varth: Operation Operation",
    "willow.zip": "Willow",
    "wof.zip": "Warriors of Fate",
    "wonder3.zip": "Wonder 3"
}

subprocess.run([ADB, "connect", DEV])
out = subprocess.run([ADB, "-s", DEV, "shell", "ls", "/sdcard/ROMs/arcade"], capture_output=True, text=True).stdout
files = [f.strip() for f in out.splitlines() if f.strip().endswith('.zip')]

items = []
for f in sorted(files):
    if f == "neogeo.zip" or f == "qsound.zip":
        continue # bios files
    label = NAMES.get(f, f.replace(".zip", "").upper())
    items.append({
        "path": f"/sdcard/ROMs/arcade/{f}",
        "label": label,
        "core_path": "/data/user/0/com.retroarch/cores/fbneo_libretro_android.so",
        "core_name": "Arcade (FinalBurn Neo)",
        "crc32": "DETECT",
        "db_name": "FBNeo - Arcade Games.lpl"
    })

playlist = {
    "version": "1.5",
    "default_core_path": "/data/user/0/com.retroarch/cores/fbneo_libretro_android.so",
    "default_core_name": "Arcade (FinalBurn Neo)",
    "label_display_mode": 0,
    "right_thumbnail_mode": 0,
    "left_thumbnail_mode": 0,
    "thumbnail_match_mode": 0,
    "sort_mode": 0,
    "items": items
}

local_pl = "FBNeo - Arcade Games.lpl"
with open(local_pl, "w", encoding="utf-8") as fp:
    json.dump(playlist, fp, indent=2, ensure_ascii=False)

print(f"Playlist generada con {len(items)} juegos.")
subprocess.run([ADB, "-s", DEV, "push", local_pl, "/sdcard/RetroArch/playlists/FBNeo - Arcade Games.lpl"])
subprocess.run([ADB, "-s", DEV, "push", local_pl, "/sdcard/RetroArch/playlists/Arcade.lpl"])
print("Playlist enviada a RetroArch en el Nokia!")
