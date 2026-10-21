#!/usr/bin/env bash
set -e

APP_NAME="CyberSQLInjector"
BIN_NAME="cyber_import"
VERSION="2.0.77"
APP_DIR="AppDir"
VENV_DIR=".build_venv"

echo -e "\e[1;36m[*] 1. Configurando entorno virtual aislado...\e[0m"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

# Usar estrictamente el pip del entorno virtual
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install pyinstaller

echo -e "\e[1;36m[*] 2. Compilando binario con PyInstaller...\e[0m"
"$VENV_DIR/bin/pyinstaller" --noconfirm --onedir --windowed \
    --name "$BIN_NAME" \
    --collect-all tkinter \
    cyber_import.py

echo -e "\e[1;36m[*] 3. Ensamblando estructura AppDir...\e[0m"
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR/usr/bin"
mkdir -p "$APP_DIR/usr/share/icons/hicolor/scalable/apps"

# Copiar archivos compilados
cp -r "dist/$BIN_NAME"/* "$APP_DIR/usr/bin/"

# Crear icono vectorial Cyberpunk
cat << 'EOF' > "$APP_DIR/cyber_import.svg"
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <rect width="128" height="128" fill="#08090d" rx="20"/>
  <rect x="14" y="24" width="100" height="80" fill="#10121b" stroke="#00f0ff" stroke-width="3" rx="8"/>
  <text x="64" y="62" fill="#00ff75" font-family="monospace" font-size="16" font-weight="bold" text-anchor="middle">&gt; CYBER_SQL</text>
  <circle cx="64" cy="82" r="5" fill="#ff0055"/>
</svg>
EOF
cp "$APP_DIR/cyber_import.svg" "$APP_DIR/usr/share/icons/hicolor/scalable/apps/cyber_import.svg"

# Crear lanzador Desktop
cat << EOF > "$APP_DIR/cyber_import.desktop"
[Desktop Entry]
Name=Cyber SQL Injector
Exec=cyber_import
Icon=cyber_import
Type=Application
Categories=Development;Database;
Terminal=false
EOF

# Crear runtime AppRun
cat << 'EOF' > "$APP_DIR/AppRun"
#!/bin/sh
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/bin:${LD_LIBRARY_PATH}"
exec "${HERE}/usr/bin/cyber_import" "$@"
EOF
chmod +x "$APP_DIR/AppRun"

echo -e "\e[1;36m[*] 4. Obteniendo appimagetool...\e[0m"
if [ ! -f "appimagetool" ]; then
    curl -sL -o appimagetool "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x appimagetool
fi

echo -e "\e[1;36m[*] 5. Generando paquete AppImage final...\e[0m"
ARCH=x86_64 ./appimagetool --appimage-extract-and-run "$APP_DIR" "${APP_NAME}-${VERSION}-x86_64.AppImage"

# Limpieza de archivos temporales
rm -rf build dist "$BIN_NAME.spec" "$APP_DIR" "$VENV_DIR"

echo -e "\e[1;32m[✓] Proceso completado exitosamente: ${APP_NAME}-${VERSION}-x86_64.AppImage\e[0m"
