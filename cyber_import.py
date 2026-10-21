#!/usr/bin/env python3
"""
CYBER_SQL // INJECTOR v2.0.77
Multiplatform MySQL Database Deployment Tool with Cyberpunk HUD.
Zero external dependencies (Pure Python Standard Library).
"""

import os
import sys
import glob
import shutil
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# ---------------- PALETA CYBERPUNK ----------------
C_BG_VOID    = "#08090d"
C_PANEL      = "#10121b"
C_PANEL_ALT  = "#161926"
C_CYAN       = "#00f0ff"
C_PINK       = "#ff0055"
C_YELLOW     = "#ffe600"
C_GREEN      = "#00ff75"
C_TEXT       = "#d8dbf0"
C_MUTED      = "#5d627d"
C_ALERT      = "#ff2a2a"

FONT_MONO      = ("Consolas", 10)
FONT_MONO_BOLD = ("Consolas", 10, "bold")
FONT_TITLE     = ("Consolas", 16, "bold")
FONT_SUBTITLE  = ("Consolas", 8)

# ---------------- UTILIDADES DEL SISTEMA ----------------
def find_mysql_binary():
    in_path = shutil.which("mysql")
    if in_path:
        return in_path

    candidates = []
    if sys.platform.startswith("linux"):
        candidates = [
            "/opt/lampp/bin/mysql",
            "/usr/bin/mysql",
            "/usr/local/bin/mysql",
            "/usr/bin/mariadb"
        ]
    elif sys.platform == "win32":
        candidates = [
            r"C:\xampp\mysql\bin\mysql.exe",
            r"C:\laragon\bin\mysql\*\bin\mysql.exe",
            r"C:\Program Files\MySQL\MySQL Server *\bin\mysql.exe",
            r"C:\Program Files\MariaDB *\bin\mysql.exe"
        ]
    elif sys.platform == "darwin":  # macOS
        candidates = [
            "/Applications/XAMPP/xamppfiles/bin/mysql",
            "/opt/homebrew/bin/mysql",
            "/usr/local/bin/mysql"
        ]

    for item in candidates:
        if "*" in item:
            matches = glob.glob(item)
            if matches:
                return sorted(matches)[-1]
        elif os.path.exists(item):
            return item
    return ""

