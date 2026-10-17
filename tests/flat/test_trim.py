"""
tests/flat/test_trim.py

Tratteggio delle linee di piega (MAP.md D63): la piega resta una, con l'asse
intero in `geometry`; i tratti stanno in `dashes` e sono quello che topo
disegna. Le misure sono uguali per tutte o scelte da una regola del chiamante.
"""
import math
import unittest

import topo
from topo.core.primitives import LineSeg
from snapbend.flat import LAYER_BENDING, DashPattern, describe_features, detect_flat, trim_bending_lines


def _read(outline, bends):
    segments = topo.geometry.polygon(outline)
    segments += [LineSeg(start=a, end=b) for a, b in bends]
    return detect_flat(topo.heal(topo.load_segments(segments)), "bending")


def _plate():
    # lamiera 300x200 con una piega lunga 300 e una corta 200
    return _read([(0, 0), (300, 0), (300, 200), (0, 200)],
                 [((0, 100), (300, 100)), ((150, 0), (150, 200))])


def _by_length(result):
    return sorted(result.clusters[0].features("bending_lines"), key=lambda b: b.length)


class TestTrimBendingLines(unittest.TestCase):

    def test_same_pattern_for_every_bend(self):
        result = trim_bending_lines(_plate(), DashPattern(head=20, tail=20, middle=20, n_middle=1))
        for bl in _by_length(result):
            self.assertEqual(len(bl.dashes), 3)
            self.assertEqual([round(math.dist(a, b), 9) for a, b in bl.dashes], [20, 20, 20])

    def test_axis_stays_whole_and_bend_count_does_not_change(self):
        result = _plate()
        before = describe_features(result.clusters[0])["bending_lines"]
        trim_bending_lines(result, DashPattern(head=20, tail=20, middle=20, n_middle=2))
        short, long_ = _by_length(result)
        self.assertAlmostEqual(short.length, 200)
        self.assertAlmostEqual(long_.length, 300)
        self.assertEqual(describe_features(result.clusters[0])["bending_lines"], before)

    def test_dashes_are_what_topo_draws(self):
        result = trim_bending_lines(_plate(), DashPattern(head=10, tail=10, middle=10, n_middle=3))
        for bl in _by_length(result):
            self.assertEqual(len(bl.contours), 5)
            self.assertEqual(bl.to_dict()["dashes"][0][0], bl.dashes[0][0])

    def test_rule_chooses_per_bend_and_none_keeps_it_whole(self):
        rule = lambda bl: DashPattern(head=30, tail=30) if bl.length > 250 else None
        short, long_ = _by_length(trim_bending_lines(_plate(), rule))
        self.assertEqual(short.dashes, [])
        self.assertEqual(len(short.contours), 1)
        self.assertNotIn("dashes", short.to_dict())
        self.assertEqual(len(long_.dashes), 2)

    def test_covered_bend_stays_whole(self):
        result = trim_bending_lines(_plate(), DashPattern(head=100, tail=100, middle=50, n_middle=1))
        short, long_ = _by_length(result)
        self.assertEqual(short.dashes, [])
        self.assertEqual(len(long_.dashes), 3)

    def test_trimming_again_replaces_the_dashes(self):
        result = trim_bending_lines(_plate(), DashPattern(head=10, tail=10, middle=10, n_middle=4))
        trim_bending_lines(result, DashPattern(head=10, tail=10))
        for bl in _by_length(result):
            self.assertEqual(len(bl.dashes), 2)

    def test_dxf_has_one_line_per_dash(self):
        result = trim_bending_lines(_plate(), DashPattern(head=20, tail=20, middle=20, n_middle=1))
        lines = [e for e in topo.to_dxf(result).modelspace().query("LINE")
                 if e.dxf.layer == LAYER_BENDING]
        self.assertEqual(len(lines), 6)


if __name__ == "__main__":
    unittest.main()
