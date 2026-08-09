# ANALISIS_NAVEGACION

## 1. Resumen general del prototipo

### Objetivo que representa
`Aula al Día` es un prototipo académico que representa un flujo simple para que un apoderado o estudiante recupere información faltante de una clase: contenidos vistos, tarea, instrucciones y materiales compartidos por otros usuarios del mismo curso.

El propósito observable en el código no es operar como plataforma oficial del colegio, sino como apoyo colaborativo entre apoderados y estudiantes usando datos simulados.

### Tecnología utilizada
- `Python`
- `Streamlit`
- Estado de sesión con `st.session_state`
- Datos mock locales definidos en `data.py`
- Pruebas automatizadas con `unittest` y `streamlit.testing.v1`

No hay base de datos, backend externo, autenticación real, almacenamiento de archivos ni integraciones externas.

### Estructura principal del proyecto
- `app.py`: interfaz, navegación, estado de sesión y lógica principal.
- `data.py`: datos ficticios base del demo, perfiles y clases.
- `test_app.py`: pruebas de flujos reales implementados.
- `README.md`: descripción general del prototipo.
- `.streamlit/config.toml`: configuración visual básica de Streamlit.

## 2. Mapa completo de navegación

## Rutas y estados reales
El prototipo no usa múltiples páginas físicas de Streamlit. Toda la navegación se controla con `st.session_state.current_page` y, para el detalle de clase, con `st.session_state.selected_class_id`.

### 2.1 Pantalla de inicio
- Nombre lógico: `Inicio`
- Se muestra cuando no hay perfil seleccionado.
- Contiene:
  - Hero principal con nombre del prototipo y tagline.
  - Selector de perfil: `Apoderado` o `Estudiante`.
  - Botón `Ingresar al demo →`.
- Resultado:
  - Al ingresar, guarda el perfil en sesión y lleva a `Panel`.

### 2.2 Selección de perfil
- No existe como pantalla independiente.
- Es un bloque dentro de `Inicio`.
- Solo permite elegir entre dos perfiles demo:
  - `Apoderado`
  - `Estudiante`
- Ambos perfiles tienen exactamente las mismas funciones.
- La única diferencia real es el nombre del contribuyente que queda registrado al aportar material.

### 2.3 Panel principal
- Nombre lógico: `Panel`
- Es la primera vista después del ingreso.
- Contiene:
  - saludo con nombre del perfil;
  - datos del estudiante, curso y colegio;
  - botón `📚 Ver las clases y su material`;
  - botón `➕ Aportar información`.
- No muestra métricas, resumen numérico ni listado de clases recientes en el código actual.

### 2.4 Clases
- Nombre lógico: `Clases`
- Vista principal de consulta.
- Contiene:
  - filtros por asignatura, fecha y palabra clave;
  - botón `Limpiar filtros`;
  - listado de clases agrupadas por asignatura;
  - tarjetas por clase con botón `Ver material`.
- Si no hay resultados, muestra un estado vacío con botón `➕ Aportar esta información`.

### 2.5 Detalle de una clase
- No es una página separada.
- Es un estado interno de `Clases` cuando `selected_class_id` tiene valor.
- Contiene:
  - botón `← Volver a las clases`;
  - asignatura;
  - tema;
  - fecha;
  - contenidos vistos;
  - tarea;
  - instrucciones;
  - material compartido por cada contribuyente;
  - aviso de que la información es simulada.

### 2.6 Aportar información
- Nombre lógico: `Aportar información`
- Tiene dos modos:
  - aportar a una clase existente;
  - registrar una clase nueva.
- Contiene:
  - selector de clase destino;
  - formulario dinámico según el destino elegido;
  - botón `Enviar material`.
- Después del envío exitoso:
  - redirige a `Clases`;
  - abre automáticamente el detalle de la clase afectada.

### 2.7 Acerca del prototipo
- Nombre lógico: `Acerca del prototipo`
- Resume:
  - problema;
  - usuarios;
  - objetivo;
  - funciones del demo;
  - funciones simuladas;
  - aviso académico.

