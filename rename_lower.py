import os

root = "."  # raiz do repositório

# Primeiro renomeia diretórios (de baixo para cima)
for dirpath, dirnames, filenames in os.walk(root, topdown=False):
    for name in dirnames:
        old_path = os.path.join(dirpath, name)
        new_path = os.path.join(dirpath, name.lower())
        if old_path != new_path:
            tmp_path = new_path + ".tmp_casefix"
            os.rename(old_path, tmp_path)
            os.rename(tmp_path, new_path)
            print(f"Renamed DIR: {old_path} -> {new_path}")

    # Depois arquivos
    for name in filenames:
        old_path = os.path.join(dirpath, name)
        new_path = os.path.join(dirpath, name.lower())
        if old_path != new_path:
            tmp_path = new_path + ".tmp_casefix"
            os.rename(old_path, tmp_path)
            os.rename(tmp_path, new_path)
            print(f"Renamed FILE: {old_path} -> {new_path}")
