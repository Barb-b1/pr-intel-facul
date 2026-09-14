import streamlit as st
import feedparser
from google import genai

st.set_page_config(page_title="PR-Intel | Louveira", page_icon="📊", layout="wide")
st.title("📊 PR-Intel | Louveira")

# pega a chave dos Secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def analisar(noticias):
    texto = "\n".join([n.title for n in noticias])
    prompt = f"Analise a imagem da Prefeitura de Louveira. Classifique cada notícia como POSITIVA, NEGATIVA ou NEUTRA e faça um resumo de risco:\n{texto}"
    r = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return r.text

if st.button("🔍 Buscar Notícias Agora"):
    url = "https://news.google.com/rss/search?q=Louveira&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    noticias = feed.entries[:10]
    
    st.success("PRONTO! Análise finalizada!")
    st.balloons()
    
    res = analisar(noticias)
    st.subheader("🤖 Análise de Imagem")
    st.write(res)
    
    st.subheader("📰 Últimas Notícias")
    for n in noticias:
        st.write(f"**{n.title}**")
        st.markdown(f"[Ler matéria completa]({n.link})")
        st.write("---")
