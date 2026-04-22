import os
import base64
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ─── Conteúdo dos documentos embutidos ────────────────────────────────────────

CONTEUDO_DOCX = """
1. Casos de Emergência (Risco Imediato)
Polícia Militar – Ligue 190
Quando usar: Quando a violência estiver acontecendo no momento, tiver acabado de acontecer, ou se houver risco iminente à vida da mulher.
Forma de atendimento: Atendimento telefônico 24 horas. O operador despacha uma viatura policial imediatamente para o local da ocorrência para interromper a violência, prender o agressor (em flagrante) e garantir a segurança da vítima.

2. Denúncias, Orientações e Informações
Central de Atendimento à Mulher – Ligue 180
Quando usar: Para buscar informações sobre direitos, serviços locais ou para fazer uma denúncia (inclusive de forma anônima e por terceiros).
Forma de atendimento: Serviço telefônico gratuito, nacional e 24 horas (também disponível via WhatsApp pelo número +55 61 99611-0100).

3. Atendimento Policial e Medidas Protetivas
Delegacias Especializadas de Atendimento à Mulher (DEAM)
Quando usar: Para registrar oficialmente o crime e dar andamento ao processo legal contra o agressor.
Forma de atendimento: A DEAM registra o Boletim de Ocorrência (B.O.), colhe depoimentos, encaminha a vítima para o exame de corpo de delito no IML e solicita ao juiz as Medidas Protetivas de Urgência.
Obs: Nas cidades onde não existe uma DEAM, qualquer delegacia comum é obrigada a registrar o B.O. e solicitar medidas protetivas.

Delegacias Virtuais
Quando usar: Para crimes que não exigem exame de corpo de delito imediato (ameaça, injúria, calúnia, difamação, violência psicológica e patrimonial).
Forma de atendimento: Registro do B.O. feito pela internet. Tem a mesma validade legal que o presencial.

4. Atendimento de Saúde
Hospitais e Unidades Básicas de Saúde (SUS)
Quando usar: Em casos de lesões físicas ou violência sexual.
Forma de atendimento: Em caso de violência sexual, os hospitais oferecem profilaxia contra ISTs e HIV, pílula do dia seguinte, e realizam o aborto previsto em lei. Atendimento sigiloso com suporte médico e psicológico.

5. Atendimento Integrado e Acolhimento
Casa da Mulher Brasileira
Forma de atendimento: Em um único local, a mulher encontra delegacia, juizado, Ministério Público, Defensoria Pública, apoio psicológico, assistência social e alojamento de passagem.

Centros de Referência de Atendimento à Mulher (CRAMs / CEAMs)
Forma de atendimento: Atendimento psicológico, assistência social, acompanhamento interdisciplinar e orientação jurídica gratuita.

6. Assistência Jurídica
Defensoria Pública e Ministério Público (Promotorias da Mulher)
Forma de atendimento: A Defensoria Pública atua como advogada gratuita. O Ministério Público atua na defesa dos direitos da mulher e na acusação criminal contra o agressor.

7. Aplicativos e Botão do Pânico
Aplicativos Estaduais (ex: SOS Mulher, Salve Maria, Maria da Penha Virtual)
Forma de atendimento: Em caso de quebra da medida protetiva pelo agressor, ela aciona o botão do pânico, que envia localização GPS diretamente para a central da polícia.

CANAIS ESPECÍFICOS EM SALVADOR/BAHIA:

Delegacia Virtual
Site: www.delegaciavirtual.sinesp.gov.br

Tribunal de Justiça da Bahia (TJ-BA) – Assistente Virtual Judi
WhatsApp: (71) 99978-4768

CRAM Loreta Valadares (Salvador)
Endereço: Praça Almirante Coelho Neto, nº 1, Barris (em frente à Delegacia do Idoso).
Horário: 8h às 18h. Telefone: (71) 3235-4268.

Núcleo de Defesa da Mulher – Nudem (Defensoria Pública da Bahia)
Endereço: Rua Arquimedes Gonçalves, Jardim Baiano, 3º andar, Edifício Multicab Empresarial.
Horário: 7h às 16h (senha até 15h30). Telefone: (71) 3324-1587.

Grupo de Atuação Especial em Defesa da Mulher – Gedem (MP-BA)
Endereço: Rua Arquimedes Gonçalves, nº 142, Jardim Baiano.
Horário: 8h às 12h e 14h às 18h. Telefone: (71) 3321-1949.

DEAM Salvador – Engenho Velho de Brotas
Endereço: Rua Padre Luiz Filgueiras, s/n.
Telefones: (71) 3116-7000 / 7001 / 7002 / 7003 / 7004.

DEAM Salvador – Periperi
Endereço: Rua Dr. José de Almeida, s/n.
Telefone: (71) 3117-8203.

Coordenadoria Estadual das Mulheres em Situação de Violência (TJ-BA)
Endereço: 5ª Avenida do Centro Administrativo da Bahia, nº 560, 3º andar, sala 303.
Telefones: (71) 3372-1867 / 1895.

TamoJuntas (ONG)
Assessoria jurídica, psicológica, social e pedagógica gratuita.
Endereço: Rua da Mangueira, nº 73, Nazaré, Salvador.
Contato: (71) 99185-4691.
"""

