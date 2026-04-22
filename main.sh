#!/bin/bash
# Get directory where is this file located
SCRIPT_DIR=SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load .env file
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
else
    echo "Error crítico: No se encontró el archivo .env en $SCRIPT_DIR"
    exit 1
fi

if [ -e $LOCKFILE ]; then exit; fi
touch $LOCKFILE

# Download files using rsync and logging all downloaded files to log file
rsync -avz --exclude-from=$DONE_LOG meletc@100.80.137.76:/volume1/Plex/downloads/ $TEMP_DIR

rsync -avz --inplace \
      --exclude='*.part' \
      --exclude='*.crdownload' \
      --exclude='.DS_Store' \
      --exclude-from="$LOCAL_DONE_LOG" \
      --log-format="%f" \
      "$REMOTE_USER@$REMOTE_IP:/volume1/Plex/downloads/" "$LOCAL_TEMP_DIR" | grep -v 'directory' >> "$LOCAL_DONE_LOG"
    
# Sort files using python script, inside this python script notifications will be sent
# usr/bin/python3 $SCRIPT_DIR/organizer.py

rm "$LOCFILE"

