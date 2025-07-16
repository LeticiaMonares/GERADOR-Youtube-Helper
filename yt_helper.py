import textwrap
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# IA local com modelo leve e compatível
gerador = pipeline("text2text-generation", model="mrm8488/t5-base-finetuned-summarize-news")

def gerar_titulo_com_ia_local(descricao_video):
    prompt = f"Gerar um título criativo e direto para YouTube com base na frase: '{descricao_video}'"
    resultado = gerador(prompt, max_length=20, do_sample=True, temperature=0.9)
    texto = resultado[0]["generated_text"]

    # Remove repetições, quebra na primeira frase e padroniza
    primeira_frase = texto.split(".")[0].strip().upper()
    return primeira_frase

def gerar_titulo_final(titulo_ia, numero_video, nome_jogo):
    return f"{titulo_ia} | {numero_video:02d}# {nome_jogo}"

def gerar_descricao_padrao():
    return textwrap.dedent("""\
        Fazendo live lá na roxinha de segunda a sexta as 20h 💜

        https://www.twitch.tv/le_monares
        https://www.instagram.com/le_monares/
    """)

def gerar_hashtags(nome_jogo):
    nome_formatado = nome_jogo.replace(" ", "+")
    url = f"https://tiktokhashtags.com/search/?keyword={nome_formatado}"

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        tag_list = []
        for tag in soup.select("div.tag-container a")[:5]:
            tag_text = tag.text.strip()
            if tag_text.startswith("#"):
                tag_list.append(tag_text)

        if not tag_list:
            return [f"#{nome_jogo.replace(' ', '')}", "#Gameplay", "#IndieGame", "#Steam", "#GamingBrasil"]

        return tag_list

    except Exception as e:
        print(f"(erro ao buscar hashtags, usando fallback): {e}")
        return [f"#{nome_jogo.replace(' ', '')}", "#Gameplay", "#IndieGame", "#Steam", "#GamingBrasil"]

# --- Entrada manual
descricao_curta = input("📝 Descreva o vídeo em 1 frase: ")
numero_video = int(input("🔢 Número do episódio: "))
nome_jogo = input("🎮 Nome do jogo (ex: Elden Ring): ")

# --- Geração
print("\n⏳ Gerando título com IA local...")
titulo_ia = gerar_titulo_com_ia_local(descricao_curta)
titulo_final = gerar_titulo_final(titulo_ia, numero_video, nome_jogo)
descricao = gerar_descricao_padrao()
hashtags = gerar_hashtags(nome_jogo)

# --- Resultado
print("\n--- RESULTADO COPIÁVEL ---\n")
print("🎬 TÍTULO:")
print(titulo_final)

print("\n📄 DESCRIÇÃO:")
print(descricao)

print("\n🔖 HASHTAGS:")
print(" ".join(hashtags))
