
import requests
import base64
import json
import os

# --- Configurações do GitHub --- #
GITHUB_USERNAME = "LarissaSantanajdsp" # Seu nome de usuário do GitHub
REPOSITORY_NAME = "Mapa_alunos_CALOR" # Nome do seu repositório

# --- Arquivos a serem enviados --- #
FILES_TO_UPLOAD = [
    "app_matriz_calor.py",
    "app_pilares.py",
    "requirements.txt"
]

# --- Função para obter o SHA de um arquivo existente (se houver) --- #
def get_file_sha(file_path, token):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPOSITORY_NAME}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["sha"]
    return None

# --- Função para fazer o upload/atualização do arquivo --- #
def upload_file_to_github(file_path, content, token, sha=None):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPOSITORY_NAME}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Codificar o conteúdo do arquivo em base64
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    
    data = {
        "message": f"Atualiza {file_path}" if sha else f"Adiciona {file_path}",
        "content": encoded_content
    }
    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=headers, data=json.dumps(data))
    
    if response.status_code in [200, 201]:
        print(f"✅ Arquivo {file_path} enviado/atualizado com sucesso!")
        return True
    else:
        print(f"❌ Erro ao enviar {file_path}: {response.status_code} - {response.json()}")
        return False

# --- Main --- #
if __name__ == "__main__":
    print("\n--- Automatizando Upload para o GitHub ---")
    print("Certifique-se de ter um Personal Access Token (PAT) com permissões de 'repo' e 'workflow'.")
    github_token = input("Por favor, insira seu Personal Access Token (PAT) do GitHub: ")

    # Verificar se os arquivos existem localmente
    for file_name in FILES_TO_UPLOAD:
        if not os.path.exists(file_name):
            print(f"❌ Erro: Arquivo {file_name} não encontrado no diretório atual.")
            print("Certifique-se de que os arquivos app_matriz_calor.py, app_pilares.py e requirements.txt estão na mesma pasta do script.")
            exit()

    # Ler o conteúdo dos arquivos
    file_contents = {}
    for file_name in FILES_TO_UPLOAD:
        with open(file_name, "r", encoding="utf-8") as f:
            file_contents[file_name] = f.read()

    # Fazer o upload de cada arquivo
    all_successful = True
    for file_name in FILES_TO_UPLOAD:
        print(f"Processando {file_name}...")
        existing_sha = get_file_sha(file_name, github_token)
        if not upload_file_to_github(file_name, file_contents[file_name], github_token, existing_sha):
            all_successful = False
            break

    if all_successful:
        print("\n🎉 Todos os arquivos foram enviados/atualizados com sucesso no GitHub!")
        print(f"Você pode verificar seu repositório aqui: https://github.com/{GITHUB_USERNAME}/{REPOSITORY_NAME}")
        print("Agora você pode tentar o deploy no Streamlit Cloud novamente.")
    else:
        print("\n❌ Ocorreu um erro durante o upload. Verifique as mensagens acima.")

