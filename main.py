import streamlit as st
import feedparser
import google.generativeai as genai

st.set_page_config(page_title="PR-Intel | Louveira", page_icon="📊", layout="wide")
st.title("📊 PR-Intel | Louveira")
st.write("Monitor de imagem da Prefeitura em tempo real com IA Gemini 3.6")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash-lite")

if st.button("🔍 Buscar Notícias Agora"):
    with st.spinner("Buscando..."):
        url = "https://news.google.com/rss/search?q=Louveira&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        feed = feedparser.parse(url)
        noticias = feed.entries[:10]

    st.success("PRONTO! Análise finalizada!")
    st.balloons()

    texto = "\n".join([n.title for n in noticias])
    prompt = f"Analise a imagem da Prefeitura de Louveira com base nessas notícias. Diga se cada uma é POSITIVA, NEGATIVA ou NEUTRA e faça um resumo geral de risco de imagem:\n{texto}"
    
    with st.spinner("IA analisando..."):
        resp = model.generate_content(prompt)
        st.subheader("🤖 Análise de Imagem")
        st.write(resp.text)

    st.subheader("📰 Últimas Notícias")
    for n in noticias:
        st.write(f"**{n.title}**")
        st.markdown(f"[Ler matéria completa]({n.link})")
        st.write("---")
