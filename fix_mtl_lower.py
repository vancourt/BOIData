import os, re

root = "."  # raiz do repositório

def fix_mtl(path):
    changed = False
    lines = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip().startswith(("map_Kd", "map_Ka", "map_Bump", "map_d", "map_Ns")):
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    key, filename = parts
                    lower_filename = filename.strip().lower()
                    if filename.strip() != lower_filename:
                        line = f"{key} {lower_filename}\n"
                        changed = True
            lines.append(line)
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"Fixed MTL: {path}")

def fix_obj(path):
    changed = False
    out = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            s = line.strip()
            m1 = re.match(r'^(mtllib)\s+(.+)$', s)
            m2 = re.match(r'^(usemtl)\s+(.+)$', s)
            if m1:
                k, fn = m1.groups()
                lf = fn.lower()
                if fn != lf:
                    line = f"{k} {lf}\n"
                    changed = True
            elif m2:
                k, mat = m2.groups()
                lm = mat.lower()
                if mat != lm:
                    line = f"{k} {lm}\n"
                    changed = True
            out.append(line)
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(out)
        print(f"Fixed OBJ: {path}")

for dirpath, _, filenames in os.walk(root):
    for name in filenames:
        lower = name.lower()
        path = os.path.join(dirpath, name)
        if lower.endswith(".mtl"):
            fix_mtl(path)
        elif lower.endswith(".obj"):
            fix_obj(path)
