"""
05_compare_calibrations.py
---------------------------
Per ogni pezzo di una cartella officina (MAP D60), data come argomento:

    python 05_compare_calibrations.py <cartella officina>

stampa, fianco a fianco:
  - la lunghezza dello sviluppo REALE (DXF prodotto da TruBend)
  - quella della calibrazione "default"     (DIN 6935 + cava da tabella)
  - quella della calibrazione "tipo_misurato" (valori misurati dai .bnc)

Il calcolo passa TUTTO da un punto solo: BentProfile(...).develop() con
calibration= . Nessuna matematica in questo script.
"""

import glob
import os
import re
import sys
from pathlib import Path

import ezdxf
from ezdxf import bbox

from snapbend import Bend, BentProfile, Calibration, set_officina

# --- CONFIG ---
# i DXF veri dei pezzi di prova, nelle sottocartelle L/U/Z/O della cartella
# officina; la calibrazione "tipo_misurato" viene da lì anche lei.
if len(sys.argv) != 2:
    raise SystemExit("uso: python 05_compare_calibrations.py <cartella officina con i pezzi L/U/Z/O e calibrations/>")
DATA_DIR = Path(sys.argv[1])
set_officina(DATA_DIR)

FORME = {
    "L": [114.0, 114.0],
    "U": [60.0, 110.0, 60.0],
    "Z": [60.0, 100.0, 50.0],
    "O": [40.0, 40.0, 60.0, 30.0, 70.0],
}
CAVA = {"EV1": 6, "EV2": 8, "EV5": 16, "EW50": 50, "EW60": 60, "EV60": 60}


def golden_len(path: str) -> float:
    b = bbox.extents(ezdxf.readfile(path).modelspace())
    return max(b.size.x, b.size.y)


def parse_nome(fname: str):
    """(forma, spessore, cava) dal nome "parlante"; None se il nome non li dice
    (schema nuovo `L12.dxf`: spessore e cava stanno nel .bnc, fuori da snapbend)."""
    base = os.path.splitext(os.path.basename(fname))[0]
    forma = base[0]
    found = re.search(r"s(\d+)-", base)
    if found is None:
        return None
    spess = float(found.group(1))
    suff = base.split("-")[-1]
    cava = next((v for k, v in CAVA.items() if k == suff), None)
    return forma, spess, cava


def sviluppo(calibration, forma, spess, cava) -> float:
    segmenti = FORME[forma]
    bends = [Bend(angle=90, cava=cava) for _ in range(len(segmenti) - 1)]
    flat = BentProfile(flanges=segmenti, bends=bends, thickness=spess,
                       width=50, calibration=calibration).develop()
    return flat.meta["total_length"]


def main() -> None:
    default = Calibration.load("default")
    misurato = Calibration.load("tipo_misurato")

    print(f"{'file':44} {'sp':>3} {'cava':>4} "
          f"{'REALE':>9} {'default':>9} {'Δ':>7}  {'tipo_misurato':>13} {'Δ':>7}")
    print("-" * 100)
    for path in sorted(glob.glob(str(DATA_DIR / "[LUZO]" / "*.dxf"))):
        parsed = parse_nome(path)
        if parsed is None:
            continue
        forma, spess, cava = parsed
        if forma not in FORME:
            continue
        reale = golden_len(path)
        d = sviluppo(default, forma, spess, cava)
        m = sviluppo(misurato, forma, spess, cava)
        print(f"{os.path.basename(path):44} {spess:3.0f} {str(cava):>4} "
              f"{reale:9.2f} {d:9.2f} {d - reale:+7.2f}  {m:13.2f} {m - reale:+7.2f}")


if __name__ == "__main__":
    main()
