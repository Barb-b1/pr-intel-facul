import streamlit as st
import feedparser
import os
from google import genai

st.set_page_config(page_title="PR Intel Louveira", page_icon="🗞️")
st.title("🗞️ PR Intel - Louveira")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    try:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    except:
        from dotenv import load_dotenv
        load_dotenv()
        API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)
TERMO = "Louveira"

def buscar():
    url = f"https://news.google.com/rss/search?q={TERMO}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return [{"titulo": e.title, "link": e.link} for e in feed.entries[:5]]

def analisar(noticias):
    texto = "\n".join([f"{i}. {n['titulo']} - {n['link']}" for i, n in enumerate(noticias, 1)])
    prompt = f"Analise noticias sobre '{TERMO}':\n{texto}\nPara cada: resumo 1 frase + sentimento POSITIVO/NEGATIVO/NEUTRO. Final: Resumo Geral."
    r = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return r.text

if st.button("🔍 Analisar notícias agora"):
    with st.spinner("Buscando..."):
        noticias = buscar()
    st.success(f"{len(noticias)} notícias encontradas!")
    for n in noticias:
        st.write(f"- [{n['titulo']}]({n['link']})")
    with st.spinner("Analisando com IA..."):
        res = analisar(noticias)
    st.subheader("🤖 Análise da IA")
    st.markdown(res)
else:
    st.info("Clique no botão acima para começar")