### 2.8 Otras vistas o estados existentes
- Barra lateral visible solo después de seleccionar perfil.
- Estado vacío de resultados en `Clases`.
- Mensajes de éxito temporales (`flash_message`) después de:
  - restablecer demo;
  - agregar material a clase existente;
  - crear clase nueva.
- Bloque `Clases nuevas registradas en esta sesión` dentro de `Aportar información`, visible solo si existen clases creadas por el usuario en la sesión actual.

## 3. Flujo del usuario paso a paso

### 3.1 Desde que se abre la aplicación
1. La aplicación inicializa datos base y variables de sesión.
2. Si no hay perfil seleccionado, se oculta la barra lateral.
3. Se muestra `Inicio`.
4. El usuario elige `Apoderado` o `Estudiante`.
5. Al pulsar `Ingresar al demo →`, se guarda el perfil en sesión y se abre `Panel`.

### 3.2 Consultar una clase
1. Desde `Panel`, el usuario pulsa `📚 Ver las clases y su material`, o entra a `Clases` desde la barra lateral.
2. Se muestra el listado de clases con filtros.
3. El usuario revisa las tarjetas disponibles.
4. Pulsa `Ver material` en una tarjeta.
5. La misma sección `Clases` cambia a la vista de detalle.

### 3.3 Filtrar por asignatura
1. Entrar a `Clases`.
2. Usar el `selectbox` `Asignatura`.
3. Elegir una asignatura específica o `Todas`.
4. El listado se vuelve a renderizar con los resultados filtrados.

### 3.4 Filtrar por fecha
1. Entrar a `Clases`.
2. Usar el `selectbox` `Fecha`.
3. Elegir una fecha específica o `Todas las fechas`.
4. El listado se actualiza automáticamente.

### 3.5 Buscar mediante palabra clave
1. Entrar a `Clases`.
2. Escribir texto en `Palabra clave`.
3. La búsqueda compara contra:
  - asignatura;
  - tema;
  - contenidos;
  - tarea;
  - instrucciones.
4. No busca en nombres de archivos ni en nombres de contribuyentes.

### 3.6 Abrir el detalle de una clase
1. Desde una tarjeta de `Clases`, pulsar `Ver material`.
2. Se guarda el `id` de la clase en `selected_class_id`.
3. La aplicación recarga.
4. Se muestra el detalle de esa clase.

### 3.7 Aportar nueva información

#### Caso A: agregar material a una clase existente
1. Ir a `Aportar información`.
2. Elegir una clase existente en `¿A qué clase quieres aportar material?`.
3. Completar:
  - `Tipo de material *`;
  - `Nombre de archivo simulado` opcional.
4. Pulsar `Enviar material`.
5. El material se agrega al arreglo `materials` de esa clase.
6. Se incrementa el contador `aportes_count`.
7. La app redirige al detalle de esa clase.

#### Caso B: registrar una clase nueva
1. Ir a `Aportar información`.
2. Mantener la opción `➕ Registrar una clase nueva`.
3. Completar:
  - `Asignatura *`;
  - `Fecha de la clase *`;
  - `Tema de la clase *`;
  - `Contenido o resumen *`;
  - `Tarea` opcional;
  - `Instrucciones` opcional;
  - `Tipo de material *`;
  - `Nombre de archivo simulado` opcional.
4. Pulsar `Enviar material`.
5. Se crea una nueva clase temporal con ID `USER-...`.
6. Se guarda en `st.session_state.contributions`.
7. La app redirige al detalle de esa nueva clase.

### 3.8 Cambiar de perfil
1. Desde la barra lateral, pulsar `Cambiar perfil`.
2. Se elimina el perfil activo.
3. Se vuelve a `Inicio`.
4. También se limpia `selected_class_id`.

Importante:
- El código no borra `contributions`, `aportes_count` ni filtros al cambiar de perfil.
- Por lo tanto, los aportes de la sesión siguen existiendo aunque se cambie de perfil.

### 3.9 Restablecer el demo
1. Desde la barra lateral, pulsar `↺ Restablecer demo`.
2. La app recarga `base_data` desde `data.py`.
3. Vacía `contributions`.
4. Reinicia `aportes_count`.
5. Limpia `selected_class_id`.
6. Restablece filtros a:
  - asignatura `Todas`;
  - fecha `Todas`;
  - palabra clave vacía.
