"""
tests/flat/test_pipeline_api.py
-------------------------------
(arrivato da topo tests/unit/test_pipeline_api.py, topo MAP.md D88)
Copre la superficie API introdotta in Fase 3 (MAP.md D2, D3):
  - detect_flat(doc, features="all") -> Result
  - detect_flat(result) ritorna il Result
"""

import unittest
import ezdxf

import topo
import topo_dxf
from snapbend.flat import detect_flat, describe_features, ALL_FEATURES


def _square_doc(side: float = 100.0):
    d = ezdxf.new("R2010")
    msp = d.modelspace()
    pts = [(0, 0), (side, 0), (side, side), (0, side), (0, 0)]
    for a, b in zip(pts, pts[1:]):
        msp.add_line(a, b)
    return topo_dxf.document_from_msp(msp, tolerance=0.5)


class TestPipelineApi(unittest.TestCase):

    def test_detect_flat_prende_il_documento_e_ritorna_un_result(self):
        r = detect_flat(_square_doc(), features="all", label="X")
        self.assertIsInstance(r, topo.Result)
        self.assertTrue(r.is_valid)
        self.assertEqual(r.cluster_count, 1)
        self.assertEqual(r.clusters[0].label, "X")      # le opzioni di heal passano

    def test_documento_non_valido_torna_comunque_un_result(self):
        # 3 lati di un quadrato: nessun contorno chiuso -> non valido, le lane non girano
        d = ezdxf.new("R2010")
        msp = d.modelspace()
        for a, b in [((0, 0), (100, 0)), ((100, 0), (100, 100)), ((100, 100), (0, 100))]:
            msp.add_line(a, b)
        doc = topo_dxf.document_from_msp(msp, tolerance=0.5)
        r = detect_flat(doc, features="all")
        self.assertIsInstance(r, topo.Result)
        self.assertFalse(r.is_valid)
        self.assertTrue(r.errors)

    def test_un_solo_ingresso(self):
        # niente wrapper: `detect_flat(doc)` e basta (MAP.md D78)
        import snapbend.flat
        self.assertIn("detect_flat", snapbend.flat.__all__)
        self.assertFalse(hasattr(snapbend.flat, "heal_and_detect"))


if __name__ == "__main__":
    unittest.main()
