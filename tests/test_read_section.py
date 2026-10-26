"""
Round-trip test for the drawing interpreter.

Build a section from known parameters, throw away everything but its
outline, and check `read_section` recovers:
  - is_sheet_metal / is_bent
  - the thickness
  - the centerline segments (apex to apex)
  - the bend angles (naming scheme)

A section reads the same from either end, so segments/angles are compared
up to that reversal (see `_canonical`).
"""

import math
import random
import unittest

from snapbend.model.geometry import polar_point
from snapbend.model.section import Section
from snapbend.rules.read_section import SheetThicknessTable, read_section

SHAPES = {
    "L": ([114.0, 114.0], [90.0]),
    "U": ([60.0, 110.0, 60.0], [90.0, 90.0]),
    "Z": ([60.0, 100.0, 50.0], [90.0, 270.0]),
    "O": ([40.0, 40.0, 60.0, 30.0, 70.0], [90.0, 270.0, 270.0, 90.0]),
}
THICKNESSES = [1.0, 3.0, 10.0]


def _canonical(segments, angles):
    fwd = (list(segments), list(angles))
    rev = (list(reversed(segments)),
           [round((360.0 - a) % 360.0, 4) for a in reversed(angles)])
    return min(fwd, rev, key=lambda pair: (pair[0], pair[1]))


def _polygon(pts):
    return [{"type": "line", "start": pts[i], "end": pts[(i + 1) % len(pts)]} for i in range(len(pts))]