7. Si hay perfil activo, vuelve a `Panel`; si no, vuelve a `Inicio`.

## 4. Pantallas: objetivo, información y acciones

### 4.1 Inicio
- Objetivo: entrar al demo y seleccionar perfil.
- Información mostrada:
  - nombre del prototipo;
  - descripción breve;
  - explicación de que ambos perfiles hacen lo mismo.
- Botones:
  - `Ingresar al demo →`: lleva a `Panel`.
- Campos:
  - selector de perfil.
- Filtros: no tiene.
- Acciones disponibles:
  - elegir perfil;
  - ingresar.

### 4.2 Panel
- Objetivo: servir como punto de entrada a las tareas principales.
- Información mostrada:
  - nombre del usuario;
  - estudiante;
  - curso;
  - colegio.
- Botones:
  - `📚 Ver las clases y su material`: lleva a `Clases`.
  - `➕ Aportar información`: lleva a `Aportar información`.
- Campos: no tiene.
- Filtros: no tiene.
- Acciones disponibles:
  - navegar a consulta;
  - navegar a aporte.

### 4.3 Barra lateral
- Objetivo: navegación global después del ingreso.
- Información mostrada:
  - nombre del prototipo;
  - perfil activo;
  - nombre del usuario;
  - estudiante;
  - curso;
  - colegio.
- Botones:
  - `↺ Restablecer demo`: reinicia los datos de sesión.
  - `Cambiar perfil`: vuelve a `Inicio`.
- Campos:
  - `radio` con:
    - `Panel`;
    - `Clases`;
    - `Aportar información`;
    - `Acerca del prototipo`.

### 4.4 Clases
- Objetivo: encontrar y abrir clases.
- Información mostrada:
  - título `Clases`;
  - instrucción breve para filtrar;
  - cantidad de resultados;
  - grupos por asignatura;
  - tarjetas de clases.
- Botones:
  - `Limpiar filtros`;
  - `Ver material` en cada tarjeta;
  - `➕ Aportar esta información` solo si no hay resultados.
- Campos y filtros:
  - `Asignatura`;
  - `Fecha`;
  - `Palabra clave`.
- Acciones disponibles:
  - filtrar;
  - abrir detalle;
  - ir a `Aportar información` desde estado vacío.

### 4.5 Detalle de clase
- Objetivo: revisar el contenido completo de una clase.
- Información mostrada:
  - asignatura;
  - tema;
  - fecha larga;
  - contenidos vistos;
  - tarea;
  - instrucciones;
  - materiales por contribuyente;
  - nota de prototipo.
- Botones:
  - `← Volver a las clases`: vuelve al listado.
- Campos: no tiene.
- Filtros: no tiene.
- Acciones disponibles:
  - volver al listado;
  - usar barra lateral para cambiar a otra sección.

### 4.6 Aportar información
- Objetivo: agregar material a una clase o crear una nueva.
- Información mostrada:
  - explicación del propósito;
  - aclaración de que solo se guarda durante la sesión.
- Botones:
  - `Enviar material`;
  - `Ver material` en tarjetas de clases nuevas registradas durante la sesión.
- Campos:
  - selector de destino de aporte;
  - si es clase nueva:
    - asignatura;
    - fecha;
    - tema;
    - contenido o resumen;
    - tarea;
    - instrucciones;
  - siempre:
    - tipo de material;
    - nombre de archivo simulado.
- Filtros: no tiene.
- Acciones disponibles:
  - agregar material a clase existente;
  - crear clase nueva;
  - abrir clases nuevas desde el bloque inferior.

### 4.7 Acerca del prototipo
- Objetivo: explicar el alcance del demo.
- Información mostrada:
  - problema;
  - usuarios;
  - objetivo;
  - funciones del demo;
  - funciones simuladas;
  - aviso académico.
- Botones: no tiene.
- Campos: no tiene.
- Filtros: no tiene.
- Acciones disponibles:
  - solo lectura;
  - navegación mediante barra lateral.

