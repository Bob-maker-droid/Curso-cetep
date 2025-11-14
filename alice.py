from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time
from duckduckgo_search import DDGS  # 🔍 Adicionado

app = Flask(__name__)
CORS(app)

# =======================
# CONTEXTO E HISTÓRICO
# =======================
contexto_usuario = {}
historico_usuario = {}
ultima_interacao = {}

# =======================
# SAUDAÇÕES
# =======================
SAUDACOES = {
    "bom dia": ["bom dia", "manhã"],
    "boa tarde": ["boa tarde", "tarde"],
    "boa noite": ["boa noite", "noite"],
    "geral": ["oi", "olá", "eae", "opa", "hey", "salve", "fala", "iae"]
}

RESPOSTAS_SAUDACOES = {
    "bom dia": [
        "Bom diaaa 🌞! Preparado pro dia?",
        "Bom dia! Já tomou seu cafézinho? ☕",
        "Dia novo, novas ideias 🌱"
    ],
    "boa tarde": [
        "Boa tarde 🌇! Como tá o ritmo do dia?",
        "E aí, boa tarde! Já fez uma pausa?",
        "Boa tarde 😄 espero que o dia esteja tranquilo!"
    ],
    "boa noite": [
        "Boa noite 🌙! Hora de desacelerar, né?",
        "Opa, boa noite 😴 como foi o dia?",
        "Noite boa é com boa conversa ✨"
    ],
    "geral": [
        "Oi 😄 tudo certo por aí?",
        "Eae! Como tá indo o dia?",
        "Opa, fala comigo 😎",
        "Olá! Pronto(a) pra conversar?"
    ]
}

# =======================
# INTENÇÕES E RESPOSTAS
# =======================
INTENCOES = {
    "musica": ["música", "rock", "pop", "rap", "mpb", "sertanejo", "banda", "cantor"],
    "filme": ["filme", "cinema", "ator", "atriz", "série", "netflix"],
    "comida": ["comida", "fome", "pizza", "hamburguer", "lanche", "restaurante"],
    "tempo": ["tempo", "frio", "calor", "chuva", "sol", "clima"],
    "humor": ["feliz", "triste", "cansado", "animado", "entediado"],
    "jogo": ["jogo", "videogame", "game", "jogar", "steam"],
    "agroecologia": ["agroecologia", "meio ambiente", "sustentável", "plantio", "agricultura"],
    "edificacoes": ["edificações", "engenharia", "construção", "obra"],
    "informatica": ["informática", "computador", "programação", "tecnologia"],
    "nutricao": ["nutrição", "alimento", "dieta", "saúde"],
    "quimica": ["química", "laboratório", "substância", "análise"]
}

RESPOSTAS_TEMAS = {
    "musica": [
        "Música é uma das melhores companhias, né? 🎶",
        "Nada como uma boa playlist pra mudar o clima 😌",
        "Tem algum estilo que você curte mais?"
    ],
    "filme": [
        "Filmes são tipo portais pra outros mundos 🎬",
        "Gosta mais de ação, comédia ou ficção?",
        "Eu sou fã dos que têm um bom plot twist 👀"
    ],
    "comida": [
        "Comida boa é alegria em forma de prato 🍲",
        "Se pudesse escolher agora, o que pediria?",
        "Adoro quando o cheiro da comida já entrega que tá bom 😋"
    ],
    "tempo": [
        "O tempo anda meio doido, né? 🌦️",
        "Prefere dias frios ou quentes?",
        "Nada como chuva pra dar vontade de cochilar ☔"
    ],
    "humor": [
        "Como tá o humor hoje? 😌",
        "Acontece, tem dias que o astral muda.",
        "Importante é tentar manter a calma ✨"
    ],
    "jogo": [
        "Jogos são uma boa fuga da rotina 🎮",
        "Gosta mais de história ou competição?",
        "Eu curto games com narrativa forte 😎"
    ],
    "agroecologia": [
        "🌱 Agroecologia é incrível — une natureza, técnica e consciência.",
        "Ensina sobre plantio orgânico e equilíbrio com o meio ambiente 🍃",
        "É uma área que cresce com foco em sustentabilidade 🌎"
    ],
    "edificacoes": [
        "🏗️ Edificações forma quem dá vida às construções.",
        "Do papel à obra — tudo passa pelo técnico em edificações!",
        "Um curso com muita prática e boas oportunidades no mercado."
    ],
    "informatica": [
        "💻 Informática é o coração da era digital.",
        "Entre códigos e redes, o futuro passa pelas mãos desses técnicos 😎",
        "Dá pra criar sites, sistemas e até jogos!"
    ],
    "nutricao": [
        "🥗 Nutrição é cuidar da saúde de um jeito saboroso!",
        "É sobre refeições equilibradas e bem planejadas 💚",
        "Um curso que une ciência e cuidado com as pessoas."
    ],
    "quimica": [
        "⚗️ Química é cheia de mistérios e descobertas.",
        "De cosméticos a remédios, tudo tem química no meio 🧪",
        "É um curso pra quem ama experimentar e entender o mundo."
    ]
}

