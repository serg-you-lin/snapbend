"""
Golden test "officina 1".

NON prova la correttezza della fisica della piega (i numeri li abbiamo
messi noi nel profilo, dai .bnc): prova che la CATENA GEOMETRICA sia
giusta — somma dei segmenti, posizione delle linee di piega, versi
alternati di Z/omega — dato l'accorciamento corretto.

Gira sulle copie in tests/data/officina: i DXF col nome che dice spessore e
matrice, tracciati — niente dati locali, niente .bnc (snapbend MAP D59).
"""

import glob
import os
import re
import unittest

TOLLERANZA_MM = 0.1

DATI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "officina")

FORME = {
    "L": [114.0, 114.0],
    "U": [60.0, 110.0, 60.0],
    "Z": [60.0, 100.0, 50.0],
    "O": [40.0, 40.0, 60.0, 30.0, 70.0],
}
CAVA = {"EV1": 6, "EV2": 8, "EV5": 16, "EW50": 50, "EW60": 60, "EV60": 60}

class TestGoldenOfficina1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import ezdxf  # noqa
        from snapbend import Calibration
        cls.calibration = Calibration.load("tipo_misurato", folder=DATI)
        cls.files = sorted(glob.glob(f"{DATI}/[LUZO]/*.dxf"))
        assert cls.files, "nessun DXF di test trovato"

    def _caso(self, path):
        base = os.path.splitext(os.path.basename(path))[0]
        forma = base[0]
        # schema verboso storico: ...s<spessore>-<matrice>
        spess = float(re.search(r"s(\d+)-", base).group(1))
        cava = CAVA.get(base.split("-")[-1])
        return forma, spess, cava

    def test_lunghezza_sviluppo(self):
        import ezdxf
        from ezdxf import bbox
        from snapbend import Bend, BentProfile

        for path in self.files:
            forma, spess, cava = self._caso(path)
            if forma not in FORME:
                continue
            with self.subTest(file=os.path.basename(path)):
                b = bbox.extents(ezdxf.readfile(path).modelspace())
                reale = max(b.size.x, b.size.y)
                segmenti = FORME[forma]
                bends = [Bend(angle=90, cava=cava) for _ in range(len(segmenti) - 1)]
                flat = BentProfile(flanges=segmenti, bends=bends, thickness=spess,
                                   width=50, calibration=self.calibration).develop()
                self.assertAlmostEqual(flat.meta["total_length"], reale,
                                       delta=TOLLERANZA_MM)

    def test_posizioni_linee_di_piega(self):
        import ezdxf
        from snapbend import Bend, BentProfile

        for path in self.files:
            forma, spess, cava = self._caso(path)
            if forma not in FORME or len(FORME[forma]) < 3:
                continue  # solo i multi-piega
            with self.subTest(file=os.path.basename(path)):
                doc = ezdxf.readfile(path)
                msp = doc.modelspace()
                poly = [e for e in msp if e.dxftype() == "POLYLINE"][0]
                ys = [v.dxf.location.y for v in poly.vertices]
                xs = [v.dxf.location.x for v in poly.vertices]
                vert = (max(ys) - min(ys)) > (max(xs) - min(xs))
                o = min(ys) if vert else min(xs)
                reali = sorted(
                    (l.dxf.start.y if vert else l.dxf.start.x) - o
                    for l in msp if l.dxftype() == "LINE"
                )
                segmenti = FORME[forma]
                bends = [Bend(angle=90, cava=cava) for _ in range(len(segmenti) - 1)]
                flat = BentProfile(flanges=segmenti, bends=bends, thickness=spess,
                                   width=50, calibration=self.calibration).develop()
                nostre = sorted(
                    e["start"][0] for e in flat.entities if e.get("role") == "bending"
                )
                self.assertEqual(len(nostre), len(reali))
                for n, r in zip(nostre, reali):
                    self.assertAlmostEqual(n, r, delta=TOLLERANZA_MM)


if __name__ == "__main__":
    unittest.main()
