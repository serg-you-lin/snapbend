# snapbend — code index

**Generated file — do not edit by hand.** Regenerate with:

```
python tests/gen_index.py
```

What this is: the lookup table of *what already exists* in the package, down to internal helpers. `docs/API.md` documents the public surface (`snapbend.<name>`) with full cards; this file lists every module-level function and class so nothing gets rewritten because it was not found. Signatures and docstring lines come straight from the source, so they cannot drift.

`27` modules · `91` module-level functions · `20` classes · `4419` lines of code.

Sections: [Lookup](#lookup) · [Duplicate names](#duplicate-names) · [Dependency rule](#dependency-rule) · [By module](#by-module) · [Internal dependencies](#internal-dependencies)

---

## Lookup

Every module-level name in the package, alphabetically. **Search here before writing a new helper.**

| name | kind | location | what |
|---|---|---|---|
| `_arc_point` | func | `snapbend/rules/read_section.py:113` |  |
| `_assign_to_part` | func | `snapbend/flat/detect.py:645` |  |
| `_belongs_to_cluster` | func | `snapbend/flat/detect.py:630` | Un'entità aperta (marking/bending) appartiene al cluster se la sua |
| `Bend` | class | `snapbend/core/bend.py:103` | Una singola piega fra due flange consecutive. |
| `bend_allowance_din6935` | func | `snapbend/rules/deduction.py:76` | Lunghezza dell'asse neutro dentro la piega, con K stimato DIN 6935. |
| `bend_deduction` | func | `snapbend/rules/deduction.py:49` | Accorciamento di piega, formula della fibra neutra. |
| `_bend_lines` | func | `snapbend/io/dxf.py:299` | Una riga per piega nell'header — gli stessi numeri che dice |
| `_bending_line` | func | `snapbend/flat/detect.py:306` |  |
| `_bending_line_from_data` | func | `snapbend/flat/detect.py:746` |  |
| `BendingLine` | class | `snapbend/flat/model/bending_line.py:22` |  |
| `BendResult` | class | `snapbend/core/bend.py:168` | Esito del calcolo di UNA piega dentro `BentProfile.develop()` (o di |
| `BentProfile` | class | `snapbend/core/bend.py:200` | Profilo piegato: N flange (quote a MEZZERIA) unite da N-1 pieghe. |
| `Calibration` | class | `snapbend/rules/deduction.py:239` | Una calibrazione = i dati di calcolo di un'officina. |
| `_canonical` | func | `snapbend/rules/read_section.py:402` | A section reads the same from either end. Pick a deterministic |
| `_cap` | func | `snapbend/model/section.py:416` |  |
| `centerline_to_external_flange` | func | `snapbend/rules/deduction.py:145` | Inversa di `external_to_centerline_flange`: da mezzeria a esterno-esterno. |
| `_chain_vertex` | func | `snapbend/rules/read_section.py:474` |  |
| `_check_orientation` | func | `snapbend/model/geometry.py:40` |  |
| `_circular_inners` | func | `snapbend/flat/detect.py:400` | (contour, diameter, center) per ogni inner geometricamente circolare. |
| `ClassifiedEntity` | class | `snapbend/flat/model/classified.py:13` | Risultato della classificazione di una entità da detect_flat(). |
| `Cone` | class | `snapbend/core/cone.py:140` |  |
| `Cylinder` | class | `snapbend/core/cylinder.py:79` |  |
| `deduction_din6935` | func | `snapbend/rules/deduction.py:81` | Accorciamento di piega con K stimato DIN 6935 (scorciatoia di |
| `DeductionInfo` | class | `snapbend/rules/deduction.py:199` | Accorciamento di piega + da dove viene il numero. |
| `describe_features` | func | `snapbend/flat/detect.py:140` | Conteggio ricco per i tipi **noti di forge** — fori per tipo, pieghe |
| `_detect_bending` | func | `snapbend/flat/detect.py:318` | Una piega attraversa il pezzo (`forge.geometry.splits_polygon`, prolungata di |
| `_detect_engrave` | func | `snapbend/flat/detect.py:512` | Inferenza geometrica delle incisioni — NON ANCORA IMPLEMENTATA. |
| `detect_flat` | func | `snapbend/flat/detect.py:101` | Classifica le feature dentro le parti già trovate da heal(). |
| `_detect_holes` | func | `snapbend/flat/detect.py:385` | Lane geometrica: promuove a `Hole` i contorni interni circolari. |
| `_detect_labeled` | func | `snapbend/flat/detect.py:189` |  |
| `develop_from_external_flanges` | func | `snapbend/human_layer.py:35` | Come `BentProfile.develop()`, ma `external_flanges` sono quote |
| `_direction` | func | `snapbend/rules/read_section.py:292` |  |
| `_dist` | func | `snapbend/rules/read_section.py:105` |  |
| `_Edge` | class | `snapbend/rules/read_section.py:128` |  |
| `_edge_end` | func | `snapbend/model/section.py:408` |  |
| `_edge_start` | func | `snapbend/model/section.py:400` |  |
| `_edge_to_entity` | func | `snapbend/model/section.py:420` |  |
| `_endpoint_counts` | func | `snapbend/rules/read_section.py:431` |  |
| `Engraving` | class | `snapbend/flat/model/engraving.py:32` |  |
| `_engraving_from_closed` | func | `snapbend/flat/detect.py:551` |  |
| `_engraving_from_open` | func | `snapbend/flat/detect.py:535` |  |
| `_ensure_detected` | func | `snapbend/flat/detect.py:43` | `cluster.detected`, creandolo alla prima scrittura. |
| `_entities_bbox` | func | `snapbend/io/dxf.py:196` | Bbox degli entity grezzi (linee/archi, schema `FlatGeometry.entities`) |
| `estimate_k_factor` | func | `snapbend/core/bend.py:83` | Stima un K-factor di partenza da materiale + rapporto R/T, secondo la |
| `export_part` | func | `snapbend/human_layer.py:66` | Esporta un pezzo su un UNICO file DXF a livelli (Fase 3, MAP.md D32): |
| `external_flanges_to_centerline` | func | `snapbend/rules/deduction.py:159` | Converte l'intero elenco di flange (come lo si passerebbe a |
| `external_to_centerline_deduction` | func | `snapbend/rules/deduction.py:89` | Converte un accorciamento riferito alle quote esterne (come nei .bnc |
| `external_to_centerline_flange` | func | `snapbend/rules/deduction.py:124` | Converte la lunghezza ESTERNO-ESTERNO di una flangia (apice virtuale |
| `_extract_data` | func | `snapbend/flat/detect.py:695` |  |
| `_extract_data_from_source` | func | `snapbend/flat/detect.py:728` |  |
| `_face_pair_distances` | func | `snapbend/rules/read_section.py:257` | Perpendicular distance between lines that genuinely face each other |
| `_faceted_sector_outline` | func | `snapbend/core/cone.py:102` | Perimetro del settore sfaccettato fra i vertici dati: N corde esterne, un |
| `FlangeFace` | class | `snapbend/model/section.py:78` | Per una flangia: la faccia ESTERNA (convessa) se è coerente da un |
| `FlangeQuote` | class | `snapbend/model/section.py:92` | La quota da disegnare per una flangia nella vista in sezione |
| `FlatGeometry` | class | `snapbend/model/geometry.py:81` | Sviluppo piano di una forma sviluppabile — output di Cone.develop() / |
| `_fmt` | func | `snapbend/model/section.py:63` |  |
| `_free_end` | func | `snapbend/rules/read_section.py:445` |  |
| `_handle_engrave_closed` | func | `snapbend/flat/detect.py:614` |  |
| `_handle_engrave_closed_trash` | func | `snapbend/flat/detect.py:595` | Come _handle_engrave_open ma per una traccia engrave già chiusa |
| `_handle_engrave_open` | func | `snapbend/flat/detect.py:567` | Smista una traccia engrave aperta per contenimento. |
| `_has_concentric_pair` | func | `snapbend/rules/read_section.py:305` |  |
| `heal_and_detect` | func | `snapbend/flat/pipeline.py:19` | heal() + detect_flat(). `detect_flat()` viene saltato se heal() non produce |
| `Hole` | class | `snapbend/flat/model/hole.py:31` |  |
| `_hole_from_contour` | func | `snapbend/flat/detect.py:471` |  |
| `is_structural` | func | `snapbend/flat/roles.py:68` | Predicato strutturale COMPLETO: outer/inner (motore) + hole/countersink/ |
| `is_threaded_hole` | func | `snapbend/flat/holes.py:18` | True se attorno al cerchio c'è un arco a ~270° (entro ``angle_tolerance`` |
| `k_din6935` | func | `snapbend/rules/deduction.py:65` | Stima DIN 6935 del fattore K (in [0, 0.5]), dal SOLO rapporto |
| `_labeled_hole_from_contour` | func | `snapbend/flat/detect.py:489` | `ForgeContour` con ruolo foro da role_rules → `Hole(source="labeled")`. |
| `_meta_lines` | func | `snapbend/io/dxf.py:289` |  |
| `_mid` | func | `snapbend/rules/read_section.py:109` |  |
| `_mode` | func | `snapbend/rules/read_section.py:317` |  |
| `_normalize_features` | func | `snapbend/flat/detect.py:70` | Normalizza l'argomento `features` di detect_flat() in un set di stringhe. |
| `officina_file` | func | `snapbend/rules/officina.py:42` | Un file dentro la cartella officina, se c'è una cartella officina e il file esiste. |
| `officina_folder` | func | `snapbend/rules/officina.py:31` | La cartella officina scelta con `set_officina`, o quella di `SNAPBEND_OFFICINA`; None se nessuna. |
| `_order_chain` | func | `snapbend/rules/read_section.py:452` |  |
| `_perp_distance` | func | `snapbend/rules/read_section.py:297` |  |
| `polar_point` | func | `snapbend/model/geometry.py:30` | Punto a coordinate polari (angolo in gradi). |
| `_probe_point` | func | `snapbend/flat/detect.py:687` |  |
| `_projection_overlap` | func | `snapbend/rules/read_section.py:277` |  |
| `_promote_geometric_holes` | func | `snapbend/flat/detect.py:412` |  |
| `_proxy_pts` | func | `snapbend/flat/detect.py:87` | Vertici di un proxy aperto (OpenFeature), derivati dai suoi segmenti nativi. |
| `radius_from_v_opening` | func | `snapbend/rules/deduction.py:96` | Stima del raggio interno di piega in aria da una cava a V. |
| `read_section` | func | `snapbend/rules/read_section.py:172` |  |
| `_recover_centerline` | func | `snapbend/rules/read_section.py:333` | Returns (segments, angles, pure_arc_radius, pure_arc_angle_deg) - the |
| `_RecoverError` | class | `snapbend/rules/read_section.py:329` |  |
| `_register_default_styles` | func | `snapbend/flat/roles.py:78` | Registra colore + nome layer di default per i ruoli manifatturieri — |
| `RenderContour` | class | `snapbend/flat/model/render.py:20` |  |
| `resolve_calibration` | func | `snapbend/core/bend.py:339` | Nome stringa -> `Calibration` caricata, oggetto già risolto -> se |
| `resolve_facet_bend` | func | `snapbend/core/bend.py:350` | Risolve raggio e K per UNA piega a faccette di `Cone`/`Cylinder` dalla |
| `Section` | class | `snapbend/model/section.py:110` |  |
| `SectionReading` | class | `snapbend/rules/read_section.py:88` |  |
| `_sector_entities` | func | `snapbend/core/cone.py:77` | Settore anulare simmetrico rispetto a X, ampiezza angolare `angle` (gradi). |
| `set_officina` | func | `snapbend/rules/officina.py:25` | Sceglie la cartella officina per questo programma (vince sulla variabile); None torna alla variabile. |
| `SheetThicknessTable` | class | `snapbend/rules/read_section.py:64` |  |
| `_split_into_sides` | func | `snapbend/rules/read_section.py:412` |  |
| `swap_xy` | func | `snapbend/model/geometry.py:47` | Riflette la geometria lungo la diagonale y=x (scambia gli assi X/Y) — il |
| `_sweep_deg` | func | `snapbend/rules/read_section.py:118` | Signed sweep from a0 to a1 in (-360, 360), positive when ccw. |
| `_thickness` | func | `snapbend/rules/read_section.py:224` |  |
| `tipo_cliente_coerente` | func | `snapbend/rules/deduction.py:430` | Controlla che una calibrazione mantenga la promessa del suo |
| `to_dxf` | func | `snapbend/io/dxf.py:53` | Scrive `flat` su file DXF via forge.to_dxf() — layer/colori coerenti |
| `to_forge_result` | func | `snapbend/io/dxf.py:25` | Traduce `flat` in un ForgeResult passando da forge.load_geometry() + |
| `_turn_deg` | func | `snapbend/model/section.py:67` | Signed rotation relative to going straight (>0 = to the left). |
| `_unit` | func | `snapbend/model/section.py:72` |  |
| `_write_custom` | func | `snapbend/flat/detect.py:666` |  |
| `_write_flange_quotes` | func | `snapbend/io/dxf.py:252` |  |
| `_write_meta_block` | func | `snapbend/io/dxf.py:338` |  |
| `write_part_dxf` | func | `snapbend/io/dxf.py:126` | Esporta un pezzo su un unico file a LIVELLI impilati in VERTICALE |
| `_write_reference_lines` | func | `snapbend/io/dxf.py:346` | Disegna il contorno PIENO (prima del margine) — non solo due lati |
| `write_section_dxf` | func | `snapbend/io/dxf.py:88` | Esporta la vista in sezione (Fase 3.3/3.4, MAP.md D31): il contorno |
| `_write_section_view_entities` | func | `snapbend/io/dxf.py:218` | Disegna la vista in sezione come linee/archi diretti, traslati di |
| `_write_text_lines` | func | `snapbend/io/dxf.py:322` |  |

## Duplicate names

No module-level name is defined in more than one module.

## Dependency rule

- `core` never imports `forge`, `io`, `human_layer`, `flat`
- `model` never imports `forge`, `human_layer`, `flat`
- `rules` never imports `forge`, `io`, `human_layer`, `flat`

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

### `snapbend/flat/`

#### `snapbend/flat/__init__.py` — 33 lines

_snapbend/flat/__init__.py_

No module-level function or class.

#### `snapbend/flat/detect.py` — 757 lines

_snapbend/flat/detect.py_

- `_ensure_detected(cluster: ForgeCluster) -> DetectedFeatures` — L43 — `cluster.detected`, creandolo alla prima scrittura.
- `_normalize_features(features) -> frozenset` — L70 — Normalizza l'argomento `features` di detect_flat() in un set di stringhe.
- `_proxy_pts(proxy) -> list` — L87 — Vertici di un proxy aperto (OpenFeature), derivati dai suoi segmenti nativi.
- `detect_flat(result: ForgeResult, features=None, *, max_drill_diameter: float=HOLE_DIAMETER_THRESHOLD, bending_tolerance: float=1.0, engrave_tolerance: float=1.0) -> ForgeResult` — L101 — Classifica le feature dentro le parti già trovate da heal().
- `describe_features(cluster: ForgeCluster) -> dict` — L140 — Conteggio ricco per i tipi **noti di forge** — fori per tipo, pieghe
- `_detect_labeled(result: ForgeResult) -> None` — L189
- `_bending_line(cluster, start, end, length, source='geometric')` — L306
- `_detect_bending(result: ForgeResult, bending_tolerance: float=1.0) -> None` — L318 — Una piega attraversa il pezzo (`forge.geometry.splits_polygon`, prolungata di
- `_detect_holes(result: ForgeResult, max_drill_diameter: float=HOLE_DIAMETER_THRESHOLD) -> None` — L385 — Lane geometrica: promuove a `Hole` i contorni interni circolari.
- `_circular_inners(cluster: ForgeCluster) -> list` — L400 — (contour, diameter, center) per ogni inner geometricamente circolare.
- `_promote_geometric_holes(cluster: ForgeCluster, result: ForgeResult, max_drill_diameter: float) -> None` — L412
- `_hole_from_contour(contour, diameter, center, *, hole_type, confidence, geometric_hint='', outer_diameter=None)` — L471
- `_labeled_hole_from_contour(contour)` — L489 — `ForgeContour` con ruolo foro da role_rules → `Hole(source="labeled")`.
- `_detect_engrave(result: ForgeResult, engrave_tolerance: float=1.0) -> None` — L512 — Inferenza geometrica delle incisioni — NON ANCORA IMPLEMENTATA.
- `_engraving_from_open(proxy, cluster_label: str='', source: str='labeled', confidence: float=1.0) -> Engraving` — L535
- `_engraving_from_closed(polygon, segments, cluster_label: str='', source: str='labeled', confidence: float=1.0, styles=None) -> Engraving` — L551
- `_handle_engrave_open(proxy: OpenFeature, result: ForgeResult) -> bool` — L567 — Smista una traccia engrave aperta per contenimento.
- `_handle_engrave_closed_trash(proxy, result: ForgeResult) -> bool` — L595 — Come _handle_engrave_open ma per una traccia engrave già chiusa
- `_handle_engrave_closed(inner, cluster: ForgeCluster) -> None` — L614
- `_belongs_to_cluster(ce: ClassifiedEntity, cluster: ForgeCluster) -> bool` — L630 — Un'entità aperta (marking/bending) appartiene al cluster se la sua
- `_assign_to_part(ce: ClassifiedEntity, result: ForgeResult) -> None` — L645
- `_write_custom(ce: ClassifiedEntity, cluster: ForgeCluster) -> None` — L666
- `_probe_point(ce: ClassifiedEntity) -> Optional[Point]` — L687
- `_extract_data(proxy: OpenFeature, work_type: str) -> dict` — L695
- `_extract_data_from_source(work_type: str, polygon=None) -> dict` — L728
- `_bending_line_from_data(data: dict, cluster_label: str) -> BendingLine` — L746

#### `snapbend/flat/holes.py` — 33 lines

_snapbend/flat/holes.py_

- `is_threaded_hole(center: Tuple[float, float], radius: float, all_arcs: list[ArcSeg], tolerance_center: float=1.0, angle_tolerance: float=35.0, max_radius_ratio: float=THREADED_ARC_MAX_RADIUS_RATIO) -> bool` — L18 — True se attorno al cerchio c'è un arco a ~270° (entro ``angle_tolerance``

#### `snapbend/flat/model/__init__.py` — 31 lines

_snapbend/flat/model/__init__.py_

No module-level function or class.

#### `snapbend/flat/model/bending_line.py` — 55 lines

_snapbend/flat/model/bending_line.py_

- **class** `BendingLine(OpenFeature)` — L22
  - methods: `contours`, `to_dict`

#### `snapbend/flat/model/classified.py` — 31 lines

_snapbend/flat/model/classified.py_

- **class** `ClassifiedEntity` — L13 — Risultato della classificazione di una entità da detect_flat().

#### `snapbend/flat/model/engraving.py` — 66 lines

_snapbend/flat/model/engraving.py_

- **class** `Engraving(OpenFeature)` — L32
  - methods: `closed`, `contours`, `to_dict`

#### `snapbend/flat/model/hole.py` — 71 lines

_snapbend/flat/model/hole.py_

- **class** `Hole(ClosedFeature)` — L31
  - methods: `is_void`, `contours`, `to_dict`

#### `snapbend/flat/model/render.py` — 24 lines

_snapbend/flat/model/render.py_

- **class** `RenderContour` — L20

#### `snapbend/flat/pipeline.py` — 36 lines

_snapbend/flat/pipeline.py_

- `heal_and_detect(doc: ForgeDocument, tolerance=None, label='', source_file='', features='all', max_drill_diameter: float=HOLE_DIAMETER_THRESHOLD, bending_tolerance: float=1.0, engrave_tolerance: float=1.0) -> ForgeResult` — L19 — heal() + detect_flat(). `detect_flat()` viene saltato se heal() non produce

#### `snapbend/flat/roles.py` — 102 lines

_snapbend/flat/roles.py_

- `is_structural(role) -> bool` — L68 — Predicato strutturale COMPLETO: outer/inner (motore) + hole/countersink/
- `_register_default_styles() -> None` — L78 — Registra colore + nome layer di default per i ruoli manifatturieri —

#### `snapbend/flat/thresholds.py` — 29 lines

_snapbend/flat/thresholds.py_

No module-level function or class.

### `snapbend/` (root)

#### `snapbend/human_layer.py` — 97 lines

_snapbend/human_layer.py_

- `develop_from_external_flanges(external_flanges: List[float], bends: List[Bend], thickness: float, width: float, calibration: Optional[object]=None, material: str='acciaio', orientation: str='horizontal', label: str='bent_profile') -> FlatGeometry` — L35 — Come `BentProfile.develop()`, ma `external_flanges` sono quote
- `export_part(section: 'Section', width: float, path: str, calibration: Optional[object]=None, include_section: bool=False, include_header: bool=False, tolerance: float=0.05, margin: float=20.0)` — L66 — Esporta un pezzo su un UNICO file DXF a livelli (Fase 3, MAP.md D32):

### `snapbend/io/`

#### `snapbend/io/__init__.py` — 6 lines

_snapbend/io_

No module-level function or class.

#### `snapbend/io/dxf.py` — 381 lines

_snapbend/io/dxf.py_

- `to_forge_result(flat: 'FlatGeometry', tolerance: float=0.05)` — L25 — Traduce `flat` in un ForgeResult passando da forge.load_geometry() +
- `to_dxf(flat: 'FlatGeometry', path: str, tolerance: float=0.05, annotate: bool=True, show_margin_reference: bool=False)` — L53 — Scrive `flat` su file DXF via forge.to_dxf() — layer/colori coerenti
- `write_section_dxf(section: 'Section', quotes: List['FlangeQuote'], path: str, tolerance: float=0.05, quote_clearance: float=8.0, annotate: bool=True)` — L88 — Esporta la vista in sezione (Fase 3.3/3.4, MAP.md D31): il contorno
- `write_part_dxf(flat: 'FlatGeometry', path: str, section_flat: Optional['FlatGeometry']=None, quotes: Optional[List['FlangeQuote']]=None, thickness: Optional[float]=None, include_header: bool=False, tolerance: float=0.05, quote_clearance: float=8.0, margin: float=20.0)` — L126 — Esporta un pezzo su un unico file a LIVELLI impilati in VERTICALE
- `_entities_bbox(entities: List[Dict[str, Any]])` — L196 — Bbox degli entity grezzi (linee/archi, schema `FlatGeometry.entities`)
- `_write_section_view_entities(doc_out, entities: List[Dict[str, Any]], dx: float, dy: float, layer: str='SectionView') -> None` — L218 — Disegna la vista in sezione come linee/archi diretti, traslati di
- `_write_flange_quotes(doc_out, quotes: List['FlangeQuote'], thickness: float, clearance: float) -> None` — L252
- `_meta_lines(label: str, meta: Dict[str, Any], bends: Optional[List[Any]]=None) -> List[str]` — L289
- `_bend_lines(bends: List[Any]) -> List[str]` — L299 — Una riga per piega nell'header — gli stessi numeri che dice
- `_write_text_lines(doc_out, lines: List[str], x0: float, y0: float, layer: str='Notes') -> None` — L322
- `_write_meta_block(doc_out, result, label: str, meta: Dict[str, Any], bends: Optional[List[Any]]=None) -> None` — L338
- `_write_reference_lines(doc_out, reference_entities: List[Dict[str, Any]]) -> None` — L346 — Disegna il contorno PIENO (prima del margine) — non solo due lati

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
  - methods: `to_forge_result`, `to_dxf`

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

#### `snapbend/rules/deduction.py` — 487 lines

_snapbend/rules/deduction.py_

- `bend_deduction(radius: float, thickness: float, angle_deg: float, k: float, reference: str='mezzeria') -> float` — L49 — Accorciamento di piega, formula della fibra neutra.
- `k_din6935(radius: float, thickness: float) -> float` — L65 — Stima DIN 6935 del fattore K (in [0, 0.5]), dal SOLO rapporto
- `bend_allowance_din6935(radius: float, thickness: float, angle_deg: float) -> float` — L76 — Lunghezza dell'asse neutro dentro la piega, con K stimato DIN 6935.
- `deduction_din6935(radius: float, thickness: float, angle_deg: float, reference: str='mezzeria') -> float` — L81 — Accorciamento di piega con K stimato DIN 6935 (scorciatoia di
- `external_to_centerline_deduction(external_deduction: float, thickness: float, angle_deg: float) -> float` — L89 — Converte un accorciamento riferito alle quote esterne (come nei .bnc
- `radius_from_v_opening(v_opening: float) -> float` — L96 — Stima del raggio interno di piega in aria da una cava a V.
- `external_to_centerline_flange(external_length: float, thickness: float, angle_before: Optional[float]=None, angle_after: Optional[float]=None) -> float` — L124 — Converte la lunghezza ESTERNO-ESTERNO di una flangia (apice virtuale
- `centerline_to_external_flange(centerline_length: float, thickness: float, angle_before: Optional[float]=None, angle_after: Optional[float]=None) -> float` — L145 — Inversa di `external_to_centerline_flange`: da mezzeria a esterno-esterno.
- `external_flanges_to_centerline(external_flanges: list[float], bend_angles: list[float], thickness: float) -> list[float]` — L159 — Converte l'intero elenco di flange (come lo si passerebbe a
- **class** `DeductionInfo` — L199 — Accorciamento di piega + da dove viene il numero.
- **class** `Calibration` — L239 — Una calibrazione = i dati di calcolo di un'officina.
  - methods: `__init__`, `tipo_cliente`, `load`, `_field`, `v_opening_for_thickness`, `k_for_material`, `_measured_row`, `_has_measured_for_thickness`, `bend_allowance_din`, `centerline_deduction`, `deduction_detail`
- `tipo_cliente_coerente(calibration: Calibration) -> list[str]` — L430 — Controlla che una calibrazione mantenga la promessa del suo

#### `snapbend/rules/officina.py` — 48 lines

_snapbend/rules/officina.py_

- `set_officina(path) -> None` — L25 — Sceglie la cartella officina per questo programma (vince sulla variabile); None torna alla variabile.
- `officina_folder() -> Optional[Path]` — L31 — La cartella officina scelta con `set_officina`, o quella di `SNAPBEND_OFFICINA`; None se nessuna.
- `officina_file(*parts: str) -> Optional[Path]` — L42 — Un file dentro la cartella officina, se c'è una cartella officina e il file esiste.

#### `snapbend/rules/read_section.py` — 477 lines

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
- `_face_pair_distances(edges: List[_Edge]) -> List[float]` — L257 — Perpendicular distance between lines that genuinely face each other
- `_projection_overlap(a: _Edge, b: _Edge) -> float` — L277
- `_direction(line: _Edge) -> float` — L292
- `_perp_distance(a: _Edge, b: _Edge) -> float` — L297
- `_has_concentric_pair(edges: List[_Edge], thickness: float) -> bool` — L305
- `_mode(values: List[float]) -> float` — L317
- **class** `_RecoverError(RuntimeError)` — L329
- `_recover_centerline(edges: List[_Edge], thickness: float, tol: float)` — L333 — Returns (segments, angles, pure_arc_radius, pure_arc_angle_deg) - the
- `_canonical(segments: List[float], angles: List[float])` — L402 — A section reads the same from either end. Pick a deterministic
- `_split_into_sides(edges: List[_Edge], caps: List[_Edge], tol: float)` — L412
- `_endpoint_counts(chain: List[_Edge], tol: float)` — L431
- `_free_end(chain: List[_Edge], tol: float) -> Point` — L445
- `_order_chain(chain: List[_Edge], start: Point, tol: float)` — L452
- `_chain_vertex(chain: List[_Edge], k: int, tol: float) -> Point` — L474

## Internal dependencies

Which `snapbend` modules each module imports — "what works with what". Modules with no internal import are omitted.

| module | imports |
|---|---|
| `snapbend/__init__.py` | `snapbend.core.bend` · `snapbend.core.cone` · `snapbend.core.cylinder` · `snapbend.human_layer` · `snapbend.model.geometry` · `snapbend.model.section` · `snapbend.rules.deduction` · `snapbend.rules.officina` · `snapbend.rules.read_section` |
| `snapbend/core/bend.py` | `snapbend.model.geometry` · `snapbend.rules.deduction` |
| `snapbend/core/cone.py` | `snapbend.core.bend` · `snapbend.model.geometry` |
| `snapbend/core/cylinder.py` | `snapbend.core.bend` · `snapbend.model.geometry` |
| `snapbend/flat/__init__.py` | `snapbend.flat.detect` · `snapbend.flat.model` · `snapbend.flat.pipeline` · `snapbend.flat.roles` · `snapbend.flat.thresholds` |
| `snapbend/flat/detect.py` | `snapbend.flat.holes` · `snapbend.flat.model` · `snapbend.flat.roles` · `snapbend.flat.thresholds` |
| `snapbend/flat/holes.py` | `snapbend.flat.thresholds` |
| `snapbend/flat/model/__init__.py` | `snapbend.flat.model.bending_line` · `snapbend.flat.model.classified` · `snapbend.flat.model.engraving` · `snapbend.flat.model.hole` · `snapbend.flat.model.render` |
| `snapbend/flat/model/bending_line.py` | `snapbend.flat.model.render` · `snapbend.flat.roles` |
| `snapbend/flat/model/engraving.py` | `snapbend.flat.model.render` · `snapbend.flat.roles` |
| `snapbend/flat/model/hole.py` | `snapbend.flat.model.render` · `snapbend.flat.roles` |
| `snapbend/flat/pipeline.py` | `snapbend.flat.detect` · `snapbend.flat.roles` · `snapbend.flat.thresholds` |
| `snapbend/human_layer.py` | `snapbend.core.bend` · `snapbend.io.dxf` · `snapbend.model.geometry` · `snapbend.model.section` · `snapbend.rules.deduction` |
| `snapbend/io/dxf.py` | `snapbend.flat` · `snapbend.model.geometry` · `snapbend.model.section` |
| `snapbend/model/geometry.py` | `snapbend.io.dxf` |
| `snapbend/model/section.py` | `snapbend.core.bend` · `snapbend.io.dxf` · `snapbend.model.geometry` · `snapbend.rules.deduction` |
| `snapbend/rules/deduction.py` | `snapbend.rules.officina` |
| `snapbend/rules/read_section.py` | `snapbend.rules.officina` |

