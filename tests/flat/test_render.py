"""
tests/flat/test_render.py
-------------------------
Come forge disegna la lettura di snapbend (forge MAP.md D90): fori, svasature
e pieghe arrivano in `to_dxf` solo attraverso `cluster.detected`, ognuno sul
layer del suo ruolo, una volta sola.
"""

import unittest

import forge

from snapbend.flat import detect_flat, LAYER_HOLE, LAYER_COUNTERSINK, LAYER_THREADED_HOLE, LAYER_BENDING


def _plate():
    # piastra 100x50 con due cerchi concentrici e uno singolo
    doc = forge.load_geometry([
        {"type": "polygon", "points": [(0, 0), (100, 0), (100, 50), (0, 50)]},
        {"type": "circle", "center": (20, 25), "radius": 3},
        {"type": "circle", "center": (20, 25), "radius": 6},
        {"type": "circle", "center": (70, 25), "radius": 4},
    ])
    return doc, forge.heal(doc)


def _layers(out):
    return [e.dxf.layer for e in out.modelspace()]


class TestRender(unittest.TestCase):

    def test_001_i_fori_non_sono_scritti_due_volte(self):
        # (arrivato da forge tests/unit/test_attached_export.py)
        doc, result = _plate()
        detect_flat(result, "holes")
        n_holes = len(result.clusters[0].features("holes"))
        self.assertGreater(n_holes, 0)
        # un'entità per foro, sul layer del suo tipo: nessun doppione
        layers = _layers(forge.to_dxf(result, doc))
        self.assertEqual(
            sum(1 for l in layers if l in (LAYER_HOLE, LAYER_COUNTERSINK, LAYER_THREADED_HOLE)),
            n_holes,
        )

    def test_002_la_svasatura_va_sul_suo_layer(self):
        doc, result = _plate()
        detect_flat(result, "holes")
        layers = _layers(forge.to_dxf(result, doc))
        self.assertEqual(layers.count(LAYER_COUNTERSINK), 1)
        self.assertEqual(layers.count(LAYER_HOLE), 1)

    def test_003_una_piega_e_una_line(self):
        doc = forge.load_geometry([
            {"type": "polygon", "points": [(0, 0), (100, 0), (100, 50), (0, 50)]},
            {"type": "line", "start": (50, 0), "end": (50, 50)},
        ])
        result = forge.heal(doc)
        detect_flat(result, "bending")
        out = forge.to_dxf(result, doc)
        bends = [e for e in out.modelspace() if e.dxf.layer == LAYER_BENDING]
        self.assertEqual([e.dxftype() for e in bends], ["LINE"])

    def test_004_foro_etichettato_da_load_geometry(self):
        # (arrivato da forge tests/unit/adapters/test_geometry_loader.py)
        doc = forge.load_geometry([
            {"type": "polygon", "points": [(0, 0), (100, 0), (100, 50), (0, 50)], "role": "outer"},
            {"type": "circle", "center": (20, 25), "radius": 5, "role": "hole"},
        ])
        from snapbend.flat import heal_and_detect
        result = heal_and_detect(doc, label="rect_test")
        self.assertTrue(result.is_valid, result.errors)
        self.assertEqual(len(result.clusters[0].features("holes")), 1)



class TestBendingRule(unittest.TestCase):
    """Una piega attraversa il pezzo (snapbend MAP.md D52)."""

    def _bends(self, *lines):
        entities = [{"type": "polygon",
                     "points": [(0, 0), (100, 0), (100, 50), (0, 50)]}]
        entities += [{"type": "line", "start": a, "end": b} for a, b in lines]
        result = forge.heal(forge.load_geometry(entities))
        detect_flat(result, "bending")
        return result.clusters[0].features("bending_lines")

    def test_001_da_bordo_a_bordo_e_una_piega(self):
        self.assertEqual(len(self._bends(((50, 0), (50, 50)))), 1)

    def test_002_parallela_vicino_al_bordo_non_e_una_piega(self):
        # estremi a 0.99 mm dal bordo, ma la linea corre lungo il bordo
        self.assertEqual(self._bends(((30, 0.99), (40, 0.99))), [])

    def test_003_righino_storto_vicino_al_bordo_non_e_una_piega(self):
        # a 45°, tutti e due gli estremi entro 1 mm dallo stesso bordo
        self.assertEqual(self._bends(((30, 0.1), (30.9, 0.95))), [])

    def _bends_with_window(self, window):
        # pezzo 100x50; due tratti sulla retta y=25, da bordo a x=40 e da x=60 a bordo
        entities = [{"type": "polygon",
                     "points": [(0, 0), (100, 0), (100, 50), (0, 50)]},
                    {"type": "line", "start": (0, 25), "end": (40, 25)},
                    {"type": "line", "start": (60, 25), "end": (100, 25)}]
        if window:
            entities.append({"type": "polygon",
                             "points": [(40, 10), (60, 10), (60, 40), (40, 40)]})
        result = forge.heal(forge.load_geometry(entities))
        detect_flat(result, "bending")
        return result.clusters[0].features("bending_lines")

    def test_004_piega_interrotta_da_un_vuoto_e_una_piega(self):
        # D53: lo spazio fra i due tratti sta tutto dentro la finestra
        self.assertEqual(len(self._bends_with_window(True)), 2)

    def test_005_tratti_separati_da_materiale_non_sono_una_piega(self):
        # in mezzo c'è materiale e la linea non è disegnata: non la si inventa
        self.assertEqual(self._bends_with_window(False), [])


if __name__ == "__main__":
    unittest.main()
