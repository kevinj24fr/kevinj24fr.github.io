# kevinj24fr.github.io

Source for [kevinj24fr.github.io](https://kevinj24fr.github.io/), the site of Kevin Joseph, Dr.-Ing.,
Research Group Leader of the Laboratory for NeuroEngineering, Department of Neurosurgery,
Medical Center – University of Freiburg.

This file is the brief for whoever edits the site next, human or agent. Read it before changing
anything. `CLAUDE.md` holds the short version of the rules for Claude Code sessions.

## What the site is trying to say

One question, tested three ways. How do glial cells receive, integrate, and transmit signals in
intact human brain tissue, and does their response determine what the tissue does next? The
perturbations are an implanted device, a tumour, and protein pathology. The readouts are
electrophysiology, spatial and single-cell genomics, and morphometry. The laboratory is one of few
that studies tumours and implanted devices in the same tissue with the same methods.

The message a cold reader should take away: a method-first lab that measures the brain's response
to injury in living human tissue, builds its own instruments (wet and computational), says what it
would mean if it is right, and says what it cannot yet prove.

Kevin writes Rust first; the tools page proves it with commands rather than descriptions.

## How the site says it (the conventions)

These were arrived at through revision and are deliberate. Keep them.

- **The work speaks. No meta-commentary.** Nothing about the site itself, nothing about Kevin's
  values stated as values. Rejected and removed: a "How I work" rules section, a "stance" line,
  a "most frequent co-authors" list, a dated "now" line, a footer boasting "static html · no
  analytics". The one exception is the colophon, which is opt-in (footer link only, not in nav or
  sitemap).
- **Nothing that goes stale.** No news, no status, no "last updated". Dates appear only as data
  provenance ("as recorded by OpenAlex, 23 Oct 2026"), never as a claim of recency.
- **No counts as boasts.** No "38 papers", no headcount, no citation totals on the page.
  Citation counts exist in `scripts/openalex.json` but are not shown; Kevin declined them.
- **Evidence grammar.** In prose, a published claim is a link to its DOI (class `ev`, ink-coloured,
  journal and year on hover); an open question is plain text, usually introduced with "Open:".
  The rule is never explained on the page; it is stated once in the colophon.
- **Lab structure.** The GitHub organisation 3DBMandNE-Lab is shared by two groups: 3DBM, led by
  Vidhya M. Ravi, and NE, the Laboratory for NeuroEngineering, led by Kevin. Never call the org
  "Kevin's lab" or say he leads 3DBM.
- **What stays off the site.** Material from the W3 application that is application-specific:
  reference numbers, cover letter, habilitation note, grant amounts, the CIBSS/SFB integration
  pitch, in-press papers that cannot be verified by DOI. Internal tools (the claims pipeline,
  Vigil, Crucible) are not named; the site conveys their stance by obeying the same rules.
- **Design.** Paper and ink. Navy ink `#14213d`, firebrick accent `#b22222`, off-white paper.
  Serif headings, sans body, monospace labels. System fonts only. Light and dark themes via
  `prefers-color-scheme` plus a toggle. Cards for the research threads, two columns for tools.
  Minimalist figures: the perturbation–response–readout diagram, the trajectory strip, the
  Equal Earth collaborator map with a small Europe inset.

## Pages

| URL | Body file | Contents |
|---|---|---|
| `/` | `scripts/pages/home.html` | hero, sidecar, question + diagram + stakes, six thread cards, lab section, five lead papers, "looking for" |
| `/research/` | `scripts/pages/research.html` | the question, by-disease index, trajectory strip, three platforms, findings, three aims, funded projects |
| `/papers/` | `scripts/pages/papers.html` | lead-author papers with roles, then all papers by year |
| `/tools/` | `scripts/pages/tools.html` | tools as typed commands, plus a line of smaller packages |
| `/about/` | `scripts/pages/about.html` | career timeline, the laboratory, collaborator map, teaching, service, contact |
| `/colophon/` | `scripts/pages/colophon.html` | how the site is built; footer link only |
| `/data/` | `scripts/pages/data.html` | the JSON files behind the site |
| 404 | `scripts/pages/404.html` | one line, links to index, papers, colophon |

Shared header, footer, metadata, JSON-LD and the figures are produced by `scripts/build.py`.

## Build

```sh
python3 -I scripts/build.py
```

Writes every page, `sitemap.xml`, `robots.txt`, and copies the data files to `data/`. No
dependencies beyond Python 3. Deterministic. Commit the generated files; GitHub Pages serves
`main` as-is with no build step.

Template placeholders available in page bodies:

- `{{L:title prefix|label}}` — link to a paper by the start of its title; label ending in a year
  is italicised as a journal citation, otherwise rendered as an evidence link.
- `{{LEAD}}` — the five lead-author papers with roles (list `LEAD` in `build.py`).
- `{{ALL}}` — all papers grouped by year. `{{N_ALL}}` — their count.
- `{{TRAJECTORY}}`, `{{COLLAB}}`, `{{ABSTRACTS}}`, `{{DATA_DATE}}`.

After changing `assets/css/style.css` or `assets/js/main.js`, bump `V` in `build.py` so browsers
fetch the new file instead of applying a cached stylesheet to new markup.

## Data and how to refresh it

| File | Source | Refresh |
|---|---|---|
| `publications.json` | Google Scholar CSV export (Scholar blocks scraping; Kevin exports it) filtered to papers and preprints; DOIs via Crossref, journal version preferred over bioRxiv/SSRN/Research Square | re-export CSV, rebuild the JSON the same way, keep the `selected` field |
| `scripts/openalex.json` | OpenAlex, per DOI: authorships with institutions and countries, citation counts, plus the author summary | `python3 -I scripts/fetch_openalex.py` |
| `scripts/trajectory.json` | every Scholar entry classified by kind (paper, abstract, thesis) and topic by title regexes | regenerate from the CSV with the same rules (they live in the git history of this README's first version and in the classifier used to make the file) |
| `scripts/world.json` | Equal Earth projection of outlines from the R `maps` package, simplified; includes the Europe inset box | only if the map needs changing |
| `assets/img/card.png` | 1200×630 social preview, rendered by headless Chrome from `scripts/card/card.html` | re-render after a design or title change |

Set `DATA_DATE` in `build.py` whenever the data files are refreshed. It is printed on the
trajectory and map captions and on `/data/`.

## Open items the next session may pick up

- The `karna` repository is private but linked from the tools page; either make it public or
  repoint the links to the lab org.
- The website field is still empty on ORCID, Google Scholar, LinkedIn, and the GitHub profile
  (the last needs the `user` scope on the gh token). Only Kevin can fill these.
- Google Search Console verification: add the token file when Kevin provides it.
- Custom domain: undecided.
- Citation counts are cached and could be shown; Kevin has so far said no.

## Git

Commits are authored and committed by Kevin Joseph only. No co-author trailers, no session
links, no tool attribution. Push over HTTPS with gh as the credential helper:

```sh
git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin main
```
