from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time
from duckduckgo_search import DDGS
import wikipedia

app = Flask(__name__)
CORS(app)

wikipedia.set_lang("pt")

# =======================
# CONTEXTO DO USUÁRIO
# =======================
ultima_interacao = {}

# =======================
# PESQUISA APRIMORADA
# =======================
def pesquisar_online(termo):
    """
    Tenta obter informações de forma limpa e objetiva:
    1) Wikipedia
    2) DuckDuckGo (texto)
    """

    # --- WIKIPEDIA ---
    try:
        resumo = wikipedia.summary(termo, sentences=4)
        if resumo:
            return resumo.strip()
    except:
        pass

    # --- DUCKDUCKGO ---
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(termo, max_results=3))

        if not resultados:
            return None

        textos = []
        for r in resultados:
            body = r.get("body")
            if body and body.strip():
                textos.append(body.strip())

        return "\n\n".join(textos) if textos else None

    except:
        return None

# =======================
# DETECÇÃO DE INTENÇÃO
# =======================
def detectar_intencao(msg):
    msg = msg.lower()

    regras = {
        "saudacao": ["oi", "ola", "olá", "bom dia", "boa tarde", "boa noite"],
        "pesquisa": ["pesquise", "procure", "me diga sobre", "o que é", "quem foi", "pesquisar"],
        "jogo": ["jogo", "game", "fase", "inimigo", "nível", "alice"],
        "duvida": ["como faz", "como faço", "o que significa", "explica"],
        "agradecimento": ["obrigado", "valeu", "tmj"]
    }

    for tipo, palavras in regras.items():
        if any(p in msg for p in palavras):
            return tipo

    return "geral"

# =======================
# RESPOSTAS DEFINITIVAS
# =======================
RESPOSTAS = {
    "saudacao": [
        "Oi! Como posso ajudar agora?",
        "Olá! O que você precisa?",
        "E aí! Pode mandar sua pergunta."
    ],

    "agradecimento": [
        "Tamo junto! Qualquer coisa só chamar.",
        "Disponha! Precisa de mais alguma coisa?",
        "Valeu! Se quiser continuar, é só falar."
    ],

    "duvida": [
        "Beleza, me explique certinho o que você quer entender.",
        "Claro, qual parte está deixando dúvida?",
        "Tranquilo, me fala o que exatamente você quer saber."
    ],

    "jogo": [
        "Seu projeto tá indo muito bem. O que quer ajustar agora?",
        "Fala do game — posso ajudar com história, gameplay ou design.",
        "Boa! Qual parte do jogo você quer melhorar?"
    ],

    "geral": [
        "Entendi. Me explica melhor o que você quer.",
        "Certo. Quer detalhar mais um pouco?",
        "Tá, continue. O que exatamente você precisa?"
    ]
}

# =======================
# SISTEMA DE RESPOSTA
# =======================
def responder(mensagem, usuario_id):
    msg_original = mensagem.strip()
    msg = msg_original.lower()

    ultima_interacao[usuario_id] = time.time()
    intencao = detectar_intencao(msg)

    # ---------- PESQUISA ----------
    if intencao == "pesquisa":
        termo = (
            msg.replace("pesquise", "")
               .replace("procure", "")
               .replace("me diga sobre", "")
               .replace("pesquisar", "")
               .replace("o que é", "")
               .replace("quem foi", "")
               .strip()
        )

        if not termo:
            return "Me diga o que você quer que eu pesquise."

        resultado = pesquisar_online(termo)

        if not resultado:
            return f"Não encontrei nada sólido sobre **{termo}**. Pode especificar melhor?"

        return resultado

    # ---------- RESPOSTAS NORMAIS ----------
    lista = RESPOSTAS.get(intencao, RESPOSTAS["geral"])
    return random.choice(lista)

# =======================
# ENDPOINT FLASK
# =======================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    mensagem = data.get("message", "")
    usuario_id = data.get("user_id", "default")

    resposta = responder(mensagem, usuario_id)
    return jsonify({"response": resposta})

# =======================
# EXECUÇÃO
# =======================
if __name__ == "__main__":
    app.run(debug=True)
