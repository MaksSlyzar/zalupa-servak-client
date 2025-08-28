import os
import platform

system = platform.system()
if system == "Linux":
    MINECRAFT_DIR = os.path.expanduser("~/.minecraft")
elif system == "Windows":
    MINECRAFT_DIR = os.path.join(os.getenv("APPDATA"), ".minecraft")
else:
    MINECRAFT_DIR = os.getcwd()

MODS_DIR = os.path.join("./", "mods")
if not os.path.exists(MODS_DIR):
    os.makedirs(MODS_DIR)

mods_list_path = os.path.join("./mods_list.txt")

with open(mods_list_path, "w") as f:
    for root, dirs, files in os.walk(MODS_DIR):
        for file in files:
            if file.endswith(".jar"):
                f.write(file + "\n")

print(f"Mods list saved to: {mods_list_path}")

