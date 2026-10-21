#!/usr/bin/env bash
# ==============================================================================
# CYBER_SQL // LAUNCHER FOR LINUX & macOS
# ==============================================================================

# Obtener directorio donde reside este script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

# 1. Verificar si python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "\e[1;31m[!] Error: python3 no está instalado o no se encuentra en el PATH.\e[0m"
    exit 1
fi

# 2. Comprobar si el módulo tkinter está presente
python3 -c "import tkinter" &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "\e[1;33m[!] Advertencia: Tkinter no está instalado en tu entorno de Python.\e[0m"
    echo -e "\e[1;36m[i] Ejecuta uno de los siguientes comandos según tu distribución:\e[0m"
    echo "    - Debian / Ubuntu / Mint:  sudo apt install python3-tk"
    echo "    - Arch / Manjaro:          sudo pacman -S tk"
    echo "    - Fedora / RHEL:           sudo dnf install python3-tkinter"
    exit 1
fi

# 3. Validar existencia del script principal
if [ ! -f "cyber_import.py" ]; then
    echo -e "\e[1;31m[!] Error: No se encontró 'cyber_import.py' en el directorio actual.\e[0m"
    exit 1
fi

# 4. Lanzar la aplicación
echo -e "\e[1;32m[✓] Iniciando CYBER_SQL INJECTOR...\e[0m"
python3 cyber_import.py "$@"
