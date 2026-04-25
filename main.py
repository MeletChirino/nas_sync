import os
import subprocess
import json
from pathlib import Path

# --- OPERATIONAL MODE ---
DEBUG = True  # Set to False for production/silent mode
# Localizar la carpeta del script para que funcione en Cron
SCRIPT_DIR = Path(__file__).parent

def send_telegram_notification(item, secrets, status="success"):
    """
    Sends a notification via Telegram API using system curl.
    status: "success", "ignored", or "error"
    """
    token = secrets['telegram']['token']
    chat_id = secrets['telegram']['chat_id']

    if not token or not chat_id:
        if DEBUG: print("⚠️ Telegram credentials missing. Skipping notification.")
        return

    # Personalización del mensaje según el estado
    icons = {"success": "✅", "ignored": "⏭️", "error": "❌"}
    titles = {
        "success": "*Download Complete*",
        "ignored": "*File Ignored (No Match)*",
        "error": "*Transfer Failed*"
    }

    icon = icons.get(status, "🔔")
    title = titles.get(status, "*Notification*")
    print(f"Item: {item}")

    message = f"{icon} {title}\n\n*Serie:* `{item['title']}`\n\n*File:* `{item['name']}`\n*Host:* `{secrets['remote']['ip']}`"

    # Comando curl para evitar dependencias de Python
    command = [
        "curl", "-s", "-X", "POST",
        f"https://api.telegram.org/bot{token}/sendMessage",
        "-d", f"chat_id={chat_id}",
        "-d", f"text={message}",
        "-d", "parse_mode=Markdown"
    ]

    try:
        # Ejecutamos en segundo plano para no retrasar el script principal
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        if DEBUG: print(f"❌ Could not send Telegram notification: {e}")

def load_config():
    try:
        if DEBUG: print(F"Open {SCRIPT_DIR}/secrets.json")
        # Load secrets
        with open(SCRIPT_DIR / "secrets.json", "r") as f:
            secrets = json.load(f)

        if DEBUG: print(F"Open {SCRIPT_DIR}/config.json")
        # Load library config
        with open(SCRIPT_DIR / "config.json", "r") as f:
            config = json.load(f)

        return secrets, config
    except Exception as e:
        print(F"Error: {e}")

def sort_file(name, library_map):
    name_lower = name.lower()
    for map in library_map:
        if any(key in name_lower for key in map['keywords']):
            return map['destino']
    return None

def ignore_file(file, download_list):
    # A. Ignore if it's a directory (identified by the '/' suffix from ls -F)
    if file.endswith('/'):
        if DEBUG: print(f"📁 Ignoring directory: {file}")
        return True

    # B. Ignore empty strings, temporary files, or already downloaded files
    if not file or file.endswith('.part') or file in download_list:
        return True

    return False

def classify_file(filename, rules):
    """
    Matches the filename against JSON rules.
    Returns the destination folder if a match is found, otherwise None.
    """
    name_lower = filename.lower()
    for rule in rules:
        if any(key.lower() in name_lower for key in rule['keywords']):
            if DEBUG: print(f"--> Title match")
            if "season" in rules:
                if any(key.lower() in name_lower for key in rule['season']):
                    if DEBUG: print(f"--> Season match")
                    return rule['destination'], rule["title"]
            else:
                return rule['destination'], rule["title"]
    return None, rule["title"]

def main():
    secrets, config = load_config()

    # Ejemplo de uso de las variables
    user = secrets['remote']['user']
    ip = secrets['remote']['ip']
    remote_host = f"{user}@{ip}"
    remote_dir = secrets['remote']['directory']
    local_library = secrets['local']['library']

    print(f"Iniciando sincronización con {remote_host}...")
    # ... resto de la lógica de rsync ...

    log_db = secrets['local']['transferred_log']
    print(f"Opening {log_db}")
    if os.path.exists(log_db):
        with open(log_db, "r") as f:
            download_list = set(f.read().splitlines())
    else:
        download_list = set()
    print(F"Download list {download_list}")

    # Get remote file list via SSH
    if DEBUG: print(f"🔍 Connecting to {remote_host}...")

    # ls -F appends '/' to directories, allowing us to identify and ignore them
    ssh_command = ["ssh", remote_host, f"ls -F {remote_dir}"]
    ssh_result = subprocess.run(ssh_command, capture_output=True, text=True)

    if ssh_result.returncode != 0:
        if DEBUG: print(f"❌ SSH Error: {ssh_result.stderr}")
        return

    remote_items = ssh_result.stdout.splitlines()

    if DEBUG: print(f"remote files: {remote_items}")

    downloadable_items = []
    # Process items
    for item in remote_items:

        if ignore_file(item, download_list): continue
        if DEBUG: print(f"Analize item: {item}")

        # MATCH VERIFICATION (Only download if it exists in our rules)
        target_subfolder, title = classify_file(item, config['library'])

        clean_name = item[0:-1]
        is_file_in_database = False
        if DEBUG: print(f"--> Verify if {clean_name} is on database")
        # Check if the file is already in our local database
        if clean_name in download_list:
            if DEBUG: print(f"✅ Skipping: '{clean_name}' is already in the log.")
            continue

        if ".part" in item:
            continue

        if target_subfolder:
            if DEBUG: print(f"🎯 Match found: {item} -> {target_subfolder}")
            final_destination_path = os.path.join(local_library, target_subfolder)
            os.makedirs(final_destination_path, exist_ok=True)
            item_dict = {
                "title": title,
                "name": item,
                "final_destination": final_destination_path + "/",
            }
            downloadable_items.append(item_dict)
        else:
            if DEBUG: print(f"⏭️ No match for '{item}'. Skipping.")

    # Download selected items
    for item in downloadable_items:
        # Remove * at the end of the name
        item["name"] = item["name"][0:-1]
        # D. Configure Rsync options based on DEBUG mode
        rsync_options = ["-az"]
        if DEBUG:
            rsync_options = ["-avz", "--progress"]
            print(f"🚀 Starting transfer for {item['name']}...")

        rsync_source = f"{remote_host}:\"{remote_dir}/{item['name']}\""
        rsync_command = ["rsync"] + rsync_options + [rsync_source, item['final_destination']]

        # Execute rsync
        print(F"RUN: {rsync_command}")
        rsync_result = subprocess.run(rsync_command)

        # Check on log file

        if rsync_result.returncode == 0:
            # E. Register in log only if the transfer was successful
            with open(log_db, "a") as f:
                f.write(f"{item['name']}\n")
            if DEBUG: print(f"✅ Logged successfully: {item['name']}")
            send_telegram_notification(item, secrets, status="success")

        else:
            if DEBUG: print(f"❌ Failed to download: {item['name']}")


main()
