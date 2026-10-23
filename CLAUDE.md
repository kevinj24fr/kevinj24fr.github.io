# Instructions for Claude Code in this repository

Read `README.md` first. It explains what the site is trying to say and the conventions that
were arrived at by revision. Build on them; do not reset them.

Hard rules:

1. Commit as Kevin Joseph <kevin.joseph@uniklinik-freiburg.de>. No `Co-Authored-By`, no
   `Claude-Session`, no tool attribution anywhere in the repo. Push with
   `-c 'credential.helper=!gh auth git-credential'`.
2. Edit `scripts/pages/*.html` and `scripts/build.py`, never the generated `index.html` files.
   Run `python3 -I scripts/build.py`, check the output, commit the generated files too.
3. Bump `V` in `build.py` after any CSS or JS change.
4. No meta-commentary about the site, no stated values, no counts as boasts, nothing that goes
   stale. If a line explains the site rather than showing the work, cut it.
5. Evidence grammar: published claims are `{{L:...|...}}` links; open questions are plain text.
6. The Laboratory for NeuroEngineering is Kevin's; 3DBM is Vidhya M. Ravi's; the GitHub org is
   shared. Say it that way.
7. Internal tools and unpublished results stay off the page. Application-specific material from
   the W3 drafts stays off the page.
8. Verify locally with headless Chrome before pushing, and verify the live site after. GitHub
   Pages serves `main` directly; expect a one to two minute rebuild.

When Kevin asks for an assessment, give the assessment and stop. When he asks for a change,
make it, show it rendered, push it, and confirm it live.
