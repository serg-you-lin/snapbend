"""
tests/flat/test_holes.py
------------------------
(arrivato da forge tests/unit/test_geometry.py, forge MAP.md D88)
Test unitari per snapbend.flat.holes:
  - is_threaded_hole      : riconosce fori filettati (cerchio + arco a 270°)
  - is_countersink_outer  : riconosce il cerchio esterno di un countersink
"""

import math
import unittest

from forge.core.primitives.segments import ArcSeg

from snapbend.flat.holes import is_threaded_hole, is_countersink_outer


def make_arc(cx, cy, radius, start_angle, end_angle):
    """Crea un ArcSeg con angoli in gradi."""
    return ArcSeg(
        center=(cx, cy),
        radius=radius,
        start_angle=math.radians(start_angle),
        end_angle=math.radians(end_angle),
        ccw=True
    )



# ---------------------------------------------------------------------------
# is_threaded_hole
# ---------------------------------------------------------------------------

class TestIsThreadedHole(unittest.TestCase):

    def test_001_arco_270_gradi_e_filettato(self):
        arc = make_arc(0, 0, 6, 0, 270)
        self.assertTrue(is_threaded_hole((0, 0), 5, [arc]))

    def test_002_arco_260_gradi_entro_tolleranza(self):
        arc = make_arc(0, 0, 6, 0, 260)
        self.assertTrue(is_threaded_hole((0, 0), 5, [arc]))

    def test_003_arco_180_gradi_non_filettato(self):
        arc = make_arc(0, 0, 6, 0, 180)
        self.assertFalse(is_threaded_hole((0, 0), 5, [arc]))

    def test_004_arco_360_non_filettato(self):
        arc = make_arc(0, 0, 6, 0, 360)
        self.assertFalse(is_threaded_hole((0, 0), 5, [arc]))

    def test_005_tolleranza_custom_stretta(self):
        arc = make_arc(0, 0, 6, 0, 260)
        self.assertFalse(is_threaded_hole((0, 0), 5, [arc], angle_tolerance=1.0))

    def test_006_arco_ruotato_stesso_risultato(self):
        arc = make_arc(0, 0, 6, 45, 315)  # 270 gradi, ruotato
        self.assertTrue(is_threaded_hole((0, 0), 5, [arc]))

    def test_007_nessun_arco(self):
        self.assertFalse(is_threaded_hole((0, 0), 5, []))

    def test_008_arco_non_concentrico(self):
        arc = make_arc(100, 100, 6, 0, 270)
        self.assertFalse(is_threaded_hole((0, 0), 5, [arc]))

    def test_009_arco_piu_piccolo_del_cerchio(self):
        arc = make_arc(0, 0, 4, 0, 270)
        self.assertFalse(is_threaded_hole((0, 0), 5, [arc]))

    def test_010_piu_archi_uno_solo_valido(self):
        arc_bad = make_arc(0, 0, 6, 0, 180)   # non filettato
        arc_ok  = make_arc(0, 0, 6, 0, 270)   # filettato
        self.assertTrue(is_threaded_hole((0, 0), 5, [arc_bad, arc_ok]))

    def test_011_tolleranza_centro(self):
        # Centro leggermente spostato, entro tolleranza
        arc = make_arc(0.5, 0.5, 6, 0, 270)
        self.assertTrue(is_threaded_hole((0, 0), 5, [arc], tolerance_center=1.0))

    def test_012_centro_fuori_tolleranza(self):
        arc = make_arc(2.0, 0, 6, 0, 270)
        self.assertFalse(is_threaded_hole((0, 0), 5, [arc], tolerance_center=1.0))

    def test_013_arco_molto_piu_grande_non_filettato(self):
        # Arco concentrico a 270° ma raggio 3x il foro: bordo di flangia
        # scantonata / estremita raggiata di un profilo, non un anello filettato.
        arc = make_arc(0, 0, 16, 0, 270)
        self.assertFalse(is_threaded_hole((0, 0), 5, [arc]))

    def test_014_rapporto_raggi_custom(self):
        arc = make_arc(0, 0, 9, 0, 270)   # ratio 1.8
        self.assertFalse(is_threaded_hole((0, 0), 5, [arc]))
        self.assertTrue(is_threaded_hole((0, 0), 5, [arc], max_radius_ratio=2.0))


# ---------------------------------------------------------------------------
# is_countersink_outer
# ---------------------------------------------------------------------------

class TestIsCountersinkOuter(unittest.TestCase):

    def test_001_cerchio_grande_con_piccolo_concentrico(self):
        """Il cerchio esterno ha un cerchio più piccolo concentrico."""
        self.assertTrue(is_countersink_outer((0, 0), 10, [((0, 0), 5)]))

    def test_002_cerchio_senza_figli(self):
        self.assertFalse(is_countersink_outer((0, 0), 10, []))

    def test_003_cerchio_con_figlio_non_concentrico(self):
        self.assertFalse(is_countersink_outer((0, 0), 10, [((50, 50), 5)]))

    def test_004_cerchio_con_figlio_stesso_raggio(self):
        self.assertFalse(is_countersink_outer((0, 0), 10, [((0, 0), 10)]))

    def test_005_cerchio_con_figlio_piu_grande(self):
        self.assertFalse(is_countersink_outer((0, 0), 10, [((0, 0), 15)]))

    def test_006_piu_figli_uno_solo_concentrico(self):
        siblings = [((50, 50), 3), ((0, 0), 4)]
        self.assertTrue(is_countersink_outer((0, 0), 10, siblings))

    def test_007_tolleranza_centro(self):
        # Centro leggermente spostato, entro tolleranza
        self.assertTrue(is_countersink_outer((0, 0), 10, [((0.5, 0.5), 5)], tolerance=1.0))

    def test_008_centro_fuori_tolleranza(self):
        self.assertFalse(is_countersink_outer((0, 0), 10, [((2.0, 0), 5)], tolerance=1.0))




if __name__ == "__main__":
    unittest.main()
