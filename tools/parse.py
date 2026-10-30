"""Parse the OGP PDF text (cache/const.txt, from pypdf) into corpus.json. Deterministic; no network."""
import hashlib, json, re, sys, unicodedata
from pathlib import Path
here = Path(__file__).parent
raw = (here / 'cache' / 'const.txt').read_text(encoding='utf-8')
sha = hashlib.sha256((here / 'cache' / 'CONST.pdf').read_bytes()).hexdigest()
ROMAN = ['I','II','III','IV','V','VI','VII','VIII','IX']
HDR = re.compile(r'^(Rev\. 15 de abril de 2024.*|Revisado 15 de abril de 2024.*|.*Página\s+\d+ de 21.*|“Constitución del Estado Libre Asociado de Puerto Rico”|Constitución del Estado Libre Asociado de Puerto Rico)\s*$')
def norm(s):
    s = s.replace(' ',' ').replace('’',"'").replace('í','í')
    return re.sub(r' +',' ',s).strip()
lines = []
for l in raw.split('\n'):
    n = norm(l)
    if HDR.match(n) and n:
        lines.append('\x00')  # page boundary marker
    else:
        lines.append(n)
# blocks separated by blank lines; remember whether a page boundary was inside the gap
blocks = []; cur = []; brk = False; gap_break = False
for n in lines:
    if n == '\x00':
        brk = True; continue
    if n == '':
        if cur: blocks.append((' '.join(cur), gap_break)); cur = []; gap_break = False
        gap_break = gap_break or brk; brk = False
        continue
    if brk and not cur: gap_break = True
    brk = False
    cur.append(n)
if cur: blocks.append((' '.join(cur), gap_break))
paras = []
for t, pb in blocks:
    if paras and pb and not re.match(r'^(Sección|ARTICULO|Preámbulo)\b', t) and (t[0].islower() or paras[-1][-1] not in '.:;'):
        paras[-1] += ' ' + t
    else:
        paras.append(t)
units = {}; order = []; art = None; cur_key = None; labels = {}
def add(key, label, kind, text):
    units[key] = {'label': label, 'kind': kind, 'text': text}
for p in paras:
    p = re.sub(r'\s+', ' ', p)
    if p == 'Preámbulo':
        cur_key = 'preambulo'; units[cur_key] = {'label': 'Preámbulo', 'kind': 'preamble', 'lines': ['# Preámbulo']}; continue
    m = re.match(r'^ARTICULO ([IVX]+)$', p)
    if m:
        art = ROMAN.index(m.group(1)) + 1
        cur_key = 'art-%02d-titulo' % art
        units[cur_key] = {'label': 'Artículo %s' % m.group(1), 'kind': 'article', 'lines': ['# Artículo %s' % m.group(1)]}; continue
    m = re.match(r'^Sección (\d+)\s*\.?\s*[—-]\s*(.*)$', p)
    if m and art:
        n = int(m.group(1)); cur_key = 'art-%02d-sec-%02d' % (art, n)
        units[cur_key] = {'label': 'Art. %s, Sec. %d' % (ROMAN[art-1], n), 'kind': 'sec', 'lines': ['# Artículo %s, Sección %d' % (ROMAN[art-1], n), m.group(2)]}; continue
    units[cur_key]['lines'].append(p)
for k, u in units.items():
    u['text'] = '\n'.join(u.pop('lines')) + '\n'
sources_url = 'https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/Derechos%20Civiles/CONST/CONST.pdf'
corpus = {
 'country': {'code': 'PR', 'name': 'Puerto Rico', 'slug': 'puerto-rico', 'lang': 'es', 'tz': 'America/Puerto_Rico', 'future_branch': 'futuro',
   'publisher': {'name': 'Oficina de Gerencia y Presupuesto (OGP), Biblioteca Virtual', 'email': 'ogp@bvirtualogp.pr.gov.invalid'},
   'default_in_force_rule': {'text': 'The source gives only the revision date of its own copy (Rev. 15 de abril de 2024); the version is dated by that day.', 'source': sources_url},
   'licence_note': 'Text of the Constitution of the Commonwealth of Puerto Rico from the Biblioteca Virtual of the Oficina de Gerencia y Presupuesto del Gobierno de Puerto Rico (www.ogp.pr.gov), revision of 15 April 2024. No licence is stated; the Constitution is the official text of the Commonwealth.'},
 'sources': [{'name': 'OGP Biblioteca Virtual: Constitución del Estado Libre Asociado de Puerto Rico', 'url': sources_url, 'retrieved': '2026-10-29', 'licence': 'none stated', 'notes': 'Single PDF with a text layer, Rev. 15 de abril de 2024.'}],
 'laws': {},
 'acts': [{'slug': 'constitucion', 'short': 'Constitución', 'title': 'Constitución del Estado Libre Asociado de Puerto Rico', 'url': sources_url,
   'first_law': None, 'earlier_laws': [],
   'versions': [{'from': '2024-04-15', 'source_url': sources_url, 'sha256': sha, 'units': units, 'credits': {},
     'note': 'Oldest version available: the OGP copy revised 15 April 2024. The Constitution took effect on 25 July 1952 and has been amended since; earlier texts are not online in an official form.'}]}],
 'applies': [],
 'decisions': ['One version only: the OGP copy dated by its own revision date (15 April 2024); history before that is not reconstructed.',
   'Page headers and footers of the PDF were removed; wrapped lines were joined into paragraphs; a paragraph split by a page break was rejoined.',
   'Language: Spanish, the official language of this text; no English official text was used.'],
 'ai_use': ['Claude Code wrote the parser; it did not write or alter any legal text.']}
(here / 'corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
print(len(units), 'units'); print(list(units)[:6])
