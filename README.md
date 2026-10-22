# kevinj24fr.github.io

Source for [kevinj24fr.github.io](https://kevinj24fr.github.io/).

Static HTML and one CSS file, served by GitHub Pages from `main`. No build step is needed to
publish; `index.html` is committed as-is.

The papers section is generated:

```sh
python3 -I scripts/build.py     # publications.json + scripts/template.html -> index.html
```

`publications.json` was derived from a Google Scholar CSV export, filtered to peer-reviewed
papers and preprints, with DOIs resolved through Crossref. To update it, re-export the CSV,
regenerate the JSON, run the build, commit.

- `index.html` — the page (generated)
- `scripts/template.html` — everything except the papers list
- `scripts/build.py` — fills the papers list into the template
- `assets/css/style.css` — styles, light and dark
- `assets/js/main.js` — theme toggle and the year in the footer
