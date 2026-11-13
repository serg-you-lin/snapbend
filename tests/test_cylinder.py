import math
import unittest

from snapbend import Cylinder


class TestCylinderMath(unittest.TestCase):

    def test_width_is_mean_circumference(self):
        flat = Cylinder(outer_diameter=150, height=3895, thickness=2).develop()
        expected_width = math.pi * 148.0
        self.assertAlmostEqual(flat.meta["width"], expected_width, places=6)

    def test_inner_diameter_equals_outer_plus_two_thickness(self):
        # D81: stesso pezzo dato dall'interno o dall'esterno
        da_esterno = Cylinder(outer_diameter=150, height=500, thickness=2).develop()
        da_interno = Cylinder(inner_diameter=146, height=500, thickness=2).develop()
        self.assertAlmostEqual(da_interno.meta["width"], da_esterno.meta["width"], places=9)

    def test_both_or_neither_diameter_raises(self):
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=150, inner_diameter=146, height=500, thickness=2).develop()
        with self.assertRaises(ValueError):
            Cylinder(height=500, thickness=2).develop()

    def test_overlap_allunga_il_foglio_e_tiene_il_bbox_a_zero(self):
        # D84: l'opposto di margin — il foglio è più largo del giro nominale
        nominale = Cylinder(outer_diameter=150, height=500, thickness=2).develop()
        flat = Cylinder(outer_diameter=150, height=500, thickness=2, overlap=10).develop()
        self.assertAlmostEqual(flat.meta["width_cut"], nominale.meta["width"] + 10, places=9)
        xs = [x for x, _ in flat.entities[0]["points"]]
        self.assertAlmostEqual(min(xs), 0.0, places=9)
        self.assertEqual(len(flat.reference_entities), 1)

    def test_overlap_sfaccettato_sposta_le_pieghe_con_il_foglio(self):
        base = Cylinder(outer_diameter=150, height=500, thickness=2,
                        faceted=True, n_facets=8).develop()
        flat = Cylinder(outer_diameter=150, height=500, thickness=2,
                        faceted=True, n_facets=8, overlap=10).develop()
        pos_base = sorted(e["start"][0] for e in base.entities if e.get("role") == "bending")
        pos = sorted(e["start"][0] for e in flat.entities if e.get("role") == "bending")
        for a, b in zip(pos_base, pos):
            self.assertAlmostEqual(b, a + 5.0, places=9)

    def test_margin_e_overlap_insieme_sollevano(self):
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=150, height=500, thickness=2, margin=2, overlap=2).develop()

    def test_overlap_negativo_solleva(self):
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=150, height=500, thickness=2, overlap=-1).develop()

    def test_top_e_bottom_trim_accorciano_l_altezza(self):
        # D85: flangia in appoggio - il foglio è più basso alle due estremità
        flat = Cylinder(outer_diameter=150, height=500, thickness=2,
                        top_trim=20, bottom_trim=10).develop()
        ys = [y for _, y in flat.entities[0]["points"]]
        self.assertAlmostEqual(min(ys), 10.0, places=9)
        self.assertAlmostEqual(max(ys), 480.0, places=9)
        self.assertEqual(len(flat.reference_entities), 1)

    def test_trim_sfaccettato_accorcia_anche_le_pieghe(self):
        flat = Cylinder(outer_diameter=150, height=500, thickness=2, faceted=True,
                        n_facets=8, bottom_trim=10, top_trim=20).develop()
        pieghe = [e for e in flat.entities if e.get("role") == "bending"]
        self.assertEqual(len(pieghe), 7)
        for e in pieghe:
            self.assertAlmostEqual(e["start"][1], 10.0, places=9)
            self.assertAlmostEqual(e["end"][1], 480.0, places=9)

    def test_trim_negativo_o_che_mangia_tutto_solleva(self):
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=150, height=500, thickness=2, top_trim=-1).develop()
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=150, height=500, thickness=2,
                     top_trim=300, bottom_trim=200).develop()

    def test_entity_is_a_polygon(self):
        flat = Cylinder(outer_diameter=150, height=3895, thickness=2).develop()
        self.assertEqual(len(flat.entities), 1)
        entity = flat.entities[0]
        self.assertEqual(entity["type"], "polygon")
        self.assertEqual(len(entity["points"]), 4)

    def test_thickness_too_large_raises(self):
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=10, height=50, thickness=15).develop()

    def test_non_positive_dimension_raises(self):
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=0, height=50).develop()

    def test_default_orientation_puts_circumference_on_x(self):
        # default orientation="vertical": nessuno swap — X=circonferenza
        # (width), Y=lunghezza assiale (height), costruzione canonica.
        flat = Cylinder(outer_diameter=150, height=3895, thickness=2).develop()
        xs = [p[0] for p in flat.entities[0]["points"]]
        ys = [p[1] for p in flat.entities[0]["points"]]
        self.assertAlmostEqual(max(xs) - min(xs), flat.meta["width"], places=3)
        self.assertAlmostEqual(max(ys) - min(ys), 3895, places=3)

    def test_horizontal_orientation_puts_length_on_x(self):
        # orientation="horizontal": swap — l'asse lungo (height) va su X,
        # la circonferenza (width) su Y.
        flat = Cylinder(outer_diameter=150, height=3895, thickness=2, orientation="horizontal").develop()
        xs = [p[0] for p in flat.entities[0]["points"]]
        ys = [p[1] for p in flat.entities[0]["points"]]
        self.assertAlmostEqual(max(xs) - min(xs), 3895, places=3)
        self.assertAlmostEqual(max(ys) - min(ys), flat.meta["width"], places=3)

    def test_invalid_orientation_raises(self):
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=150, height=500, orientation="diagonal").develop()

    def test_margin_shortens_circumference_not_length(self):
        # Il margine toglie materiale a destra e sinistra (sviluppo/
        # circonferenza, per la cucitura longitudinale del rotolo), non
        # sopra/sotto — l'altezza (lunghezza assiale) resta invariata.
        no_margin = Cylinder(outer_diameter=150, height=500, thickness=2).develop()
        with_margin = Cylinder(outer_diameter=150, height=500, thickness=2, margin=2).develop()
        self.assertAlmostEqual(with_margin.meta["height"], no_margin.meta["height"], places=6)
        self.assertAlmostEqual(with_margin.meta["width_cut"], with_margin.meta["width"] - 2.0, places=6)

    def test_margin_produces_one_closed_reference_outline(self):
        # orientation="vertical" (canonico, default): X=circonferenza,
        # Y=lunghezza — il contorno pieno di riferimento deve essere alto
        # quanto height e largo quanto la circonferenza PIENA (non ridotta).
        flat = Cylinder(outer_diameter=150, height=500, thickness=2, margin=2, orientation="vertical").develop()
        self.assertEqual(len(flat.reference_entities), 1)
        ref = flat.reference_entities[0]
        self.assertEqual(ref["type"], "polygon")
        ys = [p[1] for p in ref["points"]]
        xs = [p[0] for p in ref["points"]]
        self.assertAlmostEqual(max(ys) - min(ys), 500, places=6)
        self.assertAlmostEqual(max(xs) - min(xs), flat.meta["width"], places=6)

    def test_no_margin_means_no_reference_lines(self):
        flat = Cylinder(outer_diameter=150, height=500, thickness=2).develop()
        self.assertEqual(flat.reference_entities, [])

    def test_margin_too_large_raises(self):
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=10, height=50, margin=1000).develop()

    def test_full_sector_angle_matches_default_width(self):
        # sector_angle=360 (default esplicito) deve tornare la stessa
        # formula di sempre — nessuna differenza per chi non lo tocca.
        implicit = Cylinder(outer_diameter=150, height=500, thickness=2).develop()
        explicit = Cylinder(outer_diameter=150, height=500, thickness=2, sector_angle=360.0).develop()
        self.assertAlmostEqual(implicit.meta["width"], explicit.meta["width"], places=9)

    def test_partial_sector_angle_width(self):
        # MAP.md D42 — sella calandrata: R300 (raggio medio) su 60°, senza
        # richiudere il giro. width = raggio_medio * angolo in radianti.
        r_mean = 300.0
        thickness = 3.0
        diameter = 2 * r_mean + thickness  # diametro ESTERNO, come da convenzione
        flat = Cylinder(outer_diameter=diameter, height=400, thickness=thickness, sector_angle=60.0).develop()
        expected_width = math.radians(60.0) * r_mean
        self.assertAlmostEqual(flat.meta["width"], expected_width, places=6)
        self.assertAlmostEqual(flat.meta["sector_angle_deg"], 60.0)

    def test_sector_angle_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=150, height=500, sector_angle=0.0).develop()
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=150, height=500, sector_angle=361.0).develop()

    def test_split_in_half_matches_explicit_sector_angle(self):
        # MAP.md D46: split=2 e' una scorciatoia, non una via diversa.
        via_split = Cylinder(outer_diameter=150, height=500, split=2).develop()
        via_angle = Cylinder(outer_diameter=150, height=500, sector_angle=180.0).develop()
        self.assertAlmostEqual(via_split.meta["width"], via_angle.meta["width"])
        self.assertAlmostEqual(via_split.meta["sector_angle_deg"], 180.0)

    def test_split_and_sector_angle_together_raises(self):
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=150, height=500, sector_angle=180.0, split=2).develop()

    def test_split_below_one_raises(self):
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=150, height=500, split=0).develop()


