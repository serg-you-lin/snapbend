# snapbend — code index

**Generated file — do not edit by hand.** Regenerate with:

```
python tests/gen_index.py
```

What this is: the lookup table of *what already exists* in the package, down to internal helpers. `docs/API.md` documents the public surface (`snapbend.<name>`) with full cards; this file lists every module-level function and class so nothing gets rewritten because it was not found. Signatures and docstring lines come straight from the source, so they cannot drift.

`30` modules · `99` module-level functions · `22` classes · `4557` lines of code.

Sections: [Lookup](#lookup) · [Duplicate names](#duplicate-names) · [Dependency rule](#dependency-rule) · [By module](#by-module) · [Internal dependencies](#internal-dependencies)

---

## Lookup

Every module-level name in the package, alphabetically. **Search here before writing a new helper.**

| name | kind | location | what |
|---|---|---|---|
| `_arc_point` | func | `snapbend/rules/read_section.py:113` |  |
| `_assign_to_part` | func | `snapbend/flat/detect.py:617` | Scrive `ce` nel cluster che la contiene; False se nessuno la contiene: |
| `_belongs_to_cluster` | func | `snapbend/flat/detect.py:602` | Un'entità aperta (marking/bending) appartiene al cluster se la sua |
| `Bend` | class | `snapbend/core/bend.py:103` | Una singola piega fra due flange consecutive. |
| `bend_allowance_din6935` | func | `snapbend/rules/deduction.py:76` | Lunghezza dell'asse neutro dentro la piega, con K stimato DIN 6935. |
| `bend_deduction` | func | `snapbend/rules/deduction.py:49` | Accorciamento di piega, formula della fibra neutra. |
| `_bend_lines` | func | `snapbend/io/dxf.py:302` | Una riga per piega nell'header — gli stessi numeri che dice |
| `_bending_line` | func | `snapbend/flat/detect.py:293` |  |
| `_bending_line_from_data` | func | `snapbend/flat/detect.py:731` |  |
| `BendingLine` | class | `snapbend/flat/model/bending_line.py:22` |  |
| `BendResult` | class | `snapbend/core/bend.py:168` | Esito del calcolo di UNA piega dentro `BentProfile.develop()` (o di |
| `BentProfile` | class | `snapbend/core/bend.py:200` | Profilo piegato: N flange (quote a MEZZERIA) unite da N-1 pieghe. |
| `Calibration` | class | `snapbend/rules/deduction.py:237` | Una calibrazione = i dati di calcolo di un'officina. |
| `_canonical` | func | `snapbend/rules/read_section.py:413` | A section reads the same from either end. Pick a deterministic |
| `_cap` | func | `snapbend/model/section.py:416` |  |
| `centerline_to_external_flange` | func | `snapbend/rules/deduction.py:143` | Inversa di `external_to_centerline_flange`: da mezzeria a esterno-esterno. |
| `_centroid` | func | `snapbend/flat/detect.py:671` | Baricentro esatto della curva chiusa; None se non racchiude area. |
| `_chain_vertex` | func | `snapbend/rules/read_section.py:479` |  |
| `_check_orientation` | func | `snapbend/model/geometry.py:40` |  |
| `_circle` | func | `snapbend/flat/detect.py:387` | (diametro, centro) se il contorno è un cerchio per `topo.geometry.contour_shape`, |
| `_circular_inners` | func | `snapbend/flat/detect.py:397` | (contour, diameter, center) per ogni inner geometricamente circolare. |
| `ClassifiedEntity` | class | `snapbend/flat/model/classified.py:14` | Risultato della classificazione di una entità da detect_flat(). |
| `Cone` | class | `snapbend/core/cone.py:140` |  |
| `_contours` | func | `snapbend/drawing/sections.py:59` | (contorno, cluster_ref) per ogni outer, inner e curva chiusa in loose. |
| `Cylinder` | class | `snapbend/core/cylinder.py:79` |  |
| `DashPattern` | class | `snapbend/flat/trim.py:21` | Misure del tratteggio di una piega: `head` sul primo capo, `tail` |
| `deduction_din6935` | func | `snapbend/rules/deduction.py:81` | Accorciamento di piega con K stimato DIN 6935 (scorciatoia di |
| `DeductionInfo` | class | `snapbend/rules/deduction.py:197` | Accorciamento di piega + da dove viene il numero. |
| `default_radius` | func | `snapbend/rules/deduction.py:102` | Raggio interno quando non c'è né un raggio esplicito né una cava nota: |
| `describe_features` | func | `snapbend/flat/detect.py:130` | Conteggio ricco per i tipi **noti di topo** — fori per tipo, pieghe |
| `_detect_bending` | func | `snapbend/flat/detect.py:306` | Una piega attraversa il pezzo (`topo.geometry.splits_contour`, prolungata di |
| `_detect_engrave` | func | `snapbend/flat/detect.py:508` | Inferenza geometrica delle incisioni — NON ANCORA IMPLEMENTATA. |
| `detect_flat` | func | `snapbend/flat/detect.py:91` | Classifica le feature dentro le parti già trovate da heal(). |
| `_detect_holes` | func | `snapbend/flat/detect.py:358` | Lane geometrica: promuove a `Hole` i contorni interni circolari. |
| `_detect_labeled` | func | `snapbend/flat/detect.py:179` |  |
| `develop_from_external_flanges` | func | `snapbend/human_layer.py:35` | Come `BentProfile.develop()`, ma `external_flanges` sono quote |
| `_direction` | func | `snapbend/rules/read_section.py:298` |  |
| `_dist` | func | `snapbend/rules/read_section.py:105` |  |
| `DrawnSection` | class | `snapbend/drawing/sections.py:31` | Una sezione di lamiera trovata nella tavola. |
| `_Edge` | class | `snapbend/rules/read_section.py:128` |  |
| `_edge_end` | func | `snapbend/model/section.py:408` |  |
| `_edge_start` | func | `snapbend/model/section.py:400` |  |
| `_edge_to_entity` | func | `snapbend/model/section.py:420` |  |
| `_endpoint_counts` | func | `snapbend/rules/read_section.py:443` |  |
| `Engraving` | class | `snapbend/flat/model/engraving.py:29` |  |
| `_engraving_from_closed` | func | `snapbend/flat/detect.py:546` |  |
| `_engraving_from_open` | func | `snapbend/flat/detect.py:531` |  |
| `_ensure_detected` | func | `snapbend/flat/detect.py:33` | `cluster.detected`, creandolo alla prima scrittura. |
| `_entities_bbox` | func | `snapbend/io/dxf.py:199` | Bbox degli entity grezzi (linee/archi, schema `FlatGeometry.entities`) |
| `_entity` | func | `snapbend/drawing/sections.py:87` | Segmento nativo di topo -> entità dello schema di `read_section()` |
| `estimate_k_factor` | func | `snapbend/core/bend.py:83` | Stima un K-factor di partenza da materiale + rapporto R/T, secondo la |
| `export_part` | func | `snapbend/human_layer.py:66` | Esporta un pezzo su un UNICO file DXF a livelli (Fase 3, MAP.md D32): |
| `external_flanges_to_centerline` | func | `snapbend/rules/deduction.py:157` | Converte l'intero elenco di flange (come lo si passerebbe a |
| `external_to_centerline_deduction` | func | `snapbend/rules/deduction.py:89` | Converte un accorciamento riferito alle quote esterne (come nei .bnc |
| `external_to_centerline_flange` | func | `snapbend/rules/deduction.py:122` | Converte la lunghezza ESTERNO-ESTERNO di una flangia (apice virtuale |
| `_extract_data` | func | `snapbend/flat/detect.py:683` |  |
| `_extract_data_from_source` | func | `snapbend/flat/detect.py:716` | Dati di un'entità chiusa (`ClosedCurve`) letti sui suoi segmenti. |
| `_face_pair_distances` | func | `snapbend/rules/read_section.py:262` | (distance, overlap) for lines that genuinely face each other |
| `_faceted_sector_outline` | func | `snapbend/core/cone.py:102` | Perimetro del settore sfaccettato fra i vertici dati: N corde esterne, un |
| `find_sections` | func | `snapbend/drawing/sections.py:44` | Tutti i contorni chiusi di `result` che `read_section()` dice lamiera |
| `FlangeFace` | class | `snapbend/model/section.py:78` | Per una flangia: la faccia ESTERNA (convessa) se è coerente da un |
| `FlangeQuote` | class | `snapbend/model/section.py:92` | La quota da disegnare per una flangia nella vista in sezione |
| `FlatGeometry` | class | `snapbend/model/geometry.py:81` | Sviluppo piano di una forma sviluppabile — output di Cone.develop() / |
| `_fmt` | func | `snapbend/model/section.py:63` |  |
| `_handle_engrave_closed` | func | `snapbend/flat/detect.py:590` |  |
| `_handle_engrave_closed_loose` | func | `snapbend/flat/detect.py:577` | Come _handle_engrave_open ma per una traccia engrave già chiusa |
| `_handle_engrave_open` | func | `snapbend/flat/detect.py:561` | Una traccia engrave aperta va al cluster che la contiene |
| `_has_concentric_pair` | func | `snapbend/rules/read_section.py:311` |  |
| `heal_and_detect` | func | `snapbend/flat/pipeline.py:18` | heal() + detect_flat(). `detect_flat()` viene saltato se heal() non produce |
| `Hole` | class | `snapbend/flat/model/hole.py:28` |  |
| `_hole_from_contour` | func | `snapbend/flat/detect.py:469` |  |
| `is_structural` | func | `snapbend/flat/roles.py:69` | Predicato strutturale COMPLETO: outer/inner (motore) + hole/countersink/ |
| `is_threaded_hole` | func | `snapbend/flat/holes.py:17` | True se attorno al cerchio c'è un arco a ~270° (entro ``angle_tolerance`` |
| `k_din6935` | func | `snapbend/rules/deduction.py:65` | Stima DIN 6935 del fattore K (in [0, 0.5]), dal SOLO rapporto |
| `_labeled_hole_from_contour` | func | `snapbend/flat/detect.py:486` | `Contour` con ruolo foro da role_rules → `Hole(source="labeled")`. |
| `_meta_lines` | func | `snapbend/io/dxf.py:292` |  |
| `_mid` | func | `snapbend/rules/read_section.py:109` |  |
| `_mode` | func | `snapbend/rules/read_section.py:323` | Il valore più frequente (entro 1e-3); con `weights`, quello di peso totale maggiore. |
| `_normalize_features` | func | `snapbend/flat/detect.py:60` | Normalizza l'argomento `features` di detect_flat() in un set di stringhe. |
| `officina_file` | func | `snapbend/rules/officina.py:36` | Un file dentro la cartella officina, se c'è una cartella officina e il file esiste. |
| `officina_folder` | func | `snapbend/rules/officina.py:27` | La cartella officina scelta con `set_officina`; None se nessuna. |
| `_order_chain` | func | `snapbend/rules/read_section.py:457` |  |
| `_perimeter` | func | `snapbend/flat/detect.py:679` |  |
| `_perp_distance` | func | `snapbend/rules/read_section.py:303` |  |
| `polar_point` | func | `snapbend/model/geometry.py:30` | Punto a coordinate polari (angolo in gradi). |
| `_probe_point` | func | `snapbend/flat/detect.py:665` |  |
| `_projection_overlap` | func | `snapbend/rules/read_section.py:283` |  |
| `_promote_geometric_holes` | func | `snapbend/flat/detect.py:409` |  |
| `_proxy_pts` | func | `snapbend/flat/detect.py:77` | Vertici di un proxy aperto (OpenCurve), derivati dai suoi segmenti nativi. |
| `radius_from_v_opening` | func | `snapbend/rules/deduction.py:96` | Stima del raggio interno di piega in aria da una cava a V. |
| `_read` | func | `snapbend/drawing/sections.py:75` | `read_section()` sugli spigoli del contorno; `None` se ha spigoli che |
| `read_section` | func | `snapbend/rules/read_section.py:172` |  |
| `_recover_centerline` | func | `snapbend/rules/read_section.py:340` | Returns (segments, angles, pure_arc_radius, pure_arc_angle_deg) - the |
| `_RecoverError` | class | `snapbend/rules/read_section.py:336` |  |
| `RenderContour` | class | `snapbend/flat/model/render.py:21` |  |
| `resolve_calibration` | func | `snapbend/core/bend.py:339` | Nome stringa -> `Calibration` caricata, oggetto già risolto -> se |
| `resolve_facet_bend` | func | `snapbend/core/bend.py:350` | Risolve raggio e K per UNA piega a faccette di `Cone`/`Cylinder` dalla |
| `_result_arcs` | func | `snapbend/flat/detect.py:374` | Ogni arco del risultato: ogni curva è contorno di un cluster o sta in |
| `Section` | class | `snapbend/model/section.py:110` |  |
| `SectionReading` | class | `snapbend/rules/read_section.py:88` |  |
| `_sector_entities` | func | `snapbend/core/cone.py:77` | Settore anulare simmetrico rispetto a X, ampiezza angolare `angle` (gradi). |
| `set_officina` | func | `snapbend/rules/officina.py:21` | Sceglie la cartella officina per questo programma; None la toglie. |
| `SheetThicknessTable` | class | `snapbend/rules/read_section.py:64` |  |
| `_split_into_sides` | func | `snapbend/rules/read_section.py:423` |  |
| `swap_xy` | func | `snapbend/model/geometry.py:47` | Riflette la geometria lungo la diagonale y=x (scambia gli assi X/Y) — il |
| `_sweep_deg` | func | `snapbend/rules/read_section.py:118` | Signed sweep from a0 to a1 in (-360, 360), positive when ccw. |
| `_thickness` | func | `snapbend/rules/read_section.py:224` |  |
| `tipo_cliente_coerente` | func | `snapbend/rules/deduction.py:428` | Controlla che una calibrazione mantenga la promessa del suo |
| `to_dxf` | func | `snapbend/io/dxf.py:54` | Scrive `flat` su file DXF via topo_dxf.to_dxf() — layer/colori coerenti |
| `to_topo_result` | func | `snapbend/io/dxf.py:26` | Traduce `flat` in un Result passando da topo.load_geometry() + |
| `trim_bending_lines` | func | `snapbend/flat/trim.py:34` | Tratteggia ogni `BendingLine` di `result` con `pattern`: le stesse misure |
| `_turn_deg` | func | `snapbend/model/section.py:67` | Signed rotation relative to going straight (>0 = to the left). |
| `_unit` | func | `snapbend/model/section.py:72` |  |
| `_write_custom` | func | `snapbend/flat/detect.py:644` |  |
| `_write_flange_quotes` | func | `snapbend/io/dxf.py:255` |  |
| `_write_meta_block` | func | `snapbend/io/dxf.py:341` |  |
| `write_part_dxf` | func | `snapbend/io/dxf.py:129` | Esporta un pezzo su un unico file a LIVELLI impilati in VERTICALE |
| `_write_reference_lines` | func | `snapbend/io/dxf.py:349` | Disegna il contorno PIENO (prima del margine) — non solo due lati |
| `write_section_dxf` | func | `snapbend/io/dxf.py:90` | Esporta la vista in sezione (Fase 3.3/3.4, MAP.md D31): il contorno |
| `_write_section_view_entities` | func | `snapbend/io/dxf.py:221` | Disegna la vista in sezione come linee/archi diretti, traslati di |
| `_write_text_lines` | func | `snapbend/io/dxf.py:325` |  |

## Duplicate names

No module-level name is defined in more than one module.

## Dependency rule

- `core` never imports `topo`, `topo_dxf`, `io`, `human_layer`, `flat`
- `model` never imports `topo`, `topo_dxf`, `human_layer`, `flat`
- `rules` never imports `topo`, `topo_dxf`, `io`, `human_layer`, `flat`
- every module never imports `topo.core`

`TYPE_CHECKING`-only imports count as violations here and must be verified by hand.

**Clean** — no violation found.

## By module

### `snapbend/` (root)

#### `snapbend/__init__.py` — 63 lines

_snapbend_

No module-level function or class.

### `snapbend/core/`

#### `snapbend/core/__init__.py` — 7 lines

_snapbend/core_

No module-level function or class.

#### `snapbend/core/bend.py` — 404 lines

_snapbend/core/bend.py_

- `estimate_k_factor(material: str, radius: float, thickness: float) -> float` — L83 — Stima un K-factor di partenza da materiale + rapporto R/T, secondo la
- **class** `Bend` — L103 — Una singola piega fra due flange consecutive.
  - methods: `from_included`, `bend_allowance`, `centerline_setback`, `outside_setback`, `inside_setback`
- **class** `BendResult` — L168 — Esito del calcolo di UNA piega dentro `BentProfile.develop()` (o di
  - methods: `to_dict`
- **class** `BentProfile` — L200 — Profilo piegato: N flange (quote a MEZZERIA) unite da N-1 pieghe.
  - methods: `_resolve_calibration`, `develop`
- `resolve_calibration(calibration)` — L339 — Nome stringa -> `Calibration` caricata, oggetto già risolto -> se
- `resolve_facet_bend(calibration, thickness: float, angle_deg: float, explicit_radius: Optional[float], explicit_k: Optional[float], material: str)` — L350 — Risolve raggio e K per UNA piega a faccette di `Cone`/`Cylinder` dalla

#### `snapbend/core/cone.py` — 355 lines

_snapbend/core/cone.py_

- `_sector_entities(r_inner: float, r_outer: float, angle: float, role: str=None) -> list` — L77 — Settore anulare simmetrico rispetto a X, ampiezza angolare `angle` (gradi).
- `_faceted_sector_outline(r_inner: float, r_outer: float, vertex_angles: list, role: str) -> list` — L102 — Perimetro del settore sfaccettato fra i vertici dati: N corde esterne, un
- **class** `Cone` — L140
  - methods: `develop`, `_develop_smooth`, `_develop_faceted`

#### `snapbend/core/cylinder.py` — 241 lines

_snapbend/core/cylinder.py_

- **class** `Cylinder` — L79
  - methods: `develop`, `_faceted_width_and_bends`

### `snapbend/drawing/`

#### `snapbend/drawing/__init__.py` — 13 lines

_snapbend/drawing/__init__.py_

No module-level function or class.

#### `snapbend/drawing/sections.py` — 98 lines

_snapbend/drawing/sections.py_

- **class** `DrawnSection` — L31 — Una sezione di lamiera trovata nella tavola.
- `find_sections(result: topo.Result, table: Optional[SheetThicknessTable]=None) -> List[DrawnSection]` — L44 — Tutti i contorni chiusi di `result` che `read_section()` dice lamiera
- `_contours(result: topo.Result) -> List[tuple]` — L59 — (contorno, cluster_ref) per ogni outer, inner e curva chiusa in loose.
- `_read(contour: ClosedContour, table: SheetThicknessTable) -> Optional[SectionReading]` — L75 — `read_section()` sugli spigoli del contorno; `None` se ha spigoli che
- `_entity(seg) -> Optional[dict]` — L87 — Segmento nativo di topo -> entità dello schema di `read_section()`

### `snapbend/flat/`

#### `snapbend/flat/__init__.py` — 35 lines

_snapbend/flat/__init__.py_

No module-level function or class.

#### `snapbend/flat/detect.py` — 743 lines

_snapbend/flat/detect.py_

- `_ensure_detected(cluster: topo.Cluster) -> topo.model.DetectedFeatures` — L33 — `cluster.detected`, creandolo alla prima scrittura.
- `_normalize_features(features) -> frozenset` — L60 — Normalizza l'argomento `features` di detect_flat() in un set di stringhe.
- `_proxy_pts(proxy) -> list` — L77 — Vertici di un proxy aperto (OpenCurve), derivati dai suoi segmenti nativi.
- `detect_flat(result: topo.Result, features=None, *, max_drill_diameter: float=HOLE_DIAMETER_THRESHOLD, bending_tolerance: float=1.0, engrave_tolerance: float=1.0) -> topo.Result` — L91 — Classifica le feature dentro le parti già trovate da heal().
- `describe_features(cluster: topo.Cluster) -> dict` — L130 — Conteggio ricco per i tipi **noti di topo** — fori per tipo, pieghe
- `_detect_labeled(result: topo.Result) -> None` — L179
- `_bending_line(cluster, start, end, length, source='geometric')` — L293
- `_detect_bending(result: topo.Result, bending_tolerance: float=1.0) -> None` — L306 — Una piega attraversa il pezzo (`topo.geometry.splits_contour`, prolungata di
- `_detect_holes(result: topo.Result, max_drill_diameter: float=HOLE_DIAMETER_THRESHOLD) -> None` — L358 — Lane geometrica: promuove a `Hole` i contorni interni circolari.
- `_result_arcs(result: topo.Result) -> list[topo.primitives.ArcSeg]` — L374 — Ogni arco del risultato: ogni curva è contorno di un cluster o sta in
- `_circle(contour) -> tuple[Optional[float], Optional[tuple]]` — L387 — (diametro, centro) se il contorno è un cerchio per `topo.geometry.contour_shape`,
- `_circular_inners(cluster: topo.Cluster) -> list` — L397 — (contour, diameter, center) per ogni inner geometricamente circolare.
- `_promote_geometric_holes(cluster: topo.Cluster, arcs: list[topo.primitives.ArcSeg], max_drill_diameter: float) -> None` — L409
- `_hole_from_contour(contour, diameter, center, *, hole_type, confidence, geometric_hint='', outer_diameter=None)` — L469
- `_labeled_hole_from_contour(contour)` — L486 — `Contour` con ruolo foro da role_rules → `Hole(source="labeled")`.
- `_detect_engrave(result: topo.Result, engrave_tolerance: float=1.0) -> None` — L508 — Inferenza geometrica delle incisioni — NON ANCORA IMPLEMENTATA.
- `_engraving_from_open(proxy, cluster_label: str='', source: str='labeled', confidence: float=1.0) -> Engraving` — L531
- `_engraving_from_closed(curve, cluster_label: str='', source: str='labeled', confidence: float=1.0) -> Engraving` — L546
- `_handle_engrave_open(proxy: topo.model.OpenCurve, result: topo.Result) -> bool` — L561 — Una traccia engrave aperta va al cluster che la contiene
- `_handle_engrave_closed_loose(proxy, result: topo.Result) -> bool` — L577 — Come _handle_engrave_open ma per una traccia engrave già chiusa
- `_handle_engrave_closed(inner, cluster: topo.Cluster) -> None` — L590
- `_belongs_to_cluster(ce: ClassifiedEntity, cluster: topo.Cluster) -> bool` — L602 — Un'entità aperta (marking/bending) appartiene al cluster se la sua
- `_assign_to_part(ce: ClassifiedEntity, result: topo.Result) -> bool` — L617 — Scrive `ce` nel cluster che la contiene; False se nessuno la contiene:
- `_write_custom(ce: ClassifiedEntity, cluster: topo.Cluster) -> None` — L644
- `_probe_point(ce: ClassifiedEntity) -> Optional[tuple]` — L665
- `_centroid(curve) -> Optional[tuple]` — L671 — Baricentro esatto della curva chiusa; None se non racchiude area.
- `_perimeter(curve) -> float` — L679
- `_extract_data(proxy: topo.model.OpenCurve, work_type: str) -> dict` — L683
- `_extract_data_from_source(work_type: str, curve) -> dict` — L716 — Dati di un'entità chiusa (`ClosedCurve`) letti sui suoi segmenti.
- `_bending_line_from_data(data: dict, cluster_label: str) -> BendingLine` — L731

#### `snapbend/flat/holes.py` — 32 lines

_snapbend/flat/holes.py_

- `is_threaded_hole(center: Tuple[float, float], radius: float, all_arcs: list[topo.primitives.ArcSeg], tolerance_center: float=1.0, angle_tolerance: float=35.0, max_radius_ratio: float=THREADED_ARC_MAX_RADIUS_RATIO) -> bool` — L17 — True se attorno al cerchio c'è un arco a ~270° (entro ``angle_tolerance``

#### `snapbend/flat/model/__init__.py` — 31 lines

_snapbend/flat/model/__init__.py_

No module-level function or class.

#### `snapbend/flat/model/bending_line.py` — 59 lines

_snapbend/flat/model/bending_line.py_

- **class** `BendingLine(topo.model.OpenCurve)` — L22
  - methods: `contours`, `to_dict`

#### `snapbend/flat/model/classified.py` — 33 lines

_snapbend/flat/model/classified.py_

- **class** `ClassifiedEntity` — L14 — Risultato della classificazione di una entità da detect_flat().

#### `snapbend/flat/model/engraving.py` — 57 lines

_snapbend/flat/model/engraving.py_

- **class** `Engraving(topo.model.OpenCurve)` — L29
  - methods: `contours`, `to_dict`

#### `snapbend/flat/model/hole.py` — 67 lines

_snapbend/flat/model/hole.py_

- **class** `Hole(topo.model.ClosedCurve)` — L28
  - methods: `is_void`, `contours`, `to_dict`

#### `snapbend/flat/model/render.py` — 24 lines

_snapbend/flat/model/render.py_

- **class** `RenderContour` — L21

#### `snapbend/flat/pipeline.py` — 35 lines

_snapbend/flat/pipeline.py_

- `heal_and_detect(doc: topo.Document, tolerance=None, label='', source_file='', features='all', max_drill_diameter: float=HOLE_DIAMETER_THRESHOLD, bending_tolerance: float=1.0, engrave_tolerance: float=1.0) -> topo.Result` — L18 — heal() + detect_flat(). `detect_flat()` viene saltato se heal() non produce

#### `snapbend/flat/roles.py` — 98 lines

_snapbend/flat/roles.py_

- `is_structural(role) -> bool` — L69 — Predicato strutturale COMPLETO: outer/inner (motore) + hole/countersink/

#### `snapbend/flat/thresholds.py` — 29 lines

_snapbend/flat/thresholds.py_

No module-level function or class.

#### `snapbend/flat/trim.py` — 52 lines

_snapbend/flat/trim.py_

- **class** `DashPattern` — L21 — Misure del tratteggio di una piega: `head` sul primo capo, `tail`
- `trim_bending_lines(result: topo.Result, pattern: Union[DashPattern, DashRule]) -> topo.Result` — L34 — Tratteggia ogni `BendingLine` di `result` con `pattern`: le stesse misure

### `snapbend/` (root)

#### `snapbend/human_layer.py` — 97 lines

_snapbend/human_layer.py_

- `develop_from_external_flanges(external_flanges: List[float], bends: List[Bend], thickness: float, width: float, calibration: Optional[object]=None, material: str='acciaio', orientation: str='horizontal', label: str='bent_profile') -> FlatGeometry` — L35 — Come `BentProfile.develop()`, ma `external_flanges` sono quote
- `export_part(section: 'Section', width: float, path: str, calibration: Optional[object]=None, include_section: bool=False, include_header: bool=False, tolerance: float=0.05, margin: float=20.0)` — L66 — Esporta un pezzo su un UNICO file DXF a livelli (Fase 3, MAP.md D32):

### `snapbend/io/`

#### `snapbend/io/__init__.py` — 6 lines

_snapbend/io_

No module-level function or class.

#### `snapbend/io/dxf.py` — 384 lines

_snapbend/io/dxf.py_

- `to_topo_result(flat: 'FlatGeometry', tolerance: float=0.05)` — L26 — Traduce `flat` in un Result passando da topo.load_geometry() +
- `to_dxf(flat: 'FlatGeometry', path: str, tolerance: float=0.05, annotate: bool=True, show_margin_reference: bool=False)` — L54 — Scrive `flat` su file DXF via topo_dxf.to_dxf() — layer/colori coerenti
- `write_section_dxf(section: 'Section', quotes: List['FlangeQuote'], path: str, tolerance: float=0.05, quote_clearance: float=8.0, annotate: bool=True)` — L90 — Esporta la vista in sezione (Fase 3.3/3.4, MAP.md D31): il contorno
- `write_part_dxf(flat: 'FlatGeometry', path: str, section_flat: Optional['FlatGeometry']=None, quotes: Optional[List['FlangeQuote']]=None, thickness: Optional[float]=None, include_header: bool=False, tolerance: float=0.05, quote_clearance: float=8.0, margin: float=20.0)` — L129 — Esporta un pezzo su un unico file a LIVELLI impilati in VERTICALE
- `_entities_bbox(entities: List[Dict[str, Any]])` — L199 — Bbox degli entity grezzi (linee/archi, schema `FlatGeometry.entities`)
- `_write_section_view_entities(doc_out, entities: List[Dict[str, Any]], dx: float, dy: float, layer: str='SectionView') -> None` — L221 — Disegna la vista in sezione come linee/archi diretti, traslati di
- `_write_flange_quotes(doc_out, quotes: List['FlangeQuote'], thickness: float, clearance: float) -> None` — L255
- `_meta_lines(label: str, meta: Dict[str, Any], bends: Optional[List[Any]]=None) -> List[str]` — L292
- `_bend_lines(bends: List[Any]) -> List[str]` — L302 — Una riga per piega nell'header — gli stessi numeri che dice
- `_write_text_lines(doc_out, lines: List[str], x0: float, y0: float, layer: str='Notes') -> None` — L325
- `_write_meta_block(doc_out, result, label: str, meta: Dict[str, Any], bends: Optional[List[Any]]=None) -> None` — L341
- `_write_reference_lines(doc_out, reference_entities: List[Dict[str, Any]]) -> None` — L349 — Disegna il contorno PIENO (prima del margine) — non solo due lati

### `snapbend/model/`

#### `snapbend/model/__init__.py` — 6 lines

_snapbend/model_

No module-level function or class.

#### `snapbend/model/geometry.py` — 144 lines

_snapbend/model/geometry.py_

- `polar_point(radius: float, angle_deg: float, origin: Tuple[float, float]=(0.0, 0.0)) -> Tuple[float, float]` — L30 — Punto a coordinate polari (angolo in gradi).
- `_check_orientation(orientation: str) -> None` — L40
- `swap_xy(entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]` — L47 — Riflette la geometria lungo la diagonale y=x (scambia gli assi X/Y) — il
- **class** `FlatGeometry` — L81 — Sviluppo piano di una forma sviluppabile — output di Cone.develop() /
  - methods: `to_topo_result`, `to_dxf`

#### `snapbend/model/section.py` — 428 lines

_snapbend/model/section.py_

- `_fmt(x: float) -> str` — L63
- `_turn_deg(angle_name: float) -> float` — L67 — Signed rotation relative to going straight (>0 = to the left).
- `_unit(angle_deg: float)` — L72
- **class** `FlangeFace` — L78 — Per una flangia: la faccia ESTERNA (convessa) se è coerente da un
- **class** `FlangeQuote` — L92 — La quota da disegnare per una flangia nella vista in sezione
- **class** `Section` — L110
  - methods: `default`, `from_external_flanges`, `centerline_radius`, `name`, `to_bent_profile`, `_centerline_primitives`, `_offset_chains`, `flange_faces`, `flange_quotes`, `to_dxf`, `section`
- `_edge_start(edge)` — L400
- `_edge_end(edge)` — L408
- `_cap(a, b)` — L416
- `_edge_to_entity(edge)` — L420

### `snapbend/rules/`

#### `snapbend/rules/__init__.py` — 7 lines

_snapbend/rules_

No module-level function or class.

#### `snapbend/rules/deduction.py` — 485 lines

_snapbend/rules/deduction.py_

- `bend_deduction(radius: float, thickness: float, angle_deg: float, k: float, reference: str='mezzeria') -> float` — L49 — Accorciamento di piega, formula della fibra neutra.
- `k_din6935(radius: float, thickness: float) -> float` — L65 — Stima DIN 6935 del fattore K (in [0, 0.5]), dal SOLO rapporto
- `bend_allowance_din6935(radius: float, thickness: float, angle_deg: float) -> float` — L76 — Lunghezza dell'asse neutro dentro la piega, con K stimato DIN 6935.
- `deduction_din6935(radius: float, thickness: float, angle_deg: float, reference: str='mezzeria') -> float` — L81 — Accorciamento di piega con K stimato DIN 6935 (scorciatoia di
- `external_to_centerline_deduction(external_deduction: float, thickness: float, angle_deg: float) -> float` — L89 — Converte un accorciamento riferito alle quote esterne (come nei .bnc
- `radius_from_v_opening(v_opening: float) -> float` — L96 — Stima del raggio interno di piega in aria da una cava a V.
- `default_radius(thickness: float) -> float` — L102 — Raggio interno quando non c'è né un raggio esplicito né una cava nota:
- `external_to_centerline_flange(external_length: float, thickness: float, angle_before: Optional[float]=None, angle_after: Optional[float]=None) -> float` — L122 — Converte la lunghezza ESTERNO-ESTERNO di una flangia (apice virtuale
- `centerline_to_external_flange(centerline_length: float, thickness: float, angle_before: Optional[float]=None, angle_after: Optional[float]=None) -> float` — L143 — Inversa di `external_to_centerline_flange`: da mezzeria a esterno-esterno.
- `external_flanges_to_centerline(external_flanges: list[float], bend_angles: list[float], thickness: float) -> list[float]` — L157 — Converte l'intero elenco di flange (come lo si passerebbe a
- **class** `DeductionInfo` — L197 — Accorciamento di piega + da dove viene il numero.
- **class** `Calibration` — L237 — Una calibrazione = i dati di calcolo di un'officina.
  - methods: `__init__`, `tipo_cliente`, `load`, `_field`, `v_opening_for_thickness`, `k_for_material`, `_measured_row`, `_has_measured_for_thickness`, `bend_allowance_din`, `centerline_deduction`, `deduction_detail`
- `tipo_cliente_coerente(calibration: Calibration) -> list[str]` — L428 — Controlla che una calibrazione mantenga la promessa del suo

#### `snapbend/rules/officina.py` — 42 lines

_snapbend/rules/officina.py_

- `set_officina(path) -> None` — L21 — Sceglie la cartella officina per questo programma; None la toglie.
- `officina_folder() -> Optional[Path]` — L27 — La cartella officina scelta con `set_officina`; None se nessuna.
- `officina_file(*parts: str) -> Optional[Path]` — L36 — Un file dentro la cartella officina, se c'è una cartella officina e il file esiste.

#### `snapbend/rules/read_section.py` — 482 lines

_snapbend/rules/read_section.py_

- **class** `SheetThicknessTable` — L64
  - methods: `load`, `contains`
- **class** `SectionReading` — L88
- `_dist(a: Point, b: Point) -> float` — L105
- `_mid(a: Point, b: Point) -> Point` — L109
- `_arc_point(center: Point, radius: float, angle_deg: float) -> Point` — L113
- `_sweep_deg(a0: float, a1: float, ccw: bool) -> float` — L118 — Signed sweep from a0 to a1 in (-360, 360), positive when ccw.
- **class** `_Edge` — L128
  - methods: `__init__`, `other`, `touches`
- `read_section(entities: List[dict], table: Optional[SheetThicknessTable]=None, join_tol: float=0.0001) -> SectionReading` — L172
- `_thickness(edges: List[_Edge]) -> Tuple[Optional[float], List[str]]` — L224
- `_face_pair_distances(edges: List[_Edge]) -> List[Tuple[float, float]]` — L262 — (distance, overlap) for lines that genuinely face each other
- `_projection_overlap(a: _Edge, b: _Edge) -> float` — L283
- `_direction(line: _Edge) -> float` — L298
- `_perp_distance(a: _Edge, b: _Edge) -> float` — L303
- `_has_concentric_pair(edges: List[_Edge], thickness: float) -> bool` — L311
- `_mode(values: List[float], weights: Optional[List[float]]=None) -> float` — L323 — Il valore più frequente (entro 1e-3); con `weights`, quello di peso totale maggiore.
- **class** `_RecoverError(RuntimeError)` — L336
- `_recover_centerline(edges: List[_Edge], thickness: float, tol: float)` — L340 — Returns (segments, angles, pure_arc_radius, pure_arc_angle_deg) - the
- `_canonical(segments: List[float], angles: List[float])` — L413 — A section reads the same from either end. Pick a deterministic
- `_split_into_sides(edges: List[_Edge], caps: List[_Edge], tol: float)` — L423
- `_endpoint_counts(chain: List[_Edge], tol: float)` — L443
- `_order_chain(chain: List[_Edge], start: Point, tol: float)` — L457
- `_chain_vertex(chain: List[_Edge], k: int, tol: float) -> Point` — L479

## Internal dependencies

Which `snapbend` modules each module imports — "what works with what". Modules with no internal import are omitted.

| module | imports |
|---|---|
| `snapbend/__init__.py` | `snapbend.core.bend` · `snapbend.core.cone` · `snapbend.core.cylinder` · `snapbend.human_layer` · `snapbend.model.geometry` · `snapbend.model.section` · `snapbend.rules.deduction` · `snapbend.rules.officina` · `snapbend.rules.read_section` |
| `snapbend/core/bend.py` | `snapbend.model.geometry` · `snapbend.rules.deduction` |
| `snapbend/core/cone.py` | `snapbend.core.bend` · `snapbend.model.geometry` |
| `snapbend/core/cylinder.py` | `snapbend.core.bend` · `snapbend.model.geometry` |
| `snapbend/drawing/__init__.py` | `snapbend.drawing.sections` |
| `snapbend/drawing/sections.py` | `snapbend.rules.read_section` |
| `snapbend/flat/__init__.py` | `snapbend.flat.detect` · `snapbend.flat.model` · `snapbend.flat.pipeline` · `snapbend.flat.roles` · `snapbend.flat.thresholds` · `snapbend.flat.trim` |
| `snapbend/flat/detect.py` | `snapbend.flat.holes` · `snapbend.flat.model` · `snapbend.flat.roles` · `snapbend.flat.thresholds` |
| `snapbend/flat/holes.py` | `snapbend.flat.thresholds` |
| `snapbend/flat/model/__init__.py` | `snapbend.flat.model.bending_line` · `snapbend.flat.model.classified` · `snapbend.flat.model.engraving` · `snapbend.flat.model.hole` · `snapbend.flat.model.render` |
| `snapbend/flat/model/bending_line.py` | `snapbend.flat.model.render` · `snapbend.flat.roles` |
| `snapbend/flat/model/engraving.py` | `snapbend.flat.model.render` · `snapbend.flat.roles` |
| `snapbend/flat/model/hole.py` | `snapbend.flat.model.render` · `snapbend.flat.roles` |
| `snapbend/flat/pipeline.py` | `snapbend.flat.detect` · `snapbend.flat.roles` · `snapbend.flat.thresholds` |
| `snapbend/flat/trim.py` | `snapbend.flat.model` |
| `snapbend/human_layer.py` | `snapbend.core.bend` · `snapbend.io.dxf` · `snapbend.model.geometry` · `snapbend.model.section` · `snapbend.rules.deduction` |
| `snapbend/io/dxf.py` | `snapbend.flat` · `snapbend.flat.roles` · `snapbend.model.geometry` · `snapbend.model.section` |
| `snapbend/model/geometry.py` | `snapbend.io.dxf` |
| `snapbend/model/section.py` | `snapbend.core.bend` · `snapbend.io.dxf` · `snapbend.model.geometry` · `snapbend.rules.deduction` |
| `snapbend/rules/deduction.py` | `snapbend.rules.officina` |
| `snapbend/rules/read_section.py` | `snapbend.rules.officina` |

