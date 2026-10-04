"""
tests/flat/test_writeback.py
----------------------------
(arrivato da forge tests/integration/test_writeback.py, forge MAP.md D88)
Routing dei layer di processo in `forge.to_dxf` dopo `detect_flat()`: foro,
svasatura, piega, incisione.
"""

import unittest
from pathlib import Path

import forge
from snapbend.flat import (
    detect_flat, LAYER_HOLE, LAYER_COUNTERSINK, LAYER_BENDING, LAYER_ENGRAVE,
)

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "data" / "flat"


def _pipeline(name, *, detect=False, name_roles=None):
    """heal (+ detect) → to_dxf. Ritorna (result, msp_out)."""
    doc = forge.load_dxf(EXAMPLES_DIR / name, role_rules=forge.name_rules(name_roles or {}))
    result = forge.heal(doc)
    if detect:
        detect_flat(result, features="all")
    doc_out = forge.to_dxf(result, doc)
    return result, doc_out.modelspace()


def _layers_of(msp, dxftype):
    return {e.dxf.layer for e in msp.query(dxftype)}


# ---------------------------------------------------------------------------
# CIRCLE piccolo → LAYER_HOLE
# ---------------------------------------------------------------------------

class TestWritebackCircleHole(unittest.TestCase):

    def setUp(self):
        # D15: la promozione a foro è di detect_flat(features="holes"), non di heal().
        self.result, self.msp = _pipeline("rect_with_circle_hole.dxf", detect=True)

    def test_001_circle_on_hole_layer(self):
        self.assertIn(LAYER_HOLE, _layers_of(self.msp, "CIRCLE"))

    def test_002_circle_color_bylayer(self):
        for e in self.msp.query("CIRCLE"):
            if e.dxf.layer == LAYER_HOLE:
                self.assertEqual(e.dxf.color, 256)


# ---------------------------------------------------------------------------
# Countersink — routing dopo detect_flat()
# ---------------------------------------------------------------------------

class TestWritebackCountersink(unittest.TestCase):

    def setUp(self):
        self.result, self.msp = _pipeline("rect_with_countersink.dxf", detect=True)

    def test_001_countersink_on_correct_layer(self):
        circles = [e for e in self.msp.query("CIRCLE")
                   if e.dxf.layer == LAYER_COUNTERSINK]
        self.assertEqual(len(circles), 1)

    def test_002_countersink_collapsed_to_single_hole(self):
        # La coppia concentrica è un solo Hole nel modello → un solo CIRCLE,
        # sul layer Countersink (non più uno su Hole + uno su Countersink).
        self.assertEqual(len(list(self.msp.query("CIRCLE"))), 1)


# ---------------------------------------------------------------------------
# Special layers (BEND + MARK) — routing dopo detect_flat()
# ---------------------------------------------------------------------------

class TestWritebackSpecialLayers(unittest.TestCase):

    def setUp(self):
        self.result, self.msp = _pipeline(
            "rect_with_special_layers.dxf",
            detect=True,
            name_roles={"BEND": "bending", "MARK": "engrave"},
        )

    def test_001_no_source_layer_survives(self):
        # I layer originali "BEND"/"MARK" non compaiono mai nel doc_out.
        present = {e.dxf.layer for e in self.msp if e.dxf.hasattr("layer")}
        self.assertNotIn("BEND", present)
        self.assertNotIn("MARK", present)

    def test_002_bending_on_correct_layer(self):
        bending = [e for e in self.msp
                   if e.dxf.hasattr("layer") and e.dxf.layer == LAYER_BENDING]
        self.assertGreater(len(bending), 0)

    def test_003_engrave_geometry_materialized(self):
        # Regressione: to_dxf() deve scrivere la geometria delle engrave line,
        # non solo contarle nel modello.
        engrave = [e for e in self.msp
                   if e.dxf.hasattr("layer") and e.dxf.layer == LAYER_ENGRAVE]
        self.assertGreater(len(engrave), 0,
                           "Nessuna geometria engrave sul layer Engrave del doc_out")


if __name__ == "__main__":
    unittest.main()