## 5. Funciones realmente implementadas

Estas funciones sí están implementadas en el código actual:

- Selección de perfil demo.
- Cambio de perfil.
- Navegación entre `Panel`, `Clases`, `Aportar información` y `Acerca del prototipo`.
- Consulta de clases existentes cargadas desde `data.py`.
- Filtro por asignatura.
- Filtro por fecha.
- Filtro por palabra clave.
- Limpieza de filtros.
- Agrupación visual de clases por asignatura.
- Apertura de detalle de clase.
- Visualización de contenidos, tarea, instrucciones y materiales por clase.
- Registro de aporte a una clase existente.
- Registro de una clase nueva en la sesión actual.
- Redirección automática al detalle tras un aporte exitoso.
- Listado de clases nuevas creadas durante la sesión dentro de `Aportar información`.
- Restablecimiento del demo.
- Mensajes temporales de éxito.

Además, estas capacidades están cubiertas por pruebas automatizadas:
- ingreso con perfil;
- búsqueda y apertura de clase;
- creación de clase nueva;
- aporte a clase existente;
- restablecimiento del demo.

## 6. Funciones simuladas

Estas funciones aparecen solo como simulación o representación:

- Inicio de sesión real.
- Gestión de usuarios reales.
- Carga o almacenamiento real de archivos.
- Fotografías reales.
- Descarga de adjuntos.
- Persistencia permanente.
- Integración con colegio, LMS o sistema institucional.
- Notificaciones, correos o avisos push.
- Diferenciación funcional real entre apoderado y estudiante.

Observación importante:
- El nombre del campo `Nombre de archivo simulado` confirma que no existe archivo real.
- Los materiales se guardan como texto dentro de una lista de nombres.

## 7. Persistencia de datos

### Qué información permanece
Durante la sesión actual de Streamlit permanecen:
- perfil seleccionado;
- página actual;
- filtros de clases;
- clase actualmente abierta;
- contador de aportes;
- nuevas clases creadas en la sesión;
- materiales agregados a clases existentes durante la sesión.

### Qué información se pierde
Se pierde al reiniciar la sesión, recargar desde cero el proceso o usar `Restablecer demo`:
- clases nuevas creadas por el usuario;
- materiales agregados durante la sesión;
- contador de aportes;
- filtros activos;
- mensajes temporales;
- detalle de clase abierto.

### Cómo funciona el estado de sesión
- `base_data` se carga desde `data.py` usando `deepcopy`.
- `contributions` guarda clases nuevas creadas por el usuario.
- Las clases mostradas se construyen uniendo:
  - `base_data["classes"]`
  - `contributions`
- Cuando se aporta a una clase existente, no se usa `contributions`:
  - se modifica directamente la clase dentro de `base_data` de la sesión actual.
- Esto significa que hay dos formas de persistencia temporal:
  - mutación temporal de clases base en sesión;
  - almacenamiento temporal de nuevas clases en sesión.

## 8. Análisis de usabilidad

### Claridad de la navegación
- La navegación principal es simple: inicio, panel, clases, aportar y acerca.
- El número de secciones es bajo, lo que favorece la comprensión.
- La barra lateral ayuda a moverse entre secciones una vez que el usuario ingresó.

### Facilidad para saber dónde está el usuario
- En secciones principales, el título ayuda a identificar ubicación.
- En detalle de clase, el usuario sigue técnicamente dentro de `Clases`, pero eso no es totalmente evidente porque no hay breadcrumb ni etiqueta tipo `Clases > Detalle`.
- La barra lateral mantiene la opción `Clases`, pero no indica subnivel.

### Facilidad para volver atrás
- Desde detalle existe un botón explícito `← Volver a las clases`.
- Desde cualquier sección se puede navegar por la barra lateral.
- No existe historial, breadcrumb ni acceso directo al panel desde botones internos, salvo la barra lateral.

### Cantidad de pasos para tareas principales
- Consultar una clase: pocos pasos.
- Filtrar por asignatura, fecha o palabra clave: directo.
- Abrir detalle: un clic desde tarjeta.
- Aportar material: relativamente simple, aunque crear clase nueva exige más campos.

