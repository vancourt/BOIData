import os
import requests

def get_github_files_recursive():
    """Recupera recursivamente todos os arquivos do repositório GitHub"""
    base_url = "https://api.github.com/repos/vancourt/BOIData/git/trees/main?recursive=1"
    response = requests.get(base_url)

    if response.status_code != 200:
        print(f"Erro ao acessar o repositório GitHub: {response.status_code}")
        return []

    data = response.json()
    github_files = []

    for item in data['tree']:
        if item['type'] == 'blob':  # Somente arquivos, não diretórios
            github_files.append(item['path'])

    return github_files
def get_local_files():
    local_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            # Ignorar arquivos do próprio script e da lista local
            if file in ['compare_github_files.py', 'local_files.txt', 'missing_files.txt']:
                continue
            # Converter caminho relativo e usar formato Unix
            rel_path = os.path.relpath(os.path.join(root, file), '.').replace('\\', '/')
            local_files.append(rel_path)
    return local_files

def main():
    print("Obtendo lista de arquivos do GitHub...")
    github_files = get_github_files_recursive()
    print(f"Encontrados {len(github_files)} arquivos no GitHub")

    print("Obtendo lista de arquivos locais...")
    local_files = get_local_files()
    print(f"Encontrados {len(local_files)} arquivos locais")

    # Encontrar arquivos que estão no repositório local mas não no GitHub
    missing_files = [file for file in local_files if file not in github_files]

    # Salvar os arquivos faltantes em um arquivo
    with open('missing_files.txt', 'w', encoding='utf-8') as f:
        for file in missing_files:
            f.write(file + '\n')

    print(f"\n{len(missing_files)} arquivos faltando no GitHub. Lista salva em 'missing_files.txt'.")
    print("Arquivos para upload:")
    for i, file in enumerate(missing_files[:10]):
        print(f"- {file}")
    if len(missing_files) > 10:
        print(f"- ... e mais {len(missing_files) - 10} arquivos")

if __name__ == "__main__":
    main()