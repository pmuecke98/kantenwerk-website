# Kantenwerk-Website – Regeln für Claude

Statischer One-Pager (HTML/CSS) für Kantenwerk – Skiservice von Hand in Leverkusen. Hosting: Netlify, verbunden mit `main`.

## Niemals direkt auf `main`

Jeder Stand auf `main` löst ein Netlify-Live-Deploy aus. Der Free-Tarif hat 300 Credits/Monat, ein Live-Deploy
kostet 15 Credits; ist das Guthaben leer, wird die Seite pausiert. Deshalb:

- **Nie** `git push` nach `main`, nie auf `main` committen, nie einen Pull Request selbst mergen.
- Jede Änderung – auch ein Tippfehler – auf einem Branch `vorschau/<thema>`, pushen, Pull-Request-Link nennen.
- Philipp mergt selbst. Mehrere Änderungen nach Möglichkeit auf einem Branch sammeln (ein Merge = ein Deploy)
  und klar sagen, wann ein Branch fertig zum Mergen ist.
- Vor neuer Arbeit `main` holen und den Branch davon abzweigen; vor jedem Push `git pull --rebase` auf dem Branch
  (Philipp ändert gelegentlich selbst im Browser).
- Im Clone den pre-push-Hook einrichten, der Pushes nach `main` blockiert (siehe unten).

```sh
printf '#!/bin/sh\nwhile read l ls r rs; do [ "$r" = "refs/heads/main" ] && echo "Push nach main blockiert" >&2 && exit 1; done; exit 0\n' > .git/hooks/pre-push && chmod +x .git/hooks/pre-push
```

## Vor jedem Push

- `python3 tests/check_site.py` muss grün sein.
- `npx html-validate index.html impressum.html datenschutz.html danke.html` muss grün sein.
- Sichtbare Änderungen per Screenshot (Desktop 1440 px und Handy 390 px) prüfen.

## Inhaltliche Fallen

- FAQ steht doppelt: sichtbar in `#faq` und im JSON-LD-Block `FAQPage` – immer beide ändern.
- Preise stehen dreifach: Karten in `#preise`, FAQ, `LocalBusiness.hasOfferCatalog`.
- Kontaktdaten: `index.html`, `impressum.html`, `datenschutz.html`, `LocalBusiness`.
- Keine externen Ressourcen (Google Fonts, Tracking, Cookies) – Schriften liegen in `fonts/`.
- Rechtliche Aussagen (Haftung, Widerruf) nicht verschärfen ohne Hinweis auf rechtliche Prüfung.
