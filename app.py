import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Analisador de Sentimentos Offline",
    page_icon="🤖",
    layout="centered"
)

def traduzir_para_ingles(texto: str) -> str:
    """
    Traduz o texto inserido para o inglês de forma invisível usando deep-translator.
    Se falhar na tradução ou o texto estiver vazio, retorna o texto original.
    """
    if not texto.strip():
        return texto
    
    try:
        # Usamos 'auto' para detectar automaticamente o idioma e traduzir para 'en' (inglês)
        tradutor = GoogleTranslator(source='auto', target='en')
        texto_traduzido = tradutor.translate(texto)
        return texto_traduzido if texto_traduzido else texto
    except Exception as e:
        # Em caso de falha de conexão/tradução, prossegue com o texto original
        return texto

def analisar_sentimento(texto: str):
    """
    Realiza a tradução invisível (se necessário) e analisa a polaridade com TextBlob.
    Retorna a classificação (Positivo, Negativo ou Neutro) e a pontuação de polaridade.
    """
    # Traduz para o inglês para garantir maior precisão no TextBlob
    texto_processado = traduzir_para_ingles(texto)
    
    # Processa o sentimento localmente
    blob = TextBlob(texto_processado)
    polaridade = blob.sentiment.polarity  # Valor entre -1.0 e 1.0
    
    # Classificação baseada na polaridade
    if polaridade > 0.05:
        classificacao = "Positivo"
    elif polaridade < -0.05:
        classificacao = "Negativo"
    else:
        classificacao = "Neutro"
        
    return classificacao, polaridade

def main():
    # Cabeçalho da aplicação
    st.title("📊 Analisador de Sentimentos Offline")
    st.markdown(
        """
        Esta é uma versão **Offline** desenvolvida com bibliotecas tradicionais de Python 
        (**TextBlob** e **deep-translator**). Nenhum dado é enviado para APIs de IA generativa (como OpenAI ou Google Gemini); 
        todo o processamento de PLN ocorre localmente ou através de tradução automática base.
        """
    )
    
    st.divider()

    # Área de texto para entrada do usuário
    texto_usuario = st.text_area(
        "Digite seu texto abaixo (pode ser em português ou inglês):",
        placeholder="Ex: Eu adorei este aplicativo, ele é simplesmente fantástico! / I love this app!",
        height=150
    )

    # Botão de análise
    if st.button("Analisar", type="primary"):
        if not texto_usuario.strip():
            st.warning("⚠️ Por favor, digite algum texto antes de clicar em analisar.")
        else:
            with st.spinner("Analisando sentimento..."):
                sentimento, polaridade = analisar_sentimento(texto_usuario)
            
            st.subheader("Resultado da Análise:")
            
            # Exibição visual utilizando componentes apropriados do Streamlit
            if sentimento == "Positivo":
                st.success(f"**Sentimento:** Positivo 😊 (Polaridade: {polaridade:.2f})")
            elif sentimento == "Negativo":
                st.error(f"**Sentimento:** Negativo 😞 (Polaridade: {polaridade:.2f})")
            else:
                st.warning(f"**Sentimento:** Neutro 😐 (Polaridade: {polaridade:.2f})")

if __name__ == "__main__":
    main()
