"""
tests/flat/test_roles.py
------------------------
(arrivato da forge tests/unit/test_role.py, forge MAP.md D88)
Il vocabolario di processo di snapbend.flat.roles e la convivenza con i ruoli
di un altro consumatore (D30).
"""

import unittest

import forge
from forge.model.role import role_str
from snapbend.flat import detect_flat, is_structural


class TestManufacturingIsStructural(unittest.TestCase):
    """
    Predicato ESTESO — outer/inner (motore) + hole/countersink/threaded_hole
    (processo) — quello che `heal_and_detect()` passa a
    `forge.heal(is_structural=...)`.
    """

    def test_ruoli_manifatturieri_strutturali(self):
        for r in ("outer", "inner", "hole", "countersink", "threaded_hole"):
            self.assertTrue(is_structural(r))

    def test_marcatura_e_arredo_restano_non_strutturali(self):
        for r in ("bending", "engrave", "marking", "frame", "unknown"):
            self.assertFalse(is_structural(r))


class TestConsumerRolesSurviveDetect(unittest.TestCase):
    """D30: un ruolo che detect_flat non classifica resta in trash, intatto."""

    def _framed_doc(self):
        # cornice grande + due pezzi dentro, tutti geometricamente distinti
        return forge.load_geometry([
            {"type": "polygon", "role": "frame",
             "points": [(0, 0), (400, 0), (400, 300), (0, 300)]},
            {"type": "polygon", "role": "outer",
             "points": [(20, 20), (120, 20), (120, 120), (20, 120)]},
            {"type": "polygon", "role": "outer",
             "points": [(200, 20), (300, 20), (300, 120), (200, 120)]},
        ])

    def test_detect_non_sposta_il_ruolo_custom_fuori_dalla_trash(self):
        result = forge.heal(self._framed_doc())
        trash_prima = len(result.trash_entities)
        frame_prima = sum(1 for t in result.trash_entities
                          if role_str(getattr(t, "role", "")) == "frame")
        self.assertGreater(frame_prima, 0)

        detect_flat(result, features="all")

        frame_dopo = sum(1 for t in result.trash_entities
                         if role_str(getattr(t, "role", "")) == "frame")
        self.assertEqual(frame_dopo, frame_prima)
        self.assertEqual(len(result.trash_entities), trash_prima)
        # niente ClassifiedEntity scollegato, niente warning "non contenuta"
        self.assertEqual(result.classified_entities, [])
        self.assertFalse([w for w in result.warnings if "non contenuta" in w])



if __name__ == "__main__":
    unittest.main()
