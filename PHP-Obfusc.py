# ──────────────────────────────────────────────────────────────────────────────
#  Zeta - PHP Obfuscator Tool
#  Style   : Zeta-Obfuscator-Tool (BenzoXdev)
#  Moteur  : yakpro-po (pmdunggh fork) via subprocess PHP
#  Fallback: moteur Python natif si PHP absent
#  Deps    : colorama uniquement  (pip install colorama)
# ──────────────────────────────────────────────────────────────────────────────

import sys
import os
import re
import shutil
import logging
import datetime
import ctypes
import random
import string
import subprocess
import colorama
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor
from colorama import init
init(autoreset=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
_BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
log_filename  = 'php-obfuscator.log'
output_folder = 'PHP-Obfuscated'
github        = 'github.com/BenzoXdev'
telegram      = 't.me/benzoXdev'
instagram     = 'instagram.com/just._.amar_x1'
by            = 'BenzoXdev'

# Chemin yakpro-po (fork pmdunggh, présent dans yakpro-po/)
YAKPRO_PHP    = os.path.join(_BASE_DIR, 'yakpro-po', 'yakpro-po.php')
YAKPRO_CNF    = os.path.join(_BASE_DIR, 'yakpro-po', 'yakpro-po.cnf')

# ═══════════════════════════════════════════════════════════════════════════════
#  COULEURS & PREFIXES  (style Zeta-Obfuscator-Tool)
# ═══════════════════════════════════════════════════════════════════════════════
_c     = colorama.Fore
red    = _c.RED
white  = _c.WHITE
green  = _c.GREEN
reset  = _c.RESET

BEFORE = f'{red}[{white}'
AFTER  = f'{red}]'
INPUT  = f'{BEFORE}>{AFTER} |'
INFO   = f'{BEFORE}!{AFTER} |'
ERROR  = f'{BEFORE}x{AFTER} |'
ADD    = f'{BEFORE}+{AFTER} |'
WAIT   = f'{BEFORE}~{AFTER} |'

# ═══════════════════════════════════════════════════════════════════════════════
#  LOGGING
# ═══════════════════════════════════════════════════════════════════════════════
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def current_time_hour():
    return datetime.datetime.now().strftime('%H:%M:%S')

def ts():
    return BEFORE + current_time_hour() + AFTER

def Title(title):
    if sys.platform.startswith('win'):
        ctypes.windll.kernel32.SetConsoleTitleW(f'Zeta - PHP Obfuscator | {title}')
    else:
        sys.stdout.write(f'\033]2;Zeta - PHP Obfuscator | {title}\a')

def Clear():
    os.system('cls' if sys.platform.startswith('win') else 'clear')

# ═══════════════════════════════════════════════════════════════════════════════
#  DETECTION PHP + YAKPRO
# ═══════════════════════════════════════════════════════════════════════════════
def _check_php():
    """Vérifie que PHP est disponible dans le PATH."""
    try:
        r = subprocess.run(['php', '--version'], capture_output=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False

def _check_yakpro(path):
    """Vérifie que yakpro-po.php existe à l'emplacement donné."""
    return os.path.isfile(path)

# ═══════════════════════════════════════════════════════════════════════════════
#  SELECTION FICHIERS / DOSSIER  (tkinter + fallback manuel)
# ═══════════════════════════════════════════════════════════════════════════════
def ChoosePHPFiles():
    print(f'{ts()} {INPUT} Choisissez un ou plusieurs fichiers PHP -> {reset}')
    chosen = []
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        php_files = filedialog.askopenfilenames(
            parent=root,
            title='Zeta - PHP Obfuscator | Choisir fichier(s) PHP',
            filetypes=[('Fichiers PHP', '*.php'), ('Tous', '*.*')]
        )
        if php_files:
            chosen = list(php_files)
            for p in chosen:
                print(f'{ts()} {ADD} Fichier choisi : {white}{p}{reset}')
            return chosen
    except Exception:
        pass
    print(f'{ts()} {INFO} Aucun fichier selectionne via fenetre.')
    try:
        rep = input(f'{ts()} {INPUT} Chemin(s) (separes par virgules) -> {reset}').strip()
    except KeyboardInterrupt:
        print()
        return []
    if rep:
        chosen = [x.strip() for x in rep.split(',') if x.strip()]
        for p in chosen:
            print(f'{ts()} {ADD} Fichier saisi : {white}{p}{reset}')
    return chosen

def ChoosePHPDirectory():
    print(f'{ts()} {INPUT} Choisissez un dossier de projet PHP -> {reset}')
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        directory = filedialog.askdirectory(
            parent=root,
            title='Zeta - PHP Obfuscator | Choisir dossier PHP'
        )
        if directory:
            print(f'{ts()} {ADD} Dossier choisi : {white}{directory}{reset}')
            return directory
    except Exception:
        pass
    print(f'{ts()} {INFO} Aucun dossier selectionne via fenetre.')
    try:
        rep = input(f'{ts()} {INPUT} Chemin du dossier -> {reset}').strip()
    except KeyboardInterrupt:
        print()
        return ''
    if rep:
        print(f'{ts()} {ADD} Dossier saisi : {white}{rep}{reset}')
    return rep

# ═══════════════════════════════════════════════════════════════════════════════
#  CONFIG CNF PAR NIVEAU (yakpro-po)
# ═══════════════════════════════════════════════════════════════════════════════
def _write_level_cnf(level, cnf_path):
    """
    Génère un fichier .cnf temporaire adapté au niveau d'obfuscation.
    Basé sur la config yakpro-po.cnf du fork pmdunggh.
    """
    # Options communes à tous les niveaux
    base = {
        'parser_mode'        : "'PREFER_PHP7'",
        'scramble_mode'      : "'hexa'",
        'strip_indentation'  : 'true',
        'abort_on_error'     : 'false',
        'silent'             : 'true',
        'shuffle_stmts'      : 'false',
        'user_comment'       : 'null',
        'obfuscate_string_literal'  : 'false',
        'obfuscate_variable_name'   : 'false',
        'obfuscate_function_name'   : 'false',
        'obfuscate_class_name'      : 'false',
        'obfuscate_constant_name'   : 'false',
        'obfuscate_method_name'     : 'false',
        'obfuscate_property_name'   : 'false',
        'obfuscate_interface_name'  : 'false',
        'obfuscate_trait_name'      : 'false',
        'obfuscate_namespace_name'  : 'false',
        'obfuscate_label_name'      : 'false',
        'obfuscate_if_statement'    : 'false',
        'obfuscate_loop_statement'  : 'false',
        'scramble_length'           : '8',
    }

    # Niveau 1 — base (commentaires + indentation strip seulement)
    if level == 1:
        pass  # tout false

    # Niveau 2 — + strings + variables
    elif level == 2:
        base['obfuscate_string_literal'] = 'true'
        base['obfuscate_variable_name']  = 'true'

    # Niveau 3 — + fonctions + constantes
    elif level == 3:
        base['obfuscate_string_literal'] = 'true'
        base['obfuscate_variable_name']  = 'true'
        base['obfuscate_function_name']  = 'true'
        base['obfuscate_constant_name']  = 'true'

    # Niveau 4 — + classes + méthodes + propriétés
    elif level >= 4:
        base['obfuscate_string_literal']  = 'true'
        base['obfuscate_variable_name']   = 'true'
        base['obfuscate_function_name']   = 'true'
        base['obfuscate_constant_name']   = 'true'
        base['obfuscate_class_name']      = 'true'
        base['obfuscate_method_name']     = 'true'
        base['obfuscate_property_name']   = 'true'
        base['obfuscate_interface_name']  = 'true'
        base['obfuscate_trait_name']      = 'true'
        base['obfuscate_namespace_name']  = 'true'
        base['obfuscate_label_name']      = 'true'
        if level == 5:
            base['obfuscate_if_statement']   = 'true'
            base['obfuscate_loop_statement'] = 'true'
            base['shuffle_stmts']            = 'true'
            base['scramble_length']          = '16'

    lines = ['<?php', '// Zeta-PHP-Obfuscator generated config']
    for k, v in base.items():
        lines.append(f'$conf->{k} = {v};')
    lines.append('?>')

    with open(cnf_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# ═══════════════════════════════════════════════════════════════════════════════
#  MOTEUR YAKPRO-PO  (subprocess PHP)
# ═══════════════════════════════════════════════════════════════════════════════
def _yakpro_obfuscate_file(input_file, output_file, cnf_path, yakpro_path):
    """Lance yakpro-po sur un fichier et écrit le résultat dans output_file."""
    cmd = [
        'php', yakpro_path,
        '--config-file', cnf_path,
        input_file,
        '-o', output_file,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            err = (result.stderr or result.stdout or 'Erreur inconnue').strip()
            return False, err
        return True, None
    except subprocess.TimeoutExpired:
        return False, 'Timeout (> 60s)'
    except Exception as e:
        return False, str(e)

# ═══════════════════════════════════════════════════════════════════════════════
#  MOTEUR PYTHON NATIF (fallback — aucun PHP requis)
# ═══════════════════════════════════════════════════════════════════════════════
def _rand_var(length=8):
    first = random.choice(string.ascii_letters)
    rest  = ''.join(random.choices(string.ascii_letters + string.digits, k=length - 1))
    return first + rest

def _encode_string_octal(s):
    return ''.join(f'\\{ord(c):03o}' for c in s)

def _encode_string_hex(s):
    return ''.join(f'\\x{ord(c):02x}' for c in s)

def _strip_php_comments(code):
    result = []
    i, length = 0, len(code)
    in_single = in_double = False
    while i < length:
        c = code[i]
        if c == "'" and not in_double:
            in_single = not in_single; result.append(c); i += 1; continue
        if c == '"' and not in_single:
            in_double = not in_double; result.append(c); i += 1; continue
        if in_single or in_double:
            result.append(c); i += 1; continue
        if c == '/' and i + 1 < length and code[i + 1] == '*':
            i += 2
            while i < length - 1 and not (code[i] == '*' and code[i + 1] == '/'):
                i += 1
            i += 2; result.append(' '); continue
        if (c == '/' and i + 1 < length and code[i + 1] == '/') or c == '#':
            while i < length and code[i] != '\n':
                i += 1
            continue
        result.append(c); i += 1
    return ''.join(result)

def _compact_php_whitespace(code):
    code = re.sub(r'[ \t]+', ' ', code)
    code = re.sub(r'\n\s*\n+', '\n', code)
    return code.strip()

def _obfuscate_php_strings(code, mode='octal'):
    encode = _encode_string_octal if mode == 'octal' else _encode_string_hex
    result = []; i = 0; length = len(code); in_single = False
    while i < length:
        c = code[i]
        if c == "'" and not in_single:
            in_single = True; result.append(c); i += 1; continue
        if c == "'" and in_single:
            in_single = False; result.append(c); i += 1; continue
        if in_single:
            result.append(c); i += 1; continue
        if c == '"':
            i += 1; content = []
            while i < length:
                ch = code[i]
                if ch == '\\' and i + 1 < length:
                    content.append(ch); content.append(code[i + 1]); i += 2; continue
                if ch == '"':
                    i += 1; break
                content.append(ch); i += 1
            inner = ''.join(content)
            if '$' not in inner and len(inner) > 0:
                result.append(f'"{encode(inner)}"')
            else:
                result.append(f'"{inner}"')
            continue
        result.append(c); i += 1
    return ''.join(result)

_PHP_SUPERGLOBALS = {
    '$_GET','$_POST','$_REQUEST','$_SESSION','$_COOKIE',
    '$_SERVER','$_ENV','$_FILES','$_GLOBALS','$this','$argc','$argv',
}

def _rename_php_variables(code):
    all_vars = set(re.findall(r'\$[a-zA-Z_][a-zA-Z0-9_]*', code))
    mapping  = {v: '$_0x' + ''.join(random.choices('0123456789abcdef', k=8))
                for v in all_vars - _PHP_SUPERGLOBALS}
    for old, new in mapping.items():
        code = re.sub(re.escape(old) + r'(?=[^a-zA-Z0-9_]|$)', new, code)
    return code

def _wrap_base64_eval(code):
    import base64
    body = code.lstrip()
    tag  = '<?php\n' if body.startswith('<?php') else '<?php\n'
    body = body[5:] if body.startswith('<?php') else body
    encoded   = base64.b64encode(body.encode('utf-8')).decode('ascii')
    n, size   = 4, len(encoded)
    part_len  = max(1, (size + n - 1) // n)
    parts     = [(encoded[i * part_len:(i + 1) * part_len]) for i in range(n)]
    parts     = (parts + [''] * n)[:n]
    var_names = [_rand_var(10) for _ in range(n)]
    cv        = _rand_var(10)
    assigns   = '\n'.join(f'${v} = "{p}";' for v, p in zip(var_names, parts))
    concat    = ' . '.join(f'${v}' for v in var_names)
    return f'{tag}{assigns}\n${cv} = {concat};\neval(base64_decode(${cv}));\n'

def _native_obfuscate(code, level):
    code = _strip_php_comments(code)
    code = _compact_php_whitespace(code)
    if level >= 2:
        code = _obfuscate_php_strings(code, 'octal')
    if level >= 3:
        code = _obfuscate_php_strings(code, 'hex')
        code = _rename_php_variables(code)
    if level >= 4:
        code = _rename_php_variables(code)
    if level >= 5:
        code = _wrap_base64_eval(code)
    return code

# ═══════════════════════════════════════════════════════════════════════════════
#  OBFUSCATION D'UN FICHIER (yakpro ou fallback natif)
# ═══════════════════════════════════════════════════════════════════════════════
def obfuscate_one(input_file, output_dir, level, create_backup,
                  use_yakpro=False, yakpro_path=None, cnf_path=None):
    if not os.path.isfile(input_file):
        print(f'{ts()} {ERROR} Fichier introuvable : {white}{input_file}{reset}')
        logging.error(f'File not found: {input_file}')
        return False

    if create_backup:
        backup = f'{os.path.splitext(input_file)[0]}_backup.php'
        shutil.copy2(input_file, backup)
        print(f'{ts()} {INFO} Backup : {white}{backup}{reset}')
        logging.info(f'Backup: {backup}')

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f'obfuscated_{os.path.basename(input_file)}')

    try:
        if use_yakpro and yakpro_path and cnf_path:
            ok, err = _yakpro_obfuscate_file(input_file, out_path, cnf_path, yakpro_path)
            if not ok:
                print(f'{ts()} {ERROR} YakPro : {white}{err}{reset}')
                logging.error(f'YakPro error on {input_file}: {err}')
                return False
        else:
            with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
                code = f.read()
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(_native_obfuscate(code, level))

        print(f'{ts()} {ADD} Obfusque -> {white}{out_path}{reset}')
        logging.info(f'Obfuscated: {out_path}')
        return True
    except Exception as e:
        print(f'{ts()} {ERROR} Erreur : {white}{e}{reset}')
        logging.error(f'Error: {e}')
        return False

def process_directory(directory, output_dir, level, exclude_list, create_backup,
                      use_yakpro, yakpro_path, cnf_path, max_workers=4):
    file_list = []
    for root, _, files in os.walk(directory):
        for fname in files:
            if not fname.lower().endswith('.php'):
                continue
            fpath = os.path.join(root, fname)
            if any(os.path.commonpath([fpath, ex]) == os.path.abspath(ex) for ex in exclude_list):
                continue
            rel    = os.path.relpath(root, directory)
            target = os.path.join(output_dir, rel)
            file_list.append((fpath, target, level, create_backup, use_yakpro, yakpro_path, cnf_path))
    if not file_list:
        print(f'{ts()} {ERROR} Aucun .php trouve dans : {white}{directory}{reset}')
        return
    total = len(file_list)
    print(f'{ts()} {INFO} {total} fichier(s) PHP trouve(s). Obfuscation en cours...')
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        results = list(ex.map(lambda a: obfuscate_one(*a), file_list))
    done = sum(1 for r in results if r)
    print(f'{ts()} {ADD} {done}/{total} fichier(s) obfusque(s).')

# ═══════════════════════════════════════════════════════════════════════════════
#  BANNIERE
# ═══════════════════════════════════════════════════════════════════════════════
def show_banner(use_yakpro):
    engine = f'{red}YakPro-Po{white}' if use_yakpro else f'{red}Python Natif{white}'
    print(f'''{red}

                        ██████╗ ██╗  ██╗██████╗      ██████╗ ██████╗ ███████╗██╗   ██╗███████╗ ██████╗
                        ██╔══██╗██║  ██║██╔══██╗    ██╔═══██╗██╔══██╗██╔════╝██║   ██║██╔════╝██╔════╝
                        ██████╔╝███████║██████╔╝    ██║   ██║██████╔╝█████╗  ██║   ██║███████╗██║
                        ██╔═══╝ ██╔══██║██╔═══╝     ██║   ██║██╔══██╗██╔══╝  ██║   ██║╚════██║██║
                        ██║     ██║  ██║██║         ╚██████╔╝██████╔╝██║     ╚██████╔╝███████║╚██████╗
                        ╚═╝     ╚═╝  ╚═╝╚═╝          ╚═════╝ ╚═════╝ ╚═╝      ╚═════╝ ╚══════╝ ╚═════╝

                {white}                    PHP Obfuscator — Moteur : {engine}

                                        ╔════════════════════════════╗
                                        ║    {red}PHP Obfuscator Tool{white}     ║
                                        ╚════════════════════════════╝

{red}[{white}>{red}]{red} GitHub   : {white}{github}
{red}[{white}>{red}]{red} Telegram : {white}{telegram}
''')

# ═══════════════════════════════════════════════════════════════════════════════
#  MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
def Zeta_PHP_Obfuscator():
    # ── Détection moteur ──────────────────────────────────────────────────
    php_ok    = _check_php()
    yakpro_ok = _check_yakpro(YAKPRO_PHP)
    use_yakpro = php_ok and yakpro_ok

    Clear()
    Title(f'By: {by}')
    show_banner(use_yakpro)

    if use_yakpro:
        print(f'{ts()} {ADD} Moteur : {white}yakpro-po (PHP){reset} detecte -> {white}{YAKPRO_PHP}{reset}')
    else:
        if not php_ok:
            print(f'{ts()} {INFO} PHP non detecte — moteur Python natif utilise.')
        elif not yakpro_ok:
            print(f'{ts()} {INFO} yakpro-po.php absent — moteur Python natif utilise.')
            print(f'{ts()} {INFO} Pour activer YakPro : assurez-vous que {white}yakpro-po/yakpro-po.php{reset} existe.')

    # ── Mode ───────────────────────────────────────────────────────────────
    print(f'''
    {red}[{white}1{red}] {white}Fichier unique
    {red}[{white}2{red}] {white}Plusieurs fichiers
    {red}[{white}3{red}] {white}Dossier de projet entier
    ''')
    try:
        mode = int(input(f'{ts()} {INPUT} Mode (1/2/3) -> {reset}'))
    except (ValueError, KeyboardInterrupt):
        print(f'\n{ts()} {ERROR} Entree invalide.')
        return
    if mode not in (1, 2, 3):
        print(f'{ts()} {ERROR} Choisissez 1, 2 ou 3.')
        return

    # ── Niveau ─────────────────────────────────────────────────────────────
    if use_yakpro:
        print(f'''
    {red}[{white}1{red}] {white}Faible     — Compactage / strip commentaires
    {red}[{white}2{red}] {white}Moyen      — + Strings + Variables
    {red}[{white}3{red}] {white}Fort       — + Fonctions + Constantes
    {red}[{white}4{red}] {white}Tres Fort  — + Classes, Methodes, Proprietes, Namespaces
    {red}[{white}5{red}] {white}Extreme    — + If/Loop obfuscation + Shuffle statements
        ''')
    else:
        print(f'''
    {red}[{white}1{red}] {white}Faible     — Strip commentaires + compactage
    {red}[{white}2{red}] {white}Moyen      — + Encodage strings octal
    {red}[{white}3{red}] {white}Fort       — + Encodage strings hex + renommage variables
    {red}[{white}4{red}] {white}Tres Fort  — + Double passe renommage
    {red}[{white}5{red}] {white}Extreme    — + Wrapper base64/eval
        ''')
    try:
        level = int(input(f'{ts()} {INPUT} Niveau d\'obfuscation (1-5) -> {reset}'))
    except (ValueError, KeyboardInterrupt):
        print(f'\n{ts()} {ERROR} Entree invalide.')
        return
    if level not in (1, 2, 3, 4, 5):
        print(f'{ts()} {ERROR} Choisissez 1 a 5.')
        return

    # ── Backup ─────────────────────────────────────────────────────────────
    create_backup = False
    try:
        bk = input(f'{ts()} {INPUT} Creer des backups ? (o/n) -> {reset}').strip().lower()
        create_backup = bk in ('o', 'y', 'oui', 'yes')
    except KeyboardInterrupt:
        print()
        return

    # ── Dossier de sortie ──────────────────────────────────────────────────
    out_default = os.path.join(_BASE_DIR, output_folder)
    try:
        custom  = input(f'{ts()} {INPUT} Dossier de sortie [{white}{out_default}{red}] (ENTREE=defaut) -> {reset}').strip()
        out_dir = custom if custom else out_default
    except KeyboardInterrupt:
        print()
        return

    # ── CNF temporaire pour yakpro ─────────────────────────────────────────
    cnf_tmp = None
    if use_yakpro:
        cnf_tmp = os.path.join(_BASE_DIR, 'yakpro-po', f'_zeta_level{level}.cnf')
        _write_level_cnf(level, cnf_tmp)

    # ── Exclusions ─────────────────────────────────────────────────────────
    exclude_list = []
    if mode == 3:
        try:
            ex_raw = input(f'{ts()} {INPUT} Chemins a exclure (espace=sep, ENTREE=passer) -> {reset}').strip()
            exclude_list = [os.path.abspath(e) for e in ex_raw.split() if e]
        except KeyboardInterrupt:
            print()
            return

    # ── Selection & obfuscation ────────────────────────────────────────────
    if mode == 1:
        files = ChoosePHPFiles()
        if not files:
            print(f'{ts()} {ERROR} Aucun fichier selectionne.')
            return
        fp = files[0]
        if not fp.lower().endswith('.php'):
            print(f'{ts()} {ERROR} Pas un .php : {white}{fp}{reset}')
            return
        print(f'{ts()} {WAIT} Obfuscation : {white}{os.path.basename(fp)}{reset}..')
        obfuscate_one(fp, out_dir, level, create_backup, use_yakpro, YAKPRO_PHP, cnf_tmp)

    elif mode == 2:
        files = ChoosePHPFiles()
        if not files:
            print(f'{ts()} {ERROR} Aucun fichier selectionne.')
            return
        print(f'{ts()} {WAIT} Obfuscation de {len(files)} fichier(s)..')
        ok = sum(
            obfuscate_one(fp, out_dir, level, create_backup, use_yakpro, YAKPRO_PHP, cnf_tmp)
            for fp in files if fp.lower().endswith('.php')
        )
        print(f'{ts()} {ADD} {ok}/{len(files)} fichier(s) obfusque(s).')

    else:
        directory = ChoosePHPDirectory()
        if not directory or not os.path.isdir(directory):
            print(f'{ts()} {ERROR} Dossier invalide.')
            return
        print(f'{ts()} {WAIT} Scan du dossier..')
        process_directory(directory, out_dir, level, exclude_list, create_backup,
                          use_yakpro, YAKPRO_PHP, cnf_tmp)

    # Nettoyage CNF temporaire
    if cnf_tmp and os.path.isfile(cnf_tmp):
        try:
            os.remove(cnf_tmp)
        except Exception:
            pass

    print(f'{ts()} {INFO} Sortie : {white}{out_dir}{reset}')
    print(f'{ts()} {INFO} Log    : {white}{log_filename}{reset}')

# ═══════════════════════════════════════════════════════════════════════════════
#  POINT D'ENTREE
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    try:
        while True:
            Zeta_PHP_Obfuscator()
            try:
                input(f'{BEFORE + current_time_hour() + AFTER} {INPUT} Appuyez sur ENTREE pour continuer.. ')
            except KeyboardInterrupt:
                print()
                break
    except KeyboardInterrupt:
        print()