class TestCylinderPartialFaceted(unittest.TestCase):
    """MAP.md D46 — sfaccettato diviso in pezzi (es. due meta' saldate)."""

    def test_split_in_half_gives_half_the_facets(self):
        full = Cylinder(outer_diameter=150, height=500, thickness=2, faceted=True, n_facets=8).develop()
        half = Cylinder(
            outer_diameter=150, height=500, thickness=2, faceted=True, n_facets=8, split=2,
        ).develop()
        self.assertEqual(half.meta["n_facets"], 4)
        self.assertEqual(half.meta["n_facets_full"], 8)
        self.assertEqual(len(half.bends), 3)   # 4 faccette -> 3 giunti
        # Faccetta/angolo di piega sono proprieta' del poligono INTERO,
        # identiche fra il pezzo intero e la meta'.
        self.assertAlmostEqual(half.meta["facet_width"], full.meta["facet_width"])
        self.assertAlmostEqual(half.meta["facet_bend_radius"], full.meta["facet_bend_radius"])

    def test_margin_on_half_trims_the_weld_edges(self):
        # Lo stesso parametro margin che accorcia il pezzo intero (MAP.md
        # D46: "stessi parametri di accorciamento") vale sui due bordi
        # della meta' — quelli che poi si saldano all'altra meta'.
        no_margin = Cylinder(
            outer_diameter=150, height=500, thickness=2, faceted=True, n_facets=8, split=2,
        ).develop()
        with_margin = Cylinder(
            outer_diameter=150, height=500, thickness=2, faceted=True, n_facets=8, split=2, margin=2,
        ).develop()
        self.assertAlmostEqual(with_margin.meta["width_cut"], with_margin.meta["width"] - 2.0)
        self.assertAlmostEqual(with_margin.meta["width"], no_margin.meta["width"])

    def test_split_not_on_a_facet_boundary_raises(self):
        # 8 faccette non si dividono in 3 parti uguali su un confine esatto.
        with self.assertRaises(ValueError):
            Cylinder(
                outer_diameter=150, height=500, thickness=2, faceted=True, n_facets=8, split=3,
            ).develop()


