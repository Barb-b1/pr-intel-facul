import feedparser
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
TERMO_BUSCA = "Louveira"

# Cliente novo do Google
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def buscar_noticias(termo):
    print(f"Buscando noticias sobre: {termo}...\n")
    url = f"https://news.google.com/rss/search?q={termo}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    noticias = []
    for entry in feed.entries[:5]:
        noticias.append({"titulo": entry.title, "link": entry.link})
    return noticias

def analisar_com_ia(noticias):
    print("Analisando com IA do Gemini 3.5...\n")
    texto = ""
    for i, n in enumerate(noticias, 1):
        texto += f"{i}. {n['titulo']} - {n['link']}\n"
    
    prompt = f"Analise essas noticias sobre '{TERMO_BUSCA}':\n{texto}\nPara cada uma: resumo de 15 palavras e sentimento POSITIVO/NEGATIVO/NEUTRO. No final resumo geral de 2 linhas."
    
    # Modelo novo que o erro pediu
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    noticias = buscar_noticias(TERMO_BUSCA)
    for n in noticias:
        print(f" - {n['titulo']}")
    print("\n" + "="*40 + "\n")
    analise = analisar_com_ia(noticias)
    print(analise)
    print("\nPRONTO! Parte 2 finalizada!")