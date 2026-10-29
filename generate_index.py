#!/usr/bin/env python3
"""Vygeneruje úvodný rozcestník (index.html) pre repozitár projekty.

Spúšťa sa automaticky pri každom push (GitHub Actions), lokálne: python generate_index.py

Štruktúra: <projekt>/index.html   (napr. hodiny/index.html)

Pravidlá:
- projekt = priečinok v koreni, v ktorom existuje index.html
- priečinky začínajúce na "." alebo "_" sa ignorujú (napr. _sablona)
- názov karty = <title> z index.html projektu, inak názov priečinka
- projekty sú v jednom zozname zoradené podľa názvu (bez ohľadu na diakritiku)
- už existujúci index.html v koreni, ktorý nevznikol týmto skriptom (chýba v ňom značka), sa neprepíše
"""
import html
import re
import unicodedata
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
MARK = "<!-- generate_index.py -->"
PAGE_TITLE = "Pachove Projekty"
PAGE_SUB = "Zbierka malých projektov."

CSS = """
:root{--bg:#04060c;--panel:rgba(12,16,28,.86);--line:rgba(140,160,215,.22);--text:#e2e8f5;--muted:#a3adc6;--gold:#f3b453;--gold2:#ffd88a}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;min-height:100vh;font:17px/1.6 system-ui,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--text);background:radial-gradient(1200px 600px at 20% -10%,#101a33 0%,transparent 60%),var(--bg)}
.wrap{max-width:1100px;margin:0 auto;padding:16px 16px 40px}
.top{display:flex;align-items:center;gap:18px;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:8px 0 28px}
.logo{width:96px;height:96px;flex:0 0 auto;border-radius:50%;display:block;box-shadow:0 0 0 2px var(--line),0 6px 18px rgba(0,0,0,.45)}
h1{margin:0;font-size:16px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}
.sub{color:var(--muted);margin:6px 0 0}
.sum{color:var(--muted);font-size:14px;margin:10px 0 0}
ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
li{margin:0}
a.card{display:flex;align-items:center;justify-content:space-between;gap:12px;height:100%;padding:14px 16px;color:var(--text);text-decoration:none;background:var(--panel);border:1px solid var(--line);border-radius:12px;transition:transform .15s,border-color .15s}
a.card:hover,a.card:focus-visible{transform:translateY(-2px);border-color:var(--gold)}
a.card:focus-visible{outline:3px solid var(--gold2);outline-offset:2px}
.go{color:var(--gold);font-size:20px;line-height:1;transition:transform .15s}
a.card:hover .go{transform:translateX(4px)}
.empty{color:var(--muted)}
@media (max-width:520px){ul{grid-template-columns:1fr}}
@media (max-width:420px){.logo{width:64px;height:64px}}
@media (prefers-reduced-motion:reduce){a.card,.go{transition:none}a.card:hover{transform:none}}
"""


def fold(s: str) -> str:
    """Kľúč na radenie bez diakritiky a bez ohľadu na veľkosť písmen."""
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def plural(n: int, one: str, few: str, many: str) -> str:
    if n == 1:
        return f"{n} {one}"
    if 2 <= n <= 4:
        return f"{n} {few}"
    return f"{n} {many}"


# ---------------------------------------------------------------- zber dát
projects = []  # (priecinok, nazov)
for d in ROOT.iterdir():
    if not d.is_dir() or d.name.startswith((".", "_")):
        continue
    page = d / "index.html"
    if not page.is_file():
        continue
    text = page.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    title = " ".join(m.group(1).split()) if m else ""
    projects.append((d.name, html.unescape(title) or d.name))

projects.sort(key=lambda it: fold(it[1]))

# ---------------------------------------------------------------- HTML
if projects:
    items = "\n".join(
        f'      <li><a class="card" href="{quote(name)}/">'
        f'<span>{html.escape(title)}</span><span class="go" aria-hidden="true">→</span></a></li>'
        for name, title in projects
    )
    body = f"    <ul>\n{items}\n    </ul>"
else:
    body = '    <p class="empty">Zatiaľ tu nie sú žiadne projekty.</p>'

page = f"""<!DOCTYPE html>
{MARK}
<html lang="sk">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#04060c">
  <title>{html.escape(PAGE_TITLE)}</title>
  <link rel="icon" href="logo.png">
  <style>{CSS}</style>
</head>
<body>
  <div class="wrap">
    <header class="top">
      <img class="logo" src="logo.png" width="96" height="96" alt="Logo – Pachove Projekty">
      <div>
        <h1>{html.escape(PAGE_TITLE)}</h1>
        <p class="sub">{html.escape(PAGE_SUB)}</p>
        <p class="sum">{plural(len(projects), 'projekt', 'projekty', 'projektov')}</p>
      </div>
    </header>
{body}
  </div>
</body>
</html>
"""

target = ROOT / "index.html"
if target.exists() and MARK not in target.read_text(encoding="utf-8", errors="ignore"):
    print("preskakujem index.html (ručne vytvorený súbor)")
else:
    target.write_text(page, encoding="utf-8")
    print(f"rozcestník vygenerovaný, projektov: {len(projects)}")
