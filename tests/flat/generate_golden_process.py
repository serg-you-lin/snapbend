"""
tests/flat/generate_golden_process.py
-------------------------------------
Genera la metà di processo dei golden (arrivata da forge, forge MAP.md D88):
fori, pieghe, incisioni, summary letti da detect_flat().

    tests/data/flat/golden/process/           ← un JSON per disegno singolo
    tests/data/flat/golden_multipli/process/  ← un JSON per pezzo dei fogli multipli

La geometria (outer, perimetri) la genera forge. Runna UNA VOLTA quando sei
soddisfatto dell'output corrente, mai per far passare un test.

    python tests/flat/generate_golden_process.py            # solo i mancanti
    python tests/flat/generate_golden_process.py --force    # rigenera tutti
    python tests/flat/generate_golden_process.py --only la_104
"""

import argparse
import json
from pathlib import Path

import forge
from forge.adapters.dxf.layers import role_to_dxf_layer

from snapbend.flat import detect_flat, describe_features, is_structural

DATA = Path(__file__).resolve().parent.parent / "data" / "flat"
GOLDEN_DXF_DIR = DATA / "golden"
GOLDEN_PROC_DIR = GOLDEN_DXF_DIR / "process"
MULTIPLI_DIR = DATA / "golden_multipli"
MULTIPLI_PROC_DIR = MULTIPLI_DIR / "process"
DEFAULT_TOLERANCE = 0.5
GLOBAL_NAME_ROLES = {"MARK": "engrave", "Signature": "engrave"}


def _config(path: Path) -> dict:
    p = DATA / "config" / f"{path.stem}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def _process(result, source_file: str) -> dict:
    """Metà di processo: quello che detect_flat() ha letto sul pezzo."""
    golden = {"source_file": source_file, "cluster_count": result.cluster_count, "clusters": []}
    for cluster in result.clusters:
        holes  = sorted(cluster.features("holes"),  key=lambda x: x.area, reverse=True)
        inners = sorted(cluster.inners, key=lambda x: x.area, reverse=True)
        bends  = cluster.features("bending_lines")
        engr   = cluster.features("engrave_lines")
        golden["clusters"].append({
            # area e outer per agganciare il pezzo
            "area_mm2":             round(cluster.area, 4),
            "outer_wkt":            cluster.outer.polygon.wkt,
            "holes_count":          len(holes),
            "holes_wkt":            [h.polygon.wkt for h in holes],
            "holes":                [h.to_dict() for h in holes],
            "bending_lines_count":  len(bends),
            "bending_lines":        [bl.to_dict() for bl in bends],
            "total_engrave_length": round(sum(e.length for e in engr), 4),
            "engrave_lines_count":  len(engr),
            "engrave_lines":        [e.to_dict() for e in engr],
            # summary — conteggi feature (D8, D44), solo le chiavi non-zero
            "summary": {k: v for k, v in
                        {**cluster.summary, **describe_features(cluster)}.items() if v},
            # contorni interni rimasti dopo che detect_flat ha preso i fori
            "inners_count":         len(inners),
            "inners_wkt":           [i.polygon.wkt for i in inners],
            "inners":               [i.to_dict() for i in inners],
        })
    return golden



def _write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def generate_single(force: bool, only: str = None) -> None:
    GOLDEN_PROC_DIR.mkdir(parents=True, exist_ok=True)
    for dxf_path in sorted(f for f in GOLDEN_DXF_DIR.glob("*")
                           if f.is_file() and f.suffix.lower() == ".dxf"
                           and not f.stem.endswith("_healed")):
        if only and dxf_path.stem != only:
            continue
        out = GOLDEN_PROC_DIR / f"{dxf_path.stem}.json"
        if out.exists() and not force:
            continue
        config = _config(dxf_path)
        tol = config.get("tolerance", DEFAULT_TOLERANCE)
        roles = {**GLOBAL_NAME_ROLES, **config.get("name_roles", {})}
        doc = forge.load_dxf(dxf_path, upgrade=True, explode_inserts=True, flatten_z_flag=True,
                             tolerance=tol, verbose=False, role_rules=forge.name_rules(roles))
        result = forge.heal(doc, tolerance=tol, is_structural=is_structural)
        detect_flat(result, features="all")
        if not result.is_valid:
            print(f"  SKIP (non valido): {dxf_path.name}")
            continue
        _write(out, _process(result, dxf_path.name))
        print(f"  OK: {out.name}")


def generate_multipli(force: bool, only: str = None) -> None:
    MULTIPLI_PROC_DIR.mkdir(parents=True, exist_ok=True)
    for parent_path in sorted(f for f in MULTIPLI_DIR.glob("*")
                              if f.is_file() and f.suffix.lower() == ".dxf"):
        if only and parent_path.stem != only:
            continue
        tol = _config(parent_path).get("tolerance", DEFAULT_TOLERANCE)
        result = forge.heal(forge.load_dxf(parent_path, upgrade=True, explode_inserts=True),
                            tolerance=tol)
        if not result.is_valid or not result.clusters:
            print(f"  SKIP (non valido): {parent_path.name}")
            continue
        detect_flat(result, features="all")
        for part_index, cluster in enumerate(result.clusters):
            out = MULTIPLI_PROC_DIR / f"{parent_path.stem}__{part_index:03d}.json"
            if out.exists() and not force:
                continue
            process = {
                "parent_file":   parent_path.name,
                "part_index":    part_index,
                # area e outer per agganciare il pezzo
                "area_mm2":      round(cluster.area, 4),
                "outer_wkt":     cluster.outer.polygon.wkt,
                # role_to_dxf_layer: un ruolo di processo (es. "hole") ha il
                # suo layer solo via il registro di rules/palette.py
                "inners_layers": [role_to_dxf_layer(i.role)
                                  for i in cluster.features("holes") + cluster.inners],
                "summary":       {
                    k: v for k, v in
                    {**cluster.summary, **describe_features(cluster)}.items()
                    if v
                },
            }

            _write(out, process)
            print(f"  OK: {out.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--only", type=str, default=None)
    args = parser.parse_args()
    generate_single(args.force, args.only)
    generate_multipli(args.force, args.only)
