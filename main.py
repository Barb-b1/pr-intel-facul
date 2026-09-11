import streamlit as st
import feedparser
import time
from google import genai

st.set_page_config(page_title="PR Intel Louveira", page_icon="🗞️")
st.title("🗞️ PR Intel - Louveira")
st.write("Monitoramento com IA Gemini")

API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

def buscar():
    url = "https://news.google.com/rss/search?q=Louveira&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return [{"titulo": e.title, "link": e.link} for e in feed.entries[:5]]

def analisar(noticias):
    texto = "\n".join([f"{n['titulo']}" for n in noticias])
    prompt = f"Resuma essas 5 noticias sobre Louveira em 1 frase cada e diga se e POSITIVA/NEGATIVA/NEUTRA. No final faca um Resumo Geral:\n{texto}"
    
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
            return f"✅ Modelo: {modelo}\n\n{r.text}"
        except:
            time.sleep(1)
            continue
    return "Tenta de novo em 1 min - Google lotado"

if st.button("🔍 Analisar notícias agora"):
    with st.spinner("Buscando notícias..."):
        noticias = buscar()
    st.success(f"{len(noticias)} notícias encontradas!")
    for n in noticias:
        st.write(f"- [{n['titulo']}]({n['link']})")
    
    with st.spinner("Analisando com IA..."):
        res = analisar(noticias)
        st.subheader("🤖 Análise")
        st.markdown(res)
        st.balloons()
