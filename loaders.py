## Carregadores de arquivo

import os
from time import sleep
import streamlit as st
from langchain_community.document_loaders import (WebBaseLoader,
                                                  YoutubeLoader,
                                                  WikipediaLoader,
                                                  CSVLoader,
                                                  PyMuPDFLoader, ## Testar esse ou PyPDFLoader
                                                  TextLoader) 
                                                  # Avaliar: excel
                                                  
                                                  
from fake_useragent import UserAgent

## Carregador de sites

def carregador_site(url):
    """
    Carrega um site via WebBaseLoader e retorna o conteúdo
    em forma de string. Se houver erro, tenta novamente
    5 vezes com um intervalo de 3 segundos entre as tentativas.
    Se ao final não for possível carregar o site, retorna
    uma mensagem de erro e para a execução do código.
    """
    
    documento = ''
    for i in range(5):
        try:
            os.environ['USER_AGENT'] = UserAgent().random
            loader = WebBaseLoader(url, raise_for_status=True)
            lista_documentos = loader.load()
            documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
            break
        except:
            print(f'Erro ao carregar o site {i+1}')
            sleep(3)
    if documento == '':
        st.error('Não foi possível carregar o site')
        st.stop()
    return documento

def carregador_youtube(video_id): ## Necessário tratar a URL para extrair o ID do video
    """
    Carrega um vídeo do YouTube via YoutubeLoader e retorna o conteúdo
    em forma de string. O parâmetro video_id deve ser o ID do vídeo (não
    a URL completa). O idioma padrão é o português (pt).

    Args:
        video_id (str): O ID do vídeo do YouTube.

    Returns:
        str: O conteúdo do vídeo em forma de string.
    """
    loader = YoutubeLoader(video_id, add_video_info=False, language='pt') ## Necessário esclarecer o idioma na interface
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento

def carregador_pdf(caminho):
    """
    Carrega um PDF via PyMuPDFLoader e retorna o conteúdo
    em forma de string.

    Args:
        caminho (str): O caminho do arquivo PDF a ser carregado.

    Returns:
        str: O conteúdo do PDF em forma de string.
    """
    print(caminho)
    loader = PyMuPDFLoader(caminho)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento

def carregador_texto(caminho):
    """
    Carrega um arquivo de texto via TextLoader e retorna o conteúdo
    em forma de string.

    Args:
        caminho (str): O caminho do arquivo de texto a ser carregado.

    Returns:
        str: O conteúdo do arquivo de texto em forma de string.
    """
    loader = TextLoader(caminho)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento

def carregador_wikipedia(query, language): ## Testar
    """
    Carrega artigos da Wikipedia com base em uma consulta e idioma especificados,
    retornando o conteúdo em forma de lista.

    Args:
        query (str): A consulta de pesquisa para buscar artigos na Wikipedia.
        language (str): O idioma em que os artigos devem ser carregados.

    Returns:
        list: Uma lista contendo o conteúdo dos artigos carregados.
    """
    loader = WikipediaLoader(query, lang=language, load_max_docs=5)
    documento = list(loader.load())
    return documento

def carregador_csv(caminho):
    """
    Carrega um arquivo CSV via CSVLoader e retorna o conteúdo
    em forma de string.

    Args:
        caminho (str): O caminho do arquivo CSV a ser carregado.

    Returns:
        str: O conteúdo do arquivo CSV em forma de string.
    """
    loader = CSVLoader(caminho)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento

def criar_retriever(documento):
    pass