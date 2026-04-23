# 🚀 NAS Distro Automator

Una solución ligera en Python, sin dependencias externas, para sincronizar y organizar archivos (como ISOs de Linux) de forma inteligente entre un servidor remoto y un NAS local. Utiliza Python como "cerebro" para clasificar archivos mediante reglas y delega la carga pesada a rsync.

## 🛠 Cómo funciona

- Escaneo Remoto: El script se conecta vía SSH a tu NAS remoto y lista los archivos disponibles.

- Filtrado Inteligente: Ignora carpetas, archivos temporales (.part) y cualquier archivo que ya esté presente en el registro local (transfer_log).

- Coincidencia por Reglas: Verifica el nombre del archivo contra las palabras clave definidas en config.json.

- Sincronización Selectiva: Si hay una coincidencia, activa rsync para descargar el archivo directamente en su carpeta de categoría correspondiente.

- Registro (Logging): Tras una transferencia exitosa, el nombre del archivo se guarda en un log local para evitar futuras descargas duplicadas.

## ⚙️ Instalación y Configuración
### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/nas-distro-automator.git
cd nas-distro-automator
```

### 2. Configuración (Archivos JSON)

Debes crear dos archivos en la raíz del proyecto. Como este proyecto utiliza la librería nativa `json`, no es necesario instalar nada con `pip`.
`secrets.json` 🔐

Guarda tus credenciales privadas aquí. No subas este archivo a GitHub.
```json
{
  "remote": {
    "user": "tu_usuario",
    "ip": "192.168.1.XX",
    "directory": "/ruta/remota/descargas"
  },
  "local": {
    "library": "/ruta/local/biblioteca",
    "transfer_log": "/ruta/local/transfer_log.txt"
  },
  "notificaciones": {
    "telegram_token": "",
    "chat_id": ""
  }
}
```

`config.json` 📂

Define tus reglas de organización.
```json
{
  "rules": [
    {
      "destination": "distros/ubuntu",
      "keywords": ["ubuntu", "lts", "noble"]
    },
    {
      "destination": "distros/fedora",
      "keywords": ["fedora", "workstation"]
    }
  ]
}
```

### 3. Llaves SSH

Asegúrate de tener acceso SSH sin contraseña al NAS remoto:

```bash
ssh-copy-id tu_usuario@ip_remota
```
## ⏲️ Automatización (Cron)

Para ejecutar el sincronizador automáticamente, añádelo a tu crontab. Se recomienda usar un script de envoltura .sh para manejar el lockfile como se discutió.

    1. Abre el crontab: crontab -e

    2. Añade la entrada (ejemplo, cada 15 minutos):
```bash
*/15 * * * * cd /ruta/al/repo && ./launcher.sh >> ./cron_error.log 2>&1
```

## 🛰️ Próximos pasos (Roadmap)

Estamos mejorando el flujo de trabajo constantemente. Las próximas funciones planeadas son:

Notificaciones de Telegram: Integrar la función send_telegram_notification para recibir alertas en tiempo real cuando una transferencia comienza, termina o cuando un archivo es ignorado.

Registro de Errores (Error Logging): Implementar un sistema de logs detallado que capture fallos de conexión SSH o errores de escritura en disco en un archivo error.log independiente para facilitar el diagnóstico.

Verificación de Checksum: Opción para verificar la integridad del archivo usando MD5/SHA256 después de la transferencia.

Refactorización del Código: Actualmente el código es un poco "espagueti" 🍝; un pequeño refactor vendría bien para mejorar la modularidad y facilitar el mantenimiento a largo plazo.

Panel Web: Una página de estado simple para visualizar el historial de descargas desde el navegador.

## 🛡️ Seguridad

    El archivo secrets.json está ignorado por Git a través de .gitignore.

    El script utiliza subprocess con argumentos en formato de lista para prevenir inyecciones de shell.

    Modo Debug: Puedes activar DEBUG = True en sync_manager.py para ver logs detallados y el progreso de rsync durante las pruebas manuales.

Desarrollado para una gestión de NAS eficiente y organizada.
