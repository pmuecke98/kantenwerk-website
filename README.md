# Kantenwerk – Website

Website von **Kantenwerk – Skiservice von Hand in Leverkusen**: https://kantenwerk-leverkusen.de

Statischer One-Pager aus reinem HTML und CSS – kein Framework, kein Build-Schritt, keine Cookies, kein Tracking.

## Wie die Seite live geht

```
Änderung auf Branch  →  Pull Request  →  automatische Prüfungen  →  Merge nach main  →  Netlify veröffentlicht
```

- **Hosting:** Netlify (kostenloser Tarif), verbunden mit diesem Repository. Jeder Stand auf `main` ist nach
  wenigen Sekunden live. Nichts mehr per Drag & Drop hochladen.
- **Domain:** `kantenwerk-leverkusen.de` bei INWX. DNS: A-Record `@` → `75.2.60.5`, CNAME `www` →
  `kantenwerk-leverkusen.netlify.app`, dazu der TXT-Eintrag für die Google Search Console.
- **Vorschau:** Für jeden Pull Request baut Netlify eine Deploy Preview (Link im Pull Request).
- **Zurück auf eine alte Version:** Netlify → Deploys → alten Stand anklicken → „Publish deploy“.

## Arbeitsweise

- **Kleine Korrekturen** (Tippfehler, Öffnungszeit): direkt auf `main` im Browser bearbeiten.
- **Alles Sichtbare** (Design, neue Abschnitte, Fotos): eigener Branch `vorschau/<thema>`, Pull Request,
  Vorschau prüfen, dann mergen. Ein Branch pro Thema, nach dem Merge löschen.

## Dateien

| Datei | Inhalt |
| --- | --- |
| `index.html` | Die Startseite: Hero, Preise, Ablauf, Über mich, FAQ, Kontaktformular |
| `impressum.html`, `datenschutz.html` | Rechtstexte (Datenschutz erstellt mit datenschutz-generator.de, ergänzt um Netlify und WhatsApp) |
| `danke.html` | Erscheint nach dem Absenden des Formulars |
| `style.css` | Design; Farben und Schriften ganz oben unter `:root` |
| `fonts/` | Schriften lokal eingebunden (keine Verbindung zu Google, DSGVO-freundlich) |
| `favicon.svg`, `og-image.png` | Browser-Icon und Vorschaubild beim Teilen des Links |
| `robots.txt`, `sitemap.xml` | Für Suchmaschinen (Sitemap ist in der Google Search Console eingereicht) |
| `tests/check_site.py`, `.htmlvalidate.json` | Automatische Prüfungen (siehe unten) |
| `.github/workflows/website-pruefen.yml` | Startet die Prüfungen bei jedem Pull Request |

## Häufige Änderungen – worauf achten

**Preise ändern** – an drei Stellen in `index.html`:
1. Startnummern-Karten im Abschnitt `#preise`
2. FAQ-Antwort „Was kostet ein Skiservice…“ (sichtbar **und** im Block `FAQPage` oben im `<head>`)
3. `hasOfferCatalog` im Block `LocalBusiness` oben im `<head>`

**FAQ ändern** – jede Frage steht zweimal: sichtbar im Abschnitt `#faq` und im Block `FAQPage` im `<head>`
(für Google). Beide Stellen gleich halten, sonst schlägt der Test fehl.

**Kontaktdaten/Öffnungszeiten ändern** – in `index.html` (Kontakt, Ablauf, FAQ, `LocalBusiness`),
`impressum.html` und `datenschutz.html`. Danach auch im Google-Unternehmensprofil anpassen.

**Größere inhaltliche Änderung** – in `sitemap.xml` das Datum bei `<lastmod>` aktualisieren.

**Ausgeblendete Bereiche** – In `index.html` sind im Abschnitt „Der Fahrer“ die Erfolge und das Foto
auskommentiert (`<!-- ERFOLGE …` / `<!-- FOTO …`). Einblenden, sobald die Inhalte da sind; das Foto in einen
Ordner `bilder/` legen und mit `alt`-Text einbinden.

## Automatische Prüfungen

Bei jedem Pull Request und jedem Stand auf `main` prüft GitHub die Seite (Reiter „Checks“ bzw. Häkchen am Commit):

- **HTML auf Fehler** – html-validate, Regeln in `.htmlvalidate.json`
- **Inhalte** – `tests/check_site.py`:
  - keine sichtbaren Platzhalter wie `[JAHR]` oder TODO
  - alle internen Links und Sprungmarken funktionieren, Bilder haben `alt`-Text
  - FAQ auf der Seite = FAQ in den Google-Daten
  - Preise auf der Seite = Preise in den Google-Daten
  - Telefon, E-Mail und WhatsApp-Link überall gleich
  - Impressum mit Pflichtangaben, § 19-UStG-Hinweis, Rechtsseiten auf `noindex`
  - keine extern geladenen Google Fonts
  - Netlify-Formular korrekt, Sitemap und robots.txt gültig

**Grün** = mergen. **Rot** = die Meldung im Check sagt genau, was nicht passt.

Lokal ausführen:

```bash
python3 tests/check_site.py
npx html-validate index.html impressum.html datenschutz.html danke.html
```

## Formular

Netlify Forms, Formularname `anfrage`, Spam-Schutz über das versteckte Feld `bot-field`.
Anfragen landen unter Netlify → Forms und per Mail bei kantenwerk@gmail.com.
Landet eine echte Anfrage im Netlify-Spam: dort als „Not spam“ markieren.
