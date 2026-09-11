import streamlit as st
import feedparser
import os
import time
from google import genai

st.set_page_config(page_title="PR Intel Louveira", page_icon="🗞️")
st.title("🗞️ PR Intel - Louveira")
st.write("Monitoramento com IA Gemini")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = st.secrets["GOOGLE_API_KEY"]

client = genai.Client(api_key=API_KEY)

def buscar():
    url = "https://news.google.com/rss/search?q=Louveira&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return [{"titulo": e.title, "link": e.link} for e in feed.entries[:5]]

def analisar(noticias):
    texto = "\n".join([f"{n['titulo']}" for n in noticias])
    prompt = f"Resuma essas 5 noticias sobre Louveira em 1 frase cada e diga se e POSITIVA/NEGATIVA/NEUTRA. No final faca um Resumo Geral:\n{texto}"
    
    # Lista de modelos pra tentar, do mais leve pro mais pesado
    modelos = [
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash-lite", 
        "gemini-2.0-flash",
        "gemini-2.5-flash",
        "gemini-flash-latest"
    ]
    
    for modelo in modelos:
        try:
            r = client.models.generate_content(model=modelo, contents=prompt)
            return f"✅ Modelo usado: {modelo}\n\n{r.text}"
        except Exception as e:
            # se deu 503 de lotado, tenta o próximo
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                time.sleep(1)
                continue
            else:
                continue
    raise Exception("Todos os modelos lotados, tenta em 2 minutos")

if st.button("🔍 Analisar notícias agora"):
    with st.spinner("Buscando notícias..."):
        noticias = buscar()
    st.success(f"{len(noticias)} notícias encontradas!")
    for n in noticias:
        st.write(f"- [{n['titulo']}]({n['link']})")
    
    with st.spinner("Analisando com IA (trocando de modelo se lotar)..."):
        try:
            res = analisar(noticias)
            st.subheader("🤖 Análise da IA")
            st.markdown(res)
            st.balloons()
        except Exception as e:
            st.error(f"Google lotado agora: {e}")
            st.info("Clica no botão de novo em 1 minuto, é normal lotar")
else:
    st.info("Clique no botão acima para começar")
