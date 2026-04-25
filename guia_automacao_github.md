# Guia de Automação de Upload para o GitHub

Este guia irá te ajudar a usar o script `upload_to_github.py` para enviar seus arquivos (`app_matriz_calor.py`, `app_pilares.py`, `requirements.txt`) diretamente para o seu repositório no GitHub (`LarissaSantanajdsp/Mapa_alunos_CALOR`).

## Pré-requisitos
1.  **Python Instalado:** Certifique-se de ter o Python 3 instalado em seu computador.
2.  **Biblioteca `requests`:** O script utiliza a biblioteca `requests`. Se você não a tiver, instale com `pip install requests`.
3.  **Arquivos do Aplicativo:** Tenha os arquivos `app_matriz_calor.py`, `app_pilares.py` e `requirements.txt` na **mesma pasta** onde você salvará o script `upload_to_github.py`.

## Passo 1: Gere seu Personal Access Token (PAT) no GitHub

Para que o script possa acessar e modificar seu repositório, ele precisa de um token de segurança. Siga estes passos com atenção:

1.  **Acesse as Configurações do GitHub:**
    *   Faça login no [GitHub](https://github.com/).
    *   Clique na sua foto de perfil (canto superior direito) e selecione `Settings`.

2.  **Navegue até Tokens:**
    *   No menu lateral esquerdo, clique em `Developer settings`.
    *   Em `Personal access tokens`, clique em `Tokens (classic)`.

3.  **Gere um Novo Token:**
    *   Clique em `Generate new token` > `Generate new token (classic)`.
    *   **Note:** Guarde este token em um local seguro, pois ele só será exibido uma vez!

4.  **Configure o Token:**
    *   **Note:** Dê um nome descritivo (ex: `upload-streamlit-app`).
    *   **Expiration:** Escolha um período de expiração (ex: 30 dias, 90 dias ou `No expiration` se for usar com frequência).
    *   **Select scopes:** Marque as seguintes permissões (scopes):
        *   `repo` (todas as sub-opções, incluindo `public_repo`)
        *   `workflow`
    *   Clique em `Generate token`.

5.  **Copie o Token:** O GitHub exibirá o token gerado. **COPIE-O IMEDIATAMENTE!** Você não conseguirá vê-lo novamente.

## Passo 2: Salve o Script e os Arquivos

1.  **Baixe o script `upload_to_github.py`** (que será fornecido a você).
2.  **Baixe os arquivos do aplicativo:** `app_matriz_calor.py`, `app_pilares.py` e `requirements.txt`.
3.  **Coloque todos esses 4 arquivos na mesma pasta** em seu computador.

## Passo 3: Execute o Script

1.  **Abra o Terminal/Prompt de Comando:**
    *   Navegue até a pasta onde você salvou os arquivos (use o comando `cd`).
2.  **Execute o script:**
    *   Digite `python upload_to_github.py` e pressione Enter.
3.  **Insira seu PAT:**
    *   O script pedirá: `Por favor, insira seu Personal Access Token (PAT) do GitHub: `.
    *   Cole o token que você copiou no Passo 1 e pressione Enter.

## O que o Script Fará

*   Ele verificará se os arquivos `app_matriz_calor.py`, `app_pilares.py` e `requirements.txt` existem localmente.
*   Ele fará o upload ou atualizará esses arquivos diretamente na raiz do seu repositório `LarissaSantanajdsp/Mapa_alunos_CALOR`.
*   Você verá mensagens de sucesso ou erro no terminal.

Após a execução bem-sucedida do script, seus arquivos estarão no GitHub, e você poderá tentar o deploy no Streamlit Cloud novamente, seguindo as instruções do `guia_deploy_streamlit.md` que já te forneci. Lembre-se de que os arquivos devem estar na raiz do repositório no GitHub!