CONTEUDO_PDF = """
CANAIS E FORMAS DE ATENDIMENTO À MULHER EM SITUAÇÃO DE VIOLÊNCIA - SALVADOR/BA

PRIORIDADE 1 – RISCO IMEDIATO
- Ligue 190 (Polícia Militar): atendimento 24h para emergências.
- Ligue 180: orientação, denúncia e encaminhamento.
- WhatsApp Zap Respeita as Mina: apoio e orientação.

PRIORIDADE 2 – ATENDIMENTO DE SAÚDE
- Hospital da Mulher (Serviço AME): atendimento 24h para vítimas de violência sexual.

PRIORIDADE 3 – DENÚNCIA E PROTEÇÃO LEGAL
- DEAM: registro de ocorrência e medidas protetivas.
- Casa da Mulher Brasileira: atendimento integrado com polícia, justiça e apoio psicossocial.

PRIORIDADE 4 – APOIO CONTÍNUO
- CAMSID: atendimento psicológico e social.
- CREAM: apoio jurídico, psicológico e social.
- CRAM: orientação e acolhimento especializado.

PRIORIDADE 5 – ATENDIMENTO ONLINE
- Delegacia Online: registro de ocorrência pela internet.
- SAC: serviços presenciais e agendamentos.
"""

BASE_CONHECIMENTO = CONTEUDO_DOCX + "\n\n" + CONTEUDO_PDF

# ─── Equipe do projeto — EDITE AQUI ──────────────────────────────────────────
ORIENTADORA  = "Prof.ª Rosa Virgínia da Silva Oliveira"
DISCIPLINA   = "Marketing Jurídico e Posicionamento Digital"
SEMESTRE     = "4º Semestre – 2026.1"
CURSO        = "Direito – UNIFTC"

INTEGRANTES = [
    "👑 Solene Silva dos Santos (Líder)",
    "⭐ Hellen Victoria Dumont dos Santos (Vice-líder)",
    "Jeovana Isabela Cunha Reis",
    "Lavínia Caroline Goes Santos de Jesus",
    "Abraão Mendes Pinheiro",
    "Itainá Vitoria Gomes de Souza",
    "Ester Aieska Araújo de Jesus",
    "Jonatas Figueiredo da Silva",
    "Nathalia Farias Nascimento",
    "Elisangela Santos Souza",
    "Vinicius Motta de Santana",
]

