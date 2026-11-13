"""
snapbend/drawing/__init__.py
----------------------------
Lettura di una tavola a viste sopra `topo.heal().outlines()`: quali contorni chiusi
sono sezioni di lamiera (MAP.md D69). Richiede topo installato.

    from snapbend.drawing import find_sections
    sections = find_sections(topo.heal(doc, max_gap=0.5).outlines())
"""

from .sections import DrawnSection, find_sections

__all__ = ["DrawnSection", "find_sections"]
