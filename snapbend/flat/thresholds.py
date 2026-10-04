"""
snapbend/flat/thresholds.py
---------------------------
Soglie di processo di `detect_flat()` (arrivate da forge, forge MAP.md D88).

    detect.py — HOLE_DIAMETER_THRESHOLD, default di `max_drill_diameter`
    holes.py  — THREADED_ARC_MAX_RADIUS_RATIO
"""

# ---------------------------------------------------------------------------
# Soglia diametro fori — default di detect_flat(max_drill_diameter=...)
# ---------------------------------------------------------------------------
# È un parametro di PROCESSO (capacità di foratura di macchina/utensile), non
# una costante di topologia: per questo la classificazione hole/inner vive in
# detect_flat() e non in heal()/hierarchy (MAP.md D15).
# contorno circolare con Ø < soglia  → Hole (foro da punta)
# contorno circolare con Ø >= soglia → ForgeContour (inner, tagliato a contorno)
HOLE_DIAMETER_THRESHOLD: float = 32.1   # mm

# ---------------------------------------------------------------------------
# Anello filettato (rappresentazione 3/4 di cerchio)
# ---------------------------------------------------------------------------
# L'arco a ~270° che rappresenta la cresta della filettatura è concentrico al
# preforo e ha raggio di poco maggiore: per le filettature metriche il rapporto
# diametro nominale / diametro preforo è ~1.1–1.3 (M6: 6.0/5.0 = 1.2). Un arco
# molto più grande (bordo esterno di una flangia tonda scantonata, estremità
# raggiata di un profilo) NON è un anello filettato: lo si scarta con questa
# soglia sul rapporto dei raggi.
THREADED_ARC_MAX_RADIUS_RATIO: float = 1.6