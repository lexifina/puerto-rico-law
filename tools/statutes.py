"""Parse OGP compiled statute PDFs (text from pdftotext -layout, kept in cache/) into acts and merge them into corpus.json.
Reads cache/ only; deterministic. Run after parse.py. Usage: python statutes.py [penal civil utc]"""
import hashlib, json, re, sys
from pathlib import Path
here = Path(__file__).parent
BASE = 'https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/'
ACTS = {
 'penal': dict(slug='codigo-penal', short='Código Penal', title='Código Penal de Puerto Rico (Ley 146-2012, según enmendada)', pdf='penal.pdf', txt='penal.txt',
   url=BASE + 'Justicia/146-2012/146-2012.pdf', kind='art', reflow=False, rev='2026-08-05', revtxt='Rev. 05 de agosto de 2026',
   note='Oldest version available: the OGP compilation revised 5 August 2026, with the amendments of Ley 146-2012 (30 July 2012) up to Ley 155 of 31 July 2026. Earlier consolidated texts are not online in an official form.'),
 'civil': dict(slug='codigo-civil', short='Código Civil', title='Código Civil de Puerto Rico de 2020 (Ley 55-2020, según enmendada)', pdf='civil.pdf', txt='civil.txt',
   url=BASE + '55-2020.pdf', kind='art', reflow=False, rev='2026-08-21', revtxt='Rev. 21 de agosto de 2026',
   note='Oldest version available: the OGP compilation revised 21 August 2026, with the amendments of Ley 55-2020 (1 June 2020) up to Ley 191 of 19 August 2026. Earlier consolidated texts are not online in an official form.'),
 'utc': dict(slug='ley-transacciones-comerciales', short='Transacciones Comerciales', title='Ley de Transacciones Comerciales (Ley 208-1995, según enmendada)', pdf='utc.pdf', txt='utc.txt',
   url=BASE + 'Transacciones/208-1995/208-1995.pdf', kind='sec', reflow=True, rev='2025-06-23', revtxt='Rev. 23 de junio de 2025',
   note="Oldest version available: the OGP compilation revised 23 June 2025, with the amendments of Ley 208-1995 (17 August 1995) up to Ley 17 of 16 January 2014. The Ley is the Commonwealth's Uniform Commercial Code statute; it repealed Articles 353 to 548 of the Código de Comercio de 1932."),
}
FOOT = re.compile(r'^\s*Rev\. .*www\.ogp\.pr\.gov.*Página \d+ de \d+\s*$')
HEAD = re.compile(r'^\s*[“"](Código Penal de Puerto Rico|Código Civil de Puerto Rico|Ley de Transacciones Comerciales)[”"].*\]\s*$')
HDG = re.compile(r'^(LIBRO|TÍTULO|TITULO|CAPÍTULO|CAPITULO|SUBCAPÍTULO|SUBCAPITULO|SUBPARTE|SECCIÓN|SUBSECCIÓN|PARTE|DISPOSICIONES|ÍNDICE)\b')
ARTRE = re.compile(r'^\[?Artículo (\d+)([A-Z]?)\.\s*—\s*(.*)$', re.S)
SECRE = re.compile(r'^Sección (\d+) ?- ?(\d+)(?:\.(\d+))?\.?\s*—\s*(.*)$', re.S)
def norm(s):
    s = s.replace('\xa0', ' ').replace('’', "'").replace('‘', "'").replace('​', '')
    return re.sub(r'[ \t]+', ' ', s).strip()