class TestCylinderFaceted(unittest.TestCase):

    def test_facet_width_matches_inscribed_polygon_chord(self):
        flat = Cylinder(outer_diameter=150, height=500, thickness=2, faceted=True, n_facets=8).develop()
        r_mean = 148.0 / 2.0
        expected_chord = 2.0 * r_mean * math.sin(math.pi / 8)
        self.assertAlmostEqual(flat.meta["facet_width"], expected_chord, places=6)

    def test_produces_n_minus_one_bending_lines(self):
        flat = Cylinder(outer_diameter=150, height=500, thickness=2, faceted=True, n_facets=8).develop()
        bend_lines = [e for e in flat.entities if e.get("role") == "bending"]
        self.assertEqual(len(bend_lines), 7)

    def test_default_n_facets_is_eight(self):
        flat = Cylinder(outer_diameter=150, height=500, thickness=2, faceted=True).develop()
        self.assertEqual(flat.meta["n_facets"], 8)

    def test_default_bend_radius_comes_from_calibration(self):
        # MAP.md D45: senza facet_bend_radius esplicito, il raggio viene
        # dalla calibration (default = "default", D33). "default" non
        # conosce nessuna cava -> raggio = spessore (D62).
        flat = Cylinder(outer_diameter=150, height=500, thickness=2, faceted=True).develop()
        self.assertAlmostEqual(flat.meta["facet_bend_radius"], 2.0)

    def test_explicit_facet_bend_radius_still_wins(self):
        flat = Cylinder(
            outer_diameter=150, height=500, thickness=2, faceted=True, facet_bend_radius=2.0,
        ).develop()
        self.assertAlmostEqual(flat.meta["facet_bend_radius"], 2.0)

    def test_faceted_bends_populated_one_per_joint(self):
        # MAP.md D45: come BentProfile, l'operatore deve sapere come
        # impostare la macchina per ogni piega — anche sulle faccette.
        flat = Cylinder(outer_diameter=150, height=500, thickness=2, faceted=True, n_facets=8).develop()
        self.assertEqual(len(flat.bends), 7)   # N facce -> N-1 giunti
        for b in flat.bends:
            self.assertAlmostEqual(b.angle, 45.0)   # 360/8
            self.assertEqual(b.rule, "din6935")      # "default" non conosce cave
            self.assertGreater(b.bend_allowance, 0.0)

    def test_explicit_facet_k_factor_reports_as_esplicito(self):
        flat = Cylinder(
            outer_diameter=150, height=500, thickness=2, faceted=True, facet_k_factor=0.4,
        ).develop()
        self.assertEqual(flat.bends[0].rule, "esplicito")
        self.assertAlmostEqual(flat.bends[0].k_factor, 0.4)

    def test_polygon_perimeter_converges_to_circle_as_facets_grow(self):
        # Il PERIMETRO del poligono (N*corda) converge alla circonferenza —
        # ma meta["width"] no: include anche l'allowance delle N-1 pieghe,
        # che con un raggio di piega FISSO (default = thickness, non legato
        # a N) tende a una costante all'aumentare di N, non a zero. Più
        # faccette non vuol dire automaticamente più vicino allo sviluppo
        # liscio in lunghezza totale — converge la geometria, non il
        # materiale delle pieghe.
        r_mean = 148.0 / 2.0

        def chord_perimeter(n):
            return n * 2.0 * r_mean * math.sin(math.pi / n)

        circumference = math.pi * 148.0
        err_coarse = abs(chord_perimeter(8) - circumference)
        err_fine = abs(chord_perimeter(200) - circumference)
        self.assertLess(err_fine, err_coarse)
        self.assertLess(err_fine, 0.05)

    def test_n_facets_below_three_raises(self):
        with self.assertRaises(ValueError):
            Cylinder(outer_diameter=150, height=500, faceted=True, n_facets=2).develop()

    def test_margin_still_trims_circumference_not_length(self):
        # Anche sfaccettato: il margine taglia nelle due faccette estreme
        # (width_cut < width), l'altezza e la lunghezza di ogni faccetta
        # (facet_width) non cambiano.
        no_margin = Cylinder(outer_diameter=150, height=500, thickness=2, faceted=True, n_facets=8).develop()
        with_margin = Cylinder(outer_diameter=150, height=500, thickness=2, faceted=True, n_facets=8, margin=2).develop()
        self.assertAlmostEqual(with_margin.meta["height"], no_margin.meta["height"], places=6)
        self.assertAlmostEqual(with_margin.meta["facet_width"], no_margin.meta["facet_width"], places=6)
        self.assertAlmostEqual(with_margin.meta["width_cut"], with_margin.meta["width"] - 2.0, places=6)

    def test_margin_too_large_for_end_facet_raises(self):
        # margin che mangerebbe oltre la prima/ultima faccetta intera —
        # non solo un pezzetto del suo bordo — deve essere rifiutato.
        with self.assertRaises(ValueError):
            Cylinder(
                outer_diameter=150, height=500, thickness=2, faceted=True, n_facets=8, margin=200,
            ).develop()

    def test_smooth_is_still_the_default(self):
        flat = Cylinder(outer_diameter=150, height=500, thickness=2).develop()
        self.assertNotIn("n_facets", flat.meta)


if __name__ == "__main__":
    unittest.main()
