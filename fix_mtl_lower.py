# fix_all_lower.py
# 1) Renomeia TODAS as pastas e arquivos para minúsculo (com passo temporário para forçar no Windows)
# 2) Corrige referências em .MTL (map_*) e .OBJ (mtllib/usemtl) para minúsculo
# 3) Avisa se houver colisões (arquivos iguais ignorando maiúsculas)

import os
import re
from collections import defaultdict

ROOT = "."  # rode na raiz do repo

# --------------------------
# Util: renomear com salto tmp (funciona no Windows/NTFS)
# --------------------------
def force_rename(old_path, new_path):
    if old_path == new_path:
        return False
    tmp = new_path + ".tmp_casefix"
    # garante pasta destino
    os.makedirs(os.path.dirname(new_path), exist_ok=True)
    os.rename(old_path, tmp)
    os.rename(tmp, new_path)
    return True

# --------------------------
# 0) Detectar colisões (case-insensitive)
# --------------------------
def detect_collisions(start):
    seen = defaultdict(list)
    for dp, dns, fns in os.walk(start):
        for n in dns + fns:
            k = os.path.join(dp, n).lower()
            seen[k].append(os.path.join(dp, n))
    collisions = [paths for paths in seen.values() if len(paths) > 1]
    return collisions

collisions = detect_collisions(ROOT)
if collisions:
    print("WARNING: Encontradas colisões de nome (diferem só por maiúsculas/minúsculas).")
    for group in collisions:
        for p in group:
            print("  -", p)
    print("Resolva manualmente antes de continuar.\n")

# --------------------------
# 1) Renomear diretórios e arquivos para minúsculo (bottom-up)
# --------------------------
renamed_dirs = 0
renamed_files = 0

for dirpath, dirnames, filenames in os.walk(ROOT, topdown=False):
    # Diretórios
    for name in dirnames:
        old_path = os.path.join(dirpath, name)
        new_path = os.path.join(dirpath, name.lower())
        if os.path.exists(old_path) and old_path != new_path:
            if force_rename(old_path, new_path):
                renamed_dirs += 1
                print(f"Renamed DIR : {old_path} -> {new_path}")

    # Arquivos
    for name in filenames:
        old_path = os.path.join(dirpath, name)
        new_path = os.path.join(dirpath, name.lower())
        if os.path.exists(old_path) and old_path != new_path:
            if force_rename(old_path, new_path):
                renamed_files += 1
                print(f"Renamed FILE: {old_path} -> {new_path}")

print(f"\nResumo renomeação: {renamed_dirs} pastas, {renamed_files} arquivos.\n")

# --------------------------
# 2) Corrigir .MTL (map_* e nomes de material newmtl) e .OBJ (mtllib/usemtl)
#    - Para map_* com opções, tornamos minúsculo APENAS o último token (arquivo)
#    - Para mtllib com múltiplos arquivos, tornamos todos minúsculos
# --------------------------
MTL_KEYS = ("map_Kd","map_Ka","map_Bump","map_bump","bump","map_d","map_Ns","map_Ks","map_Ke","map_Pr","map_Pm","map_Ps","disp","decal","refl")
changed_count_mtl = 0
changed_count_obj = 0
changed_count_newmtl = 0
changed_count_usemtl = 0
changed_files = []

def fix_mtl(path):
    global changed_count_mtl, changed_count_newmtl
    changed = False
    out = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.rstrip("\n")
            s = line.strip()

            # newmtl <name>  -> forçamos minúsculo
            m_new = re.match(r'^(newmtl)\s+(.+)$', s)
            if m_new:
                k, name = m_new.groups()
                ln = name.lower()
                if name != ln:
                    line = f"{k} {ln}"
                    changed = True
                    changed_count_newmtl += 1
                out.append(line + "\n")
                continue

            # map_* (com ou sem opções). Tornar minúsculo o último token (arquivo)
            if any(s.startswith(k) for k in MTL_KEYS):
                parts = line.split()
                if len(parts) >= 2:
                    # último token = arquivo
                    last = parts[-1]
                    last_l = last.lower()
                    if last != last_l:
                        parts[-1] = last_l
                        line = " ".join(parts)
                        changed = True
                        changed_count_mtl += 1
                out.append(line + "\n")
                continue

            out.append(raw)
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(out)
        changed_files.append(path)
        print(f"Fixed MTL : {path}")

def fix_obj(path):
    global changed_count_obj, changed_count_usemtl
    changed = False
    out = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.rstrip("\n")
            s = line.strip()

            # mtllib pode ter múltiplos arquivos: mtllib a.mtl b.mtl
            m_lib = re.match(r'^(mtllib)\s+(.+)$', s)
            if m_lib:
                k, rest = m_lib.groups()
                files = rest.split()
                files_l = [x.lower() for x in files]
                if files != files_l:
                    line = f"{k} " + " ".join(files_l)
                    changed = True
                    changed_count_obj += 1
                out.append(line + "\n")
                continue

            # usemtl <name>  -> forçar minúsculo
            m_use = re.match(r'^(usemtl)\s+(.+)$', s)
            if m_use:
                k, name = m_use.groups()
                ln = name.lower()
                if name != ln:
                    line = f"{k} {ln}"
                    changed = True
                    changed_count_usemtl += 1
                out.append(line + "\n")
                continue

            out.append(raw)
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(out)
        changed_files.append(path)
        print(f"Fixed OBJ : {path}")

for dp, _, fs in os.walk(ROOT):
    for n in fs:
        p = os.path.join(dp, n)
        nl = n.lower()
        if nl.endswith(".mtl"):
            fix_mtl(p)
        elif nl.endswith(".obj"):
            fix_obj(p)

print("\nResumo refs corrigidas:")
print(f" - MTL map_*  : {changed_count_mtl}")
print(f" - MTL newmtl : {changed_count_newmtl}")
print(f" - OBJ mtllib : {changed_count_obj}")
print(f" - OBJ usemtl : {changed_count_usemtl}")
print(f"Arquivos alterados: {len(changed_files)}")
