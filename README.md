# kevinj24fr.github.io

Source for [kevinj24fr.github.io](https://kevinj24fr.github.io/). Static HTML and one CSS file, served by GitHub Pages from `main`.

Pages are generated. Edit the page bodies, then build and commit:

```sh
python3 -I scripts/build.py     # scripts/pages/*.html + publications.json -> index.html, research/, papers/, tools/, about/
```

- `scripts/pages/{home,research,papers,tools,about}.html` — page bodies. `{{L:title prefix|label}}` links a paper by title; `{{LEAD}}`, `{{ALL}}`, `{{N_ALL}}` fill the paper lists.
- `scripts/build.py` — shared header, footer, and metadata; bump `V` there when the stylesheet changes so browsers fetch it fresh.
- `publications.json` — from a Google Scholar CSV export, filtered to papers and preprints, DOIs resolved through Crossref.
- `assets/css/style.css`, `assets/js/main.js` — styles (light and dark) and the theme toggle.
