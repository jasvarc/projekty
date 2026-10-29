# Pachove Projekty

Zbierka malých projektov, každý ako samostatná statická stránka.

Web: https://jasvarc.github.io/projekty/

## Štruktúra

```
generate_index.py                  generuje úvodný rozcestník (spúšťa sa automaticky pri pushi)
.github/workflows/pages.yml        nasadenie na GitHub Pages
logo.png                           logo v hlavičke rozcestníka a favicon
hodiny/index.html                  jeden projekt = jeden priečinok s index.html
```

Názvy priečinkov píš bez diakritiky a medzier, malými písmenami (`hodiny`, `moja-kalkulacka`).

## Rozcestník sa generuje sám

Súbor `index.html` v koreni sa **neukladá do repozitára**. Pri každom pushi ho vytvorí `generate_index.py` v GitHub Action.

Pravidlá:

- projekt je každý priečinok v koreni, v ktorom je `index.html`,
- názov karty je `<title>` z `index.html` projektu (bez neho sa použije názov priečinka),
- projekty sú v jednom zozname zoradené podľa názvu,
- priečinky začínajúce na `_` alebo `.` sa ignorujú, hodia sa na rozpracované veci.

Lokálny náhľad: `python generate_index.py` (vygenerovaný súbor je v `.gitignore`).

## Pridanie nového projektu

1. Vytvor priečinok `nazov-projektu/` s `index.html`.
2. Daj do `index.html` zmysluplný `<title>`, ten sa zobrazí v zozname.
3. Použi relatívne cesty (`style.css`, nie `/style.css`), inak sa pod `/projekty/` rozbijú.
4. Nahraj zmeny na GitHub. Stránka aj rozcestník sa aktualizujú do 1–2 minút.

Rozcestník sa nikde ručne nemení.

## Nastavenie GitHub Pages (jednorazovo)

V repozitári: Settings → Pages → Build and deployment → Source: **GitHub Actions**. Bez toho sa rozcestník nevygeneruje.
