import os
import base64
import streamlit as st
import streamlit.components.v1 as components
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

# ─── Equipe do projeto ────────────────────────────────────────────────────────
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

# ─── CSS com animações profissionais ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

    /* ── Variáveis ── */
    :root {
        --azul:       #1B3A8C;
        --azul-escuro:#0d2260;
        --azul-medio: #2a4fa8;
        --dourado:    #c09e46; /* Softer gold */
        --dourado-claro: #d1b569;
        --fundo:      #FAFAF8; /* Warm off-white */
        --branco:     #ffffff;
        --texto:      #1a1a2e;
        --cinza-suave:#8a96b8;
        --teal-prot:  #2E8B82; /* Psicologia: proteção e cura */
        --lilac-suave:#5D5A88; /* Psicologia: calma e acolhimento */
    }

    /* ── Reset & Base ── */
    html, body, .stApp {
        font-family: 'DM Sans', sans-serif !important;
        background: var(--fundo) !important;
    }

    /* ── Keyframes ── */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-28px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(24px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(192,158,70,0); }
        50%       { box-shadow: 0 0 18px 4px rgba(192,158,70,0.25); }
    }
    @keyframes shimmer {
        0%   { background-position: -400px 0; }
        100% { background-position: 400px 0; }
    }
    @keyframes staggerIn {
        from { opacity: 0; transform: translateY(16px) scale(0.96); }
        to   { opacity: 1; transform: translateY(0) scale(1); }
    }
    @keyframes goldLine {
        from { width: 0; }
        to   { width: 100%; }
    }
    /* Animação Respiratória de UX: Mimetiza 4-5 segundos de ciclo de respiração calmo */
    @keyframes calmBreathe {
        0% { transform: scale(1) translateY(0); box-shadow: 0 4px 15px rgba(27,58,140,0.02); }
        50% { transform: scale(1.006) translateY(-2px); box-shadow: 0 12px 25px rgba(27,58,140,0.06); }
        100% { transform: scale(1) translateY(0); box-shadow: 0 4px 15px rgba(27,58,140,0.02); }
    }

    /* ── Header ── */
    .header-bar {
        background: linear-gradient(135deg, var(--azul) 0%, var(--azul-escuro) 100%);
        border-radius: 24px;
        padding: 20px 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(27,58,140,0.05), inset 0 1px 0 rgba(255,255,255,0.08);
        animation: fadeInDown 0.7s cubic-bezier(.22,1,.36,1) both;
        position: relative;
        overflow: hidden;
    }

    /* Linha dourada animada na base do header */
    .header-bar::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--dourado), transparent);
        animation: goldLine 1.2s ease 0.5s both;
    }

    .header-title {
        font-family: 'Playfair Display', serif !important;
        color: var(--branco);
        font-size: 1.5rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: -0.01em;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .header-sub {
        color: var(--dourado);
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        margin-top: 4px;
        text-transform: uppercase;
        font-family: 'DM Sans', sans-serif !important;
    }
    .logo-img {
        height: 54px;
        object-fit: contain;
        border-radius: 12px;
        background: rgba(255,255,255,0.95);
        padding: 5px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
        transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.4s;
    }
    .logo-img:hover {
        transform: scale(1.04) rotate(-1deg);
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    }

    /* ── Aviso Emergência (Pílula Proteção) ── */
    .aviso-emergencia {
        background: var(--lilac-suave);
        border-radius: 30px;
        padding: 12px 24px;
        margin: -0.5rem auto 1.8rem auto;
        color: #fff;
        font-size: 0.85rem;
        font-weight: 600;
        text-align: center;
        max-width: 250px;
        cursor: default;
        animation: fadeInDown 0.7s cubic-bezier(.22,1,.36,1) 0.15s both;
        letter-spacing: 0.02em;
        box-shadow: 0 8px 24px rgba(93, 90, 136, 0.2);
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        display: flex;
        justify-content: center;
        align-items: center;
        white-space: nowrap;
    }
    
    .aviso-emergencia .texto-oculto {
        max-width: 0;
        opacity: 0;
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
        display: inline-block;
        vertical-align: middle;
        margin-left: 0;
    }

    .aviso-emergencia:hover {
        max-width: 480px;
        background: var(--teal-prot);
        box-shadow: 0 12px 30px rgba(46, 139, 130, 0.3);
    }
    
    .aviso-emergencia:hover .texto-oculto {
        max-width: 300px;
        opacity: 1;
        margin-left: 10px;
    }

    /* ── Subtítulo ── */
    .subtitulo {
        text-align: center;
        color: var(--azul);
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
        line-height: 1.8;
        background: #fff;
        border-radius: 20px;
        padding: 18px 26px;
        border-left: 6px solid var(--dourado);
        animation: fadeInUp 0.7s cubic-bezier(.22,1,.36,1) 0.3s both, calmBreathe 6s ease-in-out infinite;
        box-shadow: 0 10px 30px rgba(27,58,140,0.04);
        position: relative;
        overflow: hidden;
    }

    /* ── Card da Equipe ── */
    .card-equipe {
        background: var(--branco);
        border-radius: 24px;
        padding: 24px 28px;
        border: 1px solid rgba(27,58,140,0.05);
        box-shadow: 0 10px 40px rgba(27,58,140,0.05);
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.7s cubic-bezier(.22,1,.36,1) 0.45s both;
        transition: box-shadow 0.4s ease, transform 0.4s ease;
    }
    .card-equipe:hover {
        box-shadow: 0 16px 45px rgba(27,58,140,0.08);
        transform: translateY(-2px);
    }
    .card-equipe h4 {
        font-family: 'DM Sans', sans-serif !important;
        color: var(--azul);
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(192,158,70, 0.3);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .card-equipe .meta {
        color: #667;
        font-size: 0.85rem;
        margin-bottom: 6px;
        font-weight: 400;
    }

    /* ── Badges ── */
    .badge {
        display: inline-block;
        background: #f4f6fa;
        color: var(--azul);
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 30px;
        padding: 6px 14px;
        margin: 4px 4px 0 0;
        border: 1px solid rgba(27,58,140,0.08);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: default;
        animation: staggerIn 0.5s ease both;
    }
    .badge:hover {
        background: var(--azul-medio);
        color: var(--branco);
        border-color: var(--azul);
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 16px rgba(27,58,140,0.15);
    }
    .badge-lider {
        background: var(--dourado);
        color: #fff;
        border-color: var(--dourado-claro);
        box-shadow: 0 2px 10px rgba(192,158,70,0.2);
    }
    .badge-lider:hover {
        background: var(--dourado-claro);
    }
    .badge-vice {
        background: var(--azul-medio);
        color: #fff;
        border-color: #3b5cbd;
    }
    .badge-vice:hover {
        background: var(--azul);
    }

    /* Delay escalonado nos badges */
    .badge:nth-child(1)  { animation-delay: 0.05s; }
    .badge:nth-child(2)  { animation-delay: 0.10s; }
    .badge:nth-child(3)  { animation-delay: 0.15s; }
    .badge:nth-child(4)  { animation-delay: 0.20s; }
    .badge:nth-child(5)  { animation-delay: 0.25s; }
    .badge:nth-child(6)  { animation-delay: 0.30s; }
    .badge:nth-child(7)  { animation-delay: 0.35s; }
    .badge:nth-child(8)  { animation-delay: 0.40s; }
    .badge:nth-child(9)  { animation-delay: 0.45s; }
    .badge:nth-child(10) { animation-delay: 0.50s; }
    .badge:nth-child(11) { animation-delay: 0.55s; }

    /* ── Chat ── */
    [data-testid="stChatMessageContent"] {
        border-radius: 18px !important;
        animation: fadeInUp 0.4s ease both;
        box-shadow: 0 4px 15px rgba(27,58,140,0.02);
    }
    [data-testid="stChatMessage"] {
        animation: fadeInUp 0.4s cubic-bezier(.22,1,.36,1) both;
    }

    /* ── Input do chat ── */
    [data-testid="stChatInput"] {
        border-radius: 20px !important;
        border: 1px solid rgba(27,58,140,0.1) !important;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: 0 4px 15px rgba(27,58,140,0.02) !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: var(--azul) !important;
        box-shadow: 0 8px 25px rgba(27,58,140,0.08) !important;
    }

    /* ── Rodapé ── */
    .rodape {
        text-align: center;
        color: var(--cinza-suave);
        font-size: 0.75rem;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(27,58,140,0.05);
        animation: fadeInUp 0.6s ease 0.6s both;
    }
    .rodape::before {
        content: '';
        display: block;
        width: 40px;
        height: 2px;
        background: var(--dourado);
        margin: 0 auto 10px;
        border-radius: 2px;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--azul) 0%, var(--azul-escuro) 100%) !important;
        border-right: 1px solid rgba(192,158,70,0.15) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #e8eeff !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background: var(--teal-prot) !important; /* Psicologia do teal na sidebar também */
        color: #fff !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        border: none !important;
        width: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(46, 139, 130, 0.25) !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(46, 139, 130, 0.4) !important;
    }

    /* Itens de integrante na sidebar */
    .sidebar-member {
        background: rgba(255,255,255,0.07);
        border-left: 4px solid var(--dourado);
        border-radius: 0 12px 12px 0;
        padding: 8px 14px;
        margin-bottom: 8px;
        font-size: 0.85rem;
        color: #e8eeff;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        animation: slideInLeft 0.4s ease both;
    }
    .sidebar-member:hover {
        background: rgba(255,255,255,0.15);
        border-color: var(--dourado-claro);
        transform: translateX(4px);
    }

    /* Spinner customizado */
    .stSpinner > div {
        border-top-color: var(--dourado) !important;
    }

    /* Selectbox */
    [data-testid="stSelectbox"] > div {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header com logos ─────────────────────────────────────────────────────────
ASSETS = os.path.join(os.path.dirname(__file__), "assets")
b64_jus = img_to_b64(os.path.join(ASSETS, "logo_jusconnect.jpeg"))
b64_uni = img_to_b64(os.path.join(ASSETS, "logo_uniftc.jpeg"))

st.markdown(f"""
<div class="header-bar">
    <div class="header-orb"></div>
    <img src="data:image/jpeg;base64,{b64_jus}" class="logo-img" alt="JusConnect">
    <div style="text-align:center; flex:1; padding: 0 16px; position:relative; z-index:1;">
        <div class="header-title">⚖️ JusConnect</div>
        <div class="header-sub">Informações Jurídicas · Canais de Atendimento · Salvador/BA</div>
    </div>
    <img src="data:image/jpeg;base64,{b64_uni}" class="logo-img" alt="UNIFTC">
</div>
""", unsafe_allow_html=True)

# ─── Aviso emergência (Dynamic Island) ────────────────────────────────────────
st.markdown("""
<div class="aviso-emergencia">
    <span>🛡️ Central de Proteção</span>
    <span class="texto-oculto">
        &nbsp;|&nbsp; <strong>190</strong> Polícia &nbsp;·&nbsp; <strong>180</strong> Mulher
    </span>
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
def render_badge(nome: str) -> str:
    if "Líder)" in nome and "Vice" not in nome:
        return f'<span class="badge badge-lider">👑 {nome}</span>'
    elif "Vice-líder" in nome:
        return f'<span class="badge badge-vice">⭐ {nome}</span>'
    else:
        return f'<span class="badge">👩‍⚖️ {nome}</span>'

badges = "".join(render_badge(n) for n in INTEGRANTES)

st.markdown(f"""
<div class="card-equipe">
    <h4>👩‍🎓 Equipe do Projeto</h4>
    <div class="meta">🏛️ <strong>{CURSO}</strong> &nbsp;·&nbsp; 📚 {DISCIPLINA} &nbsp;·&nbsp; 📅 {SEMESTRE}</div>
    <div class="meta">🎓 Orientação: <strong>{ORIENTADORA}</strong></div>
    <div style="margin-top:10px;">{badges}</div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
groq_api_key = st.secrets.get("GROQ_API_KEY")

with st.sidebar:
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:center; gap:10px; margin-bottom:12px;">
        <img src="data:image/jpeg;base64,{b64_jus}" style="height:44px; object-fit:contain; border-radius:8px; background:#fff; padding:3px; box-shadow:0 2px 8px rgba(0,0,0,0.2);">
        <img src="data:image/jpeg;base64,{b64_uni}" style="height:44px; object-fit:contain; border-radius:8px; background:#fff; padding:3px; box-shadow:0 2px 8px rgba(0,0,0,0.2);">
    </div>
    <div style="text-align:center; color:#C8A030; font-size:0.75rem; font-weight:700; letter-spacing:0.08em; margin-bottom:3px;">
        JUSCONNECT · UNIFTC
    </div>
    <div style="text-align:center; color:#a0b0e0; font-size:0.72rem; margin-bottom:14px;">
        {SEMESTRE}
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(f"""
    <div style="font-size:0.72rem; color:#C8A030; font-weight:700; margin-bottom:5px; letter-spacing:0.07em; text-transform:uppercase;">
        🎓 Orientação
    </div>
    <div style="font-size:0.8rem; color:#e8eeff; margin-bottom:12px; padding-left:4px;">
        {ORIENTADORA}
    </div>
    <div style="font-size:0.72rem; color:#C8A030; font-weight:700; margin-bottom:5px; letter-spacing:0.07em; text-transform:uppercase;">
        📚 Disciplina
    </div>
    <div style="font-size:0.8rem; color:#e8eeff; margin-bottom:12px; padding-left:4px;">
        {DISCIPLINA}
    </div>
    <div style="font-size:0.72rem; color:#C8A030; font-weight:700; margin-bottom:8px; letter-spacing:0.07em; text-transform:uppercase;">
        👩‍⚖️ Integrantes
    </div>
    """, unsafe_allow_html=True)

    for i, nome in enumerate(INTEGRANTES):
        delay = f"animation-delay:{i * 0.05:.2f}s"
        st.markdown(f"""
        <div class="sidebar-member" style="{delay}">
            {nome}
        </div>
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
        st.error("⚠️ GROQ_API_KEY não encontrada. Configure em .streamlit/secrets.toml")
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
1. Priorize as informações da base de conhecimento.
2. Se necessário, complemente com conhecimento geral confiável sobre violência doméstica, direitos das mulheres e serviços no Brasil.
3. Nunca invente telefones, endereços ou serviços específicos — só use os da base.
4. Se não souber algo específico (ex: endereço), diga que não tem essa informação e sugira ligar para o 180.
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

# ─── Botão de Saída Rápida (Panic Exit) ───────────────────────────────────────
botao_saida = """
<div id="quick-exit-btn" style="position: fixed; bottom: 20px; right: 20px; 
     background: rgba(0,0,0,0.6); color: #fff; padding: 10px 16px; 
     border-radius: 30px; font-family: 'DM Sans', sans-serif; font-size: 13px;
     font-weight: bold; cursor: pointer; backdrop-filter: blur(8px); z-index: 99999;
     box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: background 0.3s;" 
     onmouseover="this.style.background='rgba(0,0,0,0.8)'"
     onmouseout="this.style.background='rgba(0,0,0,0.6)'"
     onclick="window.parent.location.replace('https://g1.globo.com')">
     ✖ Saída Rápida (ESC)
</div>

<script>
    const docPai = window.parent.document;
    
    // Evita duplicar o listener
    if (!docPai.getElementById('quick-exit-listener')) {
        const dummy = docPai.createElement('div');
        dummy.id = 'quick-exit-listener';
        docPai.body.appendChild(dummy);

        docPai.addEventListener('keydown', function(event) {
            if(event.key === 'Escape' || event.key === 'Esc') {
                window.parent.location.replace('https://g1.globo.com'); 
            }
        });
    }

    // Evita botões duplicados a cada reload do Streamlit
    if (!docPai.getElementById('quick-exit-btn-parent')) {
        const btn = docPai.createElement('div');
        btn.innerHTML = document.getElementById('quick-exit-btn').outerHTML;
        const actualBtn = btn.firstElementChild;
        actualBtn.id = 'quick-exit-btn-parent';
        docPai.body.appendChild(actualBtn);
    }
    
    // Oculta o original de dentro do iframe
    document.getElementById('quick-exit-btn').style.display = 'none';
</script>
"""
components.html(botao_saida, height=0)