# Aula al Día

Prototipo web en Streamlit para demostrar cómo un apoderado o estudiante puede recuperar información escolar de una clase con datos ficticios.

## Objetivo

Mostrar un flujo simple para consultar materia, tareas, instrucciones, fechas y archivos simulados por curso, asignatura y fecha, además de permitir registrar un aporte temporal durante la sesión.

## Funciones implementadas

- Pantalla de ingreso simulado con selección de perfil.
- Navegación lateral simple con cuatro secciones: **Panel**, **Clases**, **Aportar información** y **Acerca del prototipo**.
- Panel con resumen: métricas, clases recientes, tareas pendientes y accesos rápidos.
- Sección **Clases** unificada: filtros por asignatura, fecha y palabra clave, resultados agrupados por asignatura en tarjetas y vista de detalle en el mismo lugar. Cada tarjeta indica la fecha de la clase (con día de la semana) y quién compartió el material.
- Cada clase puede reunir material aportado por **más de un apoderado o estudiante**; el detalle lista cada aporte por separado.
- Vista de detalle con contenidos, tarea, instrucciones y el material compartido por cada persona.
- Formulario para aportar material a una clase existente o registrar una clase nueva.
- Registro temporal de aportes en `st.session_state`.
- Botón para restablecer el demo y eliminar cambios de la sesión.

## Funciones simuladas

- Inicio de sesión real.
- Adjuntos descargables y fotografías reales.
- Integración con el establecimiento.
- Persistencia permanente de datos.
- Notificaciones o correos.

## Requisitos

- Python 3.10 o superior.
- `pip` disponible en el entorno.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución local

Comando exacto para iniciar la aplicación:

```bash
streamlit run app.py
```

Luego abre la URL local que muestre Streamlit en la terminal, normalmente `http://localhost:8501`.

## Estructura del proyecto

```text
proyecto-s2-innovacion-emprendimiento/
├── .streamlit/
│   └── config.toml
├── app.py
├── data.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Publicación en Streamlit Community Cloud

1. Sube estos archivos a un repositorio de GitHub.
2. Entra a Streamlit Community Cloud.
3. Crea una nueva app conectando ese repositorio.
4. Selecciona `app.py` como archivo principal.
5. Streamlit instalará automáticamente lo definido en `requirements.txt`.
6. Publica la aplicación.

No se requieren secretos, variables de entorno ni servicios externos.

## Datos y almacenamiento

- Todos los datos del demo son ficticios y de uso académico.
- Los aportes nuevos se almacenan solo durante la sesión actual usando `st.session_state`.
- Al reiniciar la app o usar `Restablecer demo`, se vuelven a cargar los datos de ejemplo.
