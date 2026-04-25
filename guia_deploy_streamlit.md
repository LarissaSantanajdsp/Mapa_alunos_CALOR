# Guia de Deploy no Streamlit Cloud

Este guia irá te ajudar a publicar seu aplicativo de avaliação de comunicação no Streamlit Cloud em poucos passos, de forma gratuita e permanente.

## Pré-requisitos
1.  Uma conta no [GitHub](https://github.com/).
2.  Uma conta no [Streamlit Cloud](https://share.streamlit.io/).

## Passo 1: Prepare seu Repositório no GitHub

1.  **Crie um Novo Repositório:**
    *   Acesse o GitHub e clique em `New` para criar um novo repositório.
    *   Dê um nome ao repositório (ex: `ferramentas-comunicacao`).
    *   Escolha `Public` (público) para que o Streamlit Cloud possa acessá-lo.
    *   Marque a opção `Add a README file`.
    *   Clique em `Create repository`.

2.  **Faça Upload dos Arquivos:**
    *   No seu novo repositório, clique em `Add file` > `Upload files`.
    *   Arraste e solte os seguintes arquivos do pacote ZIP que você baixou:
        *   `app_unified.py` (Este é o arquivo principal do seu aplicativo unificado)
        *   `requirements_simplified.txt` (Este arquivo informa ao Streamlit quais bibliotecas instalar)
    *   Clique em `Commit changes` para salvar os arquivos.

## Passo 2: Faça o Deploy no Streamlit Cloud

1.  **Acesse o Streamlit Cloud:**
    *   Vá para [share.streamlit.io](https://share.streamlit.io/) e faça login com sua conta do GitHub.

2.  **Crie um Novo Aplicativo:**
    *   Clique em `New app`.
    *   **Repository:** Selecione o repositório que você acabou de criar (ex: `seu-usuario/ferramentas-comunicacao`).
    *   **Main file path:** Digite `app_unified.py` (este é o nome do arquivo principal do seu aplicativo).
    *   **Python version:** Deixe como `Default`.
    *   **Advanced settings:** Clique para expandir.
        *   **Python requirements file:** Digite `requirements_simplified.txt` (este é o nome do seu arquivo de requisitos simplificado).
    *   Clique em `Deploy!`.

## Passo 3: Acesse e Use seu Aplicativo!

*   O Streamlit Cloud levará alguns minutos para instalar as dependências e iniciar seu aplicativo.
*   Assim que estiver pronto, você verá seu aplicativo funcionando e receberá um link permanente (ex: `https://seu-usuario-ferramentas-comunicacao.streamlit.app/`).
*   **Salve este link!** Ele será o endereço do seu site para sempre.

## Dicas Importantes
*   **Edição:** Para fazer alterações no seu aplicativo, basta editar o arquivo `app_unified.py` (ou `requirements_simplified.txt`) diretamente no GitHub. O Streamlit Cloud detectará as mudanças e atualizará seu aplicativo automaticamente em segundos.
*   **Dados:** Os dados que você inserir no aplicativo serão salvos automaticamente em arquivos `data_matriz_calor.json` e `data_pilares.json` no servidor do Streamlit. Se você quiser fazer backup, use os botões de download no próprio aplicativo.

Se tiver qualquer dúvida ou encontrar alguma dificuldade, não hesite em me perguntar!