class TestReadSection(unittest.TestCase):

    def test_roundtrip_golden_shapes(self):
        for shape, (segments, angles) in SHAPES.items():
            for thickness in THICKNESSES:
                d = Section.default(shape, segments, angles, thickness)
                reading = read_section(d.section().entities)
                with self.subTest(section=d.name()):
                    self.assertTrue(reading.is_sheet_metal, reading.notes)
                    self.assertTrue(reading.is_bent, reading.notes)
                    self.assertAlmostEqual(reading.thickness, thickness, delta=1e-3)

                    exp_seg, exp_ang = _canonical(segments, angles)
                    self.assertEqual(len(reading.centerline_segments), len(exp_seg))
                    for got, want in zip(reading.centerline_segments, exp_seg):
                        self.assertAlmostEqual(got, want, delta=0.05)
                    self.assertEqual(
                        [round(a) % 360 for a in reading.angles],
                        [round(a) % 360 for a in exp_ang],
                    )

    def test_entity_order_does_not_matter(self):
        # Un contorno di topo arriva come anello testa-coda, non nell'ordine
        # di Section: la lettura deve essere la stessa con le entità rimescolate.
        for shape, (segments, angles) in SHAPES.items():
            entities = Section.default(shape, segments, angles, 3.0).section().entities
            expected = read_section(entities)
            for seed in range(20):
                shuffled = list(entities)
                random.Random(seed).shuffle(shuffled)
                reading = read_section(shuffled)
                with self.subTest(shape=shape, seed=seed):
                    self.assertEqual(reading.centerline_segments, expected.centerline_segments)
                    self.assertEqual(reading.angles, expected.angles)
                    self.assertEqual(reading.notes, [])

    def test_flat_plate_any_orientation(self):
        # Piatto senza pieghe, sdraiato e in piedi: i lati lunghi si
        # fronteggiano per 200, i tappi per 3 — vince lo spessore, non la
        # lunghezza (prima pareggiavano e decideva l'ordine delle entità).
        table = SheetThicknessTable(thicknesses_mm=[2.0, 3.0], tolerance_mm=0.05)
        for pts in ([(0, 0), (200, 0), (200, 3), (0, 3)], [(0, 0), (3, 0), (3, 200), (0, 200)]):
            reading = read_section(_polygon(pts), table=table)
            with self.subTest(pts=pts):
                self.assertTrue(reading.is_sheet_metal, reading.notes)
                self.assertFalse(reading.is_bent)
                self.assertAlmostEqual(reading.thickness, 3.0, delta=1e-3)
                self.assertEqual(reading.centerline_segments, [200.0])

    def test_sharp_corner_is_a_note_not_a_crash(self):
        # L a spigolo vivo: spessore letto, mezzeria no (raggio non disegnato)
        table = SheetThicknessTable(thicknesses_mm=[2.0, 3.0], tolerance_mm=0.05)
        reading = read_section(_polygon([(0, 0), (100, 0), (100, 100), (97, 100), (97, 3), (0, 3)]), table=table)
        self.assertAlmostEqual(reading.thickness, 3.0, delta=1e-3)
        self.assertEqual(reading.centerline_segments, [])
        self.assertTrue(any("sharp corner" in n for n in reading.notes))

    def test_flat_blank_is_sheet_but_not_bent(self):
        # a plain rectangle 200 x 3: constant-distance faces, no arcs
        rect = [
            {"type": "line", "start": (0, 0), "end": (200, 0)},
            {"type": "line", "start": (200, 0), "end": (200, 3)},
            {"type": "line", "start": (200, 3), "end": (0, 3)},
            {"type": "line", "start": (0, 3), "end": (0, 0)},
        ]
        reading = read_section(rect)
        self.assertTrue(reading.is_sheet_metal)
        self.assertFalse(reading.is_bent)
        self.assertAlmostEqual(reading.thickness, 3.0, delta=1e-3)

    def test_unknown_thickness_is_not_sheet_metal(self):
        rect = [
            {"type": "line", "start": (0, 0), "end": (200, 0)},
            {"type": "line", "start": (200, 0), "end": (200, 3.7)},
            {"type": "line", "start": (200, 3.7), "end": (0, 3.7)},
            {"type": "line", "start": (0, 3.7), "end": (0, 0)},
        ]
        table = SheetThicknessTable(thicknesses_mm=[1.0, 2.0, 3.0, 4.0],
                                    tolerance_mm=0.2)
        reading = read_section(rect, table=table)
        self.assertFalse(reading.is_sheet_metal)

    def test_angle_sign_survives_down_bend(self):
        # Z has one up (90) and one down (270) bend
        d = Section.default("Z", [60.0, 100.0, 50.0], [90.0, 270.0], 3.0)
        reading = read_section(d.section().entities)
        self.assertIn(270.0, [round(a) % 360 for a in reading.angles])
        self.assertIn(90.0, [round(a) % 360 for a in reading.angles])

    def test_two_concentric_circles_are_bent_sheet_metal(self):
        # MAP.md D42 - top view of a tube: two full circles, same center,
        # radii differing by exactly the thickness. Signal 1+2+3 must all
        # fire even though there is no straight cap anywhere.
        outer_r, thickness = 75.0, 3.0
        circles = [
            {"type": "circle", "center": (0.0, 0.0), "radius": outer_r},
            {"type": "circle", "center": (0.0, 0.0), "radius": outer_r - thickness},
        ]
        reading = read_section(circles)
        self.assertTrue(reading.is_sheet_metal, reading.notes)
        self.assertTrue(reading.is_bent, reading.notes)
        self.assertAlmostEqual(reading.thickness, thickness, delta=1e-3)

    def test_two_concentric_circles_centerline_not_recovered_yet(self):
        # Detection works (test above); the flange-chain recovery is a
        # separate, not-yet-built piece (D42 step 3) - it must degrade to
        # an explicit note, not crash and not fabricate segments/angles.
        circles = [
            {"type": "circle", "center": (0.0, 0.0), "radius": 75.0},
            {"type": "circle", "center": (0.0, 0.0), "radius": 72.0},
        ]
        reading = read_section(circles)
        self.assertEqual(reading.centerline_segments, [])
        self.assertEqual(reading.angles, [])
        self.assertTrue(any("centerline not recovered" in n for n in reading.notes))

    def test_single_circle_is_too_few_edges(self):
        reading = read_section([{"type": "circle", "center": (0.0, 0.0), "radius": 75.0}])
        self.assertFalse(reading.is_sheet_metal)
        self.assertFalse(reading.is_bent)

    def test_bare_calandra_arc_is_pure_arc_not_bentprofile(self):
        # MAP.md D42/D43 - a rolled "sella": R300 (centerline), 60deg,
        # thickness 3. cap -> outer arc -> cap -> inner arc, no straight
        # flange anywhere - Cylinder/Cone territory, not BentProfile.
        r_cl, half_angle, thickness = 300.0, 30.0, 3.0
        r_out, r_in = r_cl + thickness / 2.0, r_cl - thickness / 2.0
        entities = [
            {"type": "arc", "center": (0.0, 0.0), "radius": r_out,
             "start_angle": -half_angle, "end_angle": half_angle, "ccw": True},
            {"type": "line", "start": polar_point(r_out, half_angle),
             "end": polar_point(r_in, half_angle)},
            {"type": "arc", "center": (0.0, 0.0), "radius": r_in,
             "start_angle": half_angle, "end_angle": -half_angle, "ccw": False},
            {"type": "line", "start": polar_point(r_in, -half_angle),
             "end": polar_point(r_out, -half_angle)},
        ]
        table = SheetThicknessTable(thicknesses_mm=[1.0, 2.0, 3.0, 4.0], tolerance_mm=0.2)
        reading = read_section(entities, table=table)
        self.assertTrue(reading.is_sheet_metal, reading.notes)
        self.assertTrue(reading.is_bent, reading.notes)
        self.assertAlmostEqual(reading.thickness, thickness, delta=1e-3)
        self.assertEqual(reading.centerline_segments, [])
        self.assertEqual(reading.angles, [])
        self.assertAlmostEqual(reading.pure_arc_radius, r_cl, delta=1e-3)
        self.assertAlmostEqual(reading.pure_arc_angle_deg, 2 * half_angle, delta=1e-3)



