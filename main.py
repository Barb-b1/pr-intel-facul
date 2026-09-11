import streamlit as st
import feedparser
from google import genai

st.set_page_config(page_title="PR Intel Louveira", page_icon="🗞️")
st.title("🗞️ PR Intel - Louveira")

API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

def buscar():
    url = "https://news.google.com/rss/search?q=Louveira&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return feed.entries[:5]

if st.button("🔍 Analisar agora", type="primary"):
    noticias = buscar()
    texto = "\n".join([e.title for e in noticias])
    
    # MODELO QUE FUNCIONA DE PRIMEIRA
    prompt = f"Analise: {texto}. Para cada noticia, diga POSITIVA/NEGATIVA/NEUTRA em 1 linha."
    
    try:
        r = client.models.generate_content(
            model="gemini-2.0-flash-lite", # esse é o mais leve e nunca lota
            contents=prompt
        )
        st.success("Funcionou de primeira!")
        st.write(r.text)
        for n in noticias:
            st.write(f"- {n.title}")
    except Exception as e:
        st.error(f"Erro: {e}")
        st.info("Tenta de novo em 10 seg")
