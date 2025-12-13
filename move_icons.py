
import os
import shutil

# Dynamic artifact dir from metadata or just hardcode based on previous output
artifact_dir = r"C:\Users\DELL\.gemini\antigravity\brain\c4cbb4ec-c0a5-46b7-affa-64238d7a774a"
static_dir = r"c:\Users\DELL\soyleyelim\soyleyelim\static\img"

files_to_move = {
    "burger_icon_3d_1765629498331.png": "burger_icon_3d.png",
    "pizza_icon_3d_1765629513671.png": "pizza_icon_3d.png",
    "doner_icon_3d_1765629531133.png": "doner_icon_3d.png",
    "dessert_icon_3d_1765629548643.png": "dessert_icon_3d.png"
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
