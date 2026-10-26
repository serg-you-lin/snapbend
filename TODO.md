# TODO — cosa manca, in ordine

Unico posto per il lavoro aperto. Le decisioni e il perché stanno in
`MAP.md`; qui non si ripetono, si rimanda con "vedi `MAP.md` D...".

## Richieste dai consumer (MAP.md D71)

I consumer (pippo, …) non scrivono qui: mettono le richieste nel loro
`TODO.md`, sezione `## Richieste a snapbend` (cosa, perché, chi la usa, caso
di prova). Raccoglierle: `grep -n -A40 "## Richieste a snapbend" ../*/TODO.md`.
Ognuna si smista, mai in automatico:

- **significato di processo della lamiera** (sviluppo, piega, deduzione,
  sezione, foro da forare, svasatura) → nome pubblico con scheda in
  `docs/API.md`, test e un D##;
- **fatto geometrico** (vero anche senza lamiera) → `## Richieste a topo`;
- **lettura del foglio** (viste, quote, notazione) → è di snapdraw, e
  snapbend non lo importa: il consumer traduce in termini di snapbend;
- **scelta del chiamante** (quale pezzo, per chi, colori/layer del suo file
  di taglio) → resta nel consumer.

Chiedere non basta per entrare. Un "no, resta nel consumer" si scrive qui
sotto col perché, così il consumer lo trova e non la richiede.

pippo, 4 richieste (`../pippo/TODO.md`, sezione
`## Richieste a snapbend`); la 1 smistata, le altre con una prima
lettura da confermare:
1. *Feature sullo sviluppo* — **smistata e fatta (26 ottobre, MAP.md
   D72): entra solo il riporto, il resto no.** Il riporto è
   `flat.flanges[i].position(...)` e `flat.bends[i].position`. Il
   prototipo (`../pippo/lab/flat_L.py`) fa quattro mestieri:
   - **entra in snapbend**: dove cade sullo sviluppo un punto di un'ala,
     dato come distanza da un riferimento del pezzo piegato (bordo libero
     dell'ala, o faccia esterna dell'ala vicina = apice virtuale, quota
     esterno-esterno) — è lì che si prende o no l'accorciamento. Oggi
     snapbend lo sa ma non lo dice: pippo ricava lunghezza e linea di piega
     da `flat.entities[0]["points"]` e `flat.entities[1]["start"]`
     (dizionari sciolti). Serve: ogni piega con la sua posizione sullo
     sviluppo, ogni ala col suo tratto piano, un riporto ala+distanza → u
     che rifiuta un punto oltre la linea di piega. Input in numeri, non in
     tipi di snapdraw (D71).
   - **no, è di snapdraw/pippo**: quale vista mostra quale ala, da che lato
     sta la faccia esterna, quale feature sta su quale ala.
   - **no, è di topo** (già chiesto da pippo): moto rigido/specchio dei
     segmenti, ritaglio dell'ala coperta, contorni che si annullano.
   - **no, resta a pippo**: comporre il contorno dello sviluppo dalle viste
     e scegliere cosa fare di un foro in zona di piega.
2. *Lo sviluppo torna con i fori nell'overlay* — **smistata (26 ottobre,
   MAP.md D73): c'è già, nessuna API nuova.** Fori e piega caricati coi
   ruoli di snapbend (`snapbend.flat.roles`) e passati a
   `heal_and_detect` tornano `Hole` col loro tipo (`source="labeled"`) e
   `BendingLine`, sui layer di snapbend. Tradurre i ruoli di snapdraw in
   quelli di snapbend tocca a pippo; il `promote` chiesto a topo per
   questo non serve. Il testo del richiamo non entra in `Hole` (è
   notazione del foglio).
3. *`read_section` legge il certo e segnala il resto* — **smistata (26
   ottobre, MAP.md D74), da implementare.** Il terzo tappo è il moncherino
   rimasto dritto, disegnato nello stesso contorno della L. Entra: ogni
   coppia di archi concentrici a distanza t è una piega, con angolo e
   raggio interno, anche quando la mezzeria non si ricostruisce. Non si
   danno le lunghezze delle ali in quel caso (servono le altre viste).
   Dire quale tratto è il moncherino è di snapdraw. Test: un contorno
   sintetico L + moncherino costruito con `Section`/topo, mai il disegno
   del cliente.