def parse(name):
    a = ACTS[name]; raw = (here / 'cache' / a['txt']).read_text(encoding='utf8')
    lines = raw.replace('\f', '\n').split('\n')
    end = next(i for i in range(len(lines) - 1, -1, -1) if lines[i].strip() == 'TABLA DE CONTENIDO')
    lines = lines[:end]
    blocks, cur = [], []
    pb = False
    for l in lines:
        if FOOT.match(l) or HEAD.match(l):
            if cur: blocks.append((' '.join(cur), pb)); cur = []; pb = False
            pb = True; continue
        n = norm(l)
        if n and cur and (ARTRE.match(n) or SECRE.match(n) or (HDG.match(n) and '—' in n[:60]) or re.match(r'^\((?:[a-z]{1,2}(?:\.\d)?|\d{1,2})\) ', n)):
            blocks.append((' '.join(cur), pb)); cur = []; pb = False
        if not n:
            if cur: blocks.append((' '.join(cur), pb)); cur = []; pb = False
            continue
        cur.append(n)
    if cur: blocks.append((' '.join(cur), pb))
    clean = []
    for t, pbk in blocks:
        clean.append((t, pbk))
    blocks = clean
    paras = []
    for t, pbk in blocks:
        start = bool(ARTRE.match(t) or SECRE.match(t) or HDG.match(t) or re.match(r'^\(?[0-9a-z]{1,3}[.)]|^\([^)]{1,6}\)', t))
        if paras and not start and not (ARTRE.match(paras[-1]) or SECRE.match(paras[-1])) and (pbk or a['reflow']) and (t[0].islower() or paras[-1][-1] not in '.;:”"'):
            paras[-1] += ' ' + t; continue
        paras.append(t)
    paras = [q for q in (re.sub(r'\s*\[(Nota|Enmiendas)[^\]]*\]', '', q).strip() for q in paras) if q]
    units = {}
    key = None
    skipping = False
    for p in paras:
        m = ARTRE.match(p) if a['kind'] == 'art' else SECRE.match(p)
        if m:
            if a['kind'] == 'art':
                n, suf, title = int(m.group(1)), m.group(2).lower(), m.group(3)
                k = 'art-%04d%s' % (n, '-' + suf if suf else ''); lab = 'Art. %d%s' % (n, suf.upper())
            else:
                c, n, title = int(m.group(1)), int(m.group(2)), m.group(4)
                dec = m.group(3)
                k = 'sec-%02d-%03d%s' % (c, n, '-' + dec if dec else ''); lab = 'Sec. %d-%d%s' % (c, n, '.' + dec if dec else '')
            rest = None
            mm = re.search(r'\s*\(\d+ L\.P\.R\.A\.[^)]*\)', title)
            if mm:
                rest = title[mm.end():].strip().lstrip(']').strip() or None
                title = title[:mm.start()].strip()
            title = re.sub(r'\s*\[(Nota|Enmiendas)[^\]]*\]?', '', title).strip()
            if p.startswith('['): title = title.rstrip(']').strip()
            if ' — ' in title:
                title, r2 = title.split(' — ', 1); rest = (r2 + ' ' + (rest or '')).strip()
            while k in units: k += 'x'
            units[k] = {'label': lab, 'kind': a['kind'], 'lines': ['# %s. %s' % (lab.replace('Art.', 'Artículo').replace('Sec.', 'Sección'), title)]}
            if rest:
                rest = re.sub(r'\[(Nota|Enmiendas)[^\]]*\]', '', rest).strip()
                m2 = re.search(r'\[(Nota|Enmiendas)', rest)
                if m2:
                    skipping = ']' not in rest[m2.start():]; rest = rest[:m2.start()].strip()
                if rest: units[k]['lines'].append(rest)
            key = k; continue
        if key is None: continue
        if skipping:
            if ']' in p: skipping = False
            continue
        if re.match(r'^\[(Nota|Enmiendas)', p):
            skipping = ']' not in p; continue
        if re.match(r'^\(\d+ L\.P\.R\.A\.[^)]*\)$', p): continue
        if re.match(r'^\[(Enmiendas|Nota|Ley)\b', p) and p.endswith(']'): continue
        if HDG.match(p) and ('—' in p[:60] or p.isupper()): continue
        units[key]['lines'].append(p)
    NOTE = re.compile(r'\[(Nota|Enmiendas)\b')
    for k, u in units.items():
        out, skip = [], False
        for l in u.pop('lines'):
            if skip:
                skip = ']' not in l
                continue
            if NOTE.search(l):
                l2 = re.sub(r'\s*\[(Nota|Enmiendas)\b[^\]]*\]', '', l)
                m3 = NOTE.search(l2)
                if m3:
                    skip = True; l2 = l2[:m3.start()]
                l2 = l2.strip()
                if l.startswith('# '):
                    out.append(l2)
                elif l2 and not re.fullmatch(r'\([a-z0-9.]{1,6}\)', l2):
                    out.append(l2)
                continue
            if re.fullmatch(r'\(\d+ L\.P\.R\.A\.[^)]*\)', l):
                continue
            out.append(l)
        u['text'] = '\n'.join(out) + '\n'
    return a, units
def main(names):
    cp = here / 'corpus.json'; c = json.loads(cp.read_text(encoding='utf8'))
    for name in names:
        a, units = parse(name)
        sha = hashlib.sha256((here / 'cache' / a['pdf']).read_bytes()).hexdigest()
        act = {'slug': a['slug'], 'short': a['short'], 'title': a['title'], 'url': a['url'], 'first_law': None, 'earlier_laws': [],
               'versions': [{'from': a['rev'], 'source_url': a['url'], 'sha256': sha, 'units': units, 'credits': {}, 'note': a['note']}]}
        c['acts'] = [x for x in c['acts'] if x['slug'] != a['slug']] + [act]
        src = {'name': 'OGP Biblioteca Virtual: ' + a['title'], 'url': a['url'], 'retrieved': '2026-10-30', 'licence': 'none stated', 'notes': 'Single PDF with a text layer, %s. The OGP states that the compilation is not official and may contain inadvertent errors.' % a['revtxt']}
        c['sources'] = [s for s in c['sources'] if s['url'] != a['url']] + [src]
        d = 'One version only for %s: the OGP compilation dated by its own revision date (%s); history before that is not reconstructed. Chapter and title headings and the OGP amendment notes in brackets are left out; only the articles are kept.' % (a['slug'], a['rev'])
        c['decisions'] = [x for x in c['decisions'] if not x.startswith('One version only for %s:' % a['slug'])] + [d]
        print(name, len(units), 'units')
    cp.write_text(json.dumps(c, ensure_ascii=False, indent=1) + '\n', encoding='utf8', newline='\n')
if __name__ == '__main__':
    main(sys.argv[1:] or list(ACTS))
