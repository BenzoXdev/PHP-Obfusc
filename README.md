![Zeta PHP Obfuscator](banner.png)

# Zeta - PHP Obfuscator Tool

[![License](https://img.shields.io/badge/license-MIT-red.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.6%2B-white.svg)](https://python.org)
[![By](https://img.shields.io/badge/by-BenzoXdev-red.svg)](https://github.com/BenzoXdev)

> PHP Obfuscator Tool — Powered by YakPro-Po (pmdunggh fork) with Python native fallback.  
> Style inspired by Zeta-Obfuscator-Tool by **BenzoXdev**.

---

## Contact

| Platform | Link |
|-----------|------|
| 🐙 GitHub | [github.com/BenzoXdev](https://github.com/BenzoXdev) |
| ✈️ Telegram | [t.me/benzoXdev](https://t.me/benzoXdev) |
| 📷 Instagram | [instagram.com/just._.amar_x1](https://instagram.com/just._.amar_x1) |

---

## Features

- 🔴 **Zeta style interface** — ASCII art, brackets `[>]` `[!]` `[x]` red/white, timestamp
- 🖱️ **File selection via window** — tkinter + manual input fallback
- 🔧 **Hybrid engine**:
  - ✅ **YakPro-Po** if PHP is installed (main engine, very powerful)
  - ✅ **Native Python** if PHP is missing (automatic fallback)
- 📊 **5 obfuscation levels** (Low → Extreme)
- 📁 **3 modes**: Single file, Multiple files, Entire folder
- 💾 **Automatic backup** (optional)
- 🔄 **Multi-threading** for large projects

---

## Obfuscation Levels

### With YakPro-Po (PHP required)

| Level | Effect |
|--------|-------|
| **1 — Low** | Strip comments + single line compacting |
| **2 — Medium** | + Strings + Variables |
| **3 — High** | + Functions + Constants |
| **4 — Very High** | + Classes, Methods, Properties, Namespaces |
| **5 — Extreme** | + If/Loop obfuscation + Shuffle statements |

### With Native Python Engine (fallback)

| Level | Effect |
|--------|-------|
| **1 — Low** | Strip comments + compacting |
| **2 — Medium** | + Octal string encoding (`\110\145\154`) |
| **3 — High** | + Hex string encoding (`\x48\x65\x6c`) + variable renaming `$_0x...` |
| **4 — Very High** | + Double pass variable renaming |
| **5 — Extreme** | + `base64_decode` / `eval` wrapper |

---

## Installation

### 1. Install Python 3.6+

```
https://python.org
```

### 2. Install Python dependency

```bash
pip install -r requirements.txt
```

### 3. (Optional) Enable YakPro-Po

Clone PHP-Parser into `yakpro-po/` (already included if cloned properly):

```bash
cd yakpro-po
git clone https://github.com/nikic/PHP-Parser.git
```

Then install PHP CLI:
- **Windows:** [windows.php.net](https://windows.php.net/download/)
- **Ubuntu:** `sudo apt install php-cli`

---

## Folder Structure

```
Zeta-PHP-Obfuscator/
├── Zeta-PHP-Obfuscator.py   ← Main script
├── yakpro-po/               ← YakPro-Po (pmdunggh fork)
│   ├── yakpro-po.php
│   ├── PHP-Parser/
│   └── yakpro-po.cnf
├── requirements.txt
├── banner.png
├── README.md
└── README.txt
```

---

## Usage

```bash
python Zeta-PHP-Obfuscator.py
```

Follow the interactive menus:
1. Choose the mode (file / multiple / folder)
2. Choose the obfuscation level (1-5)
3. Choose the files via the selection window
4. Retrieve the obfuscated files in `PHP-Obfuscated/`

---

## Before / After

**Before:**
```php
<?php
// Database connection
$host = "localhost";
$user = "admin";
$pass = "secret123";

function connect($host, $user, $pass) {
    return new PDO("mysql:host=$host", $user, $pass);
}
```

**After (level 3):**
```php
<?php $h="\x6c\x6f\x63\x61\x6c\x68\x6f\x73\x74"; $_0x4f3a2b1c="\x61\x64\x6d\x69\x6e"; $_0x9d2e1a3f="\x73\x65\x63\x72\x65\x74\x31\x32\x33"; function connect($_0xf1e2d3c4,$_0x7a8b9c0d,$_0x1b2c3d4e){return new PDO("mysql:host=$_0xf1e2d3c4",$_0x7a8b9c0d,$_0x1b2c3d4e);}
```

---

## License

MIT License — Free to use and modify.

---

*PHP Obfusc Tool by [BenzoXdev](https://github.com/BenzoXdev)*