def _l_with_stub():
    """L 25 x 35 esterni, t=3, raggio interno 3, col moncherino non piegato
    dell'ala da 25 disegnato nello stesso contorno (MAP.md D74): un
    rettangolo 25 x 3 che copre lo spigolo. L'arco esterno si vede solo per
    30°, poi entra nel moncherino; il lato sinistro del moncherino è un
    terzo tappo."""
    x_cut = 6.0 - 6.0 * math.cos(math.radians(30.0))     # dove l'arco esterno entra nel moncherino
    return [
        {"type": "line", "start": (0.0, 0.0), "end": (25.0, 0.0)},
        {"type": "line", "start": (25.0, 0.0), "end": (25.0, 3.0)},     # tappo, fine ala da 25
        {"type": "line", "start": (25.0, 3.0), "end": (6.0, 3.0)},
        {"type": "arc", "center": (6.0, 6.0), "radius": 3.0, "start_angle": 180.0, "end_angle": 270.0},
        {"type": "line", "start": (3.0, 6.0), "end": (3.0, 35.0)},
        {"type": "line", "start": (3.0, 35.0), "end": (0.0, 35.0)},     # tappo, fine ala da 35
        {"type": "line", "start": (0.0, 35.0), "end": (0.0, 6.0)},
        {"type": "arc", "center": (6.0, 6.0), "radius": 6.0, "start_angle": 180.0, "end_angle": 210.0},
        {"type": "line", "start": (x_cut, 3.0), "end": (0.0, 3.0)},
        {"type": "line", "start": (0.0, 3.0), "end": (0.0, 0.0)},       # lato del moncherino
    ]


