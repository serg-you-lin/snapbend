"""
tests/flat/test_inner_distance.py

`detect_flat(min_inner_distance=...)`: un contorno interno senza ruolo più
vicino di N mm all'outer diventa un `Invalid` nell'overlay e non un foro.
Senza il parametro (default `None`) snapbend non decide niente.
Un anello che TOCCA l'outer è un'altra cosa (sempre invalido, letto come
pieghe): vedi `test_bend_at_corner`.
"""
import unittest

import topo
import topo_dxf
from snapbend.flat import (
    LAYER_INVALID, LAYERS, ROLE_STYLES, detect_flat,
)

fg = topo.geometry


def _piece():
    # lamiera 100x100 centrata in (0,0): un foro Ø10 a 5 mm dal bordo sinistro
    # (centro x=-40, bordo del foro a x=-45) e uno Ø10 lontano da tutto
    segments = fg.rectangle(100, 100) + fg.circle(5, center=(-40, 0)) + fg.circle(5, center=(10, 0))
    return topo.load_segments(segments)


class TestMinInnerDistance(unittest.TestCase):

    def test_senza_limite_nessun_controllo(self):
        result = detect_flat(_piece(), "holes")
        self.assertEqual(len(result.clusters[0].features("holes")), 2)
        self.assertFalse([w for w in result.warnings if w.code == "inner-too-close"])

    def test_il_foro_vicino_e_invalido_quello_lontano_resta_foro(self):
        result = detect_flat(_piece(), "holes", min_inner_distance=8.0)
        cluster = result.clusters[0]
        self.assertEqual(len(cluster.features("holes")), 1)
        invalid = cluster.features("invalid")
        self.assertEqual([(i.reason, round(i.distance, 3)) for i in invalid], [("inner-too-close", 5.0)])
        self.assertEqual(len(cluster.inners), 0)   # via dagli inner, come un foro promosso
        self.assertEqual(len([w for w in result.warnings if w.code == "inner-too-close"]), 1)

    def test_il_limite_e_una_distanza_stretta(self):
        # il foro sta a 5 mm: un limite di 5 non lo invalida ("più vicino di")
        result = detect_flat(_piece(), "holes", min_inner_distance=5.0 - 1e-9)
        self.assertEqual(len(result.clusters[0].features("holes")), 2)

    def test_il_layer_nel_dxf(self):
        doc = _piece()
        result = detect_flat(doc, "holes", min_inner_distance=8.0)
        out = topo_dxf.to_dxf(result, doc, role_styles=ROLE_STYLES, layers=LAYERS)
        self.assertIn(LAYER_INVALID, {e.dxf.layer for e in out.modelspace()})

    def test_l_area_netta_non_cambia(self):
        # un inner invalido resta un vuoto del pezzo: stessa area con o senza limite
        a = detect_flat(_piece(), "holes")
        b = detect_flat(_piece(), "holes", min_inner_distance=8.0)
        self.assertAlmostEqual(a.clusters[0].area, b.clusters[0].area, places=6)


if __name__ == "__main__":
    unittest.main()
