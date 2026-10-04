# snapbend — working agreement

Sheet-metal engine on top of forge. Three jobs: **compute** a flat pattern from
parameters (`Cone`, `Cylinder`, `BentProfile`, pure math, zero dependencies),
**read** a contour to tell whether it is a bent sheet and with what measures
(`read_section`), and **read a flat cutting file** on top of `forge.heal()` —
holes, countersinks, threaded holes, bends, engraving (`snapbend.flat`, needs
forge). snapbend is where process meaning lives: forge says "circle", snapbend
says "hole to drill".

Python 3.11 · version in `pyproject.toml` · `import snapbend`.
Talk to Federico in Italian; everything written in the repo is English except
docstrings/comments (Italian).

## Read before you write

| situation | read |
|---|---|
| calling the library, need a signature | `docs/API.md` — one card per public name, `snapbend.flat` included |
| **about to add a function, helper or class** | `docs/INDEX.md` — every module-level name with `file:line`. Check the name *and* the job exist nowhere before writing — and check forge's `docs/INDEX.md` too: a geometric fact belongs there |
| why is it built this way, which layer may import what | `docs/ARCHITECTURE.md` |
| why was X decided | `MAP.md` — decision log `D1…Dn`. **A closed decision is not re-decided**; to reopen it, say "reopening D##" out loud |
| what's missing | `TODO.md` |
| running something end to end | numbered scripts at the repo root, listed in `SCRIPTS.md`, order in `TUTORIAL.md` |
| tests, fixtures, goldens | `tests/`, plus the `python-testing-style` skill |

`docs/INDEX.md` is **generated**. Never edit it by hand:

```
python tests/gen_index.py            # regenerate after adding/moving code
python tests/gen_index.py --check    # exit 1 if stale or the dependency rule is broken
```

`tests/test_index.py` runs the check in the suite. The rule is in
`pyproject.toml` (`[tool.gen_index.layers]`); `tests/gen_index.py` is the same
file as forge's `scripts/gen_index.py` — change it in one, copy to the other.

## Non-negotiables

1. **The calculation does not know forge exists.** `core/`, `model/`, `rules/`
   never import forge (checked by `tests/test_index.py`). forge enters only in
   `io/dxf.py` and `flat/`.
2. **Geometry is forge's, meaning is snapbend's.** "Concentric circles", "an
   arc around a circle", a contour's shape come from forge
   (`concentric_groups`, `arcs_around`, `contour_shape`). If a geometric fact
   is missing, add it to forge — never a private copy here (forge MAP.md D91).
   Thresholds that carry process meaning stay here (`flat/thresholds.py`).
3. **`detect_flat()` assumes a flat part seen from its face** (cutting file,
   development). Never run it on `forge.island()` output.
4. **Build fixtures through forge's API or snapbend's generators**, never with
   `ezdxf` directly.
5. **Never regenerate a golden to make a test pass** without first proving the
   code is right.
6. **No client data in git**: no original drawing names, part codes, client
   names — not in code, docs, MAP.md or commit messages.

## How to work

- **A concrete failing file is a symptom, not the target.** Fix the general
  mechanism, never tune for one example.
- **Geometric results are judged by eye**: give Federico DXF files he can open.
- **A decision made is a decision written**: next `D##` in `MAP.md`, with the why.
- **A large file is filtered, not read**: to find something inside a big file
  (a drawing, a log, a golden) run a filter (`grep`, a small parser) and read
  its output only.
- Refactors are clean breaks: no compatibility aliases.

## Conventions

English identifiers, Italian docstrings and comments; every module docstring
opens with the file's path. Type hints everywhere. Dataclasses for the domain;
results are typed objects, not loose dicts. Runnable scripts stay at the repo
root (VS Code Run button), no shebang lines. `README.md` in English with
`README_IT.md` as its Italian twin.