4. *Due pezzi piegati letti come non piegati* — prima un'indagine, poi si vede di chi è.

Aperti dallo smistamento, da fare quando c'è tempo:
- **Svasatura etichettata su due cerchi** (D73): due cerchi concentrici
  entrambi `COUNTERSINK` tornano due `Hole` senza `outer_diameter`; la
  lane etichettata deve accoppiarli come fa quella geometrica
  (`_promote_geometric_holes`).
- **Foro vicino alla piega** (D72): `FlatFlange.position` rifiuta solo un
  punto oltre la linea di piega; la zona dove il foro si deforma (raggio +
  spessore dalla piega, regola di processo) non la giudica nessuno. Con un
  accorciamento misurato il raggio non è noto: va deciso da dove prenderlo.


## Sezioni di lamiera in una tavola a viste (MAP.md D69)

- [x] `snapbend.drawing.find_sections(topo.island(doc, max_gap=...))`: quali
  contorni chiusi (outer, inners, `loose` chiusi) sono lamiera. Uno alla
  volta: niente tubi (D69).
- [ ] Provarlo su una tavola vera con le sezioni disegnate (con cornice e
  quote): le quote/assi che toccano la sezione la tengono nella stessa isola?
- [ ] Dalla sezione trovata allo sviluppo: `reading.centerline_segments`/
  `angles` → `BentProfile`, `pure_arc_radius` (sella) → `Cylinder` (vedi "`BentProfile`
  da un disegno letto" più sotto).
- [ ] Un pezzo con un ramo dentro la cornice (sezione + quota/asse attaccati)
  esce da `island()` come `OpenCurve` sciolte, non come contorno chiuso: `find_sections`
  non lo vede. Provare su una tavola vera.
- [ ] Sezione a spigolo vivo (raggio non disegnato): spessore letto,
  mezzeria no, con una nota. Da decidere: raggio di default (D62: raggio =
  spessore) e la si legge come piegata, o resta così.
- [ ] Un rettangolo sottile (una cava 20x3 in una vista in pianta) è lamiera
  non piegata per `read_section`: se dà fastidio, chi chiama filtra su
  `reading.is_bent`.

## Le forme di lamiera le costruisce e le riconosce snapbend (topo D136, 19 ottobre)

`topo.geometry.contour_shape` ha sei kind, elenco chiuso e stabile:
`circle`, `ellipse`, `stadium`, `rectangle`, `polygon`, `other`. topo non ne
aggiungerà altri. Ogni forma di lamiera oltre quelle è di snapbend: asola
raggiata o rettangolo raccordato, foro a D (cerchio con un piatto), asola ad
arco, foro quadro con gli spigoli raccordati, sede esagonale per un dado.

- **Costruirle**: con le primitive di topo (`LineSeg`, `ArcSeg`, …) passate a
  `topo.load_segments`, come fanno i builder di `topo.geometry` (D96). Mai
  chiedere a topo un builder per una forma di lamiera.
- **Riconoscerle**: in snapbend, partendo da un contorno che topo dà come
  `other` o `polygon` (i suoi segmenti dopo la ricomposizione). Mai chiedere
  a topo un kind nuovo.
- Quando topo darà la firma dei contorni (D121, in 1.x), il riconoscimento
  passa da lì invece che dalla ricomposizione fatta a mano.


## `snapbend.flat` — arrivato da topo (MAP.md D51-D53, 4 ottobre)

- [x] detection di un pezzo piano spostata da topo, con test e golden di
  processo (`tests/flat/`, `tests/data/flat/`).
- [x] una piega attraversa il pezzo (D52); interrotta da un vuoto resta una (D53).
- [ ] **Misura minima di una piega = regola di processo (Federico, 4
  ottobre).** Un righino di traverso in un angolo passa ancora come piega
  (D52). La soglia non è un numero fisso: dipende da spessore e cava — a 0.5
  mm anche un'aletta 3×3 si piega, a 5 mm no. Va derivata da spessore +
  calibrazione (che snapbend ha già, `rules/deduction.py`), ma un file di
  taglio non porta lo spessore: serve deciderne la sorgente (parametro del
  chiamante, cartiglio letto da snapdraw, ...). Stessa regola per una piega
  molto vicina al lato.
- [x] **Le due pieghe da 30 mm di `staffa_scarto_doppia`** (pezzi 2 e 3):
  confermate da Federico, il risultato atteso è "piega" — i golden ora le
  contano. Nel disegno sono uno smusso: riconoscerlo come tale è di snapdraw
  (lettura per viste, non ancora fatta), non di `detect_flat`.
- [ ] `_detect_engrave` resta un segnaposto (inferenza geometrica delle
  incisioni non fatta, era topo D13).
- [ ] **Lo script di produzione dello split** (ex `scripts/13_…` di topo, ora
  alla radice di snapbend, **non versionato**: ha un percorso con un codice
  pezzo; escluso con `.git/info/exclude`). È su API morte e non parte: importa
  `topo.io.text_utils` (sparito), spacchetta `load_dxf` in `(doc, msp)` (oggi
  ritorna solo il `Document`), chiama `topo.validate_msp` e
  `topo.detect` (spariti: la detection è `snapbend.flat.detect_flat`),
  `inject(texts=...)` (oggi `inject(result, data_injector, snap_distance)`,
  i testi da `result.annotations`), `split(msp, result, output_folder=...)`
  (oggi `split(result, source_doc, ...)`, e su disco `split_to_files`). Da
  riscrivere sulla API attuale e collaudare con l'overlay-check in SigmaNest
  prima di rimetterlo in produzione (Federico, 4 ottobre). Può servire da
  prototipo per vedere se la pipeline si rompe; lo script vero resta fuori da
  GitHub, sempre.

## Fatto stanotte, non ancora in cima al file (MAP.md D45/D46/D47/D49)

- [x] **`Bend.from_included()`** (MAP.md D49) — costruisce un `Bend`
  dall'angolo INCLUSO del disegno invece che dalla rotazione da piatto
  che vuole `angle` di default. `Bend(angle=120)` (l'incluso passato
  diretto, errore comune) e `Bend.from_included(120)` (giusto, dà
  `angle=60`) sviluppano lunghezze diverse — dimostrato in `04_bend.py`
  coi numeri a confronto. 6 test nuovi, 192/192.

- [x] **Angoli di piega nell'header DXF** (MAP.md D47) — `to_dxf(annotate=True)`
  e `export_part(include_header=True)` scrivevano solo `flat.meta`,
  `flat.bends` non ci arrivava mai. Ora sì: una riga sola se le pieghe
  sono tutte uguali (il caso normale per Cone/Cylinder sfaccettati), una
  riga per piega se sono diverse (BentProfile). Verificato leggendo il
  testo vero dal DXF generato, non solo stampato — 2 test nuovi, 186/186.

- [x] **`Cone`/`Cylinder` divisibili in pezzi uguali** (`split`, MAP.md
  D46) — soprattutto per lo sfaccettato: due metà saldate quando il
  pezzo è troppo grande per una lavorazione sola. `split=2` è la
  scorciatoia per `sector_angle=360/split` (`Cylinder`) o
  `full_angle/split` (`Cone`, che ora ha anche `sector_angle` — prima
  non esisteva nessun modo di limitare lo sviluppo naturale). Sfaccettato
  parziale ora supportato per entrambi (era esplicitamente "non ancora
  deciso" per `Cylinder` da D42) — deve tornare un numero intero di
  faccette, altrimenti errore esplicito. `margin` funziona così com'è,
  zero codice nuovo per quello — era già generico. Trovato e corretto un
  bug vero nel farlo: la larghezza faccetta di `Cone` sfaccettato usava
  il conteggio del pezzo invece che del poligono intero. 11 test nuovi,
  184/184 verdi.
- [x] `Cone`/`Cylinder(faceted=True)` usano la `Calibration` dell'officina
  per raggio/K dei giunti (come `BentProfile`), non più una tabella per
  materiale a parte. `flat.bends` popolato anche lì (una `BendResult`
  per giunto). Cambia il default del raggio quando `facet_bend_radius`
  non è dato (prima `= thickness`, ora dalla calibrazione — 1mm fisso
  per chi usa `"default"`, MAP.md D36). 6 test nuovi, 173/173 verdi.
  `MATERIAL_K_FACTORS`/`estimate_k_factor` orfani dal percorso di
  default, ancora pubblici — da decidere se tenerli o ritirarli.

## Priorità di fondo (MAP.md D36/D39)

La formula generica è il prodotto; i dati misurati di un'officina sono un
bonus/banco di prova, mai un blocco. Ogni scelta di setup/default si
controlla contro questi quattro casi, sempre gli stessi — nome standard
`tipo_cliente` (campo verificato da codice, `tipo_cliente_coerente()`):

| `tipo_cliente` | Chi è | Cosa gli si chiede |
|---|---|---|
| `zero_config` | sconosciuto, scarica e basta, non legge nulla | niente — zero config, `calibration="default"` |
| `cava_propria` | carpenteria vicina, mi contatta, niente CAM | solo la tabella spessore→cava (5 minuti, mai una misura) |
| `somma_interna` | vuole solo somma quote interne, zero K-factor | niente — `calibration="inside_sum"` |
| `misurato` | ha il CAM, vuole avvicinarsi per preventivare | cava + tutti i dati misurati che il CAM tira fuori, **quando li ha** — mai un prerequisito per gli altri tre |

Una scelta che serve bene `misurato` ma appesantisce o blocca gli altri
tre è quasi sempre la scelta sbagliata. Niente viene più parcheggiato "in
attesa di altri `.bnc`": o si trova una via generica, o si dichiara il
limite e si va avanti (vedi MAP.md D36).

## Fatto (fasi 1-3.5)

1. ✅ Pulizie di impostazione, `MAP.md`, script numerati + `SCRIPTS.md`.
2. ✅ Fase 1 — `section_from_part`, giro chiuso su L/U/Z/omega entro 0.01 mm.
3. ✅ Fase 2 — motore a strati, `BendResult` interrogabile, rinomine EN.
4. ✅ Fase 3 — layer umano: quote esterne↔mezzeria, vista in sezione
   quotata, `export_part()` a livelli.
5. ✅ Fase 3.5 (D36) — priorità capovolta formula-generica-prima;
   `default.json` non indovina più cave (tutta a `null`); raggio fisso
   dichiarato (`DEFAULT_UNKNOWN_RADIUS_MM = 1.0`) quando cava e raggio
   sono entrambi ignoti.

## Prossimo

- [x] `COME_FUNZIONA.md` / `TUTORIAL.md` / `README.md` / `README_IT.md` —
  riallineati a D36 (raggio fisso dichiarato per il caso A, tabella dei
  4 casi A/B/C/D).
- [x] `docs/ARCHITECTURE.md` — scritto (11 set 2026): il flusso
  topo→pippo→snapbend, cosa riceve/manda pippo da/a `read_section()`,
  i layer e la regola di dipendenza, cosa non è ancora pulito.
- [x] `docs/API.md` — scritto (11 set 2026), D16 chiusa: una scheda per
  ognuno dei 24 nomi di `snapbend.__all__`, ogni esempio verificato
  girando davvero (non solo letto dal sorgente).

## Dati che arrivano quando arrivano — mai un blocco

- [ ] **`cava_per_spessore` VERA in `tipo_misurato.json`**: `CAVE_officina_1.txt`
  ha più V per lo stesso spessore (0,5 → V4/V6/V8; 4 → V20/V24; 6 →
  V30/V40; 8 → V40/V50; 10 → V50/V60; 12 → V60/V70; 15 → V70/V90). Serve
  che Federico dica la "standard" per ciascuno. Migliora solo il caso D
  su officina 1, non morde i test (ogni provino ha la sua combinazione
  esatta fra i `misurati`).
- [ ] **K per materiale (inox/allu)**: niente più placeholder (erano
  sbagliati, sotto ogni range pubblicato — tolti, MAP.md D37). Nessuna
  fonte generica di settore è affidabile per questo (verificato, D37): si
  scende alla stima DIN generica finché Federico non porta gli `.fx` con
  materiale cambiato. Non blocca nulla.
- [ ] **Prossimo giro di provini**, solo se/quando Federico li porta:
  spessori grossi (8–20 mm, dove la formula sbaglia di più) e non-90°
  aperti (120°/150°) a s2/s5/s8.

## Angolo non a 90° — fatto per gli aperti a una piega (MAP.md D38)

- [x] **1. Angolo incluso vero nel giro dei golden**, dal `Sollwinkel` del
  `.bnc` gemello — il layer DXF resta solo per il verso su/giù.
- [x] **2. Sei golden non-90° aperti**, `La114ab{120,150}b114s{1,3,10}`,
  nel giro golden + `tipo_misurato.json` (`misurati`). Chiuso entro 0.005 mm.
- [x] **3. Match misurato sull'angolo** — verificato: `rule="misurato"`
  su tutti e 6, non il fallback DIN.
- [ ] **4. Z/omega non a 90°.** Restano fuori. Causa capita (Federico,
  11 set): la seconda piega di una Z non va in appoggio — dopo la prima
  piega il pezzo non è più piatto, quella flangia non si posiziona più
  contro il riscontro nel ciclo automatico, quindi TruBend non la misura
  come un colpo normale e il `.bnc` non ha un `Biegeverkuerzung` pulito
  per lei (confermato su `Za60ab50b100bc250c50s10`: un solo `Biegenummer`
  registrato invece di due). Non è un dato mancante da noi, è un dato che
  non esiste alla fonte in forma misurata automatica. Serve un'altra via
  per quel numero (es. misura a mano sul pezzo finito) — non altro scavo
  nei `.bnc`.

## Piega chiusa / coniatura — limite dichiarato, non un buco da tappare

Un interprete che legge solo un disegno non può sapere se una piega verrà
coniata o piegata in aria — è una scelta di processo dell'officina,
invisibile nella vista. La risposta corretta è **assumere aria** (il caso
dominante, vedi `PIEGA_IN_ARIA_E_CONIATURA.md`) e dichiararlo, non
inseguire dati di coniatura all'infinito.

- [x] Confermato con dati veri (11 set, `La114ab{50,70}b114s{1,3,10}`):
  trattati come piega in aria, lo sviluppo ricostruito sbaglia di 2–5 mm.
  `reconstruct.is_reconstructable_name()` li esclude di proposito dai
  golden — non è un buco, è il limite dichiarato.
- [ ] Se Federico porta un punzone di coniatura + angolo di montaggio,
  quei golden si chiavano a parte (spessore, angolo, punzone) — bonus,
  non prerequisito.
- [ ] `Za60ab{50,70}...s{1,3,10}`: stessa famiglia (chiusi), dopo Z aperti.

## Lettura disegno → Cone/Cylinder/BentProfile (MAP.md D42)

`read_section()` (la "dima": rileva spessore da facce parallele/
archi concentrici) resta l'unico rilevatore — instrada verso una classe
esistente o l'altra, nessuna classe geometrica nuova. Ordine consigliato,
ogni pezzo piccolo e verificabile da solo:

- [x] **1. `Cylinder`: angolo di settore opzionale** (default 360°) —
  `width = radians(angle) × raggio_medio` invece di sempre `π×diametro`,
  stessa famiglia di formula del settore di `Cone`. Sblocca lo sviluppo
  di una sella calandrata (R300, 60°) senza nessuna lettura di disegno,
  solo passando l'angolo a mano — primo pezzo utile da solo. Fatto:
  parametro `sector_angle` (default 360, invariato per chi non lo tocca),
  `faceted=True` + settore parziale rifiutato esplicito (non deciso). 5
  test nuovi, 163/163 verdi.
- [x] **2. `read_section()`: gestire `type: "circle"`** — oggi le
  entity `circle` (es. le due circonferenze concentriche di un tubo
  visto dall'alto) sono scartate in silenzio dal filtro `type in
  ("line", "arc")`. Fatto: `_Edge` legge `circle` come giro chiuso
  (lunghezza = 2πr diretta, non passa dal calcolo sweep che a 360°
  darebbe 0 per il modulo), spessore e `is_bent` lo vedono. La
  ricostruzione della centerline resta esplicitamente non fatta per
  questo caso (si degrada a nota, non crasha) — è il punto 3. 3 test
  nuovi, 166/166 verdi.
- [x] ~~3. percorso per profilo ad arco puro~~ e ~~4. `BentProfile.from_section_reading()`~~
  — non più su questa base: `read_section()` stesso passa a topo
  nativo (MAP.md D43). Si fanno lì, una volta sola, non due (vedi sotto).

## `read_section()` su topo — provato e ritrattato per intero (MAP.md D43, CHIUSA)

`rules/read_section.py` ha importato topo per una notte (prima gli interni
`topo.core.topology.*`, poi la superficie pubblica
`load_geometry`+`heal_and_detect`, allora di topo, entrambe verificate funzionanti) ed è
tornato al loop-walker fatto a mano — non perché rotto, ma perché non
c'è ancora un consumatore vero (`pippo`) per cui decidere quel
contratto. `snapbend` oggi importa topo SOLO in `io/dxf.py` e in `flat/` (D51).
Restano dal giro di stanotte: il rilevamento delle coppie di cerchi e
l'instradamento dell'arco puro (sella) verso `Cylinder`/`Cone`, portati
sul loop-walker originale — 167/167 verdi. Storico delle fasi valutate:

- [x] **0. Decisione + `pyproject.toml`** — dipendenza `topo` ora
  richiesta (non più opzionale), descrizione riscritta.
- [x] **1. `read_section()` su `topo/core/topology/graph.py` +
  `loop_finder.py`** — sostituisce `_Edge`/`_split_into_sides`/
  `_order_chain` fatti a mano. Assorbe qui il caso "profilo ad arco puro
  → `Cylinder`/`Cone`" (ex punto 3 sopra) direttamente sulla base nuova.
  Fatto: `topo.load_geometry()` costruisce il `Document`,
  `build_node_graph()`+`LoopFinder()` camminano il loop chiuso già
  ordinato. **Ritrattato lo stesso giorno** (vedi sotto): tornato al
  loop-walker fatto a mano, `snapbend` non importa più topo da
  `rules/read_section.py`. Sopravvive il risultato buono: caso arco puro
  (sella, cap→arco→cap, zero flange) riconosciuto, `centerline_segments`/
  `angles` vuoti per quel caso, campi `pure_arc_radius`/
  `pure_arc_angle_deg` su `SectionReading` — portati sul walker
  originale. 1 test nuovo (sella R300/60°/s3), **167/167 verdi**.
- [x] ~~2. `Cone`/`Cylinder`/`BentProfile.develop()` costruiscono `Edge`~~,
  ~~3. `io/dxf.py` via `to_topo_result()`~~, ~~4. test → `Edge`~~ —
  **ritrattate (MAP.md D43), non si fanno.** `topo.load_geometry()` è
  già il modo con cui topo vuole ricevere geometria da un generatore
  (il suo stesso docstring usa un settore di cono come esempio) —
  costruire `Edge` a mano rifarebbe peggio quello che fa già lui.
  `FlatGeometry` non è ridondante con `Document`: porta `meta`
  (i numeri leggibili da un piegatore) e `reference_entities` (il
  margine tratteggiato), roba di dominio `snapbend` che `Document`
  non ha. D43 resta chiusa alla fase 0-1 sopra.

## `BentProfile` da un disegno letto — resta da fare, indipendente da D43

`BentProfile.from_section_reading(reading: SectionReading, calibration=...)`
per il caso a flange dritte vere (L/U/Z lette da un disegno) — non
dipende in nessun modo dalla questione Edge/dict sopra, prende in
ingresso `read_section()`'s `centerline_segments`/`angles`/
`thickness`, stesso formato di oggi.

## Parcheggiato — Fase 4/5

- [ ] Scatole / pieghe su più assi (modello "a stella" — logica nuova
  per l'incrocio delle flange agli spigoli; usa la stessa formula
  generica già in `bend.py`/`deduction.py`, `calibration="default"`,
  zero dati misurati richiesti per partire — vedi MAP.md
  "formula generica prima" D36/D39).
- [ ] Info di piega (angolo ≠ 90°) nei DXF TruBend — dove sta quando si
  reimporta.

## Futuribili — qui dentro snapbend, non un altro progetto (11 set 2026)

Deciso da Federico: senza un pippo anche rudimentale, `snapbend` come
generatore+lettore è già in uno stato completo per quello che è (173
test verdi, calibrazione unificata D45, `docs/API.md`/`ARCHITECTURE.md`
scritti) — non è bloccato in attesa di pippo, pippo è un consumatore a
parte. Questi tre restano lavoro VERO di `snapbend`, non rimandati a un
altro repo, perché modificano/estendono la geometria che `snapbend` stesso
genera — diverso dal caso "foro nella posizione che dice il cliente"
(quello sì resta di topo/pippo a valle, vedi sotto):

- [ ] **Smussi/raggi ai 4 angoli dello sviluppo** — già prassi
  d'officina, `snapbend` oggi genera sempre spigoli vivi. Sostituisce il
  vecchio bullet "raggio sugli spigoli del contorno esterno" (era
  segnato "non deciso" — ora deciso: qui). Conseguenza diretta: la
  **larghezza netta** della flangia vista dall'alto (quella che si
  taglia davvero) non è più semplicemente `width` una volta smussati gli
  angoli — va esposta in `meta` accanto a `width`, non lasciata implicita.
- [ ] **Convertitore da profilo strutturale standard (angolare/U) a
  `Section`** — quando un angolare o un U a catalogo nella misura giusta
  non si trova/non si compra, l'officina lo piega da lamiera invece —
  stessa forma (L/U) che `snapbend` già sa sviluppare. Serve una tabella
  dati VERA (dimensioni standard angolari/profilati UNI/EN) prima di
  scrivere il convertitore — non va inventata a memoria (stesso principio
  di "verificare prima di asserire" già in altre note). Nome di lavoro:
  `Section.from_structural_profile(...)`, un'altra via d'ingresso come
  `from_external_flanges()`.
- [ ] **Posizione di ogni flangia nello sviluppo PIATTO** (non nella
  vista in sezione) — oggi `BentProfile.develop()` calcola internamente
  le posizioni delle linee di piega ma non le espone in `meta` come
  range per-flangia. Senza quello, pippo (o chiunque) non sa DOVE su un
  cut file piazzare una feature con `topo.inject()` — questo è il pezzo
  che manca perché `snapbend` continui a dire "le coordinate", non "la
  feature" (vedi sotto).

### Feature di tracciatura.
  Il caso: un disegno (quello dei segni tracciati stretti, oggi non più su disco)
  ha una serie di dentelli che partono da una linea orizzontale, che sono considerati parte del grafo giustamnete. vorrei aggiungere un parametro che sotto una certa distanza queste linee siano considerate solo dei segni di marcatura, completando il grafo solo con la linea orizzontale. Anche se ho degli inner che hanno distanza inferiore alla tolleranza di cui sopra, devono essere detectati come segni di incisione e posti sul layer 'Engrave'. probabilmente questa cosa va implementata nel modulo detect e può essere individuato il tutto solo passando detect_flat() come facciamo con le bl che hanno la loro tolleranza.
  (roba per snapbend)

## Fuori scope (di un altro layer, non "non deciso")

- [ ] Fori/altre feature sul pezzo, in posizione decisa dal disegno
  cliente — resta compito di `topo`/pippo a valle
  (`topo.inject()` esiste già per questo). Principio che li separa dai
  tre sopra: uno smusso d'angolo è `snapbend` che completa la SUA propria
  geometria generata; un foro a una coordinata del cliente è pippo che
  aggiunge qualcosa che `snapbend` non ha motivo di conoscere.
- [ ] Traduttore quote INTERNE ↔ mezzeria — proposto e ritirato da
  Federico stesso, resta qui solo perché banale da aggiungere se serve.
- [x] ~~Reverse engineering pieghe da un DXF cliente senza `.bnc`~~ —
  non più fuori scope, diventato un piano concreto: vedi sezione
  "Lettura disegno → Cone/Cylinder/BentProfile" sopra (MAP.md D42).
- [ ] Cosa esportare per il generatore di file di taglio a valle
  (`develop_from_external_flanges()` e i dati di `flange_quotes()` sono i
  candidati, non `to_dxf()` — vedi MAP.md D30/D31). Non ancora discusso
  nel dettaglio.
