# NAS SYNC
Este es mi proyectico personal para descargar archivos desde un nas donde se hacen descargas y luego organizarlos dentro de mi computador personal.

## Importante

Necesitaras un archivo .env que tenga las siguientes vairables:
```
# Configuración del NAS Remoto
REMOTE_USER=tu_usuario
REMOTE_IP=192.168.1.100
REMOTE_DIR=/volume1/downloads/distros/

# Rutas Locales (Ocultas)
LOCAL_TEMP_DIR=/home/usuario/nas/temporal
LOCAL_BIBLIO_DIR=/home/usuario/nas/biblioteca
LOCAL_DONE_LOG=/home/usuario/nas/logs/transferidos.txt

# Notificaciones
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNO
TELEGRAM_CHAT_ID=987654321
```

Tambien deberas correr el siguiente script en tu carpeta para crear el archivo de log

```
rsync -avz --exclude-from=/ruta/local/archivos_transferidos.txt \
      --log-format="%f" --dry-run \
      user@remote:/ruta/remota/ /ruta/local/temporal/ >> /ruta/local/archivos_transferidos.txt
```
