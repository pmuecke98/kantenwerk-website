# Kantenwerk – Website

Statische One-Page-Website (HTML/CSS, kein Baukasten, keine laufenden Kosten außer Domain).

## Dateien
- index.html – die Startseite
- impressum.html, datenschutz.html – Rechtstexte (Gerüst, bitte vervollständigen)
- danke.html – erscheint nach dem Absenden des Formulars
- style.css – Design; Farben ganz oben unter :root änderbar
- fonts/ – Schriften lokal (keine Verbindung zu Google, DSGVO-freundlich)
- favicon.svg – Browser-Icon

## Vor dem Veröffentlichen
Alle Platzhalter in [eckigen Klammern] ersetzen (Suche nach "[" in allen Dateien):
- [TELEFONNUMMER] und im WhatsApp-Link 49XXXXXXXXXXX (Nummer ohne 0 und ohne Leerzeichen, z. B. 491711234567)
- [STADTTEIL], [ABGABEZEITEN], [X] Werktage
- [JAHR] / [MEISTERTITEL …] in "Über mich"
- [INSTAGRAM]-Name
- Impressum: Name und Adresse
- Foto: Bild in einen Ordner "bilder/" legen und im Kommentar in index.html einsetzen

Namen ändern: "Kantenwerk" in allen Dateien per Suchen & Ersetzen austauschen.

## Online stellen mit Netlify (kostenlos)
1. Konto auf netlify.com anlegen.
2. "Add new site" → "Deploy manually" → den ganzen Ordner per Drag & Drop hochladen.
3. Unter "Forms" das Formular-Erkennen aktivieren und unter "Form notifications" deine E-Mail eintragen – Anfragen kommen dann per Mail.
4. Eigene Domain (.de) bei einem Anbieter kaufen und unter "Domain management" verbinden. HTTPS richtet Netlify automatisch ein.

Änderungen später: Dateien bearbeiten und den Ordner erneut hochladen.