### Textos que pueden ser confusos
- `Aportar información` puede sonar amplio; en la práctica se aporta material o se registra una clase.
- `Ver material` abre también contenidos, tarea e instrucciones, no solo archivos.
- `Ingresar al demo` puede parecer login real para un usuario no técnico, aunque luego se aclara que es demo.

### Botones o funciones poco evidentes
- El detalle de clase no muestra un acceso directo para aportar material a esa misma clase.
- El botón `Limpiar filtros` no indica explícitamente que restablece los tres filtros.
- `Cambiar perfil` no aclara que los aportes temporales siguen en la sesión si no se restablece el demo.

### Posibles problemas para un apoderado con conocimientos tecnológicos básicos
- Puede no entender que `Nombre de archivo simulado` no sube un archivo real.
- Puede esperar diferencia funcional entre perfil `Apoderado` y `Estudiante`.
- Puede creer que la información quedará guardada de forma permanente.
- Puede costarle entender que el detalle de clase es una subvista de `Clases` y no una página aparte.
- Puede no encontrar rápidamente cómo aportar material desde el detalle, porque debe volver o usar la barra lateral.

## 9. Puntos débiles actuales

### Navegación
- El detalle de clase no tiene breadcrumb ni contexto jerárquico.
- No hay CTA directo desde detalle para `Aportar información` sobre esa clase.
- El estado vacío de búsqueda sí ofrece aporte, pero el detalle no.

### Experiencia de usuario
- El flujo de aporte a clase existente no permite adjuntar archivo real ni vista previa.
- El campo `Nombre de archivo simulado` puede generar expectativa errónea.
- El cambio de perfil no limpia aportes previos, lo que puede mezclar acciones hechas como perfiles distintos dentro de una misma sesión.

### Claridad visual y conceptual
- `Inicio` y `selección de perfil` están mezclados en una sola pantalla; esto no es un problema técnico, pero puede dificultar documentar mentalmente el flujo.
- `Clases` combina listado y detalle en la misma sección, lo que simplifica el código pero reduce claridad de ubicación.
- El README menciona métricas, clases recientes y tareas pendientes en el panel, pero eso no aparece en el código actual.

### Consistencia funcional
- En `data.py` aparecen tipos como `Apunte de cuaderno`, `Guía compartida` y `Contenido colaborativo`, pero al crear aportes nuevos solo se permite el catálogo `Fotografía de cuaderno`, `Guía`, `Tarea`, `Instrucción`, `Otro`.
- La búsqueda por palabra clave no considera nombres de archivos ni contribuyentes, aunque ambos son parte visible del material.

## 10. Mejoras recomendadas

### Alta prioridad
- Agregar contexto de navegación en el detalle: por ejemplo `Clases > Detalle`.
- Incluir botón `Aportar material a esta clase` dentro del detalle.
- Aclarar visualmente que los datos son temporales y que `Nombre de archivo simulado` no sube archivos reales.
- Definir el comportamiento deseado al cambiar de perfil:
  - o bien limpiar aportes y filtros;
  - o bien informar explícitamente que la sesión continúa con los mismos datos.

### Prioridad media
- Permitir que la búsqueda por palabra clave también revise nombres de archivos.
- Renombrar `Ver material` por un texto más preciso, por ejemplo `Ver detalle`.
- Mostrar en `Panel` un acceso más orientado al caso principal, por ejemplo buscar por asignatura o última clase.
- Unificar o explicar mejor los tipos de material para que coincidan los datos base y el formulario.

### Mejoras futuras
- Incorporar persistencia real.
- Agregar subida real de archivos e imágenes.
- Diferenciar capacidades o vistas según perfil.
- Incorporar notificaciones o confirmaciones más ricas.
- Agregar integración institucional si el producto evoluciona más allá de prototipo.

## 11. Tabla final

