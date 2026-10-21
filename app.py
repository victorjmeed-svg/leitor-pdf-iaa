import streamlit as st
from PyPDF2 import PdfReader
from google import genai

st.set_page_config(page_title="Leitor Inteligente de PDFs", page_icon="📚", layout="centered")

st.title("📚 Leitor Inteligente de PDFs com IA")
st.write("Faça upload de um documento em PDF e faça perguntas sobre o conteúdo dele!")

# Sidebar para inserção da Chave da API
with st.sidebar:
    st.header("Configurações")
    api_key = st.text_input("Cole sua Google Gemini API Key:", type="password")
    st.markdown("[Obtenha sua API Key aqui](https://aistudio.google.com/)")

# Upload do arquivo PDF
uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

def extract_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

if uploaded_file and api_key:
    # Extrair texto do PDF
    with st.spinner("Lendo e processando o PDF..."):
        pdf_text = extract_pdf_text(uploaded_file)
    
    st.success("PDF processado com sucesso!")

    # Campo de pergunta
    question = st.text_input("O que você gostaria de saber sobre este documento?")

    if question:
        with st.spinner("Analisando o documento e gerando resposta..."):
            try:
                # Inicializa o cliente do Gemini
                client = genai.Client(api_key=api_key)
                
                # Monta o prompt combinando o contexto do PDF e a pergunta
                prompt = f"""
                Você é um assistente especialista em análise de documentos.
                Responda à pergunta do usuário utilizando ESTRITAMENTE o contexto do documento fornecido abaixo.
                Se a resposta não estiver presente no contexto, informe educadamente que o documento não contém essa informação.

                ---
                CONTEXTO DO DOCUMENTO:
                {pdf_text[:30000]}  # Limite preventivo para o tamanho do contexto
                ---

                PERGUNTA DO USUÁRIO:
                {question}
                """

                # Executa a chamada à API do Gemini
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                st.subheader("Resposta:")
                st.write(response.text)

            except Exception as e:
                st.error(f"Ocorreu um erro ao consultar o Gemini: {e}")

elif uploaded_file and not api_key:
    st.warning("Por favor, insira sua Google Gemini API Key na barra lateral para continuar.")
