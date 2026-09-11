import streamlit as st
import feedparser
import os
from google import genai

st.set_page_config(page_title="PR Intel Louveira", page_icon="🗞️")
st.title("🗞️ PR Intel - Louveira")

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
    prompt = f"Resuma essas noticias sobre Louveira e diga se sao POSITIVA/NEGATIVA/NEUTRA:\n{texto}"
    # Modelo que o Google pediu no seu erro
    r = client.models.generate_content(model="gemini-flash-latest", contents=prompt)
    return r.text

if st.button("🔍 Analisar notícias agora"):
    noticias = buscar()
    st.write(f"{len(noticias)} notícias encontradas")
    for n in noticias:
        st.write(f"- {n['titulo']}")
    st.subheader("🤖 Análise")
    st.write(analisar(noticias))
