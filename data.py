from __future__ import annotations

from copy import deepcopy
from typing import Any


APP_NAME = "Aula al Día"
APP_TAGLINE = (
    "Toda la información de tus clases en un solo lugar. Material subido por apoderados y "
    "alumnos: no es el material oficial del colegio, sino un apoyo a lo que pasa en clases."
)
APP_NOTICE = (
    "Aula al Día es un prototipo académico que busca representar una forma sencilla "
    "de recuperar contenidos, tareas e instrucciones de una clase. Toda la "
    "información utilizada en esta demostración es ficticia y no corresponde a "
    "estudiantes ni establecimientos reales."
)


BASE_DATA: dict[str, Any] = {
    "school": "Colegio Los Alerces",
    "course": "5° Básico B",
    "profiles": {
        "Apoderado": {
            "name": "Carolina Soto",
            "student_name": "Martín Soto",
            "course": "5° Básico B",
            "school": "Colegio Los Alerces",
            # `gender` y `role_label` solo definen el avatar y el tratamiento
            # con que se saluda a la persona. Ambos perfiles tienen las mismas
            # funciones en el prototipo.
            "gender": "f",
            "role_label": "Apoderada",
            "student_gender": "m",
        },
        "Estudiante": {
            "name": "Martín Soto",
            "student_name": "Martín Soto",
            "course": "5° Básico B",
            "school": "Colegio Los Alerces",
            "gender": "m",
            "role_label": "Estudiante",
            "student_gender": "m",
        },
    },
    "subjects": [
        {"name": "Matemática", "icon": "📘"},
        {"name": "Lenguaje y Comunicación", "icon": "📖"},
        {"name": "Ciencias Naturales", "icon": "🔬"},
        {"name": "Historia, Geografía y Ciencias Sociales", "icon": "🗺️"},
    ],
    # Cada clase corresponde a una asignatura en una fecha concreta y agrupa
    # los materiales que compartieron uno o más apoderados o estudiantes.
    "classes": [
        {
            "id": "MAT-2026-07-27",
            "subject": "Matemática",
            "date": "2026-07-27",
            "topic": "Suma y resta de fracciones",
            "content": [
                "Repaso de fracciones equivalentes.",
                "Suma de fracciones con igual denominador.",
                "Ejercicios desarrollados en clases.",
            ],
            "task": "Resolver ejercicios 1 al 6 de la página 42.",
            "instructions": "Mostrar el desarrollo completo de cada ejercicio.",
            "materials": [
                {
                    "contributor": "Carolina Soto",
                    "type": "Apunte de cuaderno",
                    "files": ["Foto cuaderno 1", "Foto cuaderno 2", "Guía de fracciones.pdf"],
                },
            ],
        },
        {
            "id": "MAT-2026-07-28",
            "subject": "Matemática",
            "date": "2026-07-28",
            "topic": "Fracciones con distinto denominador",
            "content": [
                "Uso del mínimo común múltiplo.",
                "Conversión a fracciones equivalentes.",
            ],
            "task": "Completar guía entregada durante la clase.",
            "instructions": "Entregar el viernes.",
            # Ejemplo de una clase con aportes de más de un apoderado.
            "materials": [
                {
                    "contributor": "Carolina Soto",
                    "type": "Guía compartida",
                    "files": ["Guía de ejercicios.pdf"],
                },
                {
                    "contributor": "Paula Rivas",
                    "type": "Fotografía de cuaderno",
                    "files": ["Foto pizarra.jpg"],
                },
            ],
        },
        {
            "id": "LEN-2026-07-27",
            "subject": "Lenguaje y Comunicación",
            "date": "2026-07-27",
            "topic": "Comprensión lectora",
            "content": [
                "Lectura de un cuento breve.",
                "Identificación de personajes y ambiente.",
            ],
            "task": "Responder preguntas 1 a 5 del texto leído.",
            "instructions": "Responder con oraciones completas.",
            "materials": [
                {
                    "contributor": "Martín Soto",
                    "type": "Apunte de cuaderno",
                    "files": ["Lectura complementaria.pdf"],
                },
            ],
        },
        {
            "id": "CIE-2026-07-26",
            "subject": "Ciencias Naturales",
            "date": "2026-07-26",
            "topic": "El sistema digestivo",
            "content": [
                "Principales órganos del sistema digestivo.",
                "Función de cada órgano.",
            ],
            "task": "Dibujar y rotular el sistema digestivo.",
            "instructions": "Utilizar el cuaderno de Ciencias.",
            "materials": [
                {
                    "contributor": "Carolina Soto",
                    "type": "Apunte de cuaderno",
                    "files": ["Imagen sistema digestivo", "Apunte de la clase.pdf"],
                },
            ],
        },
        {
            "id": "HIS-2026-07-25",
            "subject": "Historia, Geografía y Ciencias Sociales",
            "date": "2026-07-25",
            "topic": "Pueblos originarios de Chile",
            "content": [
                "Ubicación geográfica.",
                "Principales características culturales.",
            ],
            "task": "Completar cuadro comparativo.",
            "instructions": "Trabajar con las páginas 56 y 57 del libro.",
            "materials": [
                {
                    "contributor": "Martín Soto",
                    "type": "Contenido colaborativo",
                    "files": ["Cuadro comparativo.docx"],
                },
            ],
        },
    ],
}


def load_base_data() -> dict[str, Any]:
    return deepcopy(BASE_DATA)
