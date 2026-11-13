"""
14_invalid_inner.py
-------------------
`snapbend.flat.detect_flat()` e i contorni interni che non vanno bene
(MAP.md D76, D77). Due casi diversi, due parametri diversi:

  1. **Un inner troppo vicino all'outer** — una soglia di processo, del
     CHIAMANTE: `min_inner_distance` (mm, default `None` = nessun controllo,
     snapbend non ne propone uno). Un contorno interno senza ruolo più vicino
     di così all'outer diventa un `Invalid` (`reason="inner-too-close"`,
     `distance`) in `cluster.overlay["invalid"]`, sul layer `Invalid` del DXF,
     e non diventa un foro. Resta un vuoto del pezzo: l'area netta non cambia.
  2. **Un inner che TOCCA l'outer** — non una soglia: un vuoto non può avere
     bordo in comune con l'esterno, quindi non è mai un inner. Se è un anello
     di tratti (la base di una vaschetta circondata dalle sue quattro pieghe)
     i suoi lati tornano in `loose` e la lane pieghe li legge. Sempre, senza
     parametri.

Il pezzo è costruito con le primitive di topo (`topo.geometry`), niente
file da cercare. Scrive in `output/` (ignorata da git): apri
`14_invalid_inner.dxf` e cerca il layer `Invalid`.

Richiede topo installato a fianco: pip install -e <percorso a topo>
"""

from collections import Counter
from pathlib import Path

import topo
import topo_dxf

from snapbend.flat import LAYERS, ROLE_STYLES, detect_flat

OUTPUT_DIR = Path(__file__).resolve().parent / "output"

fg = topo.geometry


def lamiera():
    """200 x 100 centrata in (0, 0), sei contorni interni a distanze diverse dal bordo."""
    segments = (
        fg.rectangle(200, 100)
        + fg.circle(5, center=(-90, 0))            # a  5 mm dal bordo sinistro
        + fg.circle(5, center=(-60, 0))            # a 35 mm
        + fg.rectangle(30, 10, center=(0, 41))     # lato a 4 mm dal bordo alto
        + fg.rectangle(30, 10, center=(0, 0))      # in mezzo
        + fg.stadium(40, 6, center=(60, 41))       # a  6 mm dal bordo alto
        + fg.stadium(40, 6, center=(60, -38))      # a  9 mm dal bordo basso
    )
    return topo.load_segments(segments)


def vaschetta():
    """Base 200 x 150 con quattro ali da 40: le quattro pieghe chiudono un anello."""
    outline = [(0, -40), (200, -40), (200, 0), (240, 0), (240, 150), (200, 150),
               (200, 190), (0, 190), (0, 150), (-40, 150), (-40, 0), (0, 0)]
    pieghe = [((0, 0), (200, 0)), ((200, 0), (200, 150)),
              ((200, 150), (0, 150)), ((0, 150), (0, 0))]
    segments = fg.polygon(outline) + [topo.primitives.LineSeg(start=a, end=b) for a, b in pieghe]
    return topo.load_segments(segments)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("=== 1. inner vicini all'outer: `min_inner_distance` ===")
    doc = lamiera()
    for limite in (None, 8.0):
        result = detect_flat(doc, features="holes", min_inner_distance=limite)
        cluster = result.clusters[0]
        print(f"\nmin_inner_distance={limite}: fori={len(cluster.features('holes'))}, "
              f"inner={len(cluster.inners)}, invalidi={len(cluster.features('invalid'))}, "
              f"area netta={cluster.area:.1f} mm²")
        for invalid in cluster.features("invalid"):
            forma = fg.contour_shape(invalid).kind
            print(f"   Invalid  {invalid.reason}  a {invalid.distance:.2f} mm  ({forma})")
        for warning in result.warnings:
            if warning.code == "inner-too-close":
                print("   warning:", warning.message)

    # il DXF dell'ultimo caso: gli invalidi sono sul loro layer
    out = topo_dxf.to_dxf(result, doc, role_styles=ROLE_STYLES, layers=LAYERS)
    out.saveas(OUTPUT_DIR / "14_invalid_inner.dxf")
    layers = Counter(e.dxf.layer for e in out.modelspace())
    print("\nlayer nel DXF:", dict(layers))

    print("\n=== 2. un anello che tocca l'outer: la vaschetta ===")
    doc = vaschetta()
    result = detect_flat(doc, features="bending")
    cluster = result.clusters[0]
    print(f"inner={len(cluster.inners)}, pieghe={len(cluster.features('bending_lines'))}, "
          f"loose={len(result.loose)}, area={cluster.area:.1f} mm²")
    topo_dxf.to_dxf(result, doc, role_styles=ROLE_STYLES, layers=LAYERS) \
        .saveas(OUTPUT_DIR / "14_vaschetta.dxf")

    print(f"\nFile in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
