"""
tests/flat/test_part_fields.py

`part_fields()`: i dati di lamiera di un pezzo (materiale, spessore, quantità,
fori, colpi di piega) come `extra` di `topo.to_json`. Il JSON lo scrive topo
(solo geometria); questi campi li aggiunge snapbend (MAP.md D79).
"""
import json
import unittest

import topo

from snapbend.flat import detect_flat, part_fields

fg = topo.geometry


def _piastra():
    # 100x60 con due fori Ø6 e due pieghe da bordo a bordo; la seconda è disegnata in due
    # tratti con un foro in mezzo (D53: solo un vuoto unisce due tratti collineari)
    segments = (fg.rectangle(100, 60) + fg.circle(3, center=(-30, 0)) + fg.circle(3, center=(10, 0))
                + [topo.primitives.LineSeg(start=(-10, -30), end=(-10, 30)),
                   topo.primitives.LineSeg(start=(10, -30), end=(10, -3)),
                   topo.primitives.LineSeg(start=(10, 3), end=(10, 30))])
    return topo.load_segments(segments)


class TestPartFields(unittest.TestCase):

    def _json(self, **options):
        result = detect_flat(_piastra(), features="all")
        return json.loads(topo.to_json(result, extra=part_fields(**options))), result

    def test_i_campi_di_lamiera_nel_json_di_topo(self):
        data, _ = self._json(material="S275JR", thickness_mm=3.0, quantity=4)
        cluster = data["clusters"][0]
        self.assertEqual((cluster["material"], cluster["thickness_mm"], cluster["quantity"]),
                         ("S275JR", 3.0, 4))
        self.assertEqual((cluster["holes_count"], cluster["plain_holes_count"]), (2, 2))
        # i campi di topo restano lì, i nostri non li coprono
        self.assertIn("area", cluster)
        self.assertIn("bbox", cluster)

    def test_colpi_di_piega_non_tratti(self):
        data, result = self._json()
        cluster = data["clusters"][0]
        self.assertEqual(len(result.clusters[0].features("bending_lines")), 3)   # tratti
        self.assertEqual(cluster["overlay"]["bending_lines"], 3)                  # topo: conteggio grezzo
        self.assertEqual(cluster["bend_count"], 2)                                # colpi di piega

    def test_materiale_e_spessore_non_si_inventano(self):
        cluster = self._json()[0]["clusters"][0]
        self.assertEqual((cluster["material"], cluster["thickness_mm"]), ("N/D", "N/D"))
        self.assertEqual(cluster["quantity"], 1)

    def test_valore_per_pezzo_e_campi_extra(self):
        data, _ = self._json(material=lambda c: "INOX", extra={"ordine": "A-1"})
        cluster = data["clusters"][0]
        self.assertEqual((cluster["material"], cluster["ordine"]), ("INOX", "A-1"))

    def test_perimetro_totale(self):
        data, _ = self._json()
        cluster = data["clusters"][0]
        self.assertAlmostEqual(cluster["total_perimeter_mm"],
                               cluster["outer_perimeter"] + cluster["inner_perimeter"], places=3)

    def test_nessun_nome_di_topo_riusato(self):
        # un nome che topo scrive già darebbe ValueError: lo provano gli altri test passando
        self._json(material="X", thickness_mm=1.0, quantity=1)


if __name__ == "__main__":
    unittest.main()
