# ⚡ CYBER_SQL // BREACHER v2.0.77

> **Cross-platform MySQL & MariaDB database deployment tool with a Cyberpunk HUD.**  
> Effortlessly bypass **Error 150** (`errno: 150 "Foreign key constraint is incorrectly formed"`), stream massive multi-gigabyte SQL dumps with near-zero memory footprint, and automate database creation with zero external Python dependencies.

---

## 📥 Download Pre-built Binaries

Pre-compiled, standalone executables with zero installation requirements are available in the **[Releases](https://github.com/TU_USUARIO/cyber-sql-breacher/releases/latest)** section.

| Platform | Format | Architecture | Run Command |
|---|---|---|---|
| **Linux** | `.AppImage` | x86_64 (64-bit) | `chmod +x CyberSQLInjector-*.AppImage && ./CyberSQLInjector-*.AppImage` |
| **Windows** | `.exe` | x64 (64-bit) | Double-click to launch (Portable, no install needed) |

> **Linux Note:** On newer distributions without FUSE 2 pre-installed (e.g., Ubuntu 24.04+), launch with:  
> `./CyberSQLInjector-*.AppImage --appimage-extract-and-run`

---

## 💀 The Problem It Solves

When deploying or restoring local database dumps (exported from production, staging, or legacy systems), developers often face recurring bottlenecks:

1. **Error 1005 (errno: 150):** InnoDB rejects tables when child entities are declared prior to parent entities in the dump file, or when subtle collation/type mismatches occur.
2. **Buffer and Memory Exhaustion:** Conventional GUI clients (Workbench, phpMyAdmin, DBeaver) attempt to parse entire multi-megabyte scripts into RAM, causing freezes or throwing `max_allowed_packet` / HTTP timeout errors.
3. **Socket & Path Hell:** Switching between standard system packages and all-in-one local stacks (like **XAMPP** in `/opt/lampp` or **Laragon**) causes socket collision issues when targeting CLI binaries.

`CYBER_SQL // BREACHER` pipes raw byte streams directly to the database daemon, wraps the session in constraint-neutralizing pragmas, and provides real-time telemetry inside a lightweight, retro-futuristic HUD.

---

## ⚡ Key Features

* **Constraint Neutralization Protocol:** Automatically wraps your dump stream in `SET FOREIGN_KEY_CHECKS=0;`, `SET UNIQUE_CHECKS=0;`, and `SET NAMES utf8mb4;` to ensure frictionless imports regardless of table definition order.
* **Low-Footprint I/O Streaming:** Reads and transmits SQL files in continuous 1 MB chunks via subprocess pipelines. Never loads entire files into system memory.
* **Zero External Dependencies:** Built entirely with Python's Standard Library (`tkinter`, `subprocess`, `threading`, `shutil`). No `pip install` required to run the source.
* **Smart Binary Auto-Detection:** Automatically locates `mysql` binaries across system environments:
  * **Linux:** System PATH, XAMPP (`/opt/lampp/bin/mysql`), MariaDB.
  * **Windows:** System PATH, XAMPP (`C:\xampp\mysql\bin`), Laragon, standard program directories.
  * **macOS:** System PATH, Homebrew, XAMPP.
* **Threaded Non-Blocking HUD:** Database injection and log updates run in isolated background threads to keep the interface smooth and responsive during long transfers.

---

## 📂 Repository Structure

```text
├── cyber_import.py       # Main GUI application & I/O stream engine
├── requirements.txt      # Environment & system dependencies documentation
├── run.sh                # Zero-config launcher for Linux & macOS
├── run.bat               # Zero-config launcher for Windows
├── build_appimage.sh     # Isolated AppImage compiler for Linux (PEP 668 compliant)
├── build_exe.bat         # Standalone single-file .EXE compiler for Windows
└── .gitignore            # Git exclusion rules for dumps, builds, and venvs
```

---

## 🚀 Quick Start

### Prerequisites
* **Python 3.8+**
* Tkinter system package (pre-installed on Windows/macOS):
  * **Ubuntu / Debian / Mint:** `sudo apt install python3-tk`
  * **Arch / Manjaro / CachyOS:** `sudo pacman -S tk`
  * **Fedora / RHEL:** `sudo dnf install python3-tkinter`

### Run from Source

#### Linux & macOS
```bash
chmod +x run.sh
./run.sh
```

#### Windows
Double-click `run.bat` or run via Command Prompt:
```cmd
run.bat
```

---

## 📦 Building Standalone Binaries

Distribute standalone executables without requiring team members to install Python or configure dependencies.

### Linux (.AppImage)
Generates an isolated, portable `CyberSQLInjector-2.0.77-x86_64.AppImage` using a self-contained virtual environment (safe against PEP 668 restrictions):

```bash
chmod +x build_appimage.sh
./build_appimage.sh
```

### Windows (.EXE)
Generates a single-file portable executable in `dist\CyberSQLInjector.exe` with no background console:

```cmd
build_exe.bat
```

---

## 🛠️ How It Works Under the Hood

```text
+------------------+         Pipe Stream (1MB Chunks)         +----------------------+
|  SQL Dump File   | =======================================> |                      |
+------------------+                                          |                      |
                            [ Pre-Execution Injection ]       |  MySQL CLI Process   |
                            - SET NAMES utf8mb4               |                      |
                            - SET FOREIGN_KEY_CHECKS=0        |  --max-allowed-packet|
                            - SET UNIQUE_CHECKS=0             |    = 128M            |
                                                              |                      |
                            [ Post-Execution Injection ]      |  Target:             |
                            - SET FOREIGN_KEY_CHECKS=1        |  enterprise_core_db  |
                            - SET UNIQUE_CHECKS=1             |                      |
                                                              +----------------------+
                                                                         ||
                                                                         \/
                                                              +----------------------+
                                                              |   InnoDB Engine      |
                                                              +----------------------+
```

1. **Pre-flight Database Initialization:** Creates the database schema automatically with `CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci` and optional purge (`DROP DATABASE IF EXISTS`).
2. **Buffer Expansion:** Calls the native client with `--max_allowed_packet=128M` to prevent connection drops on large multi-row `INSERT` statements.
3. **Safe Descriptor Handshake:** Detaches and closes `stdin` safely prior to process communication, avoiding `ValueError: flush of closed file` errors and handling `BrokenPipeError` gracefully to surface real database server diagnostics.

---

## ⚙️ Configuration Reference

| Field | Default Value | Description |
|---|---|---|
| **SQL Source File** | *Empty* | Absolute path to the `.sql` backup file to import. |
| **Target Database** | `enterprise_core_db` | Name of the database schema to create or overwrite. |
| **MySQL Binary** | *Auto-detected* | Custom path to the `mysql` binary if running outside standard directories. |
| **Host / Port** | `127.0.0.1:3306` | TCP connection settings (prevents Unix socket file mismatch). |
| **User / Password** | `root` / *Empty* | Database authentication credentials. |
| **Drop If Exists** | `Checked` | Drops the schema prior to recreation to prevent collision from partial imports. |
| **Bypass Foreign Keys** | `Checked` | Overrides relational constraint checks during the import session. |

---

## 📄 License

This project is open-source software licensed under the [MIT License](LICENSE).