# ---------------- APLICACIÓN GUI ----------------
class CyberInjectorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CYBER_SQL // INJECTOR_NET_V2")
        self.geometry("780x740")
        self.minsize(720, 680)
        self.configure(bg=C_BG_VOID)

        self.mysql_bin = find_mysql_binary()
        self.setup_ui()
        self.check_initial_status()

    def setup_ui(self):
        # Header / Banner
        header_frame = tk.Frame(self, bg=C_BG_VOID, padx=15, pady=10)
        header_frame.pack(fill=tk.X)

        title_lbl = tk.Label(
            header_frame, 
            text="[ DATABASE OVERRIDE // SQL BREACHER ]", 
            fg=C_CYAN, 
            bg=C_BG_VOID, 
            font=FONT_TITLE,
            anchor="w"
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            header_frame, 
            text="CORE ENGINE: NEUTRALIZING CONSTRAINTS // PROTOCOL: FOREIGN_KEY_CHECKS=0", 
            fg=C_PINK, 
            bg=C_BG_VOID, 
            font=FONT_SUBTITLE,
            anchor="w"
        )
        sub_lbl.pack(anchor="w")

        # Contenedor de Configuración
        config_frame = tk.Frame(self, bg=C_PANEL, bd=1, relief=tk.SOLID, padx=15, pady=12)
        config_frame.pack(fill=tk.X, padx=15, pady=5)

        # SQL Target File
        tk.Label(config_frame, text="// ARCHIVO SQL FUENTE", fg=C_CYAN, bg=C_PANEL, font=FONT_MONO_BOLD).grid(row=0, column=0, sticky="w", pady=(0, 2))
        
        file_subframe = tk.Frame(config_frame, bg=C_PANEL)
        file_subframe.grid(row=1, column=0, columnspan=4, sticky="we", pady=(0, 8))
        config_frame.columnconfigure(0, weight=1)

        self.ent_file = tk.Entry(file_subframe, bg=C_PANEL_ALT, fg=C_TEXT, insertbackground=C_CYAN, font=FONT_MONO, relief=tk.FLAT, bd=4)
        self.ent_file.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        btn_browse = tk.Button(
            file_subframe, text="[ EXAMINAR ]", command=self.browse_file,
            bg=C_PANEL_ALT, fg=C_CYAN, activebackground=C_CYAN, activeforeground=C_BG_VOID,
            font=FONT_MONO_BOLD, relief=tk.FLAT, bd=0, padx=10, cursor="hand2"
        )
        btn_browse.pack(side=tk.RIGHT)

        # Base de datos y Binario
        tk.Label(config_frame, text="// BASE DE DATOS TARGET", fg=C_YELLOW, bg=C_PANEL, font=FONT_MONO_BOLD).grid(row=2, column=0, sticky="w", pady=(4, 2))
        tk.Label(config_frame, text="// BINARIO MYSQL DETECTADO", fg=C_MUTED, bg=C_PANEL, font=FONT_MONO_BOLD).grid(row=2, column=1, columnspan=3, sticky="w", pady=(4, 2), padx=(10, 0))

        self.ent_db = tk.Entry(config_frame, bg=C_PANEL_ALT, fg=C_YELLOW, insertbackground=C_YELLOW, font=FONT_MONO_BOLD, relief=tk.FLAT, bd=4)
        self.ent_db.insert(0, "databaseName")
        self.ent_db.grid(row=3, column=0, sticky="we", pady=(0, 8))

        self.ent_bin = tk.Entry(config_frame, bg=C_PANEL_ALT, fg=C_TEXT, insertbackground=C_CYAN, font=FONT_MONO, relief=tk.FLAT, bd=4)
        self.ent_bin.insert(0, self.mysql_bin)
        self.ent_bin.grid(row=3, column=1, columnspan=3, sticky="we", pady=(0, 8), padx=(10, 0))

        # Host, Port, User, Password
        conn_frame = tk.Frame(config_frame, bg=C_PANEL)
        conn_frame.grid(row=4, column=0, columnspan=4, sticky="we", pady=(4, 4))
        for i in range(4): conn_frame.columnconfigure(i, weight=1)

        tk.Label(conn_frame, text="HOST", fg=C_TEXT, bg=C_PANEL, font=FONT_MONO).grid(row=0, column=0, sticky="w")
        tk.Label(conn_frame, text="PUERTO", fg=C_TEXT, bg=C_PANEL, font=FONT_MONO).grid(row=0, column=1, sticky="w", padx=4)
        tk.Label(conn_frame, text="USUARIO", fg=C_TEXT, bg=C_PANEL, font=FONT_MONO).grid(row=0, column=2, sticky="w", padx=4)
        tk.Label(conn_frame, text="CONTRASEÑA", fg=C_TEXT, bg=C_PANEL, font=FONT_MONO).grid(row=0, column=3, sticky="w")

        self.ent_host = tk.Entry(conn_frame, bg=C_PANEL_ALT, fg=C_TEXT, insertbackground=C_CYAN, font=FONT_MONO, relief=tk.FLAT, bd=3)
        self.ent_host.insert(0, "127.0.0.1")
        self.ent_host.grid(row=1, column=0, sticky="we", padx=(0, 4), pady=(2, 0))

        self.ent_port = tk.Entry(conn_frame, bg=C_PANEL_ALT, fg=C_TEXT, insertbackground=C_CYAN, font=FONT_MONO, relief=tk.FLAT, bd=3)
        self.ent_port.insert(0, "3306")
        self.ent_port.grid(row=1, column=1, sticky="we", padx=4, pady=(2, 0))

        self.ent_user = tk.Entry(conn_frame, bg=C_PANEL_ALT, fg=C_TEXT, insertbackground=C_CYAN, font=FONT_MONO, relief=tk.FLAT, bd=3)
        self.ent_user.insert(0, "root")
        self.ent_user.grid(row=1, column=2, sticky="we", padx=4, pady=(2, 0))

        self.ent_pass = tk.Entry(conn_frame, bg=C_PANEL_ALT, fg=C_TEXT, insertbackground=C_CYAN, font=FONT_MONO, show="*", relief=tk.FLAT, bd=3)
        self.ent_pass.grid(row=1, column=3, sticky="we", padx=(4, 0), pady=(2, 0))

        # Checkboxes / Modos
        flags_frame = tk.Frame(config_frame, bg=C_PANEL)
        flags_frame.grid(row=5, column=0, columnspan=4, sticky="w", pady=(10, 0))

        self.var_drop = tk.BooleanVar(value=True)
        chk_drop = tk.Checkbutton(
            flags_frame, text="[ DROP IF EXISTS (PURGAR ANTES DE CREAR) ]",
            variable=self.var_drop, bg=C_PANEL, fg=C_PINK, activebackground=C_PANEL,
            activeforeground=C_PINK, selectcolor=C_BG_VOID, font=FONT_MONO
        )
        chk_drop.pack(side=tk.LEFT, padx=(0, 15))

        self.var_fk = tk.BooleanVar(value=True)
        chk_fk = tk.Checkbutton(
            flags_frame, text="[ BYPASS FOREIGN KEYS (FORZAR IMPORTACIÓN) ]",
            variable=self.var_fk, bg=C_PANEL, fg=C_GREEN, activebackground=C_PANEL,
            activeforeground=C_GREEN, selectcolor=C_BG_VOID, font=FONT_MONO
        )
        chk_fk.pack(side=tk.LEFT)

        # Botón de Acción Principal
        self.btn_execute = tk.Button(
            self, text=">>> INICIAR INYECCIÓN DE DATOS <<<", command=self.start_import_thread,
            bg=C_PINK, fg="#ffffff", activebackground=C_CYAN, activeforeground=C_BG_VOID,
            font=("Consolas", 12, "bold"), relief=tk.FLAT, bd=0, pady=8, cursor="hand2"
        )
        self.btn_execute.pack(fill=tk.X, padx=15, pady=(10, 5))

        # Consola / Monitor Terminal
        term_frame = tk.Frame(self, bg=C_PANEL, bd=1, relief=tk.SOLID, padx=10, pady=8)
        term_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 15))

        tk.Label(term_frame, text="// TERMINAL HUD & LIVE TELEMETRY", fg=C_GREEN, bg=C_PANEL, font=FONT_MONO_BOLD).pack(anchor="w")

        self.txt_log = tk.Text(
            term_frame, bg=C_BG_VOID, fg=C_GREEN, insertbackground=C_GREEN,
            font=FONT_MONO, relief=tk.FLAT, bd=5, state=tk.DISABLED
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    def log(self, text, color=C_GREEN):
        def _append():
            self.txt_log.config(state=tk.NORMAL)
            self.txt_log.insert(tk.END, text + "\n")
            self.txt_log.see(tk.END)
            self.txt_log.config(state=tk.DISABLED)
        self.after(0, _append)

    def browse_file(self):
        f = filedialog.askopenfilename(
            title="Seleccionar Dump SQL",
            filetypes=[("SQL Files", "*.sql"), ("Todos los archivos", "*.*")]
        )
        if f:
            self.ent_file.delete(0, tk.END)
            self.ent_file.insert(0, f)
            size_mb = os.path.getsize(f) / (1024 * 1024)
            self.log(f"[+] SQL Cargado: {os.path.basename(f)} ({size_mb:.2f} MB)", C_CYAN)

    def check_initial_status(self):
        self.log("===================================================================", C_MUTED)
        self.log(" [SYS] CYBER_SQL INJECTOR INTERFACE ONLINE", C_CYAN)
        self.log(f" [SYS] PLATAFORMA: {sys.platform.upper()}", C_TEXT)
        if self.mysql_bin:
            self.log(f" [✓] BINARIO MYSQL DETECTADO: {self.mysql_bin}", C_GREEN)
        else:
            self.log(" [!] ADVERTENCIA: Binario mysql no encontrado. Ingrésalo manualmente.", C_ALERT)
        self.log("===================================================================", C_MUTED)

    def start_import_thread(self):
        sql_file = self.ent_file.get().strip()
        db_name = self.ent_db.get().strip()
        mysql_bin = self.ent_bin.get().strip()

        if not sql_file or not os.path.isfile(sql_file):
            messagebox.showerror("Error", "Debes seleccionar un archivo .sql válido.")
            return

        if not db_name:
            messagebox.showerror("Error", "Especifica un nombre de base de datos.")
            return

        if not mysql_bin or not os.path.isfile(mysql_bin):
            messagebox.showerror("Error", "El binario de MySQL no es válido.")
            return

        self.btn_execute.config(state=tk.DISABLED, bg=C_MUTED, text="INYECTANDO DATOS...")
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        sql_file = self.ent_file.get().strip()
        db_name = self.ent_db.get().strip()
        mysql_bin = self.ent_bin.get().strip()
        host = self.ent_host.get().strip()
        port = self.ent_port.get().strip()
        user = self.ent_user.get().strip()
        pwd = self.ent_pass.get().strip()
        drop = self.var_drop.get()
        bypass_fk = self.var_fk.get()

        base_cmd = [mysql_bin, "-h", host, "-P", port, "-u", user]
        if pwd:
            base_cmd.append(f"-p{pwd}")

        try:
            # 1. Preparar la BD
            self.log(f"[*] PREPARANDO ENTORNO PARA: `{db_name}`...", C_YELLOW)
            queries = []
            if drop:
                queries.append(f"DROP DATABASE IF EXISTS `{db_name}`;")
            queries.append(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

            res = subprocess.run(base_cmd + ["-e", " ".join(queries)], capture_output=True, text=True)
            if res.returncode != 0:
                self.log(f"[!] ERROR CREANDO BD:\n{res.stderr}", C_ALERT)
                self.restore_button()
                return

            self.log(f"[✓] BASE DE DATOS `{db_name}` LISTA.", C_GREEN)

            # 2. Inyección del dump SQL con búfer y manejo seguro de streams
            file_size_mb = os.path.getsize(sql_file) / (1024 * 1024)
            self.log(f"[*] INICIANDO TRANSMISIÓN: {file_size_mb:.2f} MB...", C_CYAN)

            import_cmd = [mysql_bin, "--max_allowed_packet=128M", "-h", host, "-P", port, "-u", user, db_name]
            if pwd:
                import_cmd.insert(-1, f"-p{pwd}")

            proc = subprocess.Popen(import_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            try:
                proc.stdin.write(b"SET NAMES utf8mb4;\n")
                if bypass_fk:
                    proc.stdin.write(b"SET FOREIGN_KEY_CHECKS=0;\n")
                    proc.stdin.write(b"SET UNIQUE_CHECKS=0;\n")
                proc.stdin.flush()

                # Transmisión en bloques de 1MB
                with open(sql_file, "rb") as f:
                    while chunk := f.read(1024 * 1024):
                        proc.stdin.write(chunk)
                        proc.stdin.flush()

                if bypass_fk:
                    proc.stdin.write(b"\nSET FOREIGN_KEY_CHECKS=1;\n")
                    proc.stdin.write(b"SET UNIQUE_CHECKS=1;\n")
                proc.stdin.flush()

            except (BrokenPipeError, IOError):
                self.log("[!] La conexión con MySQL se cerró durante la transmisión.", C_ALERT)
            finally:
                # Evita ValueError ("flush of closed file") desvinculando stdin antes de communicate
                try:
                    if proc.stdin and not proc.stdin.closed:
                        proc.stdin.close()
                except Exception:
                    pass
                proc.stdin = None

            _, stderr = proc.communicate()

            if proc.returncode == 0:
                self.log(f"[✓✓✓] INYECCIÓN COMPLETADA CON ÉXITO EN `{db_name}`.", C_GREEN)
                self.after(0, lambda: messagebox.showinfo("Operación Exitosa", f"Base de datos `{db_name}` levantada sin errores."))
            else:
                self.log(f"[!] FALLO EN IMPORTACIÓN:\n{stderr.decode('utf-8', errors='replace')}", C_ALERT)

        except Exception as e:
            self.log(f"[!] EXCEPCIÓN DEL SISTEMA: {str(e)}", C_ALERT)

        self.restore_button()

    def restore_button(self):
        def _restore():
            self.btn_execute.config(state=tk.NORMAL, bg=C_PINK, text=">>> INICIAR INYECCIÓN DE DATOS <<<")
        self.after(0, _restore)

if __name__ == "__main__":
    app = CyberInjectorApp()
    app.mainloop()
