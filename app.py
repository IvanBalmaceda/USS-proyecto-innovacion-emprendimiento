from __future__ import annotations

from datetime import date, datetime
from typing import Any
from uuid import uuid4

import streamlit as st

from data import APP_NAME, APP_NOTICE, load_base_data


# Pantalla de ingreso (no aparece en la navegación lateral).
LOGIN_PAGE = "Ingreso"

# Secciones de la navegación lateral, en orden.
NAV_PAGES = [
    "Inicio",
    "Clases",
    "Guardados",
    "Aportar información",
    "Acerca del prototipo",
]

# Iconos del menú: Material Symbols que trae Streamlit (se adelgazan por CSS).
NAV_ICONS = {
    "Inicio": ":material/home:",
    "Clases": ":material/search:",
    "Guardados": ":material/star:",
    "Aportar información": ":material/add_circle:",
    "Acerca del prototipo": ":material/info:",
}

# Tinte y glifo de la ficha de cada asignatura (solo presentación).
SUBJECT_TINTS = {
    "Matemática": ("blue", "sigma"),
    "Lenguaje y Comunicación": ("green", "book"),
    "Ciencias Naturales": ("teal", "flask"),
    "Historia, Geografía y Ciencias Sociales": ("amber", "globe"),
}

# Iconos de línea propios: trazo de 1.4px, sin relleno. Se dibujan con
# `currentColor` para heredar el color del contexto.
ICON_PATHS = {
    "sigma": "<path d='M17.5 5h-11l6.2 7-6.2 7h11'/>",
    "book": ("<path d='M12 6.6C10.4 5.1 8.4 4.6 5 4.6v12.8c3.4 0 5.4.5 7 2 1.6-1.5 3.6-2 7-2V4.6"
             "c-3.4 0-5.4.5-7 2z'/><path d='M12 6.6v12.8'/>"),
    "flask": "<path d='M9 3h6M10 3v6.6L5.7 17A2.4 2.4 0 0 0 7.8 20.6h8.4A2.4 2.4 0 0 0 18.3 17L14 9.6V3'/>",
    "globe": ("<circle cx='12' cy='12' r='8.4'/><path d='M3.6 12h16.8'/>"
              "<path d='M12 3.6c2.3 2.3 3.5 5.2 3.5 8.4S14.3 18.1 12 20.4c-2.3-2.3-3.5-5.2-3.5-8.4S9.7 5.9 12 3.6z'/>"),
    "calendar": ("<rect x='3.4' y='5.2' width='17.2' height='15.4' rx='3'/>"
                 "<path d='M8.2 3v4M15.8 3v4M3.4 10.2h17.2'/>"),
    "cap": ("<path d='M2.6 8.4 12 4.2l9.4 4.2L12 12.6 2.6 8.4z'/>"
            "<path d='M6.4 10.5v4.1c0 1.7 2.5 3 5.6 3s5.6-1.3 5.6-3v-4.1'/>"),
    "user": "<circle cx='12' cy='8.2' r='3.2'/><path d='M5.2 20c0-3.3 3-5.6 6.8-5.6s6.8 2.3 6.8 5.6'/>",
    "doc": "<path d='M14 3.4H7.6a2 2 0 0 0-2 2v13.2a2 2 0 0 0 2 2h8.8a2 2 0 0 0 2-2V7.8z'/><path d='M14 3.4v4.4h4.4'/>",
    "note": ("<rect x='4.2' y='4.2' width='15.6' height='15.6' rx='3'/>"
             "<path d='M8.4 9.4h7.2M8.4 13h7.2M8.4 16.2h4'/>"),
    "star": "<path d='M12 3.8l2.7 5.4 6 .9-4.3 4.2 1 6-5.4-2.9-5.4 2.9 1-6L3.3 10l6-.9L12 3.8z'/>",
    "search": "<circle cx='11' cy='11' r='6.6'/><path d='M20.2 20.2 15.7 15.7'/>",
    "plus": "<path d='M12 5.2v13.6M5.2 12h13.6'/>",
    "info": "<circle cx='12' cy='12' r='8.4'/><path d='M12 11.2v5.6M12 7.9h.01'/>",
    "home": "<path d='M4.2 10.6 12 4.4l7.8 6.2v8.6a1.2 1.2 0 0 1-1.2 1.2h-3.4v-5.8H8.8v5.8H5.4a1.2 1.2 0 0 1-1.2-1.2z'/>",
    "layers": "<path d='M12 3.6 3.6 8.2 12 12.8l8.4-4.6L12 3.6z'/><path d='M3.6 13.4 12 18l8.4-4.6'/>",
    "download": "<path d='M12 4.4v10.2M8.2 11l3.8 3.8 3.8-3.8M4.8 19.6h14.4'/>",
    "clipboard": ("<rect x='6' y='4.6' width='12' height='15.4' rx='2.4'/>"
                  "<path d='M9.4 4.6V3.4h5.2v1.2'/><path d='M9.6 10.4h4.8M9.6 14h4.8'/>"),
    "eye": "<path d='M2.4 12S6 6.4 12 6.4 21.6 12 21.6 12 18 17.6 12 17.6 2.4 12 2.4 12z'/><circle cx='12' cy='12' r='2.8'/>",
}


# Avatares de línea. La diferencia la marcan el pelo (mujer / hombre) y las
# correas de mochila (estudiante).
_BUST = "<circle cx='12' cy='8.6' r='3.6'/><path d='M4.8 20.4c0-3.6 3.2-6 7.2-6s7.2 2.4 7.2 6'/>"
_HAIR_F = ("<path d='M7.9 9.6C7.2 6.4 8.9 4.2 12 4.2s4.8 2.2 4.1 5.4'/>"
           "<path d='M7.9 9c-1 1.6-1.2 3.4-.8 5.2M16.1 9c1 1.6 1.2 3.4.8 5.2'/>")
_HAIR_M = "<path d='M8.4 6.9C9.2 5.3 10.4 4.6 12 4.6s2.8.7 3.6 2.3'/>"
_STRAPS = "<path d='M9.3 15.1 8.6 20.4M14.7 15.1l.7 5.3'/>"

AVATARS = {
    ("adulto", "f"): _BUST + _HAIR_F,
    ("adulto", "m"): _BUST + _HAIR_M,
    ("estudiante", "f"): _BUST + _HAIR_F + _STRAPS,
    ("estudiante", "m"): _BUST + _HAIR_M + _STRAPS,
}


def avatar(kind: str, gender: str, size: int = 44) -> str:
    """Avatar del perfil: adulto o estudiante, mujer u hombre."""
    paths = AVATARS.get((kind, gender), AVATARS[("adulto", "f")])
    glyph = round(size * 0.56)
    tone = "av-student" if kind == "estudiante" else "av-adult"
    return (
        f'<span class="av-tile {tone}" style="width:{size}px;height:{size}px">'
        f"<svg viewBox='0 0 24 24' width='{glyph}' height='{glyph}' fill='none' "
        f"stroke='currentColor' stroke-width='1.4' stroke-linecap='round' "
        f"stroke-linejoin='round'>{paths}</svg></span>"
    )


def profile_avatar(profile: dict[str, Any], size: int = 44) -> str:
    """Avatar de quien está conectado, según su perfil."""
    kind = "estudiante" if st.session_state.selected_profile == "Estudiante" else "adulto"
    return avatar(kind, profile.get("gender", "f"), size)


def icon(name: str, size: int = 15) -> str:
    """SVG inline de trazo fino."""
    return (
        f"<svg viewBox='0 0 24 24' width='{size}' height='{size}' fill='none' "
        f"stroke='currentColor' stroke-width='1.4' stroke-linecap='round' "
        f"stroke-linejoin='round'>{ICON_PATHS[name]}</svg>"
    )

# Mensaje de bienvenida según el perfil elegido.
PROFILE_INTRO = {
    "Apoderado": "Revisa qué se trabajó en clases y ayuda a tu estudiante a mantenerse al día.",
    "Estudiante": "Revisa tus clases, tareas y materiales para ponerte al día.",
}

# Valores por defecto de los filtros de la sección Clases. Cada filtro es un
# widget con `key`, por lo que Streamlit conserva su valor entre reruns.
FILTER_DEFAULTS = {
    "f_subject": "Todas",
    "f_date": "Todas",
    "f_keyword": "",
}

MONTHS_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]

# Opción del formulario de aportes para registrar una clase que aún no existe.
NEW_CLASS_OPTION = "Registrar una clase nueva"

# Tipos de material que un apoderado o estudiante puede aportar.
MATERIAL_TYPES = ["Fotografía de cuaderno", "Guía", "Tarea", "Instrucción", "Otro"]

