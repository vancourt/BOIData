import os
import shutil

# Configurações
SOURCE_DIR = '.'  # Diretório atual
TARGET_DIR = 'missing_files_for_upload'  # Pasta para os arquivos faltantes
MISSING_LIST = 'missing_files.txt'  # Lista de arquivos faltantes

def organize_missing_files():
    # Criar pasta de destino
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR, exist_ok=True)

    # Ler lista de arquivos faltantes
    with open(MISSING_LIST, 'r', encoding='utf-8') as f:
        missing_files = [line.strip() for line in f.readlines()]

    # Copiar arquivos para a nova pasta
    count = 0
    for file_path in missing_files:
        if not os.path.exists(file_path):
            continue

        destination = os.path.join(TARGET_DIR, file_path)
        os.makedirs(os.path.dirname(destination), exist_ok=True)

        shutil.copy2(file_path, destination)
        count += 1

        # Exibir progresso a cada 100 arquivos
        if count % 100 == 0:
            print(f"Copiados {count} arquivos...")

    print(f"\nTudo pronto! {count} arquivos foram organizados em:")
    print(os.path.abspath(TARGET_DIR))

if __name__ == "__main__":
    organize_missing_files()