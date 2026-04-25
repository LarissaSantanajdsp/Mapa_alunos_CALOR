# Guia Rápido: Como Publicar Seu Aplicativo Streamlit no Streamlit Cloud

Este guia irá te ajudar a publicar seus aplicativos Streamlit (`app_matriz_calor.py` e `app_pilares.py`) gratuitamente no Streamlit Cloud, tornando-os acessíveis a qualquer momento e de qualquer lugar.

## Pré-requisitos

1.  **Conta GitHub:** Você precisará de uma conta no GitHub para armazenar o código do seu aplicativo. Se não tiver, crie uma em [github.com](https://github.com/).
2.  **Conta Streamlit Cloud:** Crie uma conta gratuita em [share.streamlit.io](https://share.streamlit.io/). Você pode usar sua conta GitHub para fazer login.

## Passo a Passo

### Passo 1: Crie um Repositório no GitHub

1.  Faça login no seu GitHub.
2.  Clique no sinal de `+` no canto superior direito e selecione `New repository`.
3.  Dê um nome ao seu repositório (ex: `meus-apps-streamlit`).
4.  Defina-o como `Public` (para que o Streamlit Cloud possa acessá-lo).
5.  Marque a opção `Add a README file`.
6.  Clique em `Create repository`.

### Passo 2: Faça Upload dos Arquivos para o GitHub

Você precisará fazer upload dos seguintes arquivos para o repositório que acabou de criar:

*   `app_matriz_calor.py`
*   `app_pilares.py`
*   `requirements.txt`

1.  No seu repositório GitHub, clique em `Add file` e depois em `Upload files`.
2.  Arraste e solte os três arquivos (`app_matriz_calor.py`, `app_pilares.py`, `requirements.txt`) para a área indicada.
3.  Role para baixo e clique em `Commit changes`.

### Passo 3: Faça o Deploy no Streamlit Cloud

1.  Faça login no [share.streamlit.io](https://share.streamlit.io/).
2.  No seu painel, clique em `New app`.
3.  Selecione `Deploy from GitHub`.
4.  Conecte sua conta GitHub (se ainda não estiver conectada).
5.  Preencha os detalhes do seu aplicativo:
    *   **Repository:** Selecione o repositório que você criou (ex: `seu-usuario/meus-apps-streamlit`).
    *   **Branch:** Geralmente `main` ou `master`.
    *   **Main file path:** Este é o nome do arquivo principal do seu aplicativo. Para o aplicativo da Matriz Calor vs. Competência, digite `app_matriz_calor.py`. Para o aplicativo de Avaliação por Pilares, você fará um deploy separado e digitará `app_pilares.py`.
    *   **App URL:** Será gerado automaticamente (ex: `seu-usuario-meus-apps-streamlit-app-matriz-calor.streamlit.app`).
6.  Clique em `Deploy!`.

O Streamlit Cloud levará alguns minutos para instalar as dependências e iniciar seu aplicativo. Uma vez pronto, ele estará online e você receberá um link permanente!

### Passo 4: Faça o Deploy do Segundo Aplicativo (Opcional)

Se você quiser ter ambos os aplicativos (Matriz Calor vs. Competência e Avaliação por Pilares) online, repita o **Passo 3** para o segundo aplicativo, mas no campo `Main file path`, digite `app_pilares.py`.

## Dicas Importantes

*   **Atualizações:** Sempre que você fizer alterações no código dos seus arquivos (`.py`) no GitHub e fizer um `commit`, o Streamlit Cloud detectará automaticamente e atualizará seu aplicativo online.
*   **Dados Persistentes:** O Streamlit Cloud não armazena dados persistentes por padrão. Se você precisar que os dados sejam salvos entre as sessões, precisará integrar uma solução de banco de dados (como SQLite, PostgreSQL, etc.) ao seu aplicativo. No entanto, para o uso atual, o salvamento em arquivo local (`.json`) é suficiente para a sessão, mas não para persistência entre reinícios do servidor do Streamlit Cloud.

Com este guia, você terá seus aplicativos funcionando de forma robusta e acessível!
