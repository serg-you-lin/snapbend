"""
snapbend/flat/part_fields.py
----------------------------
I dati di lamiera di un pezzo, per chi li manda altrove (un gestionale, un
CAM): materiale, spessore, quantità, numero di fori, numero di colpi di
piega. Prima dell'8 novembre li dava topo (`build_metadata` +
`metadata_schema.py`, tolti da topo D230: parlavano la lingua del dominio).
Ora sono di snapbend, e si esportano con `topo.to_json`:

    result = detect_flat(doc, features="all")
    topo.save_json(result, "pezzi.json",
                   extra=part_fields(material="S275JR", thickness_mm=3.0))

`part_fields()` non scrive JSON: restituisce la funzione `extra(cluster) -> dict`
che `topo.to_json`/`save_json` chiamano per ogni cluster. Quello che topo
scrive già (`area`, `bbox`, `outer_perimeter`, `inner_perimeter`, `inner_count`,
`label`, `overlay`) non si ripete qui: un nome già suo darebbe `ValueError`.
"""

from __future__ import annotations

import warnings
from typing import Any, Callable, Optional, Union

import topo

from .detect import describe_features

# Un valore uguale per tutti i pezzi, o una funzione `cluster -> valore` quando
# cambia da pezzo a pezzo (in un file con più pezzi).
PerPart = Union[Any, Callable[[topo.Cluster], Any]]

# Materiale e spessore non si inventano: se il chiamante non li dà il campo c'è
# comunque, con questo valore, così nessuno legge un file senza accorgersene.
NOT_AVAILABLE = "N/D"


def _value(value: PerPart, cluster: topo.Cluster):
    return value(cluster) if callable(value) else value


def part_fields(
    *,
    material:     PerPart = NOT_AVAILABLE,
    thickness_mm: PerPart = NOT_AVAILABLE,
    quantity:     PerPart = 1,
    extra:        Optional[Union[dict, Callable[[topo.Cluster], dict]]] = None,
) -> Callable[[topo.Cluster], dict]:
    """
    La funzione `extra` per `topo.to_json(result, extra=...)`, con i dati di
    lamiera di ogni pezzo.

    Dal chiamante (snapbend non ne propone nessuno: materiale e spessore sono
    una sua scelta; se non li dà il campo vale "N/D" (e c'è un
    `UserWarning`, una volta per campo e per export), un campo `None` non
    viene scritto):
      `material`, `thickness_mm`, `quantity` (default 1) — un valore, o una
      funzione `cluster -> valore` se cambiano da pezzo a pezzo.
      `extra` — altri campi suoi (un dict, o `cluster -> dict`), aggiunti in coda.

    Dal pezzo (da `describe_features` e da `Cluster.to_dict()`):
      `plain_holes_count`, `countersink_count`, `threaded_holes_count`,
      `holes_count` (la somma), `bend_count` (colpi di piega, NON tratti: le
      linee collineari contano una piega, come in `describe_features`),
      `engrave_length_mm`, `marking_length_mm`, `total_perimeter_mm`.
    """
    avvisati: set = set()

    def fields(cluster: topo.Cluster) -> dict:
        features = describe_features(cluster)
        facts = cluster.to_dict()
        out: dict = {}
        for name, value in (("material", material), ("thickness_mm", thickness_mm),
                            ("quantity", quantity)):
            value = _value(value, cluster)
            if value == NOT_AVAILABLE and name not in avvisati:
                avvisati.add(name)
                warnings.warn(f"part_fields: {name} non dato, scritto come \"{NOT_AVAILABLE}\" nel JSON",
                              UserWarning, stacklevel=2)
            if value is not None:
                out[name] = value
        plain, sink, thread = (features["plain_holes_count"], features["countersink_count"],
                               features["threaded_holes_count"])
        out.update({
            "plain_holes_count":    plain,
            "countersink_count":    sink,
            "threaded_holes_count": thread,
            "holes_count":          plain + sink + thread,
            "bend_count":           features["bending_lines"],
            "engrave_length_mm":    features["total_engrave_length"],
            "marking_length_mm":    features["total_marking_length"],
            "total_perimeter_mm":   round(facts["outer_perimeter"] + facts["inner_perimeter"], 4),
        })
        if extra is not None:
            out.update(_value(extra, cluster))
        return out

    return fields
