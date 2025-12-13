
import os
import shutil

artifact_dir = r"C:\Users\DELL\.gemini\antigravity\brain\c4cbb4ec-c0a5-46b7-affa-64238d7a774a"
static_dir = r"c:\Users\DELL\soyleyelim\soyleyelim\static\img"

files_to_move = {
    "kebap_icon_3d_1765629839273.png": "kebap_icon_3d.png",
    "cigkofte_icon_3d_1765629853631.png": "cigkofte_icon_3d.png",
    "pide_icon_3d_1765629871531.png": "pide_icon_3d.png",
    "coffee_icon_3d_1765629886187.png": "coffee_icon_3d.png",
    "street_food_icon_3d_1765629900523.png": "street_food_icon_3d.png",
    "home_food_icon_3d_1765629915509.png": "home_food_icon_3d.png"
}

if not os.path.exists(static_dir):
    os.makedirs(static_dir)

for src_name, dest_name in files_to_move.items():
    src_path = os.path.join(artifact_dir, src_name)
    dest_path = os.path.join(static_dir, dest_name)
    
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Moved {src_name} to {dest_name}")
    else:
        print(f"Source file not found: {src_path}")