| Pantalla | Acción principal | Funciona | Simulada | Problema detectado | Mejora sugerida |
|---|---|---|---|---|---|
| Inicio | Elegir perfil e ingresar | Sí | Ingreso real no existe | Puede parecer login real | Aclarar aún más que es acceso demo |
| Inicio / selección de perfil | Seleccionar `Apoderado` o `Estudiante` | Sí | Diferencias funcionales entre perfiles no existen | El usuario puede esperar experiencias distintas | Explicar en forma más visible que solo cambia el nombre del aporte |
| Panel | Ir a consultar clases o aportar información | Sí | No | Es muy básico y no resume actividad real | Agregar accesos más orientados a tareas frecuentes |
| Barra lateral | Navegar entre secciones | Sí | No | No muestra subnivel cuando se está en detalle de clase | Añadir contexto de ubicación |
| Clases | Buscar y filtrar clases | Sí | No | La búsqueda no considera archivos ni contribuyentes | Ampliar cobertura de búsqueda |
| Clases | Abrir detalle desde `Ver material` | Sí | No | El botón sugiere solo archivos | Cambiar etiqueta a `Ver detalle` |
| Clases - estado vacío | Pasar a aportar información si no hay resultados | Sí | No | Solo aparece en ausencia de resultados | Ofrecer CTA de aporte también en más lugares |
| Detalle de clase | Revisar contenidos, tarea, instrucciones y materiales | Sí | Archivos son nominales, no reales | Falta acceso directo para aportar material a esa clase | Añadir botón contextual de aporte |
| Aportar información | Agregar material a clase existente | Sí | Archivo es simulado | Puede confundirse con carga real de archivos | Cambiar campo o agregar ayuda visible |
| Aportar información | Registrar clase nueva | Sí | Persistencia permanente no existe | Requiere varios campos y no valida más allá de lo mínimo | Mejorar guía del formulario y validaciones |
| Aportar información | Ver clases nuevas de la sesión | Sí | No | Está al final y puede pasar desapercibido | Destacarlo mejor tras crear clase |
| Acerca del prototipo | Entender alcance del demo | Sí | No | No explica algunos límites de sesión con mucho detalle | Expandir explicación sobre persistencia y perfil |

## 12. Recorrido principal recomendado

Caso: `Un apoderado necesita recuperar la materia de Matemática que su hijo no logró registrar durante una clase`.

El flujo más sencillo que hoy permite el prototipo es:

1. Abrir la aplicación.
2. Elegir perfil `Apoderado`.
3. Pulsar `Ingresar al demo →`.
4. Desde `Panel`, entrar a `📚 Ver las clases y su material`.
5. En `Clases`, usar el filtro `Asignatura` y elegir `Matemática`.
6. Si recuerda la fecha, aplicar también el filtro `Fecha`.
7. Si no recuerda la fecha exacta, usar `Palabra clave` con términos del tema, por ejemplo `fracciones`.
8. Revisar las tarjetas encontradas.
9. Pulsar `Ver material` en la clase que corresponda.
10. Leer en el detalle:
  - contenidos vistos;
  - tarea;
  - instrucciones;
  - materiales aportados por otros.

Si la clase buscada no aparece o está incompleta, el siguiente flujo posible es:

1. Volver al listado o usar la barra lateral.
2. Entrar a `Aportar información`.
3. Elegir la clase existente si ya aparece, o registrar una clase nueva si no existe.
4. Completar el material disponible para dejarlo visible durante esa sesión.

## 13. Aspectos que no pueden determinarse solo desde el código

No es posible confirmar desde el código:
- comportamiento exacto en despliegues productivos con múltiples usuarios simultáneos;
- persistencia entre sesiones reales de navegador y reinicios del servidor;
- existencia de integraciones externas no incluidas en este repositorio;
- comportamiento visual exacto en dispositivos móviles, aunque la app usa layout ancho de Streamlit;
- si hubo funcionalidades removidas anteriormente y aún descritas en `README.md`.

## 14. Conclusión

El prototipo actual implementa correctamente un flujo base de demostración para:
- ingresar con perfil demo;
- consultar clases;
- filtrar información;
- abrir detalle;
- aportar material temporal;
- restablecer el estado del demo.

Su navegación es simple y suficiente para una demostración académica, pero todavía presenta limitaciones claras de orientación, persistencia, consistencia conceptual y claridad sobre qué partes son simuladas.
