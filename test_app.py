from __future__ import annotations

from datetime import date
import unittest
from unittest.mock import patch

import app
from streamlit.testing.v1 import AppTest


class FakeSessionState(dict):
    def __getattr__(self, name: str):
        return self[name]

    def __setattr__(self, name: str, value):
        self[name] = value


class AulaAlDiaAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = AppTest.from_file("app.py")
        self.app.run()

    def login_as_guardian(self) -> None:
        self.app.selectbox[0].set_value("Apoderado")
        self.app.button[0].click()
        self.app.run()

    def go_to(self, section: str) -> None:
        self.app.radio[0].set_value(section)
        self.app.run()

    def test_login_shows_panel(self) -> None:
        self.login_as_guardian()

        self.assertEqual(self.app.session_state["selected_profile"], "Apoderado")
        self.assertEqual(self.app.session_state["current_page"], "Panel")
        self.assertTrue(any("Hola, Carolina Soto" in title.value for title in self.app.title))

    def test_search_flow_finds_science_class(self) -> None:
        self.login_as_guardian()
        self.go_to("Clases")

        # Filtros en la página unificada de Clases: asignatura, fecha, estado.
        self.app.selectbox[0].set_value("Ciencias Naturales")
        self.app.selectbox[1].set_value("2026-07-26")
        self.app.text_input[0].set_value("digestivo")
        self.app.run()

        self.assertEqual(self.app.session_state["current_page"], "Clases")

        self.app.button(key="view-CIE-2026-07-26").click()
        self.app.run()

        self.assertEqual(self.app.session_state["current_page"], "Clases")
        self.assertEqual(self.app.session_state["selected_class_id"], "CIE-2026-07-26")
        self.assertTrue(any("El sistema digestivo" in title.value for title in self.app.title))

    def submit_button(self):
        return next(button for button in self.app.button if button.label == "Enviar material")

    def test_new_class_contribution_is_saved(self) -> None:
        self.login_as_guardian()
        self.go_to("Aportar información")

        # selectbox[0] es el destino ("clase nueva" por defecto).
        self.app.selectbox[1].set_value("Matemática")  # asignatura
        self.app.date_input[0].set_value(date(2026, 7, 29))
        self.app.text_input[0].set_value("Repaso para prueba")  # tema
        self.app.text_area[0].set_value("Se revisó la guía y se resolvieron dos ejercicios.")
        self.app.text_input[1].set_value("Terminar los ejercicios pendientes.")  # tarea
        self.app.text_area[1].set_value("Llevar calculadora simple.")
        self.app.selectbox[2].set_value("Guía")  # tipo de material
        self.app.text_input[2].set_value("guia-repaso.pdf")  # archivo
        self.submit_button().click()
        self.app.run()

        contributions = self.app.session_state["contributions"]
        self.assertEqual(len(contributions), 1)
        self.assertEqual(contributions[0]["materials"][0]["type"], "Guía")
        self.assertEqual(contributions[0]["materials"][0]["contributor"], "Carolina Soto")
        self.assertNotIn("status", contributions[0])
        self.assertEqual(self.app.session_state["aportes_count"], 1)
        self.assertEqual(self.app.session_state["current_page"], "Clases")
        self.assertTrue(str(self.app.session_state["selected_class_id"]).startswith("USER-"))

    def test_material_added_to_existing_class(self) -> None:
        self.login_as_guardian()
        self.go_to("Aportar información")

        # Elegimos una clase existente como destino del aporte.
        self.app.selectbox[0].set_value("CIE-2026-07-26")
        self.app.run()
        self.app.selectbox[1].set_value("Fotografía de cuaderno")  # tipo de material
        self.app.text_input[0].set_value("foto-clase.jpg")
        self.submit_button().click()
        self.app.run()

        self.assertEqual(len(self.app.session_state["contributions"]), 0)
        self.assertEqual(self.app.session_state["aportes_count"], 1)
        self.assertEqual(self.app.session_state["selected_class_id"], "CIE-2026-07-26")
        science_class = next(
            item for item in self.app.session_state["base_data"]["classes"]
            if item["id"] == "CIE-2026-07-26"
        )
        self.assertEqual(len(science_class["materials"]), 2)
        self.assertEqual(science_class["materials"][-1]["contributor"], "Carolina Soto")

    def test_reset_demo_restores_defaults(self) -> None:
        fake_state = FakeSessionState({
            "base_data": {"classes": []},
            "contributions": [{"id": "USER-123"}],
            "aportes_count": 3,
            "selected_class_id": "USER-123",
            "current_page": "Clases",
            "selected_profile": "Apoderado",
            "flash_message": None,
            "f_subject": "Matemática",
            "f_date": "2026-07-30",
            "f_keyword": "prueba",
        })
        with patch.object(app.st, "session_state", fake_state):
            app.reset_demo()

        self.assertEqual(len(fake_state["contributions"]), 0)
        self.assertEqual(fake_state["aportes_count"], 0)
        self.assertIsNone(fake_state["selected_class_id"])
        self.assertEqual(fake_state["current_page"], "Panel")
        self.assertEqual(fake_state["f_date"], "Todas")
        self.assertEqual(fake_state["f_subject"], "Todas")


if __name__ == "__main__":
    unittest.main()
