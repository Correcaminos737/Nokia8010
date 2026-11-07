import subprocess
import os

ADB = os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe")
DEV = "192.168.1.128:5555"

# Master autoconfig with hotkey disabled
AUTOCFG = """input_driver = "android"
input_device = "Microsoft X-Box 360 pad"
input_device_display_name = "EasySMX X20 Pad"
input_vendor_id = "1118"
input_product_id = "654"

input_b_btn = "0"
input_a_btn = "1"
input_y_btn = "2"
input_x_btn = "3"
input_l_btn = "4"
input_r_btn = "5"
input_select_btn = "6"
input_start_btn = "7"
input_l3_btn = "9"
input_r3_btn = "10"

input_up_btn = "h0up"
input_down_btn = "h0down"
input_left_btn = "h0left"
input_right_btn = "h0right"

input_l_x_plus_axis = "+0"
input_l_x_minus_axis = "-0"
input_l_y_plus_axis = "+1"
input_l_y_minus_axis = "-1"

# CRITICAL: Do NOT bind hotkey enable to select
input_enable_hotkey_btn = "nul"
input_menu_toggle_btn = "nul"
"""

local_cfg = "Microsoft X-Box 360 pad.cfg"
with open(local_cfg, "w", encoding="utf-8") as f:
    f.write(AUTOCFG)

subprocess.run([ADB, "connect", DEV])
# Push to autoconfig android directory
subprocess.run([ADB, "-s", DEV, "shell", "mkdir", "-p", "/sdcard/RetroArch/autoconfig/android"])
subprocess.run([ADB, "-s", DEV, "push", local_cfg, "/sdcard/RetroArch/autoconfig/android/Microsoft X-Box 360 pad.cfg"])
print("Autoconfig actualizado con input_enable_hotkey_btn = nul!")
