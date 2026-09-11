import streamlit as st
import feedparser
import google.generativeai as genai

st.set_page_config(page_title="PR Intel Louveira", page_icon="🗞️")
st.title("🗞️ PR Intel - Louveira")

API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# modelo fixo que funciona sempre
model = genai.GenerativeModel("gemini-1.5-flash")

def buscar():
    url = "https://news.google.com/rss/search?q=Louveira&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    return feed.entries[:5]

if st.button("🔍 Analisar agora", type="primary", use_container_width=True):
    with st.spinner("Buscando e analisando... leva 5 seg"):
        noticias = buscar()
        texto = "\n".join([e.title for e in noticias])
        prompt = f"Analise essas noticias de Louveira. Para cada uma, classifique POSITIVA/NEGATIVA/NEUTRA em 1 linha:\n{texto}"
        try:
            resp = model.generate_content(prompt)
            st.success("Deu certo!")
            st.write(resp.text)
            st.divider()
            for n in noticias:
                st.write(f"- {n.title}")
        except Exception as e:
            st.error(f"Erro: {e}")
            st.info("Copia esse erro e me manda o print do Manage app > Logs")
else:
    st.info("Clique no botão para analisar")
