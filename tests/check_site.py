#!/usr/bin/env python3
"""Inhaltliche Prüfungen für die Kantenwerk-Website.

Läuft lokal mit `python3 tests/check_site.py` und automatisch bei jedem
Pull Request (GitHub Actions). Nur Python-Standardbibliothek, keine Installation nötig.
"""
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "impressum.html", "datenschutz.html", "danke.html"]
PHONE = "01515 8327587"
PHONE_INTL = "4915158327587"
EMAIL = "kantenwerk@gmail.com"
DOMAIN = "https://kantenwerk-leverkusen.de/"

errors = []


def fail(msg):
    errors.append(msg)


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def strip_comments(s):
    return re.sub(r"<!--.*?-->", "", s, flags=re.S)


def visible_text(s):
    s = strip_comments(s)
    s = re.sub(r"<(script|style)\b.*?</\1>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.imgs_no_alt = [], set(), []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])
        if tag == "img" and not a.get("alt"):
            self.imgs_no_alt.append(a.get("src", "?"))
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


# 1) Grundgerüst jeder Seite
parsed = {}
for page in PAGES:
    if not (ROOT / page).exists():
        fail(f"{page}: Datei fehlt")
        continue
    src = read(page)
    c = Collector()
    c.feed(strip_comments(src))
    parsed[page] = (src, c)
    if '<html lang="de">' not in src:
        fail(f"{page}: <html lang=\"de\"> fehlt")
    if not c.title.strip():
        fail(f"{page}: <title> fehlt oder ist leer")
    if 'name="viewport"' not in src:
        fail(f"{page}: viewport-Meta-Tag fehlt (Handy-Darstellung)")
    for img in c.imgs_no_alt:
        fail(f"{page}: Bild ohne alt-Text: {img}")

# 2) Keine sichtbaren Platzhalter
for page, (src, _) in parsed.items():
    text = visible_text(src)
    for m in re.finditer(r"\[[A-ZÄÖÜ][A-ZÄÖÜ0-9 /_.,-]{1,40}\]", text):
        fail(f"{page}: sichtbarer Platzhalter {m.group(0)}")
    if re.search(r"\b(TODO|Lorem ipsum|XXXX)\b", text):
        fail(f"{page}: TODO/Lorem/XXXX im sichtbaren Text")

# 3) Interne Links und Anker zeigen auf etwas, das existiert
for page, (src, c) in parsed.items():
    for link in c.links:
        if link.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
            continue
        path, _, anchor = link.partition("#")
        target = page if path == "" else path
        if not (ROOT / target).exists():
            fail(f"{page}: Link auf fehlende Datei {link}")
        elif anchor and target in parsed and anchor not in parsed[target][1].ids:
            fail(f"{page}: Anker #{anchor} existiert nicht in {target}")

# 4) Strukturierte Daten sind gültiges JSON und passen zur Seite
index_src = parsed.get("index.html", ("", None))[0]
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', index_src, re.S)
ld = {}
for b in blocks:
    try:
        d = json.loads(b)
        ld[d.get("@type")] = d
    except json.JSONDecodeError as e:
        fail(f"index.html: strukturierte Daten kein gültiges JSON ({e})")
biz = ld.get("LocalBusiness")
if not biz:
    fail("index.html: LocalBusiness-Daten fehlen")
else:
    if biz.get("email") != EMAIL:
        fail("LocalBusiness: E-Mail passt nicht zur Website")
    if re.sub(r"\D", "", biz.get("telephone", "")) != PHONE_INTL:
        fail("LocalBusiness: Telefonnummer passt nicht zur Website")
    if biz.get("url") != DOMAIN:
        fail("LocalBusiness: url passt nicht zur Domain")

# 5) FAQ: sichtbarer Text und Google-Daten müssen übereinstimmen
faq = ld.get("FAQPage")
html_faq = re.findall(r'<details class="faq"><summary>(.*?)</summary>(.*?)</details>', index_src, re.S)
if not faq:
    fail("index.html: FAQPage-Daten fehlen")
else:
    ld_q = [q["name"] for q in faq["mainEntity"]]
    html_q = [visible_text(q) for q, _ in html_faq]
    if ld_q != html_q:
        missing = set(html_q) ^ set(ld_q)
        fail(f"FAQ: Fragen auf der Seite und in den Google-Daten unterscheiden sich: {sorted(missing) or 'Reihenfolge'}")
    norm = lambda t: re.sub(r"[^\w€%]+", "", t.replace("°", "")).lower()
    nums = lambda t: set(re.findall(r"\d+(?:,\d+)?(?:–\d+(?:,\d+)?)?", t))
    for (q, a_html), entry in zip(html_faq, faq["mainEntity"]):
        seite, google = visible_text(a_html), entry["acceptedAnswer"]["text"]
        if 'class="angles"' in a_html:
            # Antwort mit Winkel-Karten: gleiche Zahlen/Winkel auf beiden Seiten
            ok = nums(seite) == nums(google)
        else:
            ok = norm(seite) == norm(google)
        if not ok:
            fail(f"FAQ: Antwort zu „{visible_text(q)}“ weicht zwischen Seite und Google-Daten ab")

# 6) Preise auf der Seite = Preise in den Google-Daten
if biz:
    offers = {o["name"]: o["price"] for o in biz["hasOfferCatalog"]["itemListElement"]}
    text = visible_text(index_src)
    for name, price in offers.items():
        if not re.search(rf"\b{re.escape(price)}\s?€", text):
            fail(f"Preis {price} € ({name}) aus den Google-Daten steht nicht auf der Seite")

# 7) Kontaktdaten überall gleich
for page in ("index.html", "impressum.html"):
    t = visible_text(parsed[page][0])
    if PHONE not in t:
        fail(f"{page}: Telefonnummer {PHONE} fehlt")
    if EMAIL not in t:
        fail(f"{page}: E-Mail {EMAIL} fehlt")
if f"wa.me/{PHONE_INTL}" not in index_src:
    fail("index.html: WhatsApp-Link passt nicht zur Telefonnummer")

# 8) Rechtliches
imp = visible_text(parsed["impressum.html"][0])
for must in ("§ 5 DDG", "§ 19 UStG", "Leverkusen"):
    if must not in imp:
        fail(f"impressum.html: „{must}“ fehlt")
if "§ 19 UStG" not in visible_text(index_src):
    fail("index.html: Hinweis § 19 UStG bei den Preisen fehlt")
for page in ("impressum.html", "datenschutz.html", "danke.html"):
    if 'name="robots" content="noindex"' not in parsed[page][0]:
        fail(f"{page}: sollte noindex haben")
for page in PAGES:
    if not re.search(r'href="[^"]*impressum\.html"', parsed[page][0]) and page not in ("impressum.html", "danke.html"):
        fail(f"{page}: Link zum Impressum fehlt")
if "fonts.googleapis" in "".join(s for s, _ in parsed.values()):
    fail("Google Fonts werden extern geladen (Datenschutz!) – Schriften lokal einbinden")

# 9) Formular für Netlify korrekt
form = re.search(r"<form\b[^>]*>", index_src)
if not form or 'data-netlify="true"' not in form.group(0) or 'name="anfrage"' not in form.group(0):
    fail("index.html: Kontaktformular ohne data-netlify / name=\"anfrage\"")
if '<input type="hidden" name="form-name" value="anfrage">' not in index_src:
    fail("index.html: verstecktes Feld form-name fehlt")

# 10) Sitemap und robots.txt
try:
    tree = ET.parse(ROOT / "sitemap.xml")
    locs = [e.text for e in tree.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    if DOMAIN not in locs:
        fail("sitemap.xml: Startseite fehlt")
except ET.ParseError as e:
    fail(f"sitemap.xml: kein gültiges XML ({e})")
if "Sitemap: https://kantenwerk-leverkusen.de/sitemap.xml" not in read("robots.txt"):
    fail("robots.txt: Verweis auf Sitemap fehlt")

if errors:
    print(f"❌ {len(errors)} Problem(e) gefunden:\n")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("✅ Alle inhaltlichen Prüfungen bestanden.")