class TestSectionWithStub(unittest.TestCase):
    """MAP.md D74: il contorno ha più della sezione; la lamiera piegata si
    legge dalla faccia che corre intera fra i due tappi veri."""

    def test_profile_read_from_the_whole_face(self):
        for seed in range(10):
            entities = _l_with_stub()
            random.Random(seed).shuffle(entities)
            reading = read_section(entities)
            with self.subTest(seed=seed):
                self.assertTrue(reading.is_bent, reading.notes)
                self.assertAlmostEqual(reading.thickness, 3.0, delta=1e-3)
                # mezzeria apice-apice: 25 - 1.5 e 35 - 1.5
                self.assertEqual(sorted(reading.centerline_segments), [23.5, 33.5])
                self.assertIn([round(a) % 360 for a in reading.angles], ([90], [270]))
                self.assertTrue(any("one face" in n for n in reading.notes))

    def test_bend_read_even_if_the_outer_arc_is_covered(self):
        reading = read_section(_l_with_stub())
        self.assertEqual(len(reading.bends), 1)
        bend = reading.bends[0]
        self.assertAlmostEqual(bend.angle, 90.0, delta=1e-6)
        self.assertAlmostEqual(bend.inner_radius, 3.0, delta=1e-6)

    def test_bends_also_on_a_clean_section(self):
        d = Section.default("U", [60.0, 110.0, 60.0], [90.0, 90.0], 3.0)
        reading = read_section(d.section().entities)
        self.assertEqual([round(b.angle) for b in reading.bends], [90, 90])
        self.assertFalse(any("one face" in n for n in reading.notes))

    def test_no_whole_face_is_a_note(self):
        # senza la faccia interna intera (spigolo vivo dentro) non si sceglie:
        # nota, mezzeria vuota, la piega letta resta
        entities = [e for e in _l_with_stub() if not (e["type"] == "arc" and e["radius"] == 3.0)]
        entities += [{"type": "line", "start": (6.0, 3.0), "end": (3.0, 3.0)},
                     {"type": "line", "start": (3.0, 3.0), "end": (3.0, 6.0)}]
        reading = read_section(entities)
        self.assertEqual(reading.centerline_segments, [])
        self.assertTrue(any("one face" in n for n in reading.notes))
        self.assertEqual(reading.bends, [])


class TestSectionWithAPartInTheCorner(unittest.TestCase):
    """MAP.md D75: L 110 x 78 esterni, t=4, raggio esterno 8, con un altro
    pezzo (un blocco) fuso nell'angolo: copre faccia e arco interni, che non
    compaiono. Il blocco fronteggia la faccia esterna più a lungo delle due
    facce della lamiera (67.5 contro 4)."""

    ENTITIES = [
        {"type": "line", "start": (0.0, 0.0), "end": (102.0, 0.0)},
        {"type": "arc", "center": (102.0, 8.0), "radius": 8.0, "start_angle": 270.0, "end_angle": 360.0},
        {"type": "line", "start": (110.0, 8.0), "end": (110.0, 78.0)},
        {"type": "line", "start": (110.0, 78.0), "end": (106.0, 78.0)},    # testata
        {"type": "line", "start": (106.0, 78.0), "end": (106.0, 67.5)},
        {"type": "line", "start": (106.0, 67.5), "end": (40.0, 67.5)},     # il blocco
        {"type": "line", "start": (40.0, 67.5), "end": (40.0, 4.0)},
        {"type": "line", "start": (40.0, 4.0), "end": (0.0, 4.0)},
        {"type": "line", "start": (0.0, 4.0), "end": (0.0, 0.0)},          # testata
    ]

    def test_l_read_from_its_outer_face(self):
        reading = read_section(self.ENTITIES)
        self.assertTrue(reading.is_sheet_metal, reading.notes)
        self.assertTrue(reading.is_bent, reading.notes)
        self.assertAlmostEqual(reading.thickness, 4.0, delta=1e-3)
        # mezzeria: 102 + (8 - 2) e 70 + 6
        self.assertEqual(sorted(reading.centerline_segments), [76.0, 108.0])
        self.assertIn([round(a) % 360 for a in reading.angles], ([90], [270]))
        self.assertTrue(any("not a sheet thickness" in n for n in reading.notes))

if __name__ == "__main__":
    unittest.main()