# ─── Helper base64 ────────────────────────────────────────────────────────────
def img_to_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ─── Config da página ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JusConnect – Você não está sozinha",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #f0f4ff !important;
    }

    .header-bar {
        background: linear-gradient(135deg, #1B3A8C 0%, #0d2260 100%);
        border-radius: 16px;
        padding: 18px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.1rem;
        box-shadow: 0 4px 20px rgba(27,58,140,0.3);
    }
    .header-title { color: #ffffff; font-size: 1.35rem; font-weight: 700; margin: 0; }
    .header-sub   { color: #C8A030; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.06em; margin-top: 3px; }
    .logo-img     { height: 54px; object-fit: contain; border-radius: 6px; background: #fff; padding: 4px; }

    .aviso-emergencia {
        background: linear-gradient(90deg, #7b0000 0%, #b71c1c 100%);
        border-radius: 10px;
        padding: 11px 18px;
        margin-bottom: 0.9rem;
        color: #fff;
        font-size: 0.88rem;
        font-weight: 700;
        text-align: center;
        box-shadow: 0 2px 12px rgba(183,28,28,0.35);
        letter-spacing: 0.02em;
    }

    .subtitulo {
        text-align: center;
        color: #1B3A8C;
        font-size: 0.91rem;
        margin-bottom: 1rem;
        line-height: 1.7;
        background: #e8eeff;
        border-radius: 10px;
        padding: 12px 20px;
        border-left: 4px solid #C8A030;
    }

    .card-equipe {
        background: #ffffff;
        border-radius: 14px;
        padding: 18px 22px;
        border: 1px solid #dde3f5;
        box-shadow: 0 2px 12px rgba(27,58,140,0.08);
        margin-bottom: 1rem;
    }
    .card-equipe h4 {
        color: #1B3A8C;
        font-size: 0.92rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        padding-bottom: 6px;
        border-bottom: 2px solid #C8A030;
    }
    .card-equipe .meta { color: #555; font-size: 0.8rem; margin-bottom: 6px; }
    .badge {
        display: inline-block;
        background: #eef1fb;
        color: #1B3A8C;
        font-size: 0.78rem;
        font-weight: 600;
        border-radius: 20px;
        padding: 4px 12px;
        margin: 3px 3px 0 0;
        border: 1px solid #c5cef5;
    }

    [data-testid="stChatMessageContent"] { border-radius: 12px !important; }

    .rodape {
        text-align: center;
        color: #8a96b8;
        font-size: 0.71rem;
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid #dde3f5;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B3A8C 0%, #0d2260 100%) !important;
    }
    section[data-testid="stSidebar"] * { color: #e8eeff !important; }
    section[data-testid="stSidebar"] .stButton>button {
        background: #C8A030 !important;
        color: #1B3A8C !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        border: none !important;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header com logos ─────────────────────────────────────────────────────────
ASSETS = os.path.join(os.path.dirname(__file__), "assets")
b64_jus = img_to_b64(os.path.join(ASSETS, "logo_jusconnect.jpeg"))
b64_uni = img_to_b64(os.path.join(ASSETS, "logo_uniftc.jpeg"))

st.markdown(f"""
<div class="header-bar">
    <img src="data:image/jpeg;base64,{b64_jus}" class="logo-img" alt="JusConnect">
    <div style="text-align:center; flex:1; padding: 0 14px;">
        <div class="header-title">⚖️ JusConnect</div>
        <div class="header-sub">INFORMAÇÕES JURÍDICAS · CANAIS DE ATENDIMENTO · SALVADOR/BA</div>
    </div>
    <img src="data:image/jpeg;base64,{b64_uni}" class="logo-img" alt="UNIFTC">
</div>
""", unsafe_allow_html=True)

# ─── Aviso emergência ─────────────────────────────────────────────────────────
st.markdown("""
<div class="aviso-emergencia">
    🚨 EM PERIGO AGORA? &nbsp;|&nbsp; <strong>190</strong> Polícia &nbsp;·&nbsp; <strong>180</strong> Central da Mulher &nbsp;|&nbsp; 24h · Gratuito · Sigiloso
</div>
""", unsafe_allow_html=True)

# ─── Subtítulo ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="subtitulo">
    Este espaço é <strong>seguro e confidencial</strong>. Pergunte sobre seus direitos,
    onde buscar ajuda e os canais de atendimento em Salvador e na Bahia.<br>
    <strong>💙 Você não está sozinha.</strong>
</div>
""", unsafe_allow_html=True)

# ─── Card da equipe ───────────────────────────────────────────────────────────
badges = "".join(f'<span class="badge">👩‍⚖️ {n}</span>' for n in INTEGRANTES)

st.markdown(f"""
<div class="card-equipe">
    <h4>👩‍🎓 Equipe do Projeto</h4>
    <div class="meta">🏛️ <strong>{CURSO}</strong> &nbsp;·&nbsp; 📚 {DISCIPLINA} &nbsp;·&nbsp; 📅 {SEMESTRE}</div>
    <div class="meta">🎓 Orientação: <strong>{ORIENTADORA}</strong></div>
    <div style="margin-top:8px;">{badges}</div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
groq_api_key = st.secrets.get("GROQ_API_KEY")

with st.sidebar:
    # Logos lado a lado
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:center; gap:10px; margin-bottom:12px;">
        <img src="data:image/jpeg;base64,{b64_jus}" style="height:44px; object-fit:contain; border-radius:6px; background:#fff; padding:3px;">
        <img src="data:image/jpeg;base64,{b64_uni}" style="height:44px; object-fit:contain; border-radius:6px; background:#fff; padding:3px;">
    </div>
    <div style="text-align:center; color:#C8A030; font-size:0.75rem; font-weight:700; letter-spacing:0.06em; margin-bottom:4px;">
        JUSCONNECT · UNIFTC
    </div>
    <div style="text-align:center; color:#a0b0e0; font-size:0.72rem; margin-bottom:14px;">
        {SEMESTRE}
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Equipe
    st.markdown(f"""
    <div style="font-size:0.78rem; color:#C8A030; font-weight:700; margin-bottom:6px; letter-spacing:0.05em;">
        🎓 ORIENTAÇÃO
    </div>
    <div style="font-size:0.8rem; color:#e8eeff; margin-bottom:12px;">
        {ORIENTADORA}
    </div>
    <div style="font-size:0.78rem; color:#C8A030; font-weight:700; margin-bottom:6px; letter-spacing:0.05em;">
        📚 DISCIPLINA
    </div>
    <div style="font-size:0.8rem; color:#e8eeff; margin-bottom:12px;">
        {DISCIPLINA}
    </div>
    <div style="font-size:0.78rem; color:#C8A030; font-weight:700; margin-bottom:8px; letter-spacing:0.05em;">
        👩‍⚖️ INTEGRANTES
    </div>
    """, unsafe_allow_html=True)

    for nome in INTEGRANTES:
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.08);
            border-left: 3px solid #C8A030;
            border-radius: 0 6px 6px 0;
            padding: 5px 10px;
            margin-bottom: 5px;
            font-size: 0.8rem;
            color: #e8eeff;
        ">{nome}</div>
        """, unsafe_allow_html=True)

    st.divider()

    model = st.selectbox(
        "⚙️ Modelo de IA",
        ["llama-3.3-70b-versatile", "llama3-8b-8192", "gemma2-9b-it"],
        index=0,
    )
    if st.button("🗑️ Nova conversa"):
        st.session_state.messages = []
        st.rerun()

# ─── Estado ───────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    boas_vindas = (
        "Olá! 💙 Sou a assistente virtual do projeto **JusConnect**.\n\n"
        "Estou aqui para te orientar sobre seus direitos e os canais de atendimento "
        "disponíveis em Salvador e na Bahia. Você pode me perguntar, por exemplo:\n\n"
        "- *Onde posso registrar um Boletim de Ocorrência?*\n"
        "- *Qual o telefone da DEAM em Salvador?*\n"
        "- *O que é uma medida protetiva e como solicitar?*\n"
        "- *Existe apoio psicológico gratuito?*\n"
        "- *O que a Lei Maria da Penha garante?*\n\n"
        "Como posso te ajudar? ⚖️"
    )
    st.session_state.messages.append({"role": "assistant", "content": boas_vindas})

# ─── Histórico ────────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    avatar = "⚖️" if msg["role"] == "assistant" else "🙋"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ─── Input ────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Digite sua pergunta aqui..."):

    if not groq_api_key:
        st.error("⚠️ GROQ_API_KEY não encontrada. Verifique o arquivo .env.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🙋"):
        st.markdown(prompt)

    client = Groq(api_key=groq_api_key)

    system_prompt = f"""Você é a assistente virtual do projeto JusConnect, desenvolvido por alunas do curso de Direito da UNIFTC (Salvador/BA).

SEU PAPEL:
- Orientar mulheres em situação de violência doméstica sobre canais de atendimento, direitos e serviços disponíveis em Salvador e na Bahia.
- Usar linguagem simples, acolhedora e nunca julgadora.
- Sempre que houver risco de vida, reforçar que a pessoa ligue 190 imediatamente.
- Referenciar a Lei Maria da Penha quando relevante.

BASE DE CONHECIMENTO (use APENAS estas informações para responder):
\"\"\"
{BASE_CONHECIMENTO}
\"\"\"

REGRAS:
1. Responda SOMENTE com base nas informações acima. Se não souber, diga que não tem essa informação e sugira ligar no 180.
2. Seja acolhedora, empática, nunca fria ou excessivamente técnica.
3. Em qualquer sinal de perigo imediato, priorize: ligue 190.
4. Não faça julgamentos sobre a situação da pessoa.
5. Responda sempre em português brasileiro.
6. Seja direta e clara, mas mantenha o calor humano.
7. Ao listar contatos, apresente telefone e endereço de forma destacada."""

    messages_payload = [{"role": "system", "content": system_prompt}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner("Consultando base de conhecimento..."):
            response = client.chat.completions.create(
                model=model,
                messages=messages_payload,
                max_tokens=1024,
                temperature=0.4,
            )
            answer = response.choices[0].message.content
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# ─── Rodapé ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="rodape">
    ⚖️ <strong>JusConnect</strong> · Projeto Acadêmico · {CURSO} · {SEMESTRE}<br>
    Este serviço é informativo. Em emergências, ligue <strong>190</strong> ou <strong>180</strong>.
</div>
""", unsafe_allow_html=True)