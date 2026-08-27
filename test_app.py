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

    # ------------------------------------------------------------------ utils
    def login_as_guardian(self) -> None:
        self.app.selectbox(key="login_profile").set_value("Apoderado")
        self.app.button(key="home-enter-demo").click()
        self.app.run()

    def go_to(self, section: str) -> None:
        # La navegación lateral es el único radio de la app.
        self.app.radio[0].set_value(section)
        self.app.run()

    def open_science_class(self) -> None:
        self.app.button(key="classes-view-CIE-2026-07-26").click()
        self.app.run()

    def submit_button(self):
        return next(button for button in self.app.button if button.label == "Enviar material")

    def page(self) -> str:
        return self.app.session_state["current_page"]

    # ------------------------------------------------------------- navegación
    def test_login_shows_start_page(self) -> None:
        self.login_as_guardian()

        self.assertEqual(self.app.session_state["selected_profile"], "Apoderado")
        self.assertEqual(self.page(), "Inicio")
        self.assertTrue(any("Hola, Carolina" in title.value for title in self.app.title))

    def test_login_as_student_uses_student_profile(self) -> None:
        # El perfil se lee en el callback: cambiar el selector y entrar en el
        # mismo paso debe ingresar como estudiante, no con el valor anterior.
        self.app.selectbox(key="login_profile").set_value("Estudiante")
        self.app.button(key="home-enter-demo").click()
        self.app.run()

        self.assertEqual(self.app.session_state["selected_profile"], "Estudiante")
        self.assertTrue(any("Hola, Martín" in title.value for title in self.app.title))
        sidebar = next(
            block.value for block in self.app.markdown if 'class="sb-card"' in block.value
        )
        # Avatar de estudiante para quien está conectado.
        self.assertIn("av-student", sidebar)
        self.assertNotIn("av-adult", sidebar)

    def test_login_as_guardian_uses_adult_avatar(self) -> None:
        self.login_as_guardian()

        sidebar = next(
            block.value for block in self.app.markdown if 'class="sb-card"' in block.value
        )
        self.assertIn("av-adult", sidebar)
        self.assertIn("av-student", sidebar)  # el estudiante asociado
        self.assertIn("Apoderada", sidebar)

    def test_start_page_links_to_classes_and_saved(self) -> None:
        self.login_as_guardian()

        self.app.button(key="start-search").click()
        self.app.run()
        self.assertEqual(self.page(), "Clases")

        self.go_to("Inicio")
        self.app.button(key="link-saved").click()
        self.app.run()
        self.assertEqual(self.page(), "Guardados")

    def test_start_page_shows_three_recent_classes(self) -> None:
        self.login_as_guardian()

        keys = [button.key for button in self.app.button if str(button.key).startswith("start-view-")]
        self.assertEqual(len(keys), app.RECENT_LIMIT)

        # La clase más reciente del demo es la del 28/07/2026.
        self.app.button(key="start-view-MAT-2026-07-28").click()
        self.app.run()
        self.assertEqual(self.page(), "Clases")
        self.assertEqual(self.app.session_state["selected_class_id"], "MAT-2026-07-28")

    # ------------------------------------------------------------- búsquedas
    def test_search_flow_finds_science_class(self) -> None:
        self.login_as_guardian()
        self.go_to("Clases")

        # En Clases los filtros son los tres primeros widgets de entrada.
        self.app.selectbox[0].set_value("Ciencias Naturales")
        self.app.selectbox[1].set_value("2026-07-26")
        self.app.text_input[0].set_value("digestivo")
        self.app.run()

        self.open_science_class()

        self.assertEqual(self.page(), "Clases")
        self.assertEqual(self.app.session_state["selected_class_id"], "CIE-2026-07-26")
        self.assertTrue(any("El sistema digestivo" in title.value for title in self.app.title))

    def test_search_by_file_name(self) -> None:
        self.login_as_guardian()
        self.go_to("Clases")

        # "Foto pizarra.jpg" solo existe como nombre de archivo de esa clase.
        self.app.text_input[0].set_value("Foto pizarra")
        self.app.run()

        keys = [button.key for button in self.app.button if str(button.key).startswith("classes-view-")]
        self.assertEqual(keys, ["classes-view-MAT-2026-07-28"])

    def test_back_to_classes_keeps_filters(self) -> None:
        self.login_as_guardian()
        self.go_to("Clases")

        self.app.selectbox[0].set_value("Ciencias Naturales")
        self.app.text_input[0].set_value("digestivo")
        self.app.run()

        self.open_science_class()
        self.assertEqual(self.app.session_state["selected_class_id"], "CIE-2026-07-26")

        self.app.button(key="detail-back").click()
        self.app.run()

        self.assertIsNone(self.app.session_state["selected_class_id"])
        snapshot = self.app.session_state["filters_snapshot"]
        self.assertEqual(snapshot["f_subject"], "Ciencias Naturales")
        self.assertEqual(snapshot["f_keyword"], "digestivo")
        # Los widgets se redibujan con el filtro que tenía puesto el usuario.
        self.assertEqual(self.app.selectbox[0].value, "Ciencias Naturales")
        self.assertEqual(self.app.text_input[0].value, "digestivo")
        self.assertTrue(self.app.button(key="classes-view-CIE-2026-07-26"))

    # -------------------------------------------------------------- guardados
    def test_save_class_from_list(self) -> None:
        self.login_as_guardian()
        self.go_to("Clases")

        self.app.button(key="classes-save-CIE-2026-07-26").click()
        self.app.run()

        self.assertEqual(self.app.session_state["saved_class_ids"], ["CIE-2026-07-26"])
        # El botón ahora ofrece quitarla.
        self.assertTrue(self.app.button(key="classes-unsave-CIE-2026-07-26"))

    def test_unsave_class_from_list(self) -> None:
        self.login_as_guardian()
        self.go_to("Clases")

        self.app.button(key="classes-save-CIE-2026-07-26").click()
        self.app.run()
        self.app.button(key="classes-unsave-CIE-2026-07-26").click()
        self.app.run()

        self.assertEqual(self.app.session_state["saved_class_ids"], [])

    def test_save_and_unsave_from_detail(self) -> None:
        self.login_as_guardian()
        self.go_to("Clases")
        self.open_science_class()

        self.app.button(key="detail-save-CIE-2026-07-26").click()
        self.app.run()
        self.assertIn("CIE-2026-07-26", self.app.session_state["saved_class_ids"])

        self.app.button(key="detail-unsave-CIE-2026-07-26").click()
        self.app.run()
        self.assertEqual(self.app.session_state["saved_class_ids"], [])

    def test_saved_section_lists_and_opens_class(self) -> None:
        self.login_as_guardian()
        self.go_to("Clases")
        self.app.button(key="classes-save-CIE-2026-07-26").click()
        self.app.run()

        self.go_to("Guardados")
        self.assertTrue(any("Clases guardadas" in title.value for title in self.app.title))

        self.app.button(key="saved-view-CIE-2026-07-26").click()
        self.app.run()

        self.assertEqual(self.page(), "Clases")
        self.assertEqual(self.app.session_state["selected_class_id"], "CIE-2026-07-26")
        self.assertTrue(any("El sistema digestivo" in title.value for title in self.app.title))

    def test_remove_from_saved_section(self) -> None:
        self.login_as_guardian()
        self.go_to("Clases")
        self.app.button(key="classes-save-CIE-2026-07-26").click()
        self.app.run()

        self.go_to("Guardados")
        self.app.button(key="saved-unsave-CIE-2026-07-26").click()
        self.app.run()

        self.assertEqual(self.app.session_state["saved_class_ids"], [])
        # Queda el estado vacío con su acceso a Clases.
        self.assertTrue(self.app.button(key="saved-empty-search"))

    def test_empty_saved_section_links_to_classes(self) -> None:
        self.login_as_guardian()
        self.go_to("Guardados")

        self.app.button(key="saved-empty-search").click()
        self.app.run()

        self.assertEqual(self.page(), "Clases")

    # --------------------------------------------------------------- aportes
    def test_contribute_from_class_detail_preloads_class(self) -> None:
        self.login_as_guardian()
        self.go_to("Clases")
        self.open_science_class()

        self.app.button(key="detail-contribute-CIE-2026-07-26").click()
        self.app.run()

        self.assertEqual(self.page(), "Aportar información")
        self.assertEqual(self.app.session_state["contrib_target"], "CIE-2026-07-26")
        self.assertEqual(
            self.app.session_state["selected_contribution_class_id"], "CIE-2026-07-26"
        )
        rendered = " ".join(block.value for block in self.app.markdown)
        self.assertIn("Ciencias Naturales", rendered)
        self.assertIn("El sistema digestivo", rendered)

        # El aporte se envía igual que siempre.
        self.app.selectbox(key="c_material_type").set_value("Fotografía de cuaderno")
        self.app.text_input(key="c_file_name").set_value("foto-clase.jpg")
        self.submit_button().click()
        self.app.run()

        self.assertEqual(self.app.session_state["aportes_count"], 1)
        self.assertEqual(self.app.session_state["selected_class_id"], "CIE-2026-07-26")

    def test_contribute_from_menu_has_no_preloaded_class(self) -> None:
        self.login_as_guardian()
        self.go_to("Clases")
        self.open_science_class()
        self.app.button(key="detail-contribute-CIE-2026-07-26").click()
        self.app.run()

        # Volver a entrar por el menú lateral limpia la precarga.
        self.go_to("Clases")
        self.go_to("Aportar información")

        self.assertEqual(self.app.session_state["contrib_target"], app.NEW_CLASS_OPTION)
        self.assertIsNone(self.app.session_state["selected_contribution_class_id"])
        self.assertEqual(self.app.selectbox(key="contrib_target").value, app.NEW_CLASS_OPTION)

    def test_new_class_contribution_is_saved(self) -> None:
        self.login_as_guardian()
        self.go_to("Aportar información")

        self.app.selectbox(key="c_subject").set_value("Matemática")
        self.app.date_input(key="c_date").set_value(date(2026, 7, 29))
        self.app.text_input(key="c_topic").set_value("Repaso para prueba")
        self.app.text_area(key="c_summary").set_value(
            "Se revisó la guía y se resolvieron dos ejercicios."
        )
        self.app.text_input(key="c_task").set_value("Terminar los ejercicios pendientes.")
        self.app.text_area(key="c_instructions").set_value("Llevar calculadora simple.")
        self.app.selectbox(key="c_material_type").set_value("Guía")
        self.app.text_input(key="c_file_name").set_value("guia-repaso.pdf")
        self.submit_button().click()
        self.app.run()

        contributions = self.app.session_state["contributions"]
        self.assertEqual(len(contributions), 1)
        self.assertEqual(contributions[0]["materials"][0]["type"], "Guía")
        self.assertEqual(contributions[0]["materials"][0]["contributor"], "Carolina Soto")
        self.assertEqual(self.app.session_state["aportes_count"], 1)
        self.assertEqual(self.page(), "Clases")
        self.assertTrue(str(self.app.session_state["selected_class_id"]).startswith("USER-"))
        # El mensaje de éxito indica quién realizó el aporte.
        self.assertTrue(any("Carolina Soto" in alert.value for alert in self.app.success))

    def test_material_added_to_existing_class(self) -> None:
        self.login_as_guardian()
        self.go_to("Aportar información")

        self.app.selectbox(key="contrib_target").set_value("CIE-2026-07-26")
        self.app.run()
        self.app.selectbox(key="c_material_type").set_value("Fotografía de cuaderno")
        self.app.text_input(key="c_file_name").set_value("foto-clase.jpg")
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

    # ----------------------------------------------------------- restablecer
    def test_reset_demo_clears_saved_classes(self) -> None:
        self.login_as_guardian()
        self.go_to("Clases")
        self.app.button(key="classes-save-CIE-2026-07-26").click()
        self.app.run()
        self.assertEqual(len(self.app.session_state["saved_class_ids"]), 1)

        self.app.button(key="sidebar-reset-demo").click()
        self.app.run()

        self.assertEqual(self.app.session_state["saved_class_ids"], [])
        self.assertEqual(self.page(), "Inicio")

    def test_reset_demo_restores_defaults(self) -> None:
        fake_state = FakeSessionState({
            "base_data": {"classes": []},
            "contributions": [{"id": "USER-123"}],
            "aportes_count": 3,
            "selected_class_id": "USER-123",
            "saved_class_ids": ["CIE-2026-07-26"],
            "selected_contribution_class_id": "CIE-2026-07-26",
            "contrib_target": "CIE-2026-07-26",
            "current_page": "Clases",
            "nav_radio": "Clases",
            "selected_profile": "Apoderado",
            "flash_message": None,
            "f_subject": "Matemática",
            "f_date": "2026-07-30",
            "f_keyword": "prueba",
            "filters_snapshot": {"f_subject": "Matemática"},
        })
        with patch.object(app.st, "session_state", fake_state):
            app.reset_demo()

        self.assertEqual(len(fake_state["contributions"]), 0)
        self.assertEqual(fake_state["aportes_count"], 0)
        self.assertIsNone(fake_state["selected_class_id"])
        self.assertEqual(fake_state["saved_class_ids"], [])
        self.assertIsNone(fake_state["selected_contribution_class_id"])
        self.assertEqual(fake_state["contrib_target"], app.NEW_CLASS_OPTION)
        self.assertEqual(fake_state["current_page"], "Inicio")
        # Los filtros vigentes viven en el snapshot, no en las keys de widget.
        self.assertEqual(fake_state["filters_snapshot"], app.FILTER_DEFAULTS)


if __name__ == "__main__":
    unittest.main()
