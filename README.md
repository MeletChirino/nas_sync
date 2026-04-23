# 🚀 NAS Distro Automator

Una solución ligera en Python, sin dependencias externas, para sincronizar y organizar archivos (como ISOs de Linux) de forma inteligente entre un servidor remoto y un NAS local. Utiliza Python como "cerebro" para clasificar archivos mediante reglas y delega la carga pesada a rsync.
## 🛠 Cómo funciona

    Escaneo Remoto: El script se conecta vía SSH a tu NAS remoto y lista los archivos disponibles.

    Filtrado Inteligente: Ignora carpetas, archivos temporales (.part) y cualquier archivo que ya esté presente en el registro local (transfer_log).

    Coincidencia por Reglas: Verifica el nombre del archivo contra las palabras clave definidas en config.json.

    Sincronización Selectiva: Si hay una coincidencia, activa rsync para descargar el archivo directamente en su carpeta de categoría correspondiente.

    Registro (Logging): Tras una transferencia exitosa, el nombre del archivo se guarda en un log local para evitar futuras descargas duplicadas.

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
