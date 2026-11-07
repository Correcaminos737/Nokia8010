import os
import sys

sys.path.append(os.path.dirname(__file__))
import nokia_helper as nh

rmp_content = """input_remap_port_p1 = "0"
input_player1_btn_l = "2"
input_remap_port_p2 = "1"
input_player2_btn_l = "2"
"""

local_path = os.path.join(os.path.dirname(__file__), "arcade_coin_lb.rmp")
with open(local_path, "w", encoding="utf-8") as f:
    f.write(rmp_content)

cores = [
    "FinalBurn Neo",
    "FinalBurn_Neo",
    "FB Alpha 2012",
    "MAME 2003-Plus",
    "Arcade (FinalBurn Neo)"
]

nh.ensure_connected()
for c in cores:
    nh.run_adb(["shell", f"mkdir -p '/sdcard/RetroArch/config/remaps/{c}'"])
    nh.run_adb(["push", local_path, f"/sdcard/RetroArch/config/remaps/{c}/{c}.rmp"])

print("[OK] Remap file deployed for all arcade cores: LB (Left Bumper) -> Coin!")
