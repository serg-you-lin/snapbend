"""
tests/flat/test_bend_at_corner.py

Una piega senza layer che parte da uno spigolo dell'outer, collineare col
lato che arriva lì, è ancora una piega: il pezzo resta uno, l'outer è il
contorno intero, la piega va nella lane geometrica (topo MAP.md D110).
Prima la fusione collineare di topo univa piega e lato in una riga sola e
il pezzo diventava due rettangoli sovrapposti.
"""
import unittest

import topo
from snapbend.flat import detect_flat


def _read(outline, bends, extra=()):
    segments = topo.geometry.polygon(outline) + list(extra)
    segments += [topo.primitives.LineSeg(start=a, end=b) for a, b in bends]
    return detect_flat(topo.heal(topo.load_segments(segments)), "bending")


class TestBendAtCorner(unittest.TestCase):

    def assertPart(self, result, area, bends):
        self.assertTrue(result.is_valid)
        self.assertEqual(result.cluster_count, 1)
        cluster = result.clusters[0]
        self.assertAlmostEqual(cluster.outer.area, area, places=6)
        self.assertEqual(len(cluster.features("bending_lines")), bends)
        self.assertEqual(result.loose, [])

    def test_vaschetta_quattro_pieghe_su_quattro_spigoli(self):
        # base 200x150, ali da 40: ogni spigolo concavo è l'estremo di due pieghe
        outline = [(0, -40), (200, -40), (200, 0), (240, 0), (240, 150), (200, 150),
                   (200, 190), (0, 190), (0, 150), (-40, 150), (-40, 0), (0, 0)]
        bends = [((0, 0), (200, 0)), ((200, 0), (200, 150)),
                 ((200, 150), (0, 150)), ((0, 150), (0, 0))]
        self.assertPart(_read(outline, bends), 58000, 4)

    def test_due_ali_uno_spigolo_e_due_estremi_a_meta_lato(self):
        outline = [(0, -30), (300, -30), (300, 0), (330, 0), (330, 120), (0, 120)]
        bends = [((0, 0), (300, 0)), ((300, 0), (300, 120))]
        self.assertPart(_read(outline, bends), 48600, 2)

    def test_ala_stretta_con_foro(self):
        outline = [(0, 0), (400, 0), (400, 80), (325, 80), (325, 140), (75, 140), (75, 80), (0, 80)]
        result = _read(outline, [((75, 80), (325, 80))], topo.geometry.circle(8, center=(200, 40)))
        self.assertPart(result, 47000, 1)
        self.assertEqual(len(result.clusters[0].inners), 1)


if __name__ == "__main__":
    unittest.main()