# Máximo de clases recientes que muestra Inicio.
RECENT_LIMIT = 3


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700&family=Geist:wght@300;400;500;600&display=swap');

        /* ------------------------------ Tokens ------------------------------
           Azul de marca sobre plata claro. Jerarquía por profundidad y aire,
           no por saturación. */
        :root {
            --blue-50:  #F1F6FF;
            --blue-100: #DCE8FF;
            --blue-200: #C3D6FE;
            --blue-500: #2563EB;
            --blue-600: #1D4ED8;
            --blue-700: #1A3FAF;

            --ink-900: #0B1220;
            --ink-800: #1B2739;
            --ink-600: #3E4C63;
            --ink-500: #5A6A82;
            --ink-400: #7C8AA0;

            --bg: #F5F7FC;
            --surface: #FFFFFF;
            /* Bandeja del double-bezel: nunca un borde gris sólido. */
            --shell: rgba(13, 26, 51, 0.035);
            --shell-strong: rgba(13, 26, 51, 0.055);
            --hairline: rgba(13, 26, 51, 0.07);
            --hairline-2: rgba(13, 26, 51, 0.12);

            --star: #B98514;
            --star-bg: #FFF8EA;
            --star-line: rgba(185, 133, 20, 0.22);
            --ok-bg: #EEFBF3;
            --ok-600: #0A7143;
            --ok-line: rgba(10, 113, 67, 0.18);

            /* Realce interior: simula el bisel de una pieza mecanizada. */
            --inner-hi: inset 0 1px 0 rgba(255, 255, 255, 0.95);
            /* Sombras ambientales difusas y tintadas, jamás negro duro. */
            --amb-1: 0 1px 1px rgba(11, 18, 32, 0.02), 0 6px 16px -10px rgba(11, 18, 32, 0.10);
            --amb-2: 0 1px 2px rgba(11, 18, 32, 0.025), 0 14px 34px -18px rgba(11, 18, 32, 0.16),
                     0 30px 60px -40px rgba(11, 18, 32, 0.18);
            --amb-3: 0 2px 3px rgba(11, 18, 32, 0.03), 0 22px 44px -18px rgba(29, 78, 216, 0.18),
                     0 44px 80px -50px rgba(11, 18, 32, 0.28);

            --r-shell: 22px;
            --r-core: 16px;
            --r-tile: 13px;
            --r-tile-core: 9px;

            --font-display: 'Plus Jakarta Sans', 'Geist', ui-sans-serif, system-ui, sans-serif;
            --font-body: 'Geist', 'Plus Jakarta Sans', ui-sans-serif, system-ui, sans-serif;

            /* Curva con masa: entra rápido y se asienta. */
            --fluid: cubic-bezier(0.32, 0.72, 0, 1);
        }

        html { scroll-behavior: smooth; }
        .stApp {
            background:
                radial-gradient(1200px 600px at 88% -12%, rgba(37, 99, 235, 0.06), transparent 62%),
                radial-gradient(900px 500px at 2% 4%, rgba(13, 26, 51, 0.04), transparent 60%),
                var(--bg);
        }
        [data-testid="stHeader"] { background: transparent; }

        .block-container {
            max-width: 1200px;
            /* El aire es parte del diseño: la página respira. */
            padding-top: 3.2rem !important;
            padding-bottom: 6rem !important;
        }
        /* Pantalla de ingreso: columna estrecha y centrada de verdad. */
        .block-container:has(.login-page) { max-width: 560px; }

        /* --------------------------- Tipografía ----------------------------- */
        html, body, .stApp, [data-testid="stSidebar"],
        button, input, textarea, select {
            font-family: var(--font-body) !important;
            -webkit-font-smoothing: antialiased;
            text-rendering: optimizeLegibility;
        }
        h1, h2, h3, h4 {
            font-family: var(--font-display) !important;
            color: var(--ink-900);
            letter-spacing: -0.03em;
            text-wrap: balance;
        }
        .stApp h1 {
            font-size: 2.1rem;
            font-weight: 700;
            line-height: 1.08;
            margin: 0.15rem 0 0.35rem 0;
        }
        .stMarkdown p, .stMarkdown li { color: var(--ink-600); line-height: 1.62; }
        .stMarkdown p { max-width: 70ch; }
        /* Los textos secundarios deben leerse, no desvanecerse. */
        [data-testid="stCaptionContainer"] p {
            color: var(--ink-500) !important;
            font-size: 0.9rem;
            line-height: 1.55;
            max-width: 62ch;
        }
        [data-testid="stWidgetLabel"] p {
            font-size: 0.78rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.01em;
            color: var(--ink-500) !important;
        }
        hr { border-color: var(--hairline) !important; }
        .num { font-variant-numeric: tabular-nums; }

        /* Etiqueta microscópica sobre cada título de página. */
        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.22rem 0.62rem;
            border-radius: 999px;
            background: var(--surface);
            border: 1px solid var(--hairline);
            box-shadow: var(--amb-1);
            font-size: 0.63rem;
            font-weight: 600;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--blue-600);
        }
        .eyebrow svg { opacity: 0.85; }

        /* ---------------------- Double-bezel (Doppelrand) -------------------
           Cada tarjeta es una bandeja con un núcleo dentro: radios
           concéntricos, realce interior y sombra difusa. */
        [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-card), [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-row), [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-highlight), [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-saved-strip) {
            position: relative;
            background: var(--shell) !important;
            border: 1px solid var(--hairline) !important;
            border-radius: var(--r-shell) !important;
            box-shadow: var(--amb-2);
            /* 6px de bandeja + 18px de aire dentro del núcleo. */
            padding: 1.5rem !important;
        }
        [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-card)::before, [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-row)::before, [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-highlight)::before, [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-saved-strip)::before {
            content: '';
            position: absolute;
            inset: 6px;
            border-radius: var(--r-core);
            background: var(--surface);
            box-shadow: var(--inner-hi), 0 1px 2px rgba(11, 18, 32, 0.035);
            z-index: 0;
            transition: box-shadow 0.7s var(--fluid);
        }
        [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-card) > *, [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-row) > *, [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-highlight) > *, [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-saved-strip) > * {
            position: relative;
            z-index: 1;
        }
        /* El marcador no ocupa espacio. */
        [data-testid="stElementContainer"]:has(> .stMarkdown [class^="mark-"]) {
            display: none !important;
        }

        /* Bloque destacado: bandeja azul con núcleo casi blanco. */
        [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-highlight) { background: var(--blue-50) !important; border-color: var(--blue-100) !important; }
        [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-highlight)::before {
            background: linear-gradient(180deg, #FFFFFF 0%, #FBFDFF 100%);
            box-shadow: var(--inner-hi), 0 1px 2px rgba(29, 78, 216, 0.06);
        }
        [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-saved-strip) { background: var(--star-bg) !important; border-color: var(--star-line) !important; }

        /* Fila de resultado: se eleva y afina su bisel bajo el cursor. */
        [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-row) {
            padding: 1.55rem 1.55rem 1.75rem !important;
            transition: transform 0.7s var(--fluid), box-shadow 0.7s var(--fluid),
                        border-color 0.7s var(--fluid), background 0.7s var(--fluid);
            animation: settleIn 0.85s var(--fluid) both;
        }
        [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-row):hover {
            transform: translateY(-3px);
            background: var(--shell-strong) !important;
            border-color: var(--blue-200) !important;
            box-shadow: var(--amb-3);
        }
        [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-row):hover::before {
            box-shadow: var(--inner-hi), 0 1px 2px rgba(29, 78, 216, 0.10),
                        0 0 0 1px rgba(29, 78, 216, 0.05);
        }

        /* Tarjetas de Inicio: misma altura y CTA alineado al fondo. El alto
           tiene que propagarse por toda la cadena columna → wrapper → tarjeta. */
        [data-testid="stColumn"] > div { height: 100%; }
        /* `:has()` no admite anidar otro `:has()`, así que buscamos el
           marcador directamente. */
        [data-testid="stColumn"] [data-testid="stLayoutWrapper"]:has(.mark-row) {
            height: 100%;
        }
        [data-testid="stColumn"] [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-row) { height: 100%; }
        div[class*="st-key-start-view-"] { margin-top: auto; }

        /* ------------------------- Coreografía de entrada ------------------- */
        @keyframes settleIn {
            from { opacity: 0; transform: translateY(18px); filter: blur(5px); }
            to   { opacity: 1; transform: none; filter: blur(0); }
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(12px); }
            to   { opacity: 1; transform: none; }
        }
        /* Revelado ligado al scroll: nada aparece de golpe. */
        @supports (animation-timeline: view()) {
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-row) {
                animation: settleIn 0.9s var(--fluid) both;
                animation-timeline: view();
                animation-range: entry 0% entry 48%;
            }
        }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { animation: none !important; transition: none !important; }
        }

        /* -------------------------- Piezas de contenido -------------------- */
        /* Ficha de asignatura: azulejo dentro de su propia bandeja. */
        .tile {
            position: relative;
            width: 42px; height: 42px;
            border-radius: var(--r-tile);
            flex: 0 0 auto;
            display: inline-flex; align-items: center; justify-content: center;
            border: 1px solid var(--hairline);
            box-shadow: var(--amb-1);
            transition: transform 0.7s var(--fluid);
        }
        .tile::before {
            content: '';
            position: absolute; inset: 3px;
            border-radius: var(--r-tile-core);
            box-shadow: var(--inner-hi);
        }
        .tile svg { position: relative; z-index: 1; }
        [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-row):hover .tile { transform: scale(1.04) rotate(-1.5deg); }

        .tile-blue  { background: #E8F0FF; color: #1D4ED8; }
        .tile-blue::before  { background: linear-gradient(180deg, #F7FAFF, #EDF3FF); }
        .tile-green { background: #E6F7EE; color: #0A7143; }
        .tile-green::before { background: linear-gradient(180deg, #F6FDF9, #EAF9F1); }
        .tile-teal  { background: #E4F5F8; color: #0B6B7C; }
        .tile-teal::before  { background: linear-gradient(180deg, #F5FCFD, #E9F7FA); }
        .tile-amber { background: #FDF1E1; color: #96601A; }
        .tile-amber::before { background: linear-gradient(180deg, #FFFAF3, #FCF3E7); }

        /* Azulejo del avatar: mismo doble bisel que las fichas. */
        .av-tile {
            position: relative;
            flex: 0 0 auto;
            border-radius: 14px;
            display: inline-flex; align-items: center; justify-content: center;
            border: 1px solid var(--hairline);
            box-shadow: var(--amb-1);
        }
        .av-tile::before {
            content: '';
            position: absolute; inset: 3px;
            border-radius: 10px;
            box-shadow: var(--inner-hi);
        }
        .av-tile svg { position: relative; z-index: 1; }
        .av-adult { background: #E8F0FF; color: var(--blue-600); }
        .av-adult::before { background: linear-gradient(180deg, #F7FAFF, #EDF3FF); }
        .av-student { background: #E6F7EE; color: #0A7143; }
        .av-student::before { background: linear-gradient(180deg, #F6FDF9, #EAF9F1); }

        .greet-row { display: flex; align-items: center; gap: 0.9rem; }

        .class-head { display: flex; gap: 0.95rem; align-items: flex-start; }
        .subject-name {
            font-size: 0.74rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--blue-600);
        }
        .class-topic {
            font-family: var(--font-display);
            font-size: 1.12rem;
            font-weight: 600;
            line-height: 1.24;
            letter-spacing: -0.022em;
            color: var(--ink-900);
            margin: 0.22rem 0 0.45rem 0;
        }
        .class-meta {
            display: flex; flex-wrap: wrap; gap: 0.3rem 1.15rem;
            font-size: 0.82rem; color: var(--ink-500);
        }
        .class-meta span { display: inline-flex; align-items: center; gap: 0.34rem; }
        .class-meta svg { color: var(--ink-400); }

        /* Los chips cierran la tarjeta: necesitan aire abajo. */
        .chips {
            margin: 0.95rem 0 0.35rem 0;
            display: flex; flex-wrap: wrap; gap: 0.4rem;
        }
        .chip {
            display: inline-flex; align-items: center; gap: 0.3rem;
            font-size: 0.73rem;
            font-weight: 500;
            padding: 0.24rem 0.6rem;
            border-radius: 999px;
            background: var(--surface);
            border: 1px solid var(--hairline);
            color: var(--ink-600);
            box-shadow: var(--amb-1);
        }
        .chip-task { background: var(--ok-bg); border-color: var(--ok-line); color: var(--ok-600); }
        .chip-file { background: var(--blue-50); border-color: var(--blue-100); color: var(--blue-700); }
        .chip-star { background: var(--star-bg); border-color: var(--star-line); color: var(--star); }

        .file-item {
            display: flex; align-items: center; gap: 0.7rem;
            padding: 0.7rem 0;
            border-top: 1px solid var(--hairline);
        }
        .file-item:first-of-type { border-top: none; padding-top: 0.25rem; }
        .file-item .ic {
            position: relative;
            width: 34px; height: 34px; border-radius: 11px;
            background: #EEF4FF; color: var(--blue-600);
            border: 1px solid var(--hairline);
            display: inline-flex; align-items: center; justify-content: center;
            flex: 0 0 auto;
            box-shadow: var(--amb-1);
        }
        .file-item .grow { flex: 1 1 auto; min-width: 0; }
        .file-item .nm { font-size: 0.88rem; color: var(--ink-800); font-weight: 500; }
        /* El archivo es simulado: la descarga se muestra inerte, no falsa. */
        .file-item .dl {
            flex: 0 0 auto;
            display: inline-flex; align-items: center; gap: 0.3rem;
            padding: 0.24rem 0.5rem;
            border-radius: 999px;
            border: 1px dashed var(--hairline-2);
            background: #F8FAFD;
            color: var(--ink-400);
            font-size: 0.72rem;
            font-weight: 500;
            cursor: not-allowed;
        }

        /* Adelanto de la clase dentro de cada fila de resultado. */
        .excerpt {
            padding-left: 1.15rem;
            border-left: 1px solid var(--hairline);
        }
        .ex-row {
            font-size: 0.82rem;
            line-height: 1.5;
            color: var(--ink-500);
            margin-bottom: 0.35rem;
        }
        .ex-row:last-child { margin-bottom: 0; }
        .ex-k { font-weight: 600; color: var(--ink-800); }
        .ex-v {
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .file-item .sub { font-size: 0.77rem; color: var(--ink-400); }

        .block-title {
            display: flex; align-items: center; gap: 0.6rem;
            font-family: var(--font-display);
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: -0.018em;
            color: var(--ink-900);
            margin-bottom: 0.55rem;
        }
        .block-title .bt-ic {
            width: 28px; height: 28px; border-radius: 9px; flex: 0 0 auto;
            display: inline-flex; align-items: center; justify-content: center;
            background: var(--blue-50);
            border: 1px solid var(--blue-100);
            color: var(--blue-600);
        }
        .block-sep {
            border-top: 1px solid var(--hairline);
            margin: 1.3rem 0 1.05rem 0;
        }
        .section-title {
            font-family: var(--font-display);
            font-size: 1.14rem;
            font-weight: 600;
            letter-spacing: -0.025em;
            color: var(--ink-900);
        }
        .muted { color: var(--ink-500); font-size: 0.9rem; line-height: 1.55; }
        .result-count {
            font-size: 0.87rem; font-weight: 600; color: var(--ink-600);
            letter-spacing: -0.005em;
        }
        .result-count .num { color: var(--blue-600); }

        .empty-box { text-align: center; padding: 2.2rem 1rem 1.2rem 1rem; }
        .empty-box .ring {
            width: 54px; height: 54px; margin: 0 auto 0.9rem auto;
            border-radius: 999px;
            display: flex; align-items: center; justify-content: center;
            background: var(--surface);
            border: 1px solid var(--hairline);
            box-shadow: var(--amb-2);
            color: var(--ink-400);
        }
        .empty-box .ttl {
            font-family: var(--font-display);
            font-size: 1.1rem; font-weight: 600; color: var(--ink-900);
            letter-spacing: -0.02em;
        }
        .empty-box .txt {
            font-size: 0.9rem; color: var(--ink-500); margin-top: 0.35rem;
            max-width: 44ch; margin-left: auto; margin-right: auto;
        }

        .footer-note {
            margin-top: 3.2rem;
            padding-top: 1.2rem;
            border-top: 1px solid var(--hairline);
            max-width: 72ch;
            font-size: 0.82rem;
            line-height: 1.65;
            color: var(--ink-400);
        }

        /* ------------------------------ Botones -----------------------------
           Secundario: pastilla clara con bisel. Primario: píldora azul con la
           flecha en su propio círculo (button-in-button). */
        div.stButton > button,
        div.stFormSubmitButton > button {
            border-radius: 13px;
            font-family: var(--font-body) !important;
            font-weight: 500;
            font-size: 0.88rem;
            letter-spacing: -0.005em;
            border: 1px solid var(--hairline-2);
            background: var(--surface);
            color: var(--ink-800);
            box-shadow: var(--inner-hi), var(--amb-1);
            transition: transform 0.55s var(--fluid), box-shadow 0.55s var(--fluid),
                        background 0.55s var(--fluid), border-color 0.55s var(--fluid),
                        color 0.55s var(--fluid);
        }
        div.stButton > button:hover,
        div.stFormSubmitButton > button:hover {
            background: var(--blue-50);
            border-color: var(--blue-200);
            color: var(--blue-700);
            transform: translateY(-1px);
            box-shadow: var(--inner-hi), var(--amb-2);
        }
        div.stButton > button:active,
        div.stFormSubmitButton > button:active { transform: scale(0.98); }
        div.stButton > button:focus-visible,
        div.stFormSubmitButton > button:focus-visible {
            outline: 2px solid var(--blue-500);
            outline-offset: 3px;
        }

        div.stButton > button[kind="primary"],
        div.stFormSubmitButton > button[kind="primary"] {
            position: relative;
            border-radius: 999px;
            padding: 0.7rem 0.7rem 0.7rem 1.35rem;
            font-weight: 600;
            color: #fff;
            border-color: rgba(12, 33, 87, 0.35);
            background: linear-gradient(180deg, #2A5CE4 0%, var(--blue-600) 55%, #1A44BE 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.28),
                        0 10px 22px -12px rgba(29, 78, 216, 0.72),
                        0 24px 48px -30px rgba(11, 18, 32, 0.4);
        }
        /* La flecha vive dentro de su propio círculo, al ras del borde. */
        div.stButton > button[kind="primary"]::after,
        div.stFormSubmitButton > button[kind="primary"]::after {
            content: '';
            display: inline-block;
            flex: 0 0 auto;
            width: 27px; height: 27px;
            margin-left: 0.85rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.16) center / 13px 13px no-repeat
                url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12h14M13 6l6 6-6 6'/%3E%3C/svg%3E");
            box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.14);
            transition: transform 0.55s var(--fluid), background-color 0.55s var(--fluid);
        }
        div.stButton > button[kind="primary"]:hover,
        div.stFormSubmitButton > button[kind="primary"]:hover {
            color: #fff;
            border-color: rgba(12, 33, 87, 0.5);
            background: linear-gradient(180deg, #3468EC 0%, #2050D6 55%, #1A44BE 100%);
            transform: translateY(-2px);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.34),
                        0 16px 30px -12px rgba(29, 78, 216, 0.8),
                        0 34px 60px -34px rgba(11, 18, 32, 0.45);
        }
        /* Tensión cinética: el círculo se mueve dentro del botón. */
        div.stButton > button[kind="primary"]:hover::after,
        div.stFormSubmitButton > button[kind="primary"]:hover::after {
            transform: translate(3px, -1px) scale(1.06);
            background-color: rgba(255, 255, 255, 0.26);
        }

        /* Ver clase: acción principal de cada fila, con flecha que avanza. */
        div[class*="-view-"] button {
            background: var(--blue-50);
            border-color: var(--blue-100);
            color: var(--blue-700);
            font-weight: 600;
        }
        div[class*="-view-"] button::after {
            content: '';
            display: inline-block;
            flex: 0 0 auto;
            width: 14px; height: 14px;
            margin-left: 0.5rem;
            background: center / 14px 14px no-repeat
                url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%231A3FAF' stroke-width='1.7' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12h14M13 6l6 6-6 6'/%3E%3C/svg%3E");
            transition: transform 0.55s var(--fluid);
        }
        div[class*="-view-"] button:hover::after { transform: translateX(4px); }

        /* Búsqueda: píldora compacta con la lupa, sin el círculo de la flecha. */
        div.st-key-classes-search button {
            padding: 0.7rem 0.5rem;
            border-radius: 13px;
        }
        div.st-key-classes-search button::after { content: none; }
        div.st-key-classes-search button span[role="img"] { margin-right: 0 !important; }

        /* Guardar clase en el detalle: acción destacada en ámbar. */
        div[class*="st-key-detail-save-"] button {
            background: linear-gradient(180deg, #FBD65E, #F5C633);
            border-color: #E0AF1C;
            color: #3F2D06;
            font-weight: 600;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5),
                        0 10px 20px -12px rgba(224, 175, 28, 0.8);
        }
        div[class*="st-key-detail-save-"] button:hover {
            background: linear-gradient(180deg, #FCDE79, #F8CF48);
            border-color: #D3A316;
            color: #3F2D06;
        }
        /* Guardar / Quitar: acción secundaria, ámbar cuando está guardada. */
        div[class*="-unsave-"] button {
            background: var(--star-bg);
            border-color: var(--star-line);
            color: var(--star);
        }
        div[class*="-unsave-"] button:hover {
            background: #FFF3DC;
            border-color: rgba(185, 133, 20, 0.4);
            color: #8C6410;
        }

        /* Volver y enlaces: texto que se desplaza, sin caja. */
        div[class*="st-key-link-"] button {
            background: transparent;
            border: none;
            box-shadow: none;
            padding-left: 0;
            color: var(--blue-600);
            font-weight: 600;
        }
        div[class*="st-key-link-"] button:hover {
            background: transparent;
            color: var(--blue-700);
        }
        /* Volver: píldora flotante, despegada del contenido. */
        div.st-key-detail-back button {
            border-radius: 999px;
            padding: 0.45rem 1.05rem 0.45rem 0.8rem;
            background: var(--surface);
            border: 1px solid var(--hairline);
            box-shadow: var(--inner-hi), var(--amb-1);
            color: var(--blue-600);
            font-weight: 600;
        }
        div.st-key-detail-back button:hover {
            background: var(--blue-50);
            border-color: var(--blue-200);
            color: var(--blue-700);
            transform: translateX(-4px);
        }
        div[class*="st-key-link-"] button:hover { transform: translateX(4px); }

        /* Iconos dentro de botones: mismo trazo fino que los SVG propios. */
        div.stButton > button span[role="img"],
        div.stFormSubmitButton > button span[role="img"] {
            font-variation-settings: 'FILL' 0, 'wght' 250, 'GRAD' -25, 'opsz' 24 !important;
            font-size: 17px !important;
            margin-right: 0.35rem;
            vertical-align: -3px !important;
        }
        /* Estrella rellena: al guardar en el detalle y en las ya guardadas. */
        div[class*="-unsave-"] button span[role="img"],
        div[class*="st-key-detail-save-"] button span[role="img"] {
            font-variation-settings: 'FILL' 1, 'wght' 300, 'opsz' 24 !important;
        }

        /* ---------------------------- Formularios --------------------------- */
        [data-testid="stForm"] {
            position: relative;
            background: var(--shell);
            border: 1px solid var(--hairline);
            border-radius: var(--r-shell);
            box-shadow: var(--amb-2);
            padding: 1.75rem !important;
        }
        [data-testid="stForm"]::before {
            content: '';
            position: absolute; inset: 6px;
            border-radius: var(--r-core);
            background: var(--surface);
            box-shadow: var(--inner-hi), 0 1px 2px rgba(11, 18, 32, 0.035);
            z-index: 0;
        }
        [data-testid="stForm"] > * { position: relative; z-index: 1; }

        [data-baseweb="select"] > div,
        [data-baseweb="input"],
        [data-baseweb="textarea"],
        [data-baseweb="base-input"],
        .stTextArea > div > div {
            border-radius: 12px !important;
            background: var(--surface) !important;
            border: 1px solid var(--hairline-2) !important;
            box-shadow: var(--inner-hi), 0 1px 2px rgba(11, 18, 32, 0.03);
            transition: border-color 0.4s var(--fluid), box-shadow 0.4s var(--fluid);
        }
        /* El <textarea> es transparente: el marco lo dibuja su envoltorio. */
        .stTextArea textarea,
        .stTextInput input {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        [data-baseweb="select"] > div:hover,
        [data-baseweb="input"]:hover,
        [data-baseweb="textarea"]:hover { border-color: var(--ink-400) !important; }
        [data-baseweb="select"] > div:focus-within,
        [data-baseweb="input"]:focus-within,
        [data-baseweb="textarea"]:focus-within {
            border-color: var(--blue-500) !important;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12) !important;
        }
        /* La pista "Press Enter to apply" viene en inglés desde Streamlit. */
        [data-testid="InputInstructions"] { display: none !important; }

        /* ------------------------------ Sidebar ----------------------------- */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFFFFF 0%, #FCFDFF 100%);
            border-right: 1px solid var(--hairline);
        }
        [data-testid="stSidebar"] .block-container { padding-top: 1.6rem !important; }

        .sb-brand {
            display: flex; align-items: center; gap: 0.55rem;
            font-family: var(--font-display);
            font-size: 1.04rem; font-weight: 700; letter-spacing: -0.035em;
            color: var(--ink-900);
        }
        .sb-brand .logo {
            position: relative;
            width: 30px; height: 30px; border-radius: 10px;
            display: inline-flex; align-items: center; justify-content: center;
            background: linear-gradient(180deg, #2A5CE4, var(--blue-600));
            color: #fff;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.3),
                        0 8px 16px -8px rgba(29, 78, 216, 0.7);
        }
        .sb-brand .tag {
            margin-left: auto;
            font-size: 0.6rem; font-weight: 700; letter-spacing: 0.1em;
            padding: 0.16rem 0.42rem; border-radius: 999px;
            background: var(--blue-50); border: 1px solid var(--blue-100);
            color: var(--blue-600);
        }

        /* Isla de navegación: bandeja con pastillas dentro. */
        [data-testid="stSidebar"] [role="radiogroup"] {
            gap: 0.15rem;
            padding: 6px;
            border-radius: 18px;
            background: var(--shell);
            border: 1px solid var(--hairline);
            box-shadow: inset 0 1px 2px rgba(11, 18, 32, 0.03);
        }
        [data-testid="stSidebar"] [role="radiogroup"] label {
            position: relative;
            padding: 0.5rem 0.7rem;
            border-radius: 12px;
            transition: background 0.5s var(--fluid), transform 0.5s var(--fluid);
            animation: slideUp 0.6s var(--fluid) both;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(1) { animation-delay: 0.02s; }
        [data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(2) { animation-delay: 0.06s; }
        [data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(3) { animation-delay: 0.10s; }
        [data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(4) { animation-delay: 0.14s; }
        [data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(5) { animation-delay: 0.18s; }
        [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none; }
        [data-testid="stSidebar"] [role="radiogroup"] label p {
            font-size: 0.89rem; font-weight: 500; color: var(--ink-600) !important;
            letter-spacing: -0.01em;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(29, 78, 216, 0.06);
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(180deg, #2A5CE4, var(--blue-600));
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.26),
                        0 10px 20px -12px rgba(29, 78, 216, 0.75);
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
            color: #fff !important; font-weight: 600;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:focus-visible) {
            outline: 2px solid var(--blue-500); outline-offset: 3px;
        }
        /* Iconos del menú: trazo fino y preciso, no pesado. Streamlit los
           dibuja como <span role="img"> con la fuente Material Symbols. */
        [data-testid="stSidebar"] [role="radiogroup"] label p span[role="img"] {
            font-variation-settings: 'FILL' 0, 'wght' 250, 'GRAD' -25, 'opsz' 24 !important;
            font-size: 19px !important;
            margin-right: 0.4rem;
            vertical-align: -3px !important;
        }
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] { display: none; }

        .sb-card {
            margin-top: 1.1rem;
            position: relative;
            padding: 0.85rem 0.9rem;
            border-radius: 18px;
            background: var(--shell);
            border: 1px solid var(--hairline);
        }
        .sb-card .k {
            font-size: 0.62rem; font-weight: 600; letter-spacing: 0.16em;
            text-transform: uppercase; color: var(--ink-400);
        }
        .sb-card .v { font-size: 0.88rem; font-weight: 600; color: var(--ink-900); letter-spacing: -0.01em; }
        .sb-card .s { font-size: 0.78rem; color: var(--ink-400); }
        .sb-card .row { display: flex; align-items: center; gap: 0.7rem; }
        .sb-card .k { display: inline-block; margin-bottom: 0.1rem; }
        .sb-card .course { color: var(--blue-600); font-weight: 600; }
        .sb-card .sb-ic {
            flex: 0 0 auto;
            color: var(--blue-600);
            display: inline-flex; align-items: center; justify-content: center;
        }
        .sb-card .divide { border-top: 1px solid var(--hairline); margin: 0.7rem 0; }

        [data-testid="stSidebar"] div.stButton > button {
            border-radius: 12px;
            font-size: 0.85rem;
            color: var(--ink-600);
        }

        /* ------------------------------ Alertas ----------------------------- */
        [data-testid="stAlert"] {
            border-radius: 14px;
            border: 1px solid var(--hairline);
            box-shadow: var(--inner-hi), var(--amb-1);
            animation: slideUp 0.6s var(--fluid) both;
        }

        /* ----------------------------- Responsive --------------------------- */
        @media (max-width: 768px) {
            .block-container {
                padding-top: 1.8rem !important;
                padding-bottom: 3.5rem !important;
            }
            .stApp h1 { font-size: 1.7rem; }
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-card), [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-row), [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-highlight), [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-saved-strip) { padding: 1.15rem !important; }
            [data-testid="stForm"] { padding: 1.2rem !important; }
            .excerpt {
                padding-left: 0;
                border-left: none;
                padding-top: 0.75rem;
                border-top: 1px solid var(--hairline);
            }
            /* Sin rotaciones ni solapes en táctil. */
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-row):hover { transform: none; }
            [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .mark-row):hover .tile { transform: none; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Estado de la sesión
# ---------------------------------------------------------------------------


def initialize_state() -> None:
    if "base_data" not in st.session_state:
        st.session_state.base_data = load_base_data()
    if "contributions" not in st.session_state:
        st.session_state.contributions = []
    if "aportes_count" not in st.session_state:
        st.session_state.aportes_count = 0
    if "selected_profile" not in st.session_state:
        st.session_state.selected_profile = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = LOGIN_PAGE
    # Valor del radio de navegación. `set_page` lo mantiene sincronizado con
    # `current_page` para que la sección marcada sea siempre la que se ve.
    if "nav_radio" not in st.session_state:
        st.session_state.nav_radio = NAV_PAGES[0]
    if "selected_class_id" not in st.session_state:
        st.session_state.selected_class_id = None
    if "flash_message" not in st.session_state:
        st.session_state.flash_message = None
    # IDs de las clases guardadas para revisar después (solo esta sesión).
    if "saved_class_ids" not in st.session_state:
        st.session_state.saved_class_ids = []
    # Clase preseleccionada al entrar al formulario desde un detalle.
    if "selected_contribution_class_id" not in st.session_state:
        st.session_state.selected_contribution_class_id = None
    if "contrib_target" not in st.session_state:
        st.session_state.contrib_target = NEW_CLASS_OPTION
    if "form_error" not in st.session_state:
        st.session_state.form_error = None
    # Copia de los filtros: Streamlit reinicia el valor de un widget cuando
    # deja de dibujarse (al entrar al detalle), así que guardamos lo último
    # elegido para poder restaurarlo al volver al listado.
    if "filters_snapshot" not in st.session_state:
        st.session_state.filters_snapshot = dict(FILTER_DEFAULTS)


def reset_filters() -> None:
    """Callback del botón Limpiar filtros (se ejecuta antes del rerun)."""
    st.session_state.filters_snapshot = dict(FILTER_DEFAULTS)


def current_filters() -> dict[str, str]:
    """Filtros vigentes. Viven fuera de los widgets porque Streamlit reinicia
    el valor de un widget cuando deja de dibujarse (al entrar al detalle)."""
    snapshot = st.session_state.filters_snapshot
    return {key: snapshot.get(key, default) for key, default in FILTER_DEFAULTS.items()}


def remember_filters(subject: str, selected_date: str, keyword: str) -> None:
    """Guarda lo que quedó en los filtros como valor vigente de la sesión."""
    st.session_state.filters_snapshot = {
        "f_subject": subject,
        "f_date": selected_date,
        "f_keyword": keyword,
    }


def reset_demo() -> None:
    st.session_state.base_data = load_base_data()
    st.session_state.contributions = []
    st.session_state.aportes_count = 0
    st.session_state.selected_class_id = None
    st.session_state.saved_class_ids = []
    st.session_state.selected_contribution_class_id = None
    st.session_state.contrib_target = NEW_CLASS_OPTION
    st.session_state.current_page = "Inicio" if st.session_state.selected_profile else LOGIN_PAGE
    st.session_state.nav_radio = NAV_PAGES[0]
    st.session_state.flash_message = "El demo fue restablecido a los datos originales."
    reset_filters()


# ---------------------------------------------------------------------------
# Datos y utilidades
# ---------------------------------------------------------------------------


def format_display_date(raw_date: str) -> str:
    return datetime.strptime(raw_date, "%Y-%m-%d").strftime("%d/%m/%Y")


def format_long_date(raw_date: str) -> str:
    """Ej.: '24 de agosto de 2026'."""
    parsed = datetime.strptime(raw_date, "%Y-%m-%d")
    return f"{parsed.day} de {MONTHS_ES[parsed.month - 1]} de {parsed.year}"


def shorten(text: str, limit: int = 74) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1].rstrip(" ,.;") + "…"


def file_kind(file_name: str, fallback: str) -> str:
    """Formato del archivo según su extensión; si no tiene, el tipo aportado."""
    lower = file_name.lower()
    if lower.endswith(".pdf"):
        return "PDF"
    if lower.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
        return "Imagen"
    if lower.endswith((".doc", ".docx", ".odt")):
        return "Documento"
    if lower.endswith((".xls", ".xlsx", ".csv")):
        return "Planilla"
    return fallback


def plural(count: int, singular: str, many: str) -> str:
    """Ej.: 1 archivo / 3 archivos."""
    return f"{count} {singular if count == 1 else many}"


def subject_style(subject_name: str) -> tuple[str, str]:
    return SUBJECT_TINTS.get(subject_name, ("blue", "layers"))


def block_title(text: str, icon_name: str) -> str:
    """Título de bloque con su azulejo de icono."""
    return (
        f'<div class="block-title"><span class="bt-ic">{icon(icon_name, 14)}</span>{text}</div>'
    )


def eyebrow(text: str, icon_name: str) -> str:
    return f'<span class="eyebrow">{icon(icon_name, 12)}{text}</span>'


def initials(name: str) -> str:
    parts = [part for part in name.split() if part]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def class_files(item: dict[str, Any]) -> list[str]:
    return [file_name for material in item["materials"] for file_name in material["files"]]


def class_contributors(item: dict[str, Any]) -> list[str]:
    # Nombres únicos conservando el orden en que aportaron.
    return list(dict.fromkeys(material["contributor"] for material in item["materials"]))


def get_all_classes() -> list[dict[str, Any]]:
    classes = st.session_state.base_data["classes"] + st.session_state.contributions
    return sorted(classes, key=lambda item: item["date"], reverse=True)


def find_class(class_id: str) -> dict[str, Any] | None:
    return next((item for item in get_all_classes() if item["id"] == class_id), None)


def get_subjects() -> list[dict[str, str]]:
    return st.session_state.base_data["subjects"]


def get_profile_data() -> dict[str, str] | None:
    selected = st.session_state.selected_profile
    if not selected:
        return None
    return st.session_state.base_data["profiles"][selected]


def get_date_options(classes: list[dict[str, Any]]) -> list[str]:
    unique_dates = []
    seen = set()
    for item in classes:
        if item["date"] not in seen:
            unique_dates.append(item["date"])
            seen.add(item["date"])
    return ["Todas"] + unique_dates


def get_saved_classes() -> list[dict[str, Any]]:
    saved = st.session_state.saved_class_ids
    return [item for item in get_all_classes() if item["id"] in saved]


def is_saved(class_id: str) -> bool:
    return class_id in st.session_state.saved_class_ids


def toggle_saved(class_id: str) -> None:
    if is_saved(class_id):
        st.session_state.saved_class_ids.remove(class_id)
        st.session_state.flash_message = "La clase se quitó de tus guardados."
    else:
        st.session_state.saved_class_ids.append(class_id)
        st.session_state.flash_message = "La clase quedó guardada para revisarla después."


# ---------------------------------------------------------------------------
# Navegación
# ---------------------------------------------------------------------------


def set_page(page: str, selected_class_id: str | None = None) -> None:
    st.session_state.current_page = page
    st.session_state.selected_class_id = selected_class_id
    if page in NAV_PAGES:
        st.session_state.nav_radio = page
    # Entrar al formulario por el menú no debe precargar ninguna clase.
    if page == "Aportar información":
        st.session_state.selected_contribution_class_id = None
        st.session_state.contrib_target = NEW_CLASS_OPTION


# Las funciones de navegación se usan como callbacks `on_click`: Streamlit las
# ejecuta antes de volver a correr el script, así cada pasada dibuja una sola
# página con el estado final (nada de st.rerun a mitad de una pantalla).


def go_to(page: str) -> None:
    set_page(page)


def on_nav_change() -> None:
    """Callback del menú lateral."""
    set_page(st.session_state.nav_radio)


def open_class(class_id: str) -> None:
    # `filters_snapshot` ya guarda los filtros vigentes: al volver al listado
    # los widgets se redibujan desde ahí y se ven los mismos resultados.
    set_page("Clases", selected_class_id=class_id)


def back_to_classes() -> None:
    set_page("Clases")


def contribute_to_class(class_id: str) -> None:
    """Abre el formulario de aportes ya apuntando a esta clase."""
    set_page("Aportar información")
    st.session_state.selected_contribution_class_id = class_id
    st.session_state.contrib_target = class_id


def enter_demo() -> None:
    """Callback de ingreso.

    El perfil se lee de `session_state` y no por argumento: al pasarlo como
    `args` quedaría fijado el valor del render anterior, y si el usuario cambia
    el selector y entra en el mismo paso, ingresaría con el perfil equivocado."""
    st.session_state.selected_profile = st.session_state.login_profile
    st.session_state.current_page = "Inicio"
    st.session_state.nav_radio = NAV_PAGES[0]


def change_profile() -> None:
    st.session_state.selected_profile = None
    st.session_state.current_page = LOGIN_PAGE
    st.session_state.selected_class_id = None
    st.session_state.nav_radio = NAV_PAGES[0]


def show_flash_message() -> None:
    if st.session_state.flash_message:
        st.success(st.session_state.flash_message)
        st.session_state.flash_message = None


def render_sidebar() -> None:
    # En la pantalla de ingreso no mostramos barra lateral: no aporta nada.
    if not st.session_state.selected_profile:
        st.markdown(
            "<style>[data-testid='stSidebar'],"
            "[data-testid='stSidebarCollapsedControl'],"
            "[data-testid='stSidebarCollapseButton']{display:none;}</style>",
            unsafe_allow_html=True,
        )
        return

    with st.sidebar:
        profile = get_profile_data()
        st.markdown(
            f"""
            <div class="sb-brand">
                <span class="logo">{icon('layers', 16)}</span>{APP_NAME}
                <span class="tag">V2</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")

        st.radio(
            "Ir a",
            options=NAV_PAGES,
            key="nav_radio",
            format_func=lambda name: f"{NAV_ICONS[name]}  {name}",
            on_change=on_nav_change,
        )

        st.markdown(
            f"""
            <div class="sb-card">
                <div class="row">
                    {profile_avatar(profile, 40)}
                    <span>
                        <span class="k">Perfil actual</span><br>
                        <span class="v">{profile.get('role_label', st.session_state.selected_profile)}</span><br>
                        <span class="s">{profile['name']}</span>
                    </span>
                </div>
                <div class="divide"></div>
                <div class="row">
                    {avatar("estudiante", profile.get('student_gender', 'm'), 40)}
                    <span>
                        <span class="k">Estudiante asociado</span><br>
                        <span class="v">{profile['student_name']}</span><br>
                        <span class="s course">{profile['course']}</span>
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        st.button(
            ":material/restart_alt: Restablecer demo",
            key="sidebar-reset-demo",
            on_click=reset_demo,
            use_container_width=True,
        )
        st.button(
            "Cambiar perfil",
            key="sidebar-change-profile",
            on_click=change_profile,
            use_container_width=True,
        )


# ---------------------------------------------------------------------------
# Búsqueda
# ---------------------------------------------------------------------------


def filter_classes(
    classes: list[dict[str, Any]],
    subject: str = "Todas",
    selected_date: str = "Todas",
    keyword: str = "",
) -> list[dict[str, Any]]:
    keyword_normalized = keyword.strip().lower()
    filtered = []
    for item in classes:
        if subject != "Todas" and item["subject"] != subject:
            continue
        if selected_date != "Todas" and item["date"] != selected_date:
            continue
        haystack = " ".join(
            [
                item["subject"],
                item["topic"],
                " ".join(item["content"]),
                item["task"],
                item["instructions"],
                # También buscamos por nombre de archivo compartido.
                " ".join(class_files(item)),
            ]
        ).lower()
        if keyword_normalized and keyword_normalized not in haystack:
            continue
        filtered.append(item)
    return filtered


# ---------------------------------------------------------------------------
# Componentes
# ---------------------------------------------------------------------------


def class_summary_html(item: dict[str, Any], course: str, with_chips: bool = True) -> str:
    """Encabezado común de una clase: asignatura, tema, fecha y curso."""
    tint, glyph = subject_style(item["subject"])
    files = class_files(item)
    contributors = class_contributors(item)

    chips = ""
    if with_chips:
        parts = []
        if item["task"]:
            parts.append(f'<span class="chip chip-task">{icon("note", 13)}Tarea</span>')
        if files:
            parts.append(
                f'<span class="chip chip-file">{icon("doc", 13)}'
                f'{plural(len(files), "archivo", "archivos")}</span>'
            )
        if is_saved(item["id"]):
            parts.append(f'<span class="chip chip-star">{icon("star", 13)}Guardada</span>')
        chips = f'<div class="chips">{"".join(parts)}</div>' if parts else ""

    who = ", ".join(contributors[:2])
    if len(contributors) > 2:
        who += f" y {len(contributors) - 2} más"

    return f"""
    <div class="class-head">
        <span class="tile tile-{tint}">{icon(glyph, 19)}</span>
        <span>
            <span class="subject-name">{item['subject']}</span>
            <div class="class-topic">{item['topic']}</div>
            <div class="class-meta">
                <span>{icon('calendar')}<span class="num">{format_long_date(item['date'])}</span></span>
                <span>{icon('cap')}{course}</span>
                <span>{icon('user')}Por {who}</span>
            </div>
        </span>
    </div>
    {chips}
    """


def class_excerpt_html(item: dict[str, Any]) -> str:
    """Adelanto de la clase: qué se vio y qué quedó de tarea."""
    rows = []
    if item["content"]:
        rows.append(
            f'<div class="ex-row"><span class="ex-k">Vimos:</span> '
            f'<span class="ex-v">{shorten(" ".join(item["content"]))}</span></div>'
        )
    if item["task"]:
        rows.append(
            f'<div class="ex-row"><span class="ex-k">Tarea:</span> '
            f'<span class="ex-v">{shorten(item["task"])}</span></div>'
        )
    if not rows:
        rows.append('<div class="ex-row"><span class="ex-v">Sin contenido registrado.</span></div>')
    return f'<div class="excerpt">{"".join(rows)}</div>'


def render_class_row(item: dict[str, Any], course: str, key_prefix: str = "row") -> None:
    """Fila de resultado con adelanto de la clase y acciones."""
    with st.container(border=True):
        st.markdown('<div class="mark-row"></div>', unsafe_allow_html=True)
        info, excerpt, actions = st.columns(
            [2.2, 1.7, 1], gap="medium", vertical_alignment="center"
        )
        with info:
            st.markdown(class_summary_html(item, course), unsafe_allow_html=True)
        with excerpt:
            st.markdown(class_excerpt_html(item), unsafe_allow_html=True)
        with actions:
            st.button(
                "Ver clase",
                key=f"{key_prefix}-view-{item['id']}",
                on_click=open_class,
                args=(item["id"],),
                use_container_width=True,
            )
            saved = is_saved(item["id"])
            label = ":material/star: Quitar" if saved else ":material/star: Guardar"
            state = "unsave" if saved else "save"
            st.button(
                label,
                key=f"{key_prefix}-{state}-{item['id']}",
                on_click=toggle_saved,
                args=(item["id"],),
                use_container_width=True,
            )


def render_compact_class_card(item: dict[str, Any], course: str, key_prefix: str) -> None:
    """Tarjeta breve para Inicio: asignatura, tema, fecha y Ver clase."""
    tint, glyph = subject_style(item["subject"])
    with st.container(border=True):
        st.markdown('<div class="mark-row"></div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="class-head">
                <span class="tile tile-{tint}">{icon(glyph, 19)}</span>
                <span>
                    <span class="subject-name">{item['subject']}</span>
                    <div class="class-topic">{item['topic']}</div>
                </span>
            </div>
            <div class="class-meta" style="margin-top:0.75rem;flex-direction:column;gap:0.35rem">
                <span>{icon('calendar')}<span class="num">{format_long_date(item['date'])}</span></span>
                <span>{icon('cap')}{course}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        st.button(
            "Ver clase",
            key=f"{key_prefix}-view-{item['id']}",
            on_click=open_class,
            args=(item["id"],),
            use_container_width=True,
        )


# ---------------------------------------------------------------------------
# Páginas
# ---------------------------------------------------------------------------


def render_login() -> None:
    # El marcador estrecha y centra el contenedor (ver inject_styles).
    st.markdown(
        f"""
        <div class="login-page"></div>
        <div style="text-align:center;margin-bottom:1.6rem">
            <div class="sb-brand" style="justify-content:center;font-size:1.55rem">
                <span class="logo">{icon('layers', 17)}</span>{APP_NAME}
                <span class="tag">V2</span>
            </div>
            <p class="muted" style="margin:0.7rem auto 0 auto;max-width:38ch">
                Falté a clases o me falta información. ¿Cómo me pongo al día?
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown('<div class="mark-card"></div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="margin-bottom:0.9rem">{eyebrow("Ingreso", "user")}</div>'
            '<div class="section-title">Ingresar al demo</div>',
            unsafe_allow_html=True,
        )
        st.write("")
        selected = st.selectbox(
            "¿Con qué perfil quieres entrar?",
            ["Apoderado", "Estudiante"],
            key="login_profile",
        )
        # `selected` solo se usa para la vista previa de abajo; el ingreso lee
        # el valor desde session_state en su propio callback.
        preview = st.session_state.base_data["profiles"][selected]
        kind = "estudiante" if selected == "Estudiante" else "adulto"
        st.markdown(
            f'<div class="greet-row" style="margin:0.9rem 0 0.2rem 0">'
            f'{avatar(kind, preview.get("gender", "f"), 46)}'
            f'<span><span class="strong">{preview["name"]}</span><br>'
            f'<span class="muted">{preview.get("role_label", selected)} · '
            f'{preview["course"]}</span></span></div>',
            unsafe_allow_html=True,
        )
        if selected == "Apoderado":
            st.caption("Entrarás como Carolina Soto, apoderada de Martín Soto.")
        else:
            st.caption("Entrarás como Martín Soto, estudiante de 5° Básico B.")
        st.caption(
            "Ambos perfiles tienen las mismas funciones en el prototipo. El perfil solo "
            "define el nombre con el que quedan registrados los materiales que aportes."
        )
        st.write("")
        st.button(
            "Ingresar al demo",
            key="home-enter-demo",
            type="primary",
            on_click=enter_demo,
            use_container_width=True,
        )

    st.markdown(f'<p class="footer-note">{APP_NOTICE}</p>', unsafe_allow_html=True)


def render_start() -> None:
    """Pantalla Inicio."""
    profile = get_profile_data()
    classes = get_all_classes()
    saved = get_saved_classes()

    face, greeting = st.columns([0.1, 1], gap="small", vertical_alignment="center")
    face.markdown(profile_avatar(profile, 62), unsafe_allow_html=True)
    with greeting:
        st.markdown(eyebrow("Inicio", "home"), unsafe_allow_html=True)
        st.title(f"Hola, {profile['name'].split()[0]}")
    st.caption(
        "Encuentra rápidamente lo que se trabajó en clases, las tareas pendientes y el "
        "material compartido. " + PROFILE_INTRO[st.session_state.selected_profile]
    )
    show_flash_message()
    st.write("")

    # Acción principal.
    with st.container(border=True):
        st.markdown('<div class="mark-highlight"></div>', unsafe_allow_html=True)
        text_col, action_col = st.columns([3, 1], gap="medium", vertical_alignment="center")
        with text_col:
            st.markdown(
                f"""
                <div class="section-title" style="display:flex;align-items:center;gap:0.5rem">
                    <span style="color:var(--blue-600)">{icon('search', 18)}</span>
                    Buscar una clase
                </div>
                <p class="muted" style="margin:0.3rem 0 0 0">
                    Busca información por asignatura, fecha o palabra clave.
                </p>
                """,
                unsafe_allow_html=True,
            )
        with action_col:
            st.button(
                "Buscar clases",
                key="start-search",
                type="primary",
                on_click=go_to,
                args=("Clases",),
                use_container_width=True,
            )

    st.write("")
    head, link = st.columns([3, 1], gap="small", vertical_alignment="center")
    head.markdown('<div class="section-title">Clases recientes</div>', unsafe_allow_html=True)
    link.button(
        "Ver todas  →",
        key="link-all-classes",
        on_click=go_to,
        args=("Clases",),
        use_container_width=True,
    )

    recent = classes[:RECENT_LIMIT]
    if recent:
        columns = st.columns(len(recent), gap="medium")
        for column, item in zip(columns, recent):
            with column:
                render_compact_class_card(item, profile["course"], key_prefix="start")
    else:
        st.caption("Todavía no hay clases registradas en el demo.")

    st.write("")
    with st.container(border=True):
        st.markdown('<div class="mark-saved-strip"></div>', unsafe_allow_html=True)
        text_col, action_col = st.columns([3, 1], gap="medium", vertical_alignment="center")
        with text_col:
            if saved:
                detail = f"Tienes {plural(len(saved), 'clase guardada', 'clases guardadas')}."
            else:
                detail = "Guarda una clase para volver a ella más tarde."
            st.markdown(
                f"""
                <div class="section-title" style="display:flex;align-items:center;gap:0.5rem">
                    <span style="color:var(--star)">{icon('star', 18)}</span>
                    Guardados
                </div>
                <p class="muted" style="margin:0.3rem 0 0 0">{detail}</p>
                """,
                unsafe_allow_html=True,
            )
        with action_col:
            st.button(
                "Ver guardados  →",
                key="link-saved",
                on_click=go_to,
                args=("Guardados",),
                use_container_width=True,
            )

    st.markdown(
        '<p class="footer-note">Aula al Día es un prototipo académico con información '
        'ficticia.</p>',
        unsafe_allow_html=True,
    )


def render_class_detail(item: dict[str, Any]) -> None:
    profile = get_profile_data()
    course = profile["course"]

    # Al volver, los filtros del listado se reponen desde `filters_snapshot`.
    st.button(":material/arrow_back: Volver a clases", key="detail-back", on_click=back_to_classes)

    head, action = st.columns([3, 1], gap="medium", vertical_alignment="center")
    with head:
        tint, glyph = subject_style(item["subject"])
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:0.65rem;margin-bottom:0.55rem">'
            f'<span class="tile tile-{tint}">{icon(glyph, 19)}</span>'
            f'<span class="subject-name" style="font-size:0.78rem">{item["subject"]}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )
        st.title(item["topic"])
        st.markdown(
            f"""
            <div class="class-meta" style="margin-top:0.5rem">
                <span>{icon('calendar')}<span class="num">{format_long_date(item['date'])}</span></span>
                <span>{icon('cap')}{course}</span>
                <span>{icon('user')}Por {", ".join(class_contributors(item))}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with action:
        saved = is_saved(item["id"])
        label = ":material/star: Quitar de guardados" if saved else ":material/star: Guardar clase"
        state = "unsave" if saved else "save"
        st.button(
            label,
            key=f"detail-{state}-{item['id']}",
            on_click=toggle_saved,
            args=(item["id"],),
            use_container_width=True,
        )

    st.write("")
    show_flash_message()

    info_col, side_col = st.columns([1.55, 1], gap="medium")
    with info_col:
        with st.container(border=True):
            st.markdown('<div class="mark-card"></div>', unsafe_allow_html=True)
            st.markdown(block_title("¿Qué vimos?", "eye"), unsafe_allow_html=True)
            for content_item in item["content"]:
                st.write(f"- {content_item}")

            st.markdown('<div class="block-sep"></div>', unsafe_allow_html=True)
            st.markdown(block_title("Tarea", "clipboard"), unsafe_allow_html=True)
            st.write(item["task"] or "No hay tarea registrada.")

            st.markdown('<div class="block-sep"></div>', unsafe_allow_html=True)
            st.markdown(block_title("Instrucciones", "note"), unsafe_allow_html=True)
            st.write(item["instructions"] or "No hay instrucciones registradas.")

    with side_col:
        with st.container(border=True):
            st.markdown('<div class="mark-card"></div>', unsafe_allow_html=True)
            st.markdown(block_title("Material de apoyo", "doc"), unsafe_allow_html=True)
            st.caption("Material para descargar. En este prototipo los archivos son simulados.")
            rows = []
            for material in item["materials"]:
                if material["files"]:
                    for file_name in material["files"]:
                        kind = file_kind(file_name, material["type"])
                        glyph = "note" if kind == material["type"] else "doc"
                        rows.append(
                            f"""
                            <div class="file-item">
                                <span class="ic">{icon(glyph, 16)}</span>
                                <span class="grow">
                                    <span class="nm">{file_name}</span><br>
                                    <span class="sub">{kind} · {material['contributor']}</span>
                                </span>
                                <span class="dl" title="Archivo simulado: en este prototipo no se descarga">
                                    {icon('download', 13)}Descargar
                                </span>
                            </div>
                            """
                        )
                else:
                    rows.append(
                        f"""
                        <div class="file-item">
                            <span class="ic">{icon('note', 16)}</span>
                            <span>
                                <span class="nm">{material['type']}</span><br>
                                <span class="sub">Sin archivo · {material['contributor']}</span>
                            </span>
                        </div>
                        """
                    )
            if rows:
                st.markdown("".join(rows), unsafe_allow_html=True)
            else:
                st.caption("Todavía no hay material compartido para esta clase.")

    st.write("")
    with st.container(border=True):
        st.markdown('<div class="mark-highlight"></div>', unsafe_allow_html=True)
        text_col, action_col = st.columns([3, 1], gap="medium", vertical_alignment="center")
        with text_col:
            st.markdown(
                """
                <div class="section-title">¿Tienes información que pueda ayudar?</div>
                <p class="muted" style="margin:0.25rem 0 0 0">
                    Puedes aportar apuntes, instrucciones o material relacionado con esta clase.
                </p>
                """,
                unsafe_allow_html=True,
            )
        with action_col:
            st.button(
                "Aportar información de esta clase",
                key=f"detail-contribute-{item['id']}",
                type="primary",
                on_click=contribute_to_class,
                args=(item["id"],),
                use_container_width=True,
            )


def render_classes() -> None:
    classes = get_all_classes()
    profile = get_profile_data()

    # Vista de detalle cuando hay una clase seleccionada.
    if st.session_state.selected_class_id:
        selected = find_class(st.session_state.selected_class_id)
        if selected:
            render_class_detail(selected)
            return
        st.session_state.selected_class_id = None

    st.markdown(eyebrow("Clases", "search"), unsafe_allow_html=True)
    st.title("Buscar clases")
    st.caption("Encuentra rápidamente la información que necesitas.")
    show_flash_message()
    st.write("")

    subject_meta = get_subjects()
    subjects = ["Todas"] + [subject["name"] for subject in subject_meta]
    date_options = get_date_options(classes)

    # Los widgets se inicializan con los filtros vigentes. Si la fecha guardada
    # ya no existe (p. ej. tras restablecer el demo), volvemos a "Todas".
    # Los filtros son widgets controlados: el valor vigente vive en
    # `filters_snapshot` y se pasa como `index`/`value`. Así el filtro sobrevive
    # a la ida y vuelta al detalle, donde Streamlit recicla los widgets y
    # reinicia su valor.
    active = current_filters()
    if active["f_subject"] not in subjects:
        active["f_subject"] = "Todas"
    if active["f_date"] not in date_options:
        active["f_date"] = "Todas"

    with st.container(border=True):
        st.markdown('<div class="mark-card"></div>', unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(
            [1.15, 1.15, 1.55, 0.32, 0.75], vertical_alignment="bottom"
        )
        subject = col1.selectbox(
            "Asignatura", subjects, index=subjects.index(active["f_subject"])
        )
        selected_date = col2.selectbox(
            "Fecha",
            date_options,
            index=date_options.index(active["f_date"]),
            format_func=lambda value: "Todas" if value == "Todas" else format_display_date(value),
        )
        keyword = col3.text_input(
            "Palabra clave",
            value=active["f_keyword"],
            placeholder="Ej: ecuaciones, fotos, tarea…",
            help="Escribe y presiona Enter, o usa el botón de la lupa.",
        )
        # El listado ya se filtra al escribir; este botón cierra la acción para
        # quien prefiere confirmar con un clic.
        col4.button(
            ":material/search:",
            key="classes-search",
            type="primary",
            help="Aplicar los filtros",
            use_container_width=True,
        )
        col5.button(
            ":material/filter_alt_off: Limpiar",
            key="classes-clear-filters",
            on_click=reset_filters,
            help="Volver a mostrar todas las clases",
            use_container_width=True,
        )

    remember_filters(subject, selected_date, keyword)
    filtered = filter_classes(
        classes,
        subject=subject,
        selected_date=selected_date,
        keyword=keyword,
    )

    st.write("")
    st.markdown(
        f'<div class="result-count">Resultados encontrados: '
        f'<span class="num">{len(filtered)}</span></div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if not filtered:
        with st.container(border=True):
            st.markdown('<div class="mark-card"></div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="empty-box">
                    <div class="ring">{icon('search', 22)}</div>
                    <div class="ttl">Ninguna clase coincide con esos filtros</div>
                    <div class="txt">Prueba con menos filtros o una palabra más general.
                    Si la clase todavía no existe, puedes registrarla tú.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            _, center, _ = st.columns([1, 1.2, 1])
            center.button(
                "Aportar esta información",
                key="classes-empty-contribute",
                on_click=go_to,
                args=("Aportar información",),
                use_container_width=True,
            )
        return

    for item in filtered:
        render_class_row(item, profile["course"], key_prefix="classes")


def render_saved() -> None:
    profile = get_profile_data()
    saved = get_saved_classes()

    st.markdown(eyebrow("Guardados", "star"), unsafe_allow_html=True)
    st.title("Clases guardadas")
    st.caption("Aquí puedes encontrar las clases que dejaste pendientes para revisar después.")
    show_flash_message()
    st.write("")

    if not saved:
        with st.container(border=True):
            st.markdown('<div class="mark-card"></div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="empty-box">
                    <div class="ring">{icon('star', 22)}</div>
                    <div class="ttl">Todavía no tienes clases guardadas</div>
                    <div class="txt">Cuando encuentres una clase que quieras revisar después,
                    presiona Guardar.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            _, center, _ = st.columns([1, 1.2, 1])
            center.button(
                "Buscar clases",
                key="saved-empty-search",
                type="primary",
                on_click=go_to,
                args=("Clases",),
                use_container_width=True,
            )
        return

    for item in saved:
        with st.container(border=True):
            st.markdown('<div class="mark-row"></div>', unsafe_allow_html=True)
            info, actions = st.columns([3, 1], gap="medium", vertical_alignment="center")
            with info:
                st.markdown(
                    class_summary_html(item, profile["course"]), unsafe_allow_html=True
                )
            with actions:
                st.button(
                    "Ver clase",
                    key=f"saved-view-{item['id']}",
                    on_click=open_class,
                    args=(item["id"],),
                    use_container_width=True,
                )
                st.button(
                    ":material/delete: Quitar",
                    key=f"saved-unsave-{item['id']}",
                    on_click=toggle_saved,
                    args=(item["id"],),
                    use_container_width=True,
                )


def submit_contribution() -> None:
    """Callback del envío del formulario de aportes.

    Lee los campos desde `st.session_state` (todos tienen `key`), registra el
    aporte y deja la app en el detalle de la clase resultante."""
    profile = get_profile_data()
    target = st.session_state.contrib_target
    file_name = (st.session_state.get("c_file_name") or "").strip()
    material = {
        "contributor": profile["name"],
        "type": st.session_state.get("c_material_type") or MATERIAL_TYPES[0],
        "files": [file_name] if file_name else [],
    }
    st.session_state.form_error = None

    if target == NEW_CLASS_OPTION:
        subject = st.session_state.get("c_subject")
        topic = (st.session_state.get("c_topic") or "").strip()
        summary = (st.session_state.get("c_summary") or "").strip()
        if not subject or not topic or not summary:
            st.session_state.form_error = (
                "Completa los campos obligatorios (*) de la clase antes de enviar."
            )
            return
        contribution_date = st.session_state.get("c_date") or date(2026, 7, 29)
        target_id = f"USER-{uuid4().hex[:8]}"
        st.session_state.contributions.append(
            {
                "id": target_id,
                "subject": subject,
                "date": contribution_date.isoformat(),
                "topic": topic,
                "content": [line.strip() for line in summary.splitlines() if line.strip()],
                "task": (st.session_state.get("c_task") or "").strip(),
                "instructions": (st.session_state.get("c_instructions") or "").strip(),
                "materials": [material],
            }
        )
        st.session_state.flash_message = (
            f"Tu clase y su material quedaron disponibles para el resto. "
            f"Aporte registrado por {profile['name']}."
        )
    else:
        target_id = target
        find_class(target_id)["materials"].append(material)
        st.session_state.flash_message = (
            f"Tu material se agregó a la clase y ya está disponible para el resto. "
            f"Aporte registrado por {profile['name']}."
        )

    st.session_state.aportes_count += 1
    set_page("Clases", selected_class_id=target_id)


def render_contribution_form() -> None:
    st.markdown(eyebrow("Aportar", "plus"), unsafe_allow_html=True)
    st.title("Aportar información")
    st.caption(
        "Comparte información que pueda ayudar a otros estudiantes y apoderados a ponerse al día."
    )
    show_flash_message()
    st.write("")

    subjects = [subject["name"] for subject in get_subjects()]
    profile = get_profile_data()
    classes = get_all_classes()

    # El selector va FUERA del formulario para que la pantalla se actualice al
    # instante y muestre los campos correctos según lo elegido.
    def target_label(class_id: str) -> str:
        if class_id == NEW_CLASS_OPTION:
            return NEW_CLASS_OPTION
        item = next(cls for cls in classes if cls["id"] == class_id)
        return f"{item['subject']} · {format_display_date(item['date'])} · {item['topic']}"

    target = st.selectbox(
        "¿A qué clase quieres aportar material?",
        [NEW_CLASS_OPTION] + [cls["id"] for cls in classes],
        format_func=target_label,
        key="contrib_target",
    )
    is_new_class = target == NEW_CLASS_OPTION

    if st.session_state.get("form_error"):
        st.error(st.session_state.form_error)
        st.session_state.form_error = None

    with st.form("contribution-form"):
        if is_new_class:
            st.markdown(
                '<div class="block-title">Datos de la clase nueva</div>', unsafe_allow_html=True
            )
            col1, col2 = st.columns(2)
            col1.selectbox("Asignatura *", subjects, key="c_subject")
            col2.date_input(
                "Fecha de la clase *", value=date(2026, 7, 29), format="DD/MM/YYYY", key="c_date"
            )
            st.text_input("Tema de la clase *", key="c_topic")
            st.text_area("Contenido o resumen *", height=130, key="c_summary")
            st.text_input("Tarea", key="c_task")
            st.text_area("Instrucciones", height=95, key="c_instructions")
        else:
            selected_class = next(cls for cls in classes if cls["id"] == target)
            st.markdown(
                f"""
                <div class="block-title">Aportarás a esta clase</div>
                {class_summary_html(selected_class, profile['course'], with_chips=False)}
                """,
                unsafe_allow_html=True,
            )
            st.caption("Puedes cambiar la clase con el selector de arriba.")

        st.markdown('<div class="block-sep"></div>', unsafe_allow_html=True)
        st.markdown('<div class="block-title">Tu material</div>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        col3.selectbox("Tipo de material *", MATERIAL_TYPES, key="c_material_type")
        col4.text_input("Nombre del archivo", key="c_file_name")
        st.caption(
            "En este prototipo el archivo no se carga realmente; solo se registra su nombre."
        )
        st.write("")
        st.form_submit_button(
            "Enviar material", type="primary", on_click=submit_contribution
        )

    new_classes = [item for item in get_all_classes() if item["id"].startswith("USER-")]
    if new_classes:
        st.write("")
        st.markdown(
            '<div class="section-title">Clases nuevas registradas en esta sesión</div>',
            unsafe_allow_html=True,
        )
        st.write("")
        for item in new_classes:
            render_class_row(item, profile["course"], key_prefix="contrib")


def render_about() -> None:
    st.markdown(eyebrow("Prototipo", "info"), unsafe_allow_html=True)
    st.title("Acerca del prototipo")
    st.caption("Qué resuelve, para quién y hasta dónde llega esta demostración.")
    st.write("")

    col1, col2 = st.columns([1.1, 1], gap="medium")
    with col1:
        with st.container(border=True):
            st.markdown('<div class="mark-card"></div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="block-title">Problema</div>
                <p class="muted">Recuperar contenidos, tareas e instrucciones cuando la
                información de una clase no fue registrada de forma completa.</p>
                <div class="block-sep"></div>
                <div class="block-title">Usuarios</div>
                <p class="muted">Estudiantes y apoderados.</p>
                <div class="block-sep"></div>
                <div class="block-title">Objetivo</div>
                <p class="muted">Facilitar la recuperación de información escolar mediante una
                experiencia simple y organizada.</p>
                """,
                unsafe_allow_html=True,
            )
    with col2:
        with st.container(border=True):
            st.markdown('<div class="mark-card"></div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="block-title">Funciones implementadas</div>
                <div class="chips">
                    <span class="chip">Selección de perfil</span>
                    <span class="chip">Inicio</span>
                    <span class="chip">Consulta de clases</span>
                    <span class="chip">Filtros</span>
                    <span class="chip">Búsqueda por palabra clave</span>
                    <span class="chip">Detalle de clase</span>
                    <span class="chip">Guardados</span>
                    <span class="chip">Aporte temporal</span>
                    <span class="chip">Restablecimiento del demo</span>
                </div>
                <div class="block-sep"></div>
                <div class="block-title">Funciones simuladas</div>
                <div class="chips">
                    <span class="chip">Inicio de sesión real</span>
                    <span class="chip">Almacenamiento permanente</span>
                    <span class="chip">Archivos y fotografías reales</span>
                    <span class="chip">Validación oficial de contenidos</span>
                    <span class="chip">Integración con colegios</span>
                    <span class="chip">Notificaciones</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(f'<p class="footer-note">{APP_NOTICE}</p>', unsafe_allow_html=True)


def main() -> None:
    inject_styles()
    initialize_state()
    render_sidebar()

    if not st.session_state.selected_profile and st.session_state.current_page != LOGIN_PAGE:
        st.session_state.current_page = LOGIN_PAGE

    current_page = st.session_state.current_page
    if current_page == LOGIN_PAGE:
        render_login()
    elif current_page == "Inicio":
        render_start()
    elif current_page == "Clases":
        render_classes()
    elif current_page == "Guardados":
        render_saved()
    elif current_page == "Aportar información":
        render_contribution_form()
    elif current_page == "Acerca del prototipo":
        render_about()
    else:
        render_start()


if __name__ == "__main__":
    main()