RESPOSTAS_GERAIS = [
    "Entendi 👀",
    "Interessante isso!",
    "Pode crer 😌",
    "Boa observação 👏",
    "Hahaha, verdade!",
    "Sim, faz sentido!"
]

# =======================
# SUPORTE
# =======================
def detectar_saudacao(msg):
    for tipo, palavras in SAUDACOES.items():
        if any(p in msg for p in palavras):
            return tipo
    return None

def detectar_intencao(msg):
    for tema, palavras in INTENCOES.items():
        if any(p in msg for p in palavras):
            return tema
    return None

def atualizar_historico(usuario_id, msg):
    historico = historico_usuario.get(usuario_id, [])
    historico.append(msg)
    historico_usuario[usuario_id] = historico[-5:]
    ultima_interacao[usuario_id] = time.time()

def tempo_desde_ultima_msg(usuario_id):
    if usuario_id not in ultima_interacao:
        return None
    return time.time() - ultima_interacao[usuario_id]

# =======================
# NOVA FUNÇÃO DE PESQUISA
# =======================
def pesquisar_online(termo):
    """Busca resultados no DuckDuckGo e retorna o primeiro resultado em texto."""
    try:
        with DDGS() as ddgs:
            resultados = ddgs.text(termo, max_results=1)
            for r in resultados:
                return r["body"]
        return None
    except Exception as e:
        return f"Não consegui pesquisar agora 😅 (erro: {e})"

# =======================
# SISTEMA DE RESPOSTAS
# =======================
def responder(mensagem, usuario_id):
    msg = mensagem.lower().strip()
    atualizar_historico(usuario_id, msg)

    # Caso o usuário peça pra pesquisar algo
    if msg.startswith("pesquise") or msg.startswith("procure"):
        termo = msg.replace("pesquise", "").replace("procure", "").strip()
        if termo:
            resultado = pesquisar_online(termo)
            if resultado:
                return f"Pesquisei sobre **{termo}** e achei isso: {resultado}"
            else:
                return f"Não achei nada sobre **{termo}** 😅"
        else:
            return "Você quer que eu pesquise sobre o quê exatamente?"

    # Saudação
    saudacao = detectar_saudacao(msg)
    if saudacao:
        return random.choice(RESPOSTAS_SAUDACOES[saudacao])

    # Intenção
    intencao = detectar_intencao(msg)
    ultimo_tema = contexto_usuario.get(usuario_id)

    pausa = tempo_desde_ultima_msg(usuario_id)
    if pausa and pausa > 120:
        return "Achei que você tinha sumido 😅 tava por aqui te esperando."

    if intencao:
        contexto_usuario[usuario_id] = intencao
        return random.choice(RESPOSTAS_TEMAS.get(intencao, RESPOSTAS_GERAIS))
    elif ultimo_tema:
        if random.random() > 0.6:
            return f"Ainda pensando em {ultimo_tema}? 😄 {random.choice(RESPOSTAS_GERAIS)}"
        else:
            return random.choice(RESPOSTAS_TEMAS.get(ultimo_tema, RESPOSTAS_GERAIS))
    else:
        return random.choice(RESPOSTAS_GERAIS)

# =======================
# FLASK ROTA
# =======================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "")
    usuario_id = data.get("user_id", "default")

    resposta = responder(user_message, usuario_id)
    return jsonify({"response": resposta})

# =======================
# EXECUÇÃO
# =======================
if __name__ == "__main__":
    app.run(debug=True)
