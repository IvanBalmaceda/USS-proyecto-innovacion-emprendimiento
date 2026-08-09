# Instrucciones

Quiero que desarrolles un prototipo web funcional para una solución de recuperación de información escolar.

Antes de comenzar, revisa completamente el archivo:

`Definicion_Prototipo_Recuperacion_Informacion_Escolar.md`

Ese documento contiene el objetivo, alcance, funcionalidades, pantallas, datos simulados y criterios de aceptación del prototipo. Debes usarlo como especificación principal y no reemplazar sus definiciones por supuestos propios.

## Objetivo

Construir un demo simple, liviano y fácil de ejecutar que permita mostrar cómo un apoderado o estudiante puede buscar y recuperar información escolar que no pudo obtener durante una clase, como:

- materia escrita;
- tareas;
- ejercicios;
- fechas de pruebas;
- instrucciones del profesor;
- guías;
- material complementario.

El prototipo no corresponde a un sistema productivo. Su finalidad es demostrar la idea, la navegación y la experiencia principal del usuario.

## Tecnología recomendada

Desarrolla el prototipo con:

- Python 3;
- Streamlit;
- datos ficticios precargados;
- almacenamiento temporal mediante `st.session_state`;
- sin base de datos;
- sin autenticación real;
- sin servicios externos;
- sin APIs;
- sin dependencias innecesarias.

Puedes proponer otra tecnología solamente si existe una ventaja clara para mantener el demo más simple, publicable y fácil de ejecutar. En ese caso, explica brevemente la decisión antes de implementarla.

## Requisitos de desarrollo

1. Crea una aplicación completa y ejecutable.
2. Mantén el código simple, ordenado y fácil de comprender.
3. Usa una interfaz en español.
4. Diseña la experiencia principalmente para apoderados, pero que también pueda ser comprendida por estudiantes.
5. Usa datos escolares ficticios y claramente identificables como demostrativos.
6. Implementa navegación funcional entre las secciones.
7. Permite buscar y filtrar información.
8. Permite visualizar el detalle de una publicación o clase.
9. Incluye un formulario para solicitar información faltante.
10. Guarda las solicitudes solamente durante la sesión.
11. Muestra mensajes de confirmación claros.
12. No simules integraciones complejas ni agregues funciones fuera del alcance.
13. No uses una base de datos.
14. No incluyas credenciales, claves ni secretos.
15. Evita sobreingeniería.

## Diseño esperado

La interfaz debe ser:

- limpia;
- sencilla;
- liviana;
- fácil de presentar;
- responsive dentro de las capacidades de Streamlit;
- con textos naturales;
- sin apariencia excesivamente corporativa;
- apropiada para un trabajo universitario.

Usa componentes nativos de Streamlit siempre que sea posible.

## Estructura mínima del proyecto

Genera como mínimo:

```text
prototipo-informacion-escolar/
├── app.py
├── data.py
├── requirements.txt
├── README.md
└── .gitignore
```

Puedes agregar archivos auxiliares solo cuando realmente simplifiquen la solución.

## Contenido del README

El archivo `README.md` debe incluir:

- descripción breve del prototipo;
- objetivo;
- funciones implementadas;
- funciones simuladas;
- requisitos;
- instrucciones para instalación;
- instrucciones para ejecución local;
- comando exacto para iniciar la aplicación;
- estructura del proyecto;
- instrucciones básicas para publicarlo en Streamlit Community Cloud;
- aclaración de que los datos son ficticios y se almacenan solo durante la sesión.

## Ejecución local esperada

La aplicación debe poder ejecutarse con:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Datos de demostración

Incluye información ficticia suficiente para demostrar:

- diferentes asignaturas;
- varios cursos;
- distintas fechas;
- tipos de contenido;
- publicaciones completas e incompletas;
- ejemplos de tareas, pruebas, guías e instrucciones.

Los datos deben estar separados del código principal, preferentemente en `data.py`.

## Validaciones mínimas

Antes de terminar:

1. Revisa que la aplicación inicie sin errores.
2. Verifica que todas las pantallas sean accesibles.
3. Prueba los filtros y la búsqueda.
4. Prueba la visualización de detalles.
5. Prueba el registro de una solicitud.
6. Verifica que la solicitud quede visible durante la sesión.
7. Confirma que no existan botones sin función.
8. Confirma que no se requiera ningún servicio externo.
9. Revisa que `requirements.txt` contenga solo las dependencias necesarias.
10. Revisa que el README coincida con la implementación real.

## Forma de trabajo

Trabaja de manera autónoma y completa el proyecto de principio a fin.

No te limites a explicar cómo hacerlo: crea todos los archivos necesarios.

Si encuentras una ambigüedad menor, elige la alternativa más simple y coherente con el objetivo del prototipo.

No agregues funcionalidades que aumenten innecesariamente la complejidad.

Al finalizar, entrega:

1. resumen de lo desarrollado;
2. estructura final de archivos;
3. instrucciones de ejecución;
4. decisiones técnicas relevantes;
5. limitaciones del prototipo;
6. lista de funciones implementadas y simuladas.
