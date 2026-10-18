"""
tests/flat/test_role_style.py
-----------------------------
(arrivato da topo tests/integration/test_role_style.py, topo MAP.md D88)
RoleStyle di topo sui ruoli di snapbend: il magenta e il layer `Hole` di
"hole" sono le mappe `ROLE_STYLES`/`LAYERS` di snapbend.flat.roles, che chi
esporta passa a topo (topo MAP.md D128). Senza, topo non ne sa niente.
"""

import unittest

import ezdxf

import topo
from snapbend.flat import detect_flat, LAYER_HOLE, LAYERS, ROLE_STYLES


def _rect_with_hole_and_frame():
    """
    Rettangolo 100x50 con un foro (per il ruolo 'hole', noto a topo) + una
    LINE su layer FRAME fuori dal rettangolo (diventa trash col ruolo
    consumatore 'frame', mai visto da topo prima d'ora — D31).
    """
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    msp.add_line((0, 0), (100, 0))
    msp.add_line((100, 0), (100, 50))
    msp.add_line((100, 50), (0, 50))
    msp.add_line((0, 50), (0, 0))
    msp.add_circle((50, 25), 5)

    msp.add_line((200, 200), (220, 200), dxfattribs={'layer': 'FRAME'})

    doc_in = topo.document_from_msp(msp, role_rules=topo.name_rules({'FRAME': 'frame'}))
    result = topo.heal(doc_in, tolerance=0.05)
    detect_flat(result, features="all")
    return result, doc_in


class TestSnapbendMaps(unittest.TestCase):
    """
    Con le mappe di snapbend "hole" va sul layer `Hole` in magenta; un ruolo
    di consumatore che nessuno nomina (`frame`) prende il grigio di default
    dell'adapter, senza `true_color` (D31).
    """

    def setUp(self):
        self.result, self.doc_in = _rect_with_hole_and_frame()
        self.doc_out = topo.to_dxf(self.result, self.doc_in, role_styles=ROLE_STYLES, layers=LAYERS)

    def test_001_hole_layer_is_magenta(self):
        layer = self.doc_out.layers.get(LAYER_HOLE)
        self.assertTrue(layer.dxf.hasattr("true_color"))
        self.assertEqual(layer.rgb, (255, 0, 255))

    def test_002_frame_layer_created_with_consumer_color(self):
        self.assertIn('frame', self.doc_out.layers)
        layer = self.doc_out.layers.get('frame')
        self.assertFalse(layer.dxf.hasattr("true_color"))


class TestWithoutMaps(unittest.TestCase):
    """Senza le mappe di snapbend topo non sa cos'è un foro: lo scrive sul
    layer col nome dello slug, grigio (D128 — niente registro)."""

    def test_001_hole_on_slug_layer(self):
        result, doc_in = _rect_with_hole_and_frame()
        doc_out = topo.to_dxf(result, doc_in)
        names = [layer.dxf.name for layer in doc_out.layers]   # la tabella DXF ignora le maiuscole
        self.assertIn("hole", names)
        self.assertNotIn(LAYER_HOLE, names)
        self.assertFalse(doc_out.layers.get("hole").dxf.hasattr("true_color"))


class TestRoleStyleColorOverride(unittest.TestCase):
    """Il chiamante cambia un colore di snapbend componendo le mappe."""

    def setUp(self):
        self.result, self.doc_in = _rect_with_hole_and_frame()
        self.doc_out = topo.to_dxf(
            self.result, self.doc_in,
            role_styles={**ROLE_STYLES, "hole": topo.RoleStyle(color=(0, 0, 0))},
            layers=LAYERS,
        )

    def test_001_hole_layer_true_color_is_black(self):
        layer = self.doc_out.layers.get(LAYER_HOLE)
        self.assertEqual(layer.rgb, (0, 0, 0))

    def test_002_other_layers_untouched(self):
        outer_layer = self.doc_out.layers.get("OuterContour")
        self.assertFalse(outer_layer.dxf.hasattr("true_color"))


if __name__ == "__main__":
    unittest.main()
