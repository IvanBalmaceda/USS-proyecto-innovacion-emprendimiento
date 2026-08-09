# Definición del prototipo digital

## 1. Nombre provisional

**Aula al Día**

Nombre alternativo: **RecuperaClase**.

El nombre puede cambiar más adelante. Para esta primera versión se utilizará **Aula al Día**.

---

## 2. Objetivo del prototipo

Desarrollar una aplicación web simple que permita mostrar cómo estudiantes y apoderados podrían consultar información escolar que no lograron registrar durante una clase.

El prototipo debe demostrar el flujo principal de la propuesta:

1. Ingresar a la aplicación.
2. Seleccionar un estudiante y su curso.
3. Elegir una asignatura.
4. Buscar una clase por fecha.
5. Revisar los contenidos, tareas, instrucciones y archivos disponibles.
6. Simular el aporte de información de una clase.

No se requiere construir un sistema productivo. El objetivo es contar con una demostración funcional que pueda ser mostrada y validada con usuarios.

---

## 3. Problema que busca representar

Cuando un estudiante falta a clases, no alcanza a copiar toda la materia, se distrae o no comprende una instrucción, necesita recuperar posteriormente la información de la clase.

Actualmente, estudiantes y apoderados suelen recurrir a grupos de WhatsApp, compañeros, profesores u otros apoderados. Este proceso puede ser lento, depender de varias personas y entregar información incompleta o poco clara.

La propuesta busca representar una forma más sencilla y organizada de consultar contenidos escolares por curso, asignatura y fecha.

---

## 4. Tipo de prototipo

Aplicación web funcional de demostración.

### Características

- Debe funcionar en navegador.
- Debe ser simple y liviana.
- Debe tener datos de ejemplo precargados.
- No necesita base de datos.
- No necesita autenticación real.
- No necesita almacenar archivos reales.
- Toda la información puede mantenerse en memoria durante la sesión.
- Al reiniciar la aplicación, puede volver a los datos originales.

---

## 5. Tecnología recomendada

### Opción principal

**Python + Streamlit**

Motivos:

- Permite construir una aplicación web usando solamente Python.
- Es rápido para crear formularios, botones, filtros, tarjetas y navegación.
- Es suficiente para demostrar el flujo del prototipo.
- Puede publicarse posteriormente desde un repositorio de GitHub mediante Streamlit Community Cloud.

### Dependencias sugeridas

```text
streamlit
pandas
```

No incorporar frameworks o librerías adicionales salvo que sean realmente necesarias.

---

## 6. Alcance de la primera versión

### Debe incluir

- Pantalla de ingreso simulado.
- Selección de estudiante.
- Información del curso.
- Listado de asignaturas.
- Búsqueda o filtro por fecha.
- Listado de clases disponibles.
- Vista de detalle de una clase.
- Contenidos vistos.
- Tareas e instrucciones.
- Archivos o fotografías simuladas.
- Estado del contenido: validado o pendiente.
- Formulario para aportar información.
- Mensaje de confirmación al enviar un aporte.
- Datos almacenados temporalmente en memoria.

### No debe incluir

- Registro real de usuarios.
- Contraseñas reales.
- Base de datos.
- Envío de correos.
- Notificaciones reales.
- Integración con colegios.
- Carga permanente de fotografías.
- Permisos complejos.
- Procesamiento de pagos.
- Inteligencia artificial.

---

## 7. Usuarios simulados

La aplicación debe ofrecer dos perfiles de demostración:

### Apoderado

- Nombre: **Carolina Soto**.
- Estudiante asociado: **Martín Soto**.
- Curso: **5° Básico B**.
- Colegio: **Colegio Los Alerces**.

### Estudiante

- Nombre: **Martín Soto**.
- Curso: **5° Básico B**.
- Colegio: **Colegio Los Alerces**.

No se necesita una autenticación real. En la pantalla inicial debe existir un selector de perfil y un botón **Ingresar al demo**.

---

## 8. Asignaturas de ejemplo

Incluir las siguientes asignaturas:

- Matemática.
- Lenguaje y Comunicación.
- Ciencias Naturales.
- Historia, Geografía y Ciencias Sociales.

Cada asignatura debe tener un ícono simple o un emoji y una cantidad visible de clases disponibles.

---

## 9. Datos de ejemplo

### Clase 1

- Asignatura: Matemática.
- Fecha: 27/07/2026.
- Tema: Suma y resta de fracciones.
- Contenido:
  - Repaso de fracciones equivalentes.
  - Suma de fracciones con igual denominador.
  - Ejercicios desarrollados en clases.
- Tarea: Resolver ejercicios 1 al 6 de la página 42.
- Instrucción: Mostrar el desarrollo completo de cada ejercicio.
- Archivos:
  - Foto cuaderno 1.
  - Foto cuaderno 2.
  - Guía de fracciones.pdf.
- Estado: Validado por el profesor.

### Clase 2

- Asignatura: Matemática.
- Fecha: 28/07/2026.
- Tema: Fracciones con distinto denominador.
- Contenido:
  - Uso del mínimo común múltiplo.
  - Conversión a fracciones equivalentes.
- Tarea: Completar guía entregada durante la clase.
- Instrucción: Entregar el viernes.
- Archivos:
  - Guía de ejercicios.pdf.
- Estado: Aporte de apoderado pendiente de revisión.

### Clase 3

- Asignatura: Lenguaje y Comunicación.
- Fecha: 27/07/2026.
- Tema: Comprensión lectora.
- Contenido:
  - Lectura de un cuento breve.
  - Identificación de personajes y ambiente.
- Tarea: Responder preguntas 1 a 5 del texto leído.
- Instrucción: Responder con oraciones completas.
- Archivos:
  - Lectura complementaria.pdf.
- Estado: Validado por el profesor.

### Clase 4

- Asignatura: Ciencias Naturales.
- Fecha: 26/07/2026.
- Tema: El sistema digestivo.
- Contenido:
  - Principales órganos del sistema digestivo.
  - Función de cada órgano.
- Tarea: Dibujar y rotular el sistema digestivo.
- Instrucción: Utilizar el cuaderno de Ciencias.
- Archivos:
  - Imagen sistema digestivo.
  - Apunte de la clase.pdf.
- Estado: Validado por el profesor.

### Clase 5

- Asignatura: Historia.
- Fecha: 25/07/2026.
- Tema: Pueblos originarios de Chile.
- Contenido:
  - Ubicación geográfica.
  - Principales características culturales.
- Tarea: Completar cuadro comparativo.
- Instrucción: Trabajar con las páginas 56 y 57 del libro.
- Archivos:
  - Cuadro comparativo.docx.
- Estado: Información compartida por un apoderado.

---

## 10. Pantallas y navegación

La navegación puede realizarse mediante un menú lateral de Streamlit.

### Pantalla 1: Inicio

Mostrar:

- Nombre de la aplicación.
- Frase breve: **Toda la información de tus clases en un solo lugar**.
- Explicación corta del demo.
- Selector de perfil: Apoderado o Estudiante.
- Botón **Ingresar al demo**.

Al presionar el botón, guardar el perfil seleccionado en `st.session_state` y abrir la página principal.

### Pantalla 2: Página principal

Mostrar:

- Saludo al usuario.
- Nombre del estudiante.
- Curso y colegio.
- Tarjeta con clases recientes.
- Tarjeta con tareas pendientes.
- Accesos a las cuatro asignaturas.
- Botón o menú para **Buscar una clase**.
- Botón o menú para **Aportar información**.

### Pantalla 3: Asignaturas

Mostrar las asignaturas como tarjetas o botones.

Cada tarjeta debe indicar:

- Nombre de la asignatura.
- Cantidad de clases disponibles.
- Fecha de la última actualización.

Al seleccionar una asignatura, mostrar las clases disponibles.

### Pantalla 4: Lista de clases

Permitir filtrar por:

- Asignatura.
- Fecha.
- Estado del contenido.

Cada clase debe mostrar:

- Fecha.
- Tema.
- Tarea disponible: Sí o No.
- Cantidad de archivos.
- Estado: validado, pendiente o compartido.
- Botón **Ver clase**.

### Pantalla 5: Detalle de una clase

Mostrar:

- Asignatura.
- Fecha.
- Tema.
- Contenidos vistos.
- Tarea.
- Instrucciones.
- Archivos disponibles.
- Estado de validación.
- Persona que realizó el aporte.

Los archivos no necesitan descargarse realmente. Pueden mostrarse como tarjetas o botones deshabilitados con nombres de ejemplo.

Agregar un aviso visible:

> Este prototipo utiliza información simulada con fines académicos.

### Pantalla 6: Buscar una clase

Permitir seleccionar:

- Asignatura.
- Fecha.
- Palabra clave.

Mostrar los resultados coincidentes.

Si no hay resultados, mostrar:

> No encontramos información para los filtros seleccionados. Puedes solicitarla o aportar contenido.

### Pantalla 7: Aportar información

Formulario con los siguientes campos:

- Asignatura.
- Fecha.
- Tema de la clase.
- Contenido o resumen.
- Tarea.
- Instrucciones.
- Tipo de aporte:
  - Fotografía de cuaderno.
  - Guía.
  - Tarea.
  - Instrucción.
  - Otro.
- Nombre de archivo simulado.

Botón **Enviar aporte**.

Al enviar:

- Guardar el nuevo aporte en `st.session_state`.
- Asignar estado **Pendiente de revisión**.
- Mostrar el mensaje:

> Tu aporte fue registrado correctamente y quedó pendiente de revisión.

El aporte debe aparecer en la lista de clases mientras dure la sesión.

### Pantalla 8: Acerca del prototipo

Mostrar brevemente:

- Problema identificado.
- Usuarios principales.
- Objetivo del prototipo.
- Funciones implementadas.
- Funciones simuladas.

---

## 11. Estados del contenido

Utilizar tres estados visibles:

### Validado

Texto: **Validado por el profesor**.

Significa que la información se presenta como revisada dentro de la simulación.

### Pendiente

Texto: **Pendiente de revisión**.

Significa que fue aportada por un usuario y todavía no ha sido validada.

### Compartido

Texto: **Compartido por un apoderado o estudiante**.

Se utiliza para contenidos colaborativos que forman parte de la demostración.

No implementar un sistema real de aprobación.

---

## 12. Almacenamiento en memoria

Usar `st.session_state` para guardar:

- Perfil seleccionado.
- Página actual.
- Filtros aplicados.
- Aportes creados durante la sesión.
- Mensajes de confirmación.

Los datos base pueden estar definidos directamente en archivos Python o en un archivo JSON local.

### Recomendación

Usar un archivo:

```text
data/sample_data.json
```

Al iniciar la aplicación, cargar ese archivo en memoria. Los nuevos aportes se mantienen solo en `st.session_state` y no modifican el archivo original.

---

## 13. Estructura sugerida del proyecto

```text
aula-al-dia/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_data.json
├── assets/
│   ├── placeholder_cuaderno.png
│   ├── placeholder_guia.png
│   └── placeholder_archivo.png
└── .streamlit/
    └── config.toml
```

Para mantener el proyecto simple, toda la lógica también puede quedar inicialmente en `app.py`.

---

## 14. Diseño visual

El diseño debe ser sencillo, escolar y fácil de entender.

### Lineamientos

- Fondo claro.
- Títulos simples.
- Tarjetas para asignaturas y clases.
- Botones grandes y visibles.
- Textos breves.
- Diseño adaptable a computador y celular.
- No recargar la pantalla con muchos elementos.
- Mantener una navegación consistente.

### Colores sugeridos

- Azul oscuro para títulos y navegación.
- Azul claro para elementos secundarios.
- Verde para contenido validado.
- Amarillo para contenido pendiente.
- Gris para información complementaria.

No es necesario replicar los colores de la universidad.

---

## 15. Reglas funcionales

1. El usuario debe poder ingresar sin crear una cuenta.
2. El perfil seleccionado debe mantenerse durante la sesión.
3. Debe existir al menos un flujo completo para buscar y abrir una clase.
4. Los filtros deben modificar los resultados visibles.
5. El formulario de aporte debe validar los campos obligatorios.
6. Los aportes enviados deben aparecer en la aplicación durante la sesión.
7. El botón **Restablecer demo** debe borrar los cambios de la sesión y cargar nuevamente los datos de ejemplo.
8. La aplicación no debe fallar si no existen resultados.
9. Todo contenido debe estar en español.
10. Debe existir una indicación clara de que los datos son simulados.

---

## 16. Criterios de aceptación

El prototipo se considera terminado cuando permite realizar estas acciones:

### Caso 1: Consultar materia

1. Ingresar como apoderado.
2. Abrir Matemática.
3. Seleccionar la clase del 27/07/2026.
4. Ver contenidos, tarea, instrucciones y archivos.

### Caso 2: Buscar una clase

1. Ir a Buscar una clase.
2. Seleccionar Ciencias Naturales.
3. Buscar por fecha o palabra clave.
4. Abrir el resultado correspondiente.

### Caso 3: Crear un aporte

1. Ir a Aportar información.
2. Completar los campos obligatorios.
3. Enviar el formulario.
4. Ver mensaje de confirmación.
5. Comprobar que el aporte aparece con estado Pendiente de revisión.

### Caso 4: Restablecer la demostración

1. Crear al menos un aporte.
2. Presionar Restablecer demo.
3. Confirmar que se eliminan los cambios temporales.

---

## 17. Validaciones mínimas del formulario

Campos obligatorios:

- Asignatura.
- Fecha.
- Tema.
- Contenido o resumen.
- Tipo de aporte.

Si falta información, mostrar un mensaje claro y no guardar el aporte.

Ejemplo:

> Completa los campos obligatorios antes de enviar el aporte.

---

## 18. Elementos implementados y simulados

### Implementados

- Navegación entre secciones.
- Selección de perfil.
- Visualización de asignaturas.
- Filtros por asignatura y fecha.
- Búsqueda por palabra clave.
- Detalle de clases.
- Formulario de aportes.
- Guardado temporal en memoria.
- Restablecimiento del demo.

### Simulados

- Inicio de sesión.
- Identidad de estudiantes y apoderados.
- Validación por parte del profesor.
- Archivos adjuntos.
- Fotografías de cuadernos.
- Integración con el establecimiento.
- Notificaciones.
- Persistencia permanente.

---

## 19. Instrucciones para Codex

Desarrolla el proyecto completo siguiendo esta definición.

### Requisitos técnicos

- Utilizar Python 3.12 o compatible.
- Utilizar Streamlit.
- Mantener el código simple y fácil de entender.
- Evitar sobreingeniería.
- No utilizar base de datos.
- No utilizar servicios externos.
- No pedir claves, tokens ni variables secretas.
- Utilizar datos locales de ejemplo.
- Utilizar `st.session_state` para los cambios temporales.
- Crear `requirements.txt`.
- Crear `README.md` con instrucciones para ejecutar y publicar.
- Verificar que la aplicación pueda iniciarse con:

```bash
streamlit run app.py
```

### Resultado esperado

Entregar todos los archivos necesarios para ejecutar la aplicación localmente y publicarla posteriormente en Streamlit Community Cloud.

---

## 20. Publicación esperada

El proyecto debe quedar preparado para subirse a GitHub y desplegarse como una aplicación web pública de demostración.

Archivos mínimos para publicación:

```text
app.py
requirements.txt
README.md
```

El prototipo no manejará información real de estudiantes. Todos los nombres, clases, archivos y establecimientos deben ser ficticios.

---

## 21. Texto breve para mostrar dentro del demo

> Aula al Día es un prototipo académico que busca representar una forma sencilla de recuperar contenidos, tareas e instrucciones de una clase. Toda la información utilizada en esta demostración es ficticia y no corresponde a estudiantes ni establecimientos reales.

---

## 22. Prioridades de desarrollo

### Prioridad alta

- Navegación clara.
- Datos precargados.
- Consulta por asignatura y fecha.
- Detalle completo de una clase.
- Formulario de aporte.
- Guardado temporal.

### Prioridad media

- Búsqueda por palabra clave.
- Indicadores de estado.
- Tarjetas de tareas pendientes.
- Diseño adaptable a celular.

### Prioridad baja

- Animaciones.
- Gráficos.
- Personalización visual avanzada.
- Funciones administrativas.

La primera versión debe privilegiar la claridad del flujo sobre la cantidad de funciones.
