import tempfile
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from loaders import *

## TODO Avaliar criação de retriever, custo do tempo
## TODO Adicionar botão para apagar conversa
## TODO criar abas: agente de análise de dados
## TODO pensar nome

# CONFIGURAÇÕES INICIAIS

TIPOS_ARQUIVOS_VALIDOS = ['PDF', 'CSV', 'Texto', 'Site', 'Vídeo do YouTube', 'Wikipedia']

CONFIG_MODELOS = {"Ollama":
                  {"modelos": ["llama3.2:1b"]}}

MEMORIA = ConversationBufferMemory()

## Carregamento de arquivos



# INTERFACE

## JANELA PRINCIPAL

def pagina_chat():
    """
    Página principal da interface, onde o usuário pode conversar com a interface.

    A página carrega o estado do modelo e da memória do Oráculo do estado da sessão
    do Streamlit. 

    Em seguida, a página lista todas as mensagens trocadas entre o usuário e o Oráculo
    em forma de chat.

    O usuário pode digitar uma mensagem e enviar. A resposta
    é então mostrada na lista de mensagens.

    """
    st.header('FHacil', divider=True)

    st.markdown(
        """
        # Bem vindo ao FHacil

        """
    )

    #chain = st.session_state.get('chain')
    #if chain is None:
    #    st.error('Carrege o Oráculo')
    #    st.stop()

    memoria = st.session_state.get('memoria', MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    #input_usuario = st.chat_input('Fale com o oráculo')
    #if input_usuario:
    #    chat = st.chat_message('human')
    #    chat.markdown(input_usuario)

    #    chat = st.chat_message('ai')
    #    resposta = chat.write_stream(chain.stream({
    #        'input': input_usuario, 
    #        'chat_history': memoria.buffer_as_messages
    #        }))
        
    #    memoria.chat_memory.add_user_message(input_usuario)
    #    memoria.chat_memory.add_ai_message(resposta)
    #    st.session_state['memoria'] = memoria


## SIDEBAR
def sidebar():
    """
    Função responsável por criar a sidebar da interface.

    A sidebar é dividida em dois tabs: 'Upload de Arquivos' e 'Seleção de Modelos'.

    No tab 'Upload de Arquivos', o usuário pode selecionar o tipo de arquivo que deseja
    carregar e fazer o upload do arquivo em questão.


    """
    tabs = st.tabs(['Upload de Arquivos'])
    with tabs[0]:
        tipo_arquivo = st.selectbox('Selecione o tipo de arquivo', TIPOS_ARQUIVOS_VALIDOS)
        if tipo_arquivo == 'Site':
            arquivo = st.text_input('Digite a url do site')
        if tipo_arquivo == 'Wikipedia':
            arquivo = st.text_input('Digite o assunto do Wikipedia')
        if tipo_arquivo == 'Vídeo do YouTube':
            url = st.text_input('Digite a url do vídeo')
            arquivo = url.split('=')[-1]
            ## TODO: Necessário tratar a url para extrair o ID do video
        if tipo_arquivo == 'PDF':
            arquivo = st.file_uploader('Faça o upload do arquivo pdf', type=['.pdf'])
        if tipo_arquivo == 'CSV':
            arquivo = st.file_uploader('Faça o upload do arquivo csv', type=['.csv'])
        if tipo_arquivo == 'Texto':
            arquivo = st.file_uploader('Faça o upload do arquivo txt', type=['.txt'])

## Run
def main():
    """
    Função principal da aplicação.

    Responsável por criar a interface em Streamlit, incluindo a sidebar
    e a página de chat.

    Chama a função `sidebar` para criar a sidebar e a função `pagina_chat`
    para criar a página de chat.

    """
    with st.sidebar:
        sidebar()
    pagina_chat()


if __name__ == '__main__':
    main()