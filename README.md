![Zeta PHP Obfuscator](banner.png)

# Zeta - PHP Obfuscator Tool

[![License](https://img.shields.io/badge/license-MIT-red.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.6%2B-white.svg)](https://python.org)
[![By](https://img.shields.io/badge/by-BenzoXdev-red.svg)](https://github.com/BenzoXdev)

> PHP Obfuscator Tool — Powered by YakPro-Po (pmdunggh fork) with Python native fallback.  
> Style inspiré de Zeta-Obfuscator-Tool by **BenzoXdev**.

---

## Contact

| Plateforme | Lien |
|-----------|------|
| 🐙 GitHub | [github.com/BenzoXdev](https://github.com/BenzoXdev) |
| ✈️ Telegram | [t.me/benzoXdev](https://t.me/benzoXdev) |
| 📷 Instagram | [instagram.com/just._.amar_x1](https://instagram.com/just._.amar_x1) |

---

## Fonctionnalités

- 🔴 **Interface style Zeta** — ASCII art, brackets `[>]` `[!]` `[x]` rouge/blanc, horodatage
- 🖱️ **Sélection fichiers via fenêtre** — tkinter + fallback saisie manuelle
- 🔧 **Moteur hybride** :
  - ✅ **YakPro-Po** si PHP installé (moteur principal, très puissant)
  - ✅ **Python natif** si PHP absent (fallback automatique)
- 📊 **5 niveaux d'obfuscation** (Faible → Extrême)
- 📁 **3 modes** : Fichier unique, Plusieurs fichiers, Dossier entier
- 💾 **Backup automatique** optionnel
- 🔄 **Multi-threading** pour les gros projets

---

## Niveaux d'obfuscation

### Avec YakPro-Po (PHP requis)

| Niveau | Effet |
|--------|-------|
| **1 — Faible** | Strip commentaires + compactage ligne unique |
| **2 — Moyen** | + Strings + Variables |
| **3 — Fort** | + Fonctions + Constantes |
| **4 — Très Fort** | + Classes, Méthodes, Propriétés, Namespaces |
| **5 — Extrême** | + If/Loop obfuscation + Shuffle statements |

### Avec moteur Python natif (fallback)

| Niveau | Effet |
|--------|-------|
| **1 — Faible** | Strip commentaires + compactage |
| **2 — Moyen** | + Encodage strings octal (`\110\145\154`) |
| **3 — Fort** | + Encodage strings hex (`\x48\x65\x6c`) + renommage vars `$_0x...` |
| **4 — Très Fort** | + Double passe renommage variables |
| **5 — Extrême** | + Wrapper `base64_decode` / `eval` |

---

## Installation

### 1. Installer Python 3.6+

```
https://python.org
```

### 2. Installer la dépendance Python

```bash
pip install -r requirements.txt
```

### 3. (Optionnel) Activer YakPro-Po

Cloner PHP-Parser dans `yakpro-po/` (déjà inclus si cloné correctement) :

```bash
cd yakpro-po
git clone https://github.com/nikic/PHP-Parser.git
```

Puis installer PHP CLI :
- **Windows :** [windows.php.net](https://windows.php.net/download/)
- **Ubuntu :** `sudo apt install php-cli`

---

## Structure du dossier

```
Zeta-PHP-Obfuscator/
├── Zeta-PHP-Obfuscator.py   ← Script principal
├── yakpro-po/               ← YakPro-Po (fork pmdunggh)
│   ├── yakpro-po.php
│   ├── PHP-Parser/
│   └── yakpro-po.cnf
├── requirements.txt
├── banner.png
├── README.md
└── README.txt
```

---

## Utilisation

```bash
python Zeta-PHP-Obfuscator.py
```

Suivre les menus interactifs :
1. Choisir le mode (fichier / plusieurs / dossier)
2. Choisir le niveau d'obfuscation (1-5)
3. Choisir les fichiers via la fenêtre de sélection
4. Récupérer les fichiers obfusqués dans `PHP-Obfuscated/`

---

## Avant / Après

**Avant :**
```php
<?php
// Connexion à la base de données
$host = "localhost";
$user = "admin";
$pass = "secret123";

function connect($host, $user, $pass) {
    return new PDO("mysql:host=$host", $user, $pass);
}
```

**Après (niveau 3) :**
```php
<?php $h="\x6c\x6f\x63\x61\x6c\x68\x6f\x73\x74"; $_0x4f3a2b1c="\x61\x64\x6d\x69\x6e"; $_0x9d2e1a3f="\x73\x65\x63\x72\x65\x74\x31\x32\x33"; function connect($_0xf1e2d3c4,$_0x7a8b9c0d,$_0x1b2c3d4e){return new PDO("mysql:host=$_0xf1e2d3c4",$_0x7a8b9c0d,$_0x1b2c3d4e);}
```

---

## License

MIT License — Libre d'utilisation et de modification.

---

*Zeta - PHP Obfuscator Tool by [BenzoXdev](https://github.com/BenzoXdev)*
