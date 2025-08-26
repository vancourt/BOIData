import os

root = "."  # raiz do repositório

def process_file(path):
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
        print(f"Fixed: {path}")

for dirpath, _, filenames in os.walk(root):
    for name in filenames:
        if name.lower().endswith(".mtl"):
            process_file(os.path.join(dirpath, name))
