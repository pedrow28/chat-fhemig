import tempfile
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain ## corrigir
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS 
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings ## Testar
from loaders import *

## TODO Avaliar criação de retriever, custo do tempo 
## TODO Adicionar botão para apagar conversa
## TODO criar abas: agente de análise de dados
## TODO pensar nome
## TODO limpar templates nao utilizados
## Escolher embedding mais leve

# CONFIGURAÇÕES INICIAIS

TIPOS_ARQUIVOS_VALIDOS = ['PDF', 'CSV', 'Texto', 'Site', 'Vídeo do YouTube', 'Wikipedia']

CONFIG_MODELOS = "llama3.2:1b"

MEMORIA = ConversationBufferMemory()


## Carregamento de arquivos

def carrega_arquivos(tipo_arquivo, arquivo):
    print(f"TIPO E ARQUIVO: {tipo_arquivo}, {arquivo}")
    if tipo_arquivo == 'Site':
        documento = carregador_site(arquivo)
    if tipo_arquivo == 'Vídeo do YouTube':
        documento = carregador_youtube(arquivo)
    if tipo_arquivo == 'Wikipedia':
        documento = carregador_wikipedia(arquivo)
    if tipo_arquivo == 'PDF':
        print(arquivo)
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
            print(nome_temp)
        documento = carregador_pdf(nome_temp)
    if tipo_arquivo == 'CSV':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carregador_csv(nome_temp)
    if tipo_arquivo == 'Texto':
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carregador_texto(nome_temp)
    return documento



## Chain

def carrega_modelo(tipo_arquivo, arquivo):

    """
    Carrega um modelo de IA e o configura para ser usado com a interface.

    Args:
        tipo_arquivo (str): O tipo de arquivo a ser carregado.
        arquivo (bytes): O conteúdo do arquivo a ser carregado.

    Returns:
        None
    """

    chat = ChatOllama(model=CONFIG_MODELOS)

    memoria = ConversationBufferMemory()

    ## Load documentos

    documento = carrega_arquivos(tipo_arquivo, arquivo)

    ## Text splitter

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap= 200)

    splits = text_splitter.split_documents(documento)

    ## Vector Store

    vectorsore = FAISS.from_documents(documents=splits, embedding=OllamaEmbeddings(model="nomic-embed-text:latest"))

    ## Retriever

    retriever = vectorsore.as_retriever()

    system_prompt = """
            Você é um assistente especializado da Fundação Hospitalar do Estado de Minas Gerais (FHEMIG), projetado para dar suporte aos servidores da instituição.

            INSTRUÇÕES PRINCIPAIS:
            1. Forneça respostas precisas e profissionais baseadas nos documentos fornecidos
            2. Mantenha um tom cordial e respeitoso
            3. Se não tiver certeza sobre alguma informação, indique claramente
            4. Priorize a clareza e objetividade nas respostas
                                                
            HISTÓRICO:
            {history}

            CONTEXTO FORNECIDO:
            {context}

            DÚVIDA/SOLICITAÇÃO DO SERVIDOR:
            {input}

            DIRETRIZES DE RESPOSTA:
            - Baseie suas respostas apenas no contexto fornecido e conhecimentos gerais sobre administração pública
            - Caso a pergunta esteja fora do escopo dos documentos, indique isso ao usuário
            - Sempre que possível, cite a seção específica do documento que fundamenta sua resposta
            - Se necessitar de informações adicionais para uma resposta completa, solicite-as ao usuário

            """
    
    prompt =  ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", "{input}")
        ]
        )  ## Trocar contexto para retriever

    question_aswner_chain = create_stuff_documents_chain(chat, prompt)
    rag_chain = create_retrieval_chain(retriever, question_aswner_chain)

    #rag_chain = create_retrieval_chain()

    system_message = '''Você é um assistente amigável chamado Oráculo.
    Você possui acesso às seguintes informações vindas 
    de um documento {}: 

    ####
    {}
    ####

    Utilize as informações fornecidas para basear as suas respostas.

    Sempre que houver $ na sua saída, substita por S.

    Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue" 
    sugira ao usuário carregar novamente o Oráculo!'''.format(tipo_arquivo, documento)

    

    template_2 = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])

    chain_2 = template_2 | chat

    st.session_state['chain'] = rag_chain



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
    st.header('BOT', divider=True)

    st.markdown(
        """
        # Bem vindo ao BOT

        """
    )

    chain = st.session_state.get('chain')
    if chain is None:
        st.error('Carrege o BOT')
        st.stop()

    memoria = st.session_state.get('memoria', MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    input_usuario = st.chat_input('Fale com o BOT')
    if input_usuario:
        chat = st.chat_message('human')
        chat.markdown(input_usuario)
        chat = st.chat_message('ai')
        resposta = chat.write_stream(chain.stream({
            'input': input_usuario
            }))
       
        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria


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

        if st.button('Inicializar Oráculo', use_container_width=True):
            carrega_modelo(tipo_arquivo, arquivo)
        if st.button('Apagar Histórico de Conversa', use_container_width=True):
            st.session_state['memoria'] = MEMORIA

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