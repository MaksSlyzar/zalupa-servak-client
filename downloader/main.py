import dearpygui.dearpygui as dpg
import requests
import os
import threading
import time
import platform

OWNER = "MaksSlyzar"
REPO = "zalupa-servak-client"
BRANCH = "main"

system = platform.system()
if system == "Linux":
    MINECRAFT_DIR = os.path.expanduser("~/.minecraft")
elif system == "Windows":
    MINECRAFT_DIR = os.path.join(os.getenv("APPDATA"), ".minecraft")
else:
    MINECRAFT_DIR = os.getcwd()

MODS_DIR = os.path.join(MINECRAFT_DIR, "mods")
os.makedirs(MODS_DIR, exist_ok=True)

MODS_LIST_URL = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/mods_list.txt"
SERVERS_DAT_URL = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/client/servers.dat"

FONT_FILENAME = "NotoSans-Regular.ttf"
FONT_URL = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf"
FONT_PATH = os.path.join(os.path.dirname(__file__), FONT_FILENAME)
if not os.path.exists(FONT_PATH):
    r = requests.get(FONT_URL)
    r.raise_for_status()
    with open(FONT_PATH, "wb") as f:
        f.write(r.content)

def download_file(url, save_dir):
    filename = os.path.basename(url)
    save_path = os.path.join(save_dir, filename)
    if os.path.exists(save_path):
        return save_path
    r = requests.get(url)
    r.raise_for_status()
    with open(save_path, "wb") as f:
        f.write(r.content)
    size_mb = len(r.content) / (1024 * 1024)
    filename_display = filename if len(filename) <= 15 else filename[:12] + "..."
    dpg.set_value(status_text, f"Downloaded: {filename_display} ({size_mb:.2f} MB)")
    return save_path

def start_download_callback():
    dpg.set_value(status_text, "Downloading mods_list.txt...")
    r = requests.get(MODS_LIST_URL)
    r.raise_for_status()
    mods_files = r.text.splitlines()
    dpg.set_value(status_text, f"Found {len(mods_files)} mods, starting download...")

    for idx, mod_file in enumerate(mods_files):
        mod_url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/mods/{mod_file}"
        download_file(mod_url, MODS_DIR)
        dpg.set_value(progress_bar, (idx + 1) / (len(mods_files) + 1))  # +1 for servers.dat

    download_file(SERVERS_DAT_URL, MINECRAFT_DIR)
    dpg.set_value(progress_bar, 1.0)
    dpg.set_value(status_text, "Download finished!")

def show_caci():
    while True:
        time.sleep(10)
        dpg.set_value(caci_text, "Caci")
        time.sleep(1)
        dpg.set_value(caci_text, "")

dpg.create_context()
with dpg.font_registry():
    if os.path.exists(FONT_PATH):
        default_font = dpg.add_font(FONT_PATH, 22)
        dpg.bind_font(default_font)

with dpg.window(label="GitHub Downloader") as window_id:
    dpg.add_text(f"{OWNER}/{REPO}", color=(100, 200, 255))
    dpg.add_spacer(height=10)
    status_text = dpg.add_text("Waiting...")
    progress_bar = dpg.add_progress_bar(label="Progress", default_value=0.0, width=-1)
    dpg.add_spacer(height=10)
    dpg.add_button(label="Download", width=200, height=40, callback=start_download_callback)
    caci_text = dpg.add_text("", color=(255, 100, 100))

threading.Thread(target=show_caci, daemon=True).start()

dpg.create_viewport(title="GitHub Downloader")
dpg.setup_dearpygui()
screen_width = dpg.get_viewport_width()
screen_height = dpg.get_viewport_height()
dpg.configure_item(window_id, width=screen_width, height=screen_height)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

