import json
import os
import tempfile
import unittest

from snapbend import Cone, Cylinder


class TestToJson(unittest.TestCase):
    """`flat.to_json` scrive il JSON dal Result in memoria, spessore da `.meta`."""

    def _carica(self, flat, **kwargs):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "p.json")
            flat.to_json(path, **kwargs)
            with open(path, encoding="utf-8") as f:
                return json.load(f)["clusters"][0]

    def test_cylinder_prende_lo_spessore_dal_meta(self):
        flat = Cylinder(outer_diameter=150, height=500, thickness=2,
                        faceted=True, n_facets=8).develop()
        cluster = self._carica(flat, material="S275JR", quantity=3)
        self.assertEqual(cluster["thickness_mm"], 2.0)
        self.assertEqual(cluster["material"], "S275JR")
        self.assertEqual(cluster["quantity"], 3)
        self.assertEqual(cluster["bend_count"], 7)

    def test_cone_liscio_senza_pieghe(self):
        flat = Cone(top_outer_diameter=200, bottom_outer_diameter=150,
                    height=100, thickness=2).develop()
        self.assertEqual(self._carica(flat, material="S275JR")["bend_count"], 0)

    def test_quantity_si_moltiplica_per_split(self):
        # D83: un cono in due metà = due pezzi per ogni cono
        flat = Cone(top_outer_diameter=100, bottom_outer_diameter=250,
                    height=300, thickness=2, split=2).develop()
        self.assertEqual(self._carica(flat, material="S275JR")["quantity"], 2)
        self.assertEqual(self._carica(flat, material="S275JR", quantity=3)["quantity"], 6)

    def test_spessore_zero_resta_nd(self):
        flat = Cylinder(outer_diameter=150, height=500).develop()
        with self.assertWarns(UserWarning):
            cluster = self._carica(flat, material="S275JR")
        self.assertEqual(cluster["thickness_mm"], "N/D")


if __name__ == "__main__":
    unittest.main()
