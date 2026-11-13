"""
15_cono_a_settori_json.py
-------------------------
Cono in DUE METÀ (`split=2`), ciascuna a SETTORI piani (sfaccettato) uniti da
pieghe: scrive il file di taglio (.dxf) e il JSON dei metadati (.json) di una
metà. Le due metà sono uguali: `quantity` nel JSON esce 2 da solo (D83).

D_esterno sup 100, D_esterno inf 250, H 300, spessore 2. `N_FACETS` è il
numero di settori del cono INTERO: ogni metà ne prende N_FACETS/2.

Richiede topo installato a fianco.
"""

from pathlib import Path

from snapbend import Cone

TOP_DIAMETER = 100.0
BOTTOM_DIAMETER = 250.0
HEIGHT = 300.0
THICKNESS = 2.0
N_FACETS = 8
MATERIAL = "S275JR"

OUT_DIR = (Path(__file__).resolve().parent.parent.parent
           / "_debug" / "2026-11-13_snapbend_cono_2_meta_settori")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    flat = Cone(
        top_outer_diameter=TOP_DIAMETER, bottom_outer_diameter=BOTTOM_DIAMETER,
        height=HEIGHT, thickness=THICKNESS,
        split=2, faceted=True, n_facets=N_FACETS, label="cono_meta_settori",
    ).develop()

    flat.to_dxf(str(OUT_DIR / "cono_meta_settori.dxf"))
    flat.to_json(str(OUT_DIR / "cono_meta_settori.json"), material=MATERIAL)

    meta = flat.meta
    print(f"Settori per metà: {meta['n_facets']} (cono intero: {meta['n_facets_full']})")
    print(f"Angolo naturale del cono intero: {meta['full_angle_deg']:.3f}°, "
          f"per settore: {meta['facet_angle_deg']:.3f}°")
    print(f"Raggi di sviluppo: interno {meta['inner_radius']:.2f}, esterno {meta['outer_radius']:.2f}")
    print(f"Pieghe: {len(flat.bends)}, regola {sorted({b.rule for b in flat.bends})}")
    print(f"File in: {OUT_DIR}")


if __name__ == "__main__":
    main()
