"""
tests/flat/test_view_model_svg.py
---------------------------------
(arrivato da forge tests/unit/test_view_model_svg.py, forge MAP.md D88)
to_view_model()/to_svg() di forge sulla lettura di snapbend: fori, pieghe e
incisioni arrivano sotto `features` (forge D90).
"""

import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import forge
from snapbend.flat import heal_and_detect

EXAMPLES = Path(__file__).resolve().parents[1] / "data" / "flat"
MULTI_PART   = EXAMPLES / "golden" / "example_4_polylines.dxf"
SPECIAL      = EXAMPLES / "rect_with_special_layers.dxf"
MULTIFEATURE = EXAMPLES / "Multifeature.dxf"

SPECIAL_LM = {"Piega": "bending", "bend": "bending", "MARK": "engrave",
              "special": "engrave", "Filettati": "threaded_hole", "Svasati": "countersink"}


def _result(path, name_roles=None):
    doc = forge.load_dxf(str(path), tolerance=0.5, role_rules=forge.name_rules(name_roles or {}))
    return heal_and_detect(doc, features="all")


class TestViewModel(unittest.TestCase):

    def test_hole_carries_circle_metadata(self):
        vm = forge.to_view_model(_result(MULTI_PART))
        holes = [h for p in vm["clusters"] for h in p["features"]["holes"]]
        self.assertTrue(holes)
        h = holes[0]
        self.assertIn(h["hole_type"], ("plain", "countersink", "threaded"))
        self.assertGreater(h["diameter"], 0)
        self.assertEqual(len(h["center"]), 2)

    def test_holes_render_as_circles(self):
        self.assertIn("<circle", forge.to_svg(_result(MULTI_PART)))

    def test_bending_and_engrave_geometry(self):
        vm = forge.to_view_model(_result(SPECIAL, SPECIAL_LM))
        cluster = vm["clusters"][0]
        self.assertTrue(cluster["features"]["bending_lines"])
        self.assertTrue(cluster["features"]["engrave_lines"])
        for bl in cluster["features"]["bending_lines"]:
            self.assertFalse(bl["closed"])
            self.assertGreaterEqual(len(bl["points"]), 2)



@unittest.skipUnless(MULTIFEATURE.exists(), "Multifeature.dxf non tracciato")
class TestRichExample(unittest.TestCase):
    """Copertura extra sul file con tutte le feature (solo in locale)."""

    def test_all_feature_types_render(self):
        lm = {"Filettati": "threaded_hole", "Svasati": "countersink",
              "Piega": "bending", "MARK": "engrave"}
        result = _result(MULTIFEATURE, lm)
        svg = forge.to_svg(result)
        ET.fromstring(svg)
        self.assertIn("#00ff00", svg)                       # outer
        self.assertTrue("#0000ff" in svg or "#00ffff" in svg)  # foro tipato
        vm = forge.to_view_model(result)
        p = vm["clusters"][0]
        self.assertTrue(p["features"]["holes"] and p["features"]["bending_lines"] and p["features"]["engrave_lines"])



if __name__ == "__main__":
    unittest.main()
