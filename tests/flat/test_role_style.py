"""
tests/flat/test_role_style.py
-----------------------------
(arrivato da forge tests/integration/test_role_style.py, forge MAP.md D88)
RoleStyle di forge sui ruoli registrati da snapbend: il magenta di "hole" è
registrato da snapbend.flat.roles con `register_role_style`.
"""

import unittest

import ezdxf

import forge
from forge import RoleStyle
from snapbend.flat import detect_flat, LAYER_HOLE


def _rect_with_hole_and_frame():
    """
    Rettangolo 100x50 con un foro (per il ruolo 'hole', noto a forge) + una
    LINE su layer FRAME fuori dal rettangolo (diventa trash col ruolo
    consumatore 'frame', mai visto da forge prima d'ora — D31).
    """
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    msp.add_line((0, 0), (100, 0))
    msp.add_line((100, 0), (100, 50))
    msp.add_line((100, 50), (0, 50))
    msp.add_line((0, 50), (0, 0))
    msp.add_circle((50, 25), 5)

    msp.add_line((200, 200), (220, 200), dxfattribs={'layer': 'FRAME'})

    doc_in = forge.document_from_msp(msp, role_rules=forge.name_rules({'FRAME': 'frame'}))
    result = forge.heal(doc_in, tolerance=0.05)
    detect_flat(result, features="all")
    return result, doc_in


class TestRoleStyleDefaultUnchanged(unittest.TestCase):
    """
    Senza `role_styles=` passato a to_dxf(), il comportamento visivo di
    "hole" è identico a prima di D37 (stesso magenta) — ma il MECCANISMO è
    cambiato ("roles out of core"): non è più una voce hardcoded nella
    palette del motore, è `snapbend.flat.roles` che si registra il
    proprio colore con `register_role_style`, lo stesso meccanismo pubblico
    che userebbe un consumatore esterno. Per questo "hole" HA un
    `true_color` di default (registrato), mentre un ruolo di consumatore
    mai registrato (`frame`, qui) non ce l'ha.
    """

    def setUp(self):
        self.result, self.doc_in = _rect_with_hole_and_frame()
        self.doc_out = forge.to_dxf(self.result, self.doc_in)

    def test_001_hole_layer_has_registered_true_color(self):
        layer = self.doc_out.layers.get(LAYER_HOLE)
        self.assertTrue(layer.dxf.hasattr("true_color"))
        self.assertEqual(layer.rgb, (255, 0, 255))  # magenta, registrato da snapbend.flat.roles

    def test_002_frame_layer_created_with_consumer_color(self):
        # Layer creato al volo col nome dello slug (D31), colore di default
        # (grigio consumatore), nessun override richiesto.
        self.assertIn('frame', self.doc_out.layers)
        layer = self.doc_out.layers.get('frame')
        self.assertFalse(layer.dxf.hasattr("true_color"))


class TestRoleStyleColorOverride(unittest.TestCase):
    """role_styles fa override del colore di un ruolo noto a forge."""

    def setUp(self):
        self.result, self.doc_in = _rect_with_hole_and_frame()
        self.doc_out = forge.to_dxf(
            self.result, self.doc_in,
            role_styles={"hole": RoleStyle(color=(0, 0, 0))},
        )

    def test_001_hole_layer_true_color_is_black(self):
        layer = self.doc_out.layers.get(LAYER_HOLE)
        self.assertEqual(layer.rgb, (0, 0, 0))

    def test_002_other_layers_untouched(self):
        outer_layer = self.doc_out.layers.get("OuterContour")
        self.assertFalse(outer_layer.dxf.hasattr("true_color"))


class TestRoleStyleColorOverride(unittest.TestCase):
    """role_styles fa override del colore di un ruolo noto a forge."""

    def setUp(self):
        self.result, self.doc_in = _rect_with_hole_and_frame()
        self.doc_out = forge.to_dxf(
            self.result, self.doc_in,
            role_styles={"hole": RoleStyle(color=(0, 0, 0))},
        )

    def test_001_hole_layer_true_color_is_black(self):
        layer = self.doc_out.layers.get(LAYER_HOLE)
        self.assertEqual(layer.rgb, (0, 0, 0))

    def test_002_other_layers_untouched(self):
        outer_layer = self.doc_out.layers.get("OuterContour")
        self.assertFalse(outer_layer.dxf.hasattr("true_color"))


if __name__ == "__main__":
    unittest.main()
