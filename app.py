from __future__ import annotations

from datetime import date, datetime
from typing import Any
from uuid import uuid4

import streamlit as st

from data import APP_NAME, APP_NOTICE, APP_TAGLINE, load_base_data


# Secciones que aparecen en la navegación lateral (después de ingresar).
NAV_PAGES = [
    "Panel",
    "Clases",
    "Aportar información",
    "Acerca del prototipo",
]

NAV_ICONS = {
    "Panel": "🏠",
    "Clases": "📚",
    "Aportar información": "➕",
    "Acerca del prototipo": "ℹ️",
}

# Valores por defecto de los filtros de la sección Clases. Cada filtro es un
# widget con `key`, por lo que Streamlit conserva su valor entre reruns (evita
# el bug de "hay que hacer clic dos veces" que ocurre al usar `index=`).
FILTER_DEFAULTS = {
    "f_subject": "Todas",
    "f_date": "Todas",
    "f_keyword": "",
}

# Nombres en español para mostrar la fecha con día de la semana (evitamos
# depender de la configuración regional del sistema, que en Windows es poco
# fiable).
WEEKDAYS_ES = [
    "lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo",
]
MONTHS_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]

# Tipos de material que un apoderado o estudiante puede aportar.
MATERIAL_TYPES = ["Fotografía de cuaderno", "Guía", "Tarea", "Instrucción", "Otro"]


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
        .stApp {
            background: linear-gradient(180deg, #f8fbff 0%, #eef5ff 100%);
        }
        /* Tarjetas: contenedores nativos con borde (st.container(border=True)) */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 16px;
            border: 1px solid rgba(25, 76, 146, 0.18);
            background: #ffffff;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        }
        /* Encabezado de cada grupo de asignatura */
        .subject-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 1.4rem 0 0.6rem 0;
            padding-bottom: 0.4rem;
            border-bottom: 2px solid rgba(25, 76, 146, 0.15);
            color: #0f3d75;
            font-size: 1.25rem;
            font-weight: 700;
        }
        .subject-header .count {
            font-size: 0.85rem;
            font-weight: 600;
            color: #64748b;
        }
        .eyebrow {
            color: #2b6cb0;
            font-weight: 700;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .hero {
            border-radius: 18px;
            padding: 1.3rem 1.7rem;
            background: linear-gradient(135deg, #0f3d75 0%, #2b6cb0 100%);
            color: #ffffff;
            box-shadow: 0 14px 30px rgba(15, 61, 117, 0.22);
        }
        .hero-badge {
            display: inline-block;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.16);
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin-bottom: 0.6rem;
        }
        .hero h1 {
            margin: 0 0 0.3rem 0;
            font-size: 1.75rem;
            line-height: 1.15;
        }
        .hero p {
            margin: 0.15rem 0 0 0;
            color: rgba(255, 255, 255, 0.92);
            font-size: 0.95rem;
        }
        .meta {
            color: #64748b;
            font-size: 0.9rem;
        }
        .card-title {
            color: #0f3d75;
            font-weight: 700;
            font-size: 1.12rem;
            line-height: 1.25;
            margin: 0.35rem 0 0.55rem 0;
        }
        .file-chip {
            display: inline-block;
            padding: 0.32rem 0.7rem;
            margin: 0.15rem 0.3rem 0.15rem 0;
            border-radius: 999px;
            background: #eff6ff;
            color: #0f3d75;
            border: 1px solid #bfdbfe;
            font-size: 0.85rem;
        }
        .notice {
            border-left: 4px solid #0f3d75;
            background: #f1f6ff;
            border-radius: 10px;
            padding: 0.8rem 1rem;
            color: #334155;
        }
        div[data-testid="stMetricValue"] {
            color: #0f3d75;
        }
        /* Botón primario más notorio (ingreso y envío de formularios). */
        div.stButton > button[kind="primary"],
        div.stFormSubmitButton > button[kind="primary"] {
            font-size: 1.05rem;
            font-weight: 700;
            padding: 0.7rem 1rem;
            border-radius: 12px;
            box-shadow: 0 10px 22px rgba(15, 61, 117, 0.28);
            transition: transform 0.05s ease, box-shadow 0.2s ease;
        }
        div.stButton > button[kind="primary"]:hover,
        div.stFormSubmitButton > button[kind="primary"]:hover {
            box-shadow: 0 12px 26px rgba(15, 61, 117, 0.38);
            transform: translateY(-1px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
        st.session_state.current_page = "Inicio"
    if "selected_class_id" not in st.session_state:
        st.session_state.selected_class_id = None
    if "flash_message" not in st.session_state:
        st.session_state.flash_message = None
    for key, value in FILTER_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_filters() -> None:
    for key, value in FILTER_DEFAULTS.items():
        st.session_state[key] = value


def reset_demo() -> None:
    st.session_state.base_data = load_base_data()
    st.session_state.contributions = []
    st.session_state.aportes_count = 0
    st.session_state.selected_class_id = None
    st.session_state.current_page = "Panel" if st.session_state.selected_profile else "Inicio"
    st.session_state.flash_message = "El demo fue restablecido a los datos originales."
    reset_filters()


def format_display_date(raw_date: str) -> str:
    return datetime.strptime(raw_date, "%Y-%m-%d").strftime("%d/%m/%Y")


def format_class_date(raw_date: str) -> str:
    """Ej.: 'miércoles 29 de julio de 2026'."""
    parsed = datetime.strptime(raw_date, "%Y-%m-%d")
    return f"{WEEKDAYS_ES[parsed.weekday()]} {parsed.day} de {MONTHS_ES[parsed.month - 1]} de {parsed.year}"


def class_files(item: dict[str, Any]) -> list[str]:
    return [file_name for material in item["materials"] for file_name in material["files"]]


def class_contributors(item: dict[str, Any]) -> list[str]:
    # Nombres únicos conservando el orden en que aportaron.
    return list(dict.fromkeys(material["contributor"] for material in item["materials"]))


def get_all_classes() -> list[dict[str, Any]]:
    classes = st.session_state.base_data["classes"] + st.session_state.contributions
    return sorted(classes, key=lambda item: item["date"], reverse=True)


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


def set_page(page: str, selected_class_id: str | None = None) -> None:
    st.session_state.current_page = page
    st.session_state.selected_class_id = selected_class_id


def open_class(class_id: str) -> None:
    set_page("Clases", selected_class_id=class_id)
    st.rerun()


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
        st.markdown(f"### 🏫 {APP_NAME}")
        profile = get_profile_data()
        st.caption(f"Perfil activo · {st.session_state.selected_profile}")
        st.write(f"**{profile['name']}**")
        st.write(f"{profile['student_name']} · {profile['course']}")
        st.caption(profile["school"])
        st.divider()

        current = st.session_state.current_page
        index = NAV_PAGES.index(current) if current in NAV_PAGES else 0
        page = st.radio(
            "Ir a",
            options=NAV_PAGES,
            index=index,
            format_func=lambda name: f"{NAV_ICONS[name]}  {name}",
        )
        if page != current:
            set_page(page)
            st.rerun()

        st.divider()
        if st.button("↺ Restablecer demo", key="sidebar-reset-demo", use_container_width=True):
            reset_demo()
            st.rerun()
        if st.button("Cambiar perfil", key="sidebar-change-profile", use_container_width=True):
            st.session_state.selected_profile = None
            st.session_state.current_page = "Inicio"
            st.session_state.selected_class_id = None
            st.rerun()


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
            ]
        ).lower()
        if keyword_normalized and keyword_normalized not in haystack:
            continue
        filtered.append(item)
    return filtered


def render_class_card(item: dict[str, Any]) -> None:
    with st.container(border=True):
        st.markdown(f"<div class='eyebrow'>{item['subject']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card-title'>{item['topic']}</div>", unsafe_allow_html=True)
        st.caption(f"🗓️ Clase del {format_class_date(item['date'])}")

        files = class_files(item)
        tags = []
        if item["task"]:
            tags.append("📝 Con tarea")
        if files:
            tags.append(f"📎 {len(files)} archivo(s)")
        if tags:
            st.caption(" · ".join(tags))

        contributors = class_contributors(item)
        if len(contributors) == 1:
            st.caption(f"👤 Compartido por {contributors[0]}")
        else:
            st.caption(f"👥 Aportado por {len(contributors)} personas: {', '.join(contributors)}")

        if st.button("Ver material", key=f"view-{item['id']}", use_container_width=True):
            open_class(item["id"])


# ---------------------------------------------------------------------------
# Páginas
# ---------------------------------------------------------------------------


def render_home() -> None:
    # Contenido centrado y estrecho para que el inicio quepa sin scroll.
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.markdown(
            f"""
            <div class="hero">
                <span class="hero-badge">Prototipo académico</span>
                <h1>{APP_NAME}</h1>
                <p>{APP_TAGLINE}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown("#### Ingresar al demo")
            selected = st.selectbox("¿Con qué perfil quieres entrar?", ["Apoderado", "Estudiante"])
            if selected == "Apoderado":
                st.caption("👩 Entrarás como Carolina Soto, apoderada de Martín Soto.")
            else:
                st.caption("🧒 Entrarás como Martín Soto, estudiante de 5° Básico B.")
            st.caption(
                "ℹ️ Ambos perfiles ven y hacen lo mismo. El perfil solo define el nombre con el que "
                "quedan registrados los materiales que aportes."
            )
            if st.button("Ingresar al demo →", key="home-enter-demo", type="primary", use_container_width=True):
                st.session_state.selected_profile = selected
                st.session_state.current_page = "Panel"
                st.rerun()

        st.caption(
            "**¿Qué puedes hacer aquí?**  📚 Consultar clases · 🔎 Ver el detalle de cada clase · "
            "➕ Aportar material faltante."
        )


def render_dashboard() -> None:
    profile = get_profile_data()

    st.title(f"Hola, {profile['name']} 👋")
    st.caption(f"{profile['student_name']} · {profile['course']} · {profile['school']}")
    show_flash_message()

    st.write("")
    st.markdown("#### ¿Qué quieres hacer?")
    quick1, quick2 = st.columns(2)
    if quick1.button("📚 Ver las clases y su material", key="dash-classes", use_container_width=True):
        set_page("Clases")
        st.rerun()
    if quick2.button("➕ Aportar información", key="dash-contribute", use_container_width=True):
        set_page("Aportar información")
        st.rerun()


def render_class_detail(item: dict[str, Any]) -> None:
    if st.button("← Volver a las clases", key="detail-back"):
        set_page("Clases")
        st.rerun()

    st.markdown(f"<div class='eyebrow'>{item['subject']}</div>", unsafe_allow_html=True)
    st.title(item["topic"])
    st.caption(f"🗓️ Clase del {format_class_date(item['date'])}")

    info_col, side_col = st.columns([1.6, 1])
    with info_col:
        with st.container(border=True):
            st.markdown("#### Contenidos vistos")
            for content_item in item["content"]:
                st.write(f"- {content_item}")
        with st.container(border=True):
            st.markdown("#### Tarea")
            st.write(item["task"] or "Sin tarea registrada.")
            st.markdown("#### Instrucciones")
            st.write(item["instructions"] or "Sin instrucciones registradas.")
    with side_col:
        materials = item["materials"]
        with st.container(border=True):
            st.markdown(f"#### Material compartido ({len(materials)})")
            for index, material in enumerate(materials):
                st.write(f"**{material['contributor']}**")
                st.caption(material["type"])
                if material["files"]:
                    chips = "".join(
                        f"<span class='file-chip'>{name}</span>" for name in material["files"]
                    )
                    st.markdown(chips, unsafe_allow_html=True)
                else:
                    st.caption("Sin archivos adjuntos.")
                if index < len(materials) - 1:
                    st.divider()

    st.markdown(
        "<div class='notice'><strong>Nota:</strong> Este prototipo utiliza información simulada con fines académicos.</div>",
        unsafe_allow_html=True,
    )


def render_classes() -> None:
    classes = get_all_classes()

    # Vista de detalle cuando hay una clase seleccionada.
    if st.session_state.selected_class_id:
        selected = next(
            (item for item in classes if item["id"] == st.session_state.selected_class_id), None
        )
        if selected:
            render_class_detail(selected)
            return
        st.session_state.selected_class_id = None

    st.title("Clases")
    st.caption("Filtra por asignatura, fecha o palabra clave para encontrar una clase.")
    show_flash_message()

    subject_meta = get_subjects()
    subjects = ["Todas"] + [subject["name"] for subject in subject_meta]
    date_options = get_date_options(classes)

    # Si el filtro de fecha apunta a una fecha que ya no existe (p. ej. tras
    # restablecer el demo), volvemos a "Todas" para no romper el selectbox.
    if st.session_state.f_date not in date_options:
        st.session_state.f_date = "Todas"

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        # Widgets con `key`: Streamlit guarda el valor solo (un clic, no dos).
        col1.selectbox("Asignatura", subjects, key="f_subject")
        col2.selectbox(
            "Fecha",
            date_options,
            key="f_date",
            format_func=lambda value: "Todas las fechas" if value == "Todas" else format_display_date(value),
        )
        col3.text_input(
            "Palabra clave",
            key="f_keyword",
            placeholder="Ejemplo: fracciones, guía",
        )
        st.button("Limpiar filtros", key="classes-clear-filters", on_click=reset_filters)

    filtered = filter_classes(
        classes,
        subject=st.session_state.f_subject,
        selected_date=st.session_state.f_date,
        keyword=st.session_state.f_keyword,
    )

    st.write(f"**{len(filtered)}** clase(s) encontrada(s)")

    if not filtered:
        with st.container(border=True):
            st.markdown("##### 🔍 Sin resultados")
            st.write("No encontramos información para los filtros seleccionados.")
            if st.button("➕ Aportar esta información", key="classes-empty-contribute"):
                set_page("Aportar información")
                st.rerun()
        return

    # Agrupamos las clases por asignatura para que cada bloque tenga un título
    # claro y las tarjetas se lean como secciones separadas.
    icons = {subject["name"]: subject["icon"] for subject in subject_meta}
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in filtered:
        grouped.setdefault(item["subject"], []).append(item)

    ordered = [subject["name"] for subject in subject_meta if subject["name"] in grouped]
    ordered += [name for name in grouped if name not in ordered]

    for subject_name in ordered:
        items = grouped[subject_name]
        st.markdown(
            f"<div class='subject-header'>{icons.get(subject_name, '📚')} {subject_name}"
            f"<span class='count'>· {len(items)} clase(s)</span></div>",
            unsafe_allow_html=True,
        )
        columns = st.columns(2)
        for index, item in enumerate(items):
            with columns[index % 2]:
                render_class_card(item)


NEW_CLASS_OPTION = "➕ Registrar una clase nueva"


def render_contribution_form() -> None:
    st.title("Aportar información")
    st.caption(
        "Sube material de una clase para que otros apoderados y estudiantes puedan consultarlo. "
        "Puedes aportar a una clase que ya existe o registrar una nueva. Se guarda solo durante esta sesión."
    )
    show_flash_message()

    subjects = [subject["name"] for subject in get_subjects()]
    profile = get_profile_data()
    classes = get_all_classes()

    # El selector va FUERA del formulario para que la pantalla se actualice al
    # instante y muestre los campos correctos según lo elegido.
    def target_label(class_id: str) -> str:
        if class_id == NEW_CLASS_OPTION:
            return NEW_CLASS_OPTION
        item = next(cls for cls in classes if cls["id"] == class_id)
        return f"{item['subject']} · {format_class_date(item['date'])} · {item['topic']}"

    target = st.selectbox(
        "¿A qué clase quieres aportar material?",
        [NEW_CLASS_OPTION] + [cls["id"] for cls in classes],
        format_func=target_label,
        key="contrib_target",
    )
    is_new_class = target == NEW_CLASS_OPTION

    with st.form("contribution-form"):
        if is_new_class:
            st.markdown("**Datos de la clase nueva**")
            col1, col2 = st.columns(2)
            subject = col1.selectbox("Asignatura *", subjects)
            contribution_date = col2.date_input("Fecha de la clase *", value=date(2026, 7, 29), format="DD/MM/YYYY")
            topic = st.text_input("Tema de la clase *")
            summary = st.text_area("Contenido o resumen *", height=140)
            task = st.text_input("Tarea")
            instructions = st.text_area("Instrucciones", height=100)
        else:
            subject = topic = summary = task = instructions = ""
            contribution_date = None
            st.info(f"Aportarás material a: **{target_label(target)}**")

        st.markdown("**Tu material**")
        col3, col4 = st.columns(2)
        material_type = col3.selectbox("Tipo de material *", MATERIAL_TYPES)
        file_name = col4.text_input("Nombre de archivo simulado")
        submitted = st.form_submit_button("Enviar material", type="primary")

    if submitted:
        material = {
            "contributor": profile["name"],
            "type": material_type,
            "files": [file_name.strip()] if file_name.strip() else [],
        }

        if is_new_class:
            if not subject or not topic.strip() or not summary.strip():
                st.error("Completa los campos obligatorios (*) de la clase antes de enviar.")
                return
            target_id = f"USER-{uuid4().hex[:8]}"
            st.session_state.contributions.append(
                {
                    "id": target_id,
                    "subject": subject,
                    "date": contribution_date.isoformat(),
                    "topic": topic.strip(),
                    "content": [line.strip() for line in summary.splitlines() if line.strip()],
                    "task": task.strip(),
                    "instructions": instructions.strip(),
                    "materials": [material],
                }
            )
            st.session_state.flash_message = "Tu clase y su material quedaron disponibles para el resto."
        else:
            target_id = target
            existing = next(cls for cls in get_all_classes() if cls["id"] == target_id)
            existing["materials"].append(material)
            st.session_state.flash_message = "Tu material se agregó a la clase y ya está disponible para el resto."

        st.session_state.aportes_count += 1
        set_page("Clases", selected_class_id=target_id)
        st.rerun()

    new_classes = [item for item in get_all_classes() if item["id"].startswith("USER-")]
    if new_classes:
        st.divider()
        st.subheader("Clases nuevas registradas en esta sesión")
        columns = st.columns(2)
        for index, item in enumerate(new_classes):
            with columns[index % 2]:
                render_class_card(item)


def render_about() -> None:
    st.title("Acerca del prototipo")

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("#### El proyecto")
            st.write("**Problema:** recuperar materia, tareas e instrucciones cuando la información de la clase quedó incompleta.")
            st.write("**Usuarios:** apoderados y estudiantes de educación escolar.")
            st.write("**Objetivo:** un flujo simple para consultar clases por asignatura y fecha, y aportar lo que falta.")
    with col2:
        with st.container(border=True):
            st.markdown("#### Funciones del demo")
            st.write("✅ Selección de perfil de demostración.")
            st.write("✅ Consulta por asignatura, fecha y palabra clave.")
            st.write("✅ Vista de detalle de cada clase.")
            st.write("✅ Registro temporal de aportes.")
            st.write("✅ Restablecimiento del demo.")

    with st.container(border=True):
        st.markdown("#### Funciones simuladas")
        st.caption("Inicio de sesión · Archivos y fotografías reales · Integración con el colegio · Notificaciones.")

    st.markdown(f"<div class='notice'>{APP_NOTICE}</div>", unsafe_allow_html=True)


def main() -> None:
    inject_styles()
    initialize_state()
    render_sidebar()

    if not st.session_state.selected_profile and st.session_state.current_page != "Inicio":
        st.session_state.current_page = "Inicio"

    current_page = st.session_state.current_page
    if current_page == "Inicio":
        render_home()
    elif current_page == "Panel":
        render_dashboard()
    elif current_page == "Clases":
        render_classes()
    elif current_page == "Aportar información":
        render_contribution_form()
    elif current_page == "Acerca del prototipo":
        render_about()
    else:
        render_dashboard()


if __name__ == "__main__":
    main()
