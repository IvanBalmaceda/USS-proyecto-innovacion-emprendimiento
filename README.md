# Aula al Día

Prototipo web en Streamlit para demostrar cómo un apoderado o estudiante puede recuperar información escolar de una clase con datos ficticios.

## Objetivo

Mostrar un flujo simple para consultar materia, tareas, instrucciones, fechas y archivos simulados por curso, asignatura y fecha, además de permitir registrar un aporte temporal durante la sesión.

## Novedades de la versión V2

Esta iteración evoluciona el prototipo hacia una navegación más simple y comprensible,
sin cambiar la tecnología ni los datos simulados.

- **Nueva navegación lateral**: Inicio, Clases, Guardados, Aportar información y Acerca
  del prototipo, con la sección activa siempre marcada. Debajo se mantienen
  *Restablecer demo* y *Cambiar perfil*.
- **Nueva pantalla Inicio**: saludo al usuario, acceso principal *Buscar una clase*,
  hasta tres clases recientes y un resumen de los guardados. El mensaje de bienvenida
  cambia según el perfil (apoderado o estudiante).
- **Clases**: la pantalla se llama *Buscar clases* y muestra los resultados como filas
  simples con asignatura, tema, fecha, curso, si tiene tarea, cantidad de archivos y
  quién compartió. El botón pasó de *Ver material* a **Ver clase**.
- **Guardados**: nueva sección que conserva las clases marcadas durante la sesión
  (`saved_class_ids`). Se puede guardar o quitar desde el listado y desde el detalle,
  con estado vacío que invita a buscar clases. *Restablecer demo* también los borra.
- **Detalle de clase** reorganizado en bloques: identificación (asignatura, tema, fecha
  y curso), *¿Qué vimos?*, *Tarea*, *Instrucciones*, *Material de apoyo* y un cierre con
  *¿Tienes información que pueda ayudar?* que abre el formulario con la clase
  preseleccionada. Incluye *Volver a clases* conservando los filtros aplicados.
- **Búsqueda por nombre de archivo**, además de asignatura, tema, contenidos, tarea e
  instrucciones.
- **Aportar información** con textos más claros; el campo pasó a llamarse *Nombre del
  archivo* y advierte que el archivo no se carga realmente. El mensaje de éxito indica
  quién realizó el aporte.
- **Diseño**: azul como color principal, fondo claro y tarjetas con doble bisel
  (bandeja exterior y núcleo interior con radios concéntricos). Tipografía Plus Jakarta
  Sans + Geist, iconos de línea propios en SVG, sombras ambientales tintadas y movimiento
  con curvas `cubic-bezier` personalizadas (entrada ligada al scroll, menú escalonado,
  botones con física al presionar).
- **Adelanto en los resultados**: cada fila muestra *Vimos* y *Tarea* recortados, para
  reconocer la clase sin abrirla.
- **Material de apoyo**: indica el formato del archivo (PDF, Imagen, Documento) deducido
  de su nombre y lo marca como material para descargar. La acción se muestra inerte
  (borde discontinuo y cursor bloqueado) porque el archivo es simulado.
- **Avatar del perfil**: cada perfil tiene su avatar de línea según si es adulto o
  estudiante y su género, tomado de los campos `gender` / `student_gender` de `data.py`
  (no se deduce del nombre). Aparece en el ingreso, en la barra lateral y junto al saludo
  de Inicio; el tratamiento (`role_label`) muestra "Apoderada" o "Estudiante".
- **Palabra clave**: `st.text_input` aplica el valor al presionar Enter o al salir del
  campo; ese es el comportamiento nativo de Streamlit. El botón de la lupa está para
  quien prefiera confirmar con un clic. Un filtrado letra por letra requeriría un
  componente propio, fuera del alcance del prototipo.

### Detalles técnicos de la V2

- Toda la navegación usa callbacks `on_click` / `on_change` en lugar de `st.rerun()` a
  mitad de pantalla, de modo que cada pasada dibuja una sola página con el estado final.
- Los filtros son widgets controlados: el valor vigente vive en
  `st.session_state.filters_snapshot` y se pasa como `index`/`value`. Streamlit reinicia
  el valor de un widget cuando deja de dibujarse (al entrar al detalle), por lo que esta
  copia es la que permite volver al listado con los mismos filtros y resultados.
- Las tarjetas llevan un `<div class="mark-...">` como marcador porque en Streamlit 1.54
  el borde de `st.container(border=True)` se aplica al propio `stVerticalBlock`, que no
  expone un `data-testid` propio.

## Funciones implementadas

- Pantalla de ingreso simulado con selección de perfil (apoderado o estudiante).
- Navegación lateral de cinco secciones con indicación de la sección actual.
- Inicio con acceso a la búsqueda, clases recientes y resumen de guardados.
- Consulta de clases con filtros por asignatura, fecha y palabra clave (incluye nombres
  de archivo) y botón para limpiar filtros.
- Detalle de clase con contenidos, tarea, instrucciones y material de apoyo.
- Guardar y quitar clases de *Guardados* durante la sesión.
- Formulario para aportar material a una clase existente o registrar una clase nueva,
  con la clase preseleccionada cuando se llega desde su detalle.
- Registro temporal de aportes en `st.session_state`, indicando quién aportó.
- Botón para restablecer el demo, que también limpia guardados y preselecciones.

## Estado de sesión

| Clave | Para qué sirve |
| --- | --- |
| `base_data` | Copia de los datos simulados de la sesión. |
| `contributions` | Clases nuevas registradas durante la sesión. |
| `aportes_count` | Cantidad de aportes enviados. |
| `selected_profile` | Perfil elegido en el ingreso. |
| `current_page` / `nav_radio` | Página actual y sección marcada en el menú. |
| `selected_class_id` | Clase abierta en el detalle. |
| `saved_class_ids` | Clases guardadas para revisar después. |
| `selected_contribution_class_id` | Clase preseleccionada al aportar desde un detalle. |
| `contrib_target` | Destino elegido en el formulario de aportes. |
| `filters_snapshot` | Filtros vigentes de la sección Clases. |
| `flash_message` / `form_error` | Mensajes de éxito y de validación. |

## Funciones simuladas

- Inicio de sesión real.
- Almacenamiento permanente.
- Archivos y fotografías reales.
- Validación oficial de contenidos.
- Integración con colegios.
- Notificaciones.

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
├── test_app.py
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

## Pruebas

```bash
python -m unittest test_app
```

Las pruebas usan `streamlit.testing.v1.AppTest` y cubren el ingreso, la navegación,
Inicio, la búsqueda (incluida la búsqueda por nombre de archivo), el retorno al listado
conservando filtros, guardar y quitar clases desde el listado, el detalle y la sección
Guardados, el aporte con clase preseleccionada, el aporte desde el menú sin preselección
y el restablecimiento del demo.
