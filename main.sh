#!/bin/bash
LOCKFILE=/mnt/nancy/Home/meletc/temp/sync.lock
DONE_LOG=/mnt/nancy/Home/meletc/temp/file.log
TEMP_DIR=/mnt/nancy/Media/temp
#SCRIPT_PATH="path/to/project"

if [ -e $LOCKFILE ]; then exit; fi
touch $LOCKFILE

# Download files using rsync and logging all downloaded files to log file
rsync -avz --exclude-from=$DONE_LOG meletc@100.80.137.76:/volume1/Plex/downloads/ $TEMP_DIR

rsync -avz --inplace \
      --exclude='*.part' \
      --exclude='*.crdownload' \
      --exclude='.DS_Store' \
      --exclude-from="$DONE_LOG" \
      --log-format="%f" \
      meletc@100.80.137.76:/volume1/Plex/downloads/ "$TEMP_DIR" | grep -v 'directory' >> "$DONE_LOG"
    
# Sort files using python script, inside this python script notifications will be sent
# python $SCRIPT_PATH

rsync -avz --exclude-from=/ruta/local/archivos_transferidos.txt \
      --log-format="%f" --dry-run \
      user@remote:/ruta/remota/ /ruta/local/temporal/ >> /ruta/local/archivos_transferidos.txt