"""
tests/flat/test_models.py
-------------------------
(arrivato da forge tests/unit/test_models.py, forge MAP.md D88)
Test puri sui tipi di snapbend.flat: Hole, BendingLine.
"""
import unittest

from shapely.geometry import Point, Polygon, LineString

from forge.model.role import ContourRole
from snapbend.flat.model import (
    Hole, BendingLine,
    HOLE_TYPE_UNKNOWN, HOLE_TYPE_PLAIN, HOLE_TYPE_COUNTERSINK, HOLE_TYPE_THREADED,
)
from snapbend.flat.roles import HOLE, BEND


# ---------------------------------------------------------------------------
# Test Hole
# ---------------------------------------------------------------------------

class TestHole(unittest.TestCase):

    def _make_hole(self, diameter=10.0, center=(50.0, 50.0), hole_type=HOLE_TYPE_PLAIN):
        r = diameter / 2
        poly = Point(center).buffer(r, resolution=64)
        return Hole(
            polygon=poly,
            diameter=diameter,
            center=center,
            hole_type=hole_type,
            confidence=1.0,
            source="geometric",
            role='hole',
        )

    def test_001_area(self):
        """Area approssima π*r²."""
        import math
        hole = self._make_hole(diameter=10.0)
        expected = math.pi * 5.0 ** 2
        print(f"\n[Hole] area={hole.area:.4f} expected≈{expected:.4f}")
        self.assertAlmostEqual(hole.area, expected, delta=0.01)

    def test_002_bbox(self):
        """Bbox centrato sul centro del foro."""
        hole = self._make_hole(diameter=10.0, center=(50.0, 50.0))
        minx, miny, maxx, maxy = hole.bbox
        print(f"[Hole] bbox={hole.bbox}")
        self.assertAlmostEqual(minx, 45.0, delta=0.01)
        self.assertAlmostEqual(miny, 45.0, delta=0.01)
        self.assertAlmostEqual(maxx, 55.0, delta=0.01)
        self.assertAlmostEqual(maxy, 55.0, delta=0.01)

    def test_003_is_hole_always_true(self):
        """is_hole è sempre True su Hole."""
        hole = self._make_hole()
        self.assertTrue(hole.is_hole)

    def test_004_hole_type_default(self):
        """hole_type default è UNKNOWN."""
        r = 5.0
        poly = Point((0, 0)).buffer(r, resolution=64)
        hole = Hole(role=HOLE, polygon=poly, diameter=10.0, center=(0, 0))
        self.assertEqual(hole.hole_type, HOLE_TYPE_UNKNOWN)

    def test_005_to_dict_keys(self):
        """to_dict ha tutte le chiavi attese."""
        hole = self._make_hole()
        d = hole.to_dict()
        print(f"\n[Hole.to_dict] keys={list(d.keys())}")
        for key in ["hole_type", "diameter", "center", "role", "confidence", "source"]:
            self.assertIn(key, d)

    def test_006_to_dict_values(self):
        """to_dict valori corretti."""
        hole = self._make_hole(diameter=8.0, center=(10.0, 20.0))
        d = hole.to_dict()
        print(f"[Hole.to_dict] {d}")
        self.assertAlmostEqual(d["diameter"], 8.0, places=4)
        self.assertEqual(d["center"], (10.0, 20.0))
        self.assertEqual(d["hole_type"], HOLE_TYPE_PLAIN)

    def test_007_to_dict_countersink_has_outer_diameter(self):
        """to_dict include outer_diameter se presente."""
        hole = self._make_hole(hole_type=HOLE_TYPE_COUNTERSINK)
        hole.outer_diameter = 14.0
        d = hole.to_dict()
        print(f"[Hole.to_dict] outer_diameter={d.get('outer_diameter')}")
        self.assertIn("outer_diameter", d)
        self.assertAlmostEqual(d["outer_diameter"], 14.0, places=4)

    def test_008_to_dict_plain_no_outer_diameter(self):
        """to_dict NON include outer_diameter per foro plain."""
        hole = self._make_hole(hole_type=HOLE_TYPE_PLAIN)
        d = hole.to_dict()
        self.assertNotIn("outer_diameter", d)

    def test_009_confidence_default(self):
        """confidence default è 0.0."""
        r = 5.0
        poly = Point((0, 0)).buffer(r, resolution=64)
        hole = Hole(role=HOLE, polygon=poly, diameter=10.0, center=(0, 0))
        self.assertEqual(hole.confidence, 0.0)

    def test_010_source_default(self):
        """source default è stringa vuota."""
        r = 5.0
        poly = Point((0, 0)).buffer(r, resolution=64)
        hole = Hole(role=HOLE, polygon=poly, diameter=10.0, center=(0, 0))
        self.assertEqual(hole.source, "")


# ---------------------------------------------------------------------------
# Test BendingLine
# ---------------------------------------------------------------------------

class TestBendingLine(unittest.TestCase):

    def _make_bl(self, start=(0, 0), end=(100, 0), cluster_label=""):
        geom = LineString([start, end])
        import math
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        angle = math.degrees(math.atan2(dy, dx)) % 180.0
        return BendingLine(
            role=BEND,
            geometry=geom,
            length=geom.length,
            angle_deg=angle,
            cluster_label=cluster_label,
        )

    def test_001_to_dict_keys(self):
        """to_dict ha tutte le chiavi attese."""
        bl = self._make_bl(cluster_label="p1")
        d = bl.to_dict()
        print(f"\n[BendingLine.to_dict] keys={list(d.keys())}")
        for key in ["start", "end", "length", "angle_deg", "cluster_label"]:
            self.assertIn(key, d)

    def test_002_to_dict_length(self):
        """to_dict length corretta per BL orizzontale da 100mm."""
        bl = self._make_bl()
        d = bl.to_dict()
        print(f"[BendingLine.to_dict] length={d['length']}")
        self.assertAlmostEqual(d["length"], 100.0, places=4)

    def test_003_to_dict_angle(self):
        """to_dict angle_deg corretto per BL orizzontale."""
        bl = self._make_bl()
        d = bl.to_dict()
        print(f"[BendingLine.to_dict] angle_deg={d['angle_deg']}")
        self.assertAlmostEqual(d["angle_deg"], 0.0, places=4)

    def test_004_to_dict_cluster_label(self):
        """to_dict cluster_label preservato."""
        bl = self._make_bl(cluster_label="pezzo_3")
        d = bl.to_dict()
        self.assertEqual(d["cluster_label"], "pezzo_3")

    def test_005_to_dict_start_end_are_tuples(self):
        """start e end in to_dict sono tuple (x, y)."""
        bl = self._make_bl(start=(5, 10), end=(105, 10))
        d = bl.to_dict()
        print(f"[BendingLine.to_dict] start={d['start']} end={d['end']}")
        self.assertEqual(len(d["start"]), 2)
        self.assertEqual(len(d["end"]), 2)




if __name__ == "__main__":
    unittest.main()
