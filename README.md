# Projeto de IA Generativa Local para FHEMIG

Este projeto tem como objetivo implementar uma solução de **Inteligência Artificial Generativa** local, capaz de processar documentos internos (PDF, XLSX, DOCX) e responder a perguntas baseadas nesses arquivos, utilizando o modelo **Llama 3.2:1b**. A solução visa garantir conformidade com a **LGPD** e proporcionar uma interface segura e intuitiva para os usuários da FHEMIG.

## Funcionalidades

- **Upload de documentos**: Suporte para arquivos **PDF**, **XLSX** e **DOCX**.
- **Termos e condições de uso ético e responsável.**
- **Processamento de linguagem natural**: Respostas geradas a partir dos documentos fornecidos pelo usuário.
- **Interface interativa**: Desenvolvida em **Streamlit**, com integração completa com o modelo **Llama 3.2:1b**.
- **Conformidade com LGPD**: Todos os dados processados localmente, sem envio para servidores externos.

## Requisitos

Para rodar este projeto, certifique-se de que você tenha as seguintes ferramentas instaladas:

- **Python 3.8+**
- **Git** (para controle de versão)

### Bibliotecas Necessárias

As seguintes bibliotecas Python são necessárias para executar o projeto. Para instalá-las, utilize o comando:

```bash
pip install streamlit transformers langchain llama-cpp-python faiss-cpu PyMuPDF openpyxl python-docx

Principais Bibliotecas:

	•	Streamlit: Para a criação da interface web.
	•	Transformers: Para carregamento e inferência do modelo Llama.
	•	LangChain: Para implementação de RAG (Recuperação e Geração).
	•	llama-cpp-python: Implementação local do modelo Llama 3.2:1b.
	•	FAISS: Indexação eficiente para busca em documentos.
	•	PyMuPDF: Leitura e processamento de PDFs.
	•	openpyxl: Processamento de planilhas Excel.
	•	python-docx: Manipulação de arquivos Word.

Configuração

1. Clone o Repositório

git clone https://github.com/seuusuario/fhemig-ia-generativa.git
cd fhemig-ia-generativa

2. Crie e Ative o Ambiente Virtual

python3 -m venv fhemig_ia_env
source fhemig_ia_env/bin/activate

3. Instale as Dependências

pip install -r requirements.txt

4. Execute a Aplicação

Para iniciar a aplicação, use o comando abaixo:

streamlit run app.py

A aplicação será iniciada em seu navegador padrão.

Estrutura do Projeto

.
├── app.py               # Arquivo principal da aplicação em Streamlit
├── README.md            # Documentação do projeto
├── requirements.txt     # Lista de dependências
└── models/              # Diretório onde o modelo Llama será armazenado

Utilização

	1.	Carregue Documentos: Faça upload de arquivos PDF, XLSX ou DOCX.
	2.	Digite Perguntas: Insira perguntas relacionadas ao conteúdo dos documentos carregados.
	3.	Receba Respostas: A aplicação processará a pergunta e fornecerá uma resposta com base nos documentos enviados.

Conformidade com LGPD

Todo o processamento de dados é feito localmente, garantindo que as informações sensíveis não sejam compartilhadas com terceiros. A aplicação implementa mecanismos de segurança para proteger os dados pessoais, em conformidade com a Lei Geral de Proteção de Dados (LGPD).

Roadmap

	•	V1.0: Implementação inicial com suporte a PDF, XLSX e DOCX.
	•	V2.0: Integração com ferramentas de busca mais eficientes (FAISS) e melhoria na gestão de documentos.
	•	V3.0: Adicionar suporte para múltiplos usuários e gerenciamento de histórico de conversas.

Contribuição

Contribuições são bem-vindas! Para contribuir:

	1.	Faça um fork do projeto.
	2.	Crie uma nova branch (git checkout -b feature/nova-funcionalidade).
	3.	Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade').
	4.	Envie para o branch principal (git push origin feature/nova-funcionalidade).
	5.	Abra um Pull Request.

Licença

Este projeto é licenciado sob os termos da licença MIT. Consulte o arquivo LICENSE para mais informações.

Esse `README.md` inclui informações sobre o objetivo do projeto, suas funcionalidades, instruções de configuração, execução e como contribuir. Você pode ajustá-lo de acordo com a evolução do projeto e a estrutura de diretórios.