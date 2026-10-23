"""
tests/test_drawing_sections.py
------------------------------
`find_sections()` su una tavola a viste letta da `topo.island()` (MAP.md D69):
una sezione sta nell'outer di un'isola, in un `loose` chiuso dentro un'altra
isola, o in due anelli annidati (un tubo: outer + cerchio in `loose`).
Fixture costruite con `Section` e `topo.load_geometry`, mai con ezdxf.
"""

import unittest

import topo

from snapbend.drawing import find_sections
from snapbend.drawing.sections import _entity
from snapbend.model.section import Section
from snapbend.rules.read_section import SheetThicknessTable, read_section

TABLE = SheetThicknessTable(thicknesses_mm=[1.0, 2.0, 3.0, 4.0], tolerance_mm=0.2)


def _shift(entities, dx, dy):
    out = []
    for e in entities:
        e = {k: v for k, v in e.items() if k != "role"}
        for key in ("start", "end", "center"):
            if key in e:
                e[key] = (e[key][0] + dx, e[key][1] + dy)
        out.append(e)
    return out


def _rectangle(x0, y0, x1, y1):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return [{"type": "line", "start": pts[i], "end": pts[(i + 1) % 4]} for i in range(4)]


def _sheet():
    """Una tavola: L da sola, U dentro un riquadro, un tubo, un rettangolo
    pieno, un foro con smusso dentro il riquadro."""
    entities = []
    entities += _shift(Section.default("L", [114.0, 114.0], [90.0], 3.0).section().entities, 0, 0)
    entities += _shift(Section.default("U", [60.0, 110.0, 60.0], [90.0, 90.0], 2.0).section().entities, 400, 0)
    entities += _rectangle(350, -50, 600, 200)
    entities += [{"type": "circle", "center": (800.0, 0.0), "radius": 75.0},
                 {"type": "circle", "center": (800.0, 0.0), "radius": 72.0}]
    entities += _rectangle(0, 300, 200, 400)
    entities += [{"type": "circle", "center": (550.0, 150.0), "radius": 6.0},
                 {"type": "circle", "center": (550.0, 150.0), "radius": 5.0}]
    return topo.island(topo.load_geometry(entities), max_gap=0.5)


class TestFindSections(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = _sheet()
        cls.sections = find_sections(cls.result, table=TABLE)

    def _at(self, x, y):
        """La sezione il cui contorno contiene (x, y)."""
        from shapely.geometry import Point
        hits = [s for s in self.sections if s.contour.polygon.buffer(1e-6).contains(Point(x, y))]
        self.assertEqual(len(hits), 1, f"sections at {(x, y)}: {len(hits)}")
        return hits[0]

    def test_only_l_and_u_are_found(self):
        # il rettangolo 200x100, il riquadro, il tubo e lo smusso no: un
        # contorno alla volta, i profili chiusi non sono di snapbend (D69)
        self.assertEqual(len(self.sections), 2)

    def test_l_is_an_island_outer(self):
        s = self._at(114.0, 50.0)
        self.assertIs(s.contour, self.result.clusters[s.cluster_ref].outer)
        self.assertTrue(s.reading.is_bent)
        self.assertAlmostEqual(s.reading.thickness, 3.0, delta=1e-3)
        self.assertEqual(s.reading.centerline_segments, [114.0, 114.0])
        self.assertEqual(s.reading.angles, [90.0])

    def test_u_inside_a_frame_is_a_loose_contour(self):
        s = self._at(460.0, 50.0)
        self.assertIn(s.contour, self.result.loose)
        frame = self.result.clusters[s.cluster_ref].outer
        self.assertAlmostEqual(frame.polygon.area, 250.0 * 250.0, delta=1e-6)
        self.assertEqual(s.reading.centerline_segments, [60.0, 110.0, 60.0])
        self.assertEqual(s.reading.angles, [90.0, 90.0])


# Profili inventati, nessuno a catalogo: il criterio è la lamiera (facce a
# spessore costante, archi concentrici, due tappi), non un elenco di forme.
CUSTOM = {
    "sei pieghe miste": ([40.0, 70.0, 30.0, 90.0, 25.0, 60.0, 45.0],
                         [90.0, 270.0, 135.0, 90.0, 225.0, 90.0], 2.0, 2.0),
    "angoli a 120/240": ([80.0, 50.0, 80.0], [120.0, 240.0], 3.0, 4.0),
    "piega a 30 gradi": ([100.0, 100.0], [150.0], 1.0, 1.0),
    "cappello asimmetrico": ([20.0, 35.0, 70.0, 35.0, 50.0], [270.0, 90.0, 90.0, 270.0], 2.0, 3.0),
    "raggio grande": ([60.0, 60.0, 60.0], [90.0, 90.0], 3.0, 15.0),
}


class TestCustomProfiles(unittest.TestCase):

    def test_invented_profiles_are_found(self):
        for name, (segments, angles, thickness, inner_radius) in CUSTOM.items():
            entities = _shift(Section("x", segments, angles, thickness,
                                      inner_radius=inner_radius).section().entities, 0, 0)
            found = find_sections(topo.island(topo.load_geometry(entities), max_gap=0.5), table=TABLE)
            with self.subTest(profile=name):
                self.assertEqual(len(found), 1)
                reading = found[0].reading
                self.assertTrue(reading.is_bent, reading.notes)
                self.assertAlmostEqual(reading.thickness, thickness, delta=1e-3)
                self.assertEqual(reading.centerline_segments, segments)
                self.assertEqual(reading.angles, angles)

    def test_flat_plate_is_found_not_bent(self):
        # lamiera senza pieghe: un piatto 200x3 da solo e uno 3x150 dentro un riquadro
        entities = _rectangle(0, 0, 200, 3) + _rectangle(300, 0, 303, 150) + _rectangle(250, -50, 400, 200)
        result = topo.island(topo.load_geometry(entities), max_gap=0.5)
        found = sorted(find_sections(result, table=TABLE), key=lambda s: s.reading.centerline_segments)
        self.assertEqual(len(found), 2)
        self.assertEqual([s.reading.centerline_segments for s in found], [[150.0], [200.0]])
        for s in found:
            self.assertFalse(s.reading.is_bent)
            self.assertAlmostEqual(s.reading.thickness, 3.0, delta=1e-3)

    def test_thickness_not_in_table_is_not_found(self):
        # un profilo piegato vero (facce parallele, archi concentrici, due
        # tappi) ma spessore 2.5: non è nella tabella, quindi non è lamiera
        entities = _shift(Section("x", [60.0, 80.0, 60.0], [90.0, 270.0], 2.5,
                                  inner_radius=2.0).section().entities, 0, 0)
        result = topo.island(topo.load_geometry(entities), max_gap=0.5)
        self.assertEqual(find_sections(result, table=TABLE), [])
        reading = read_section([_entity(s) for s in result.clusters[0].outer.segments], table=TABLE)
        self.assertAlmostEqual(reading.thickness, 2.5, delta=1e-3)
        self.assertTrue(any("not in sheet-thickness table" in n for n in reading.notes))


if __name__ == "__main__":
    unittest.main()
