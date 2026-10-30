"""Parse OGP compiled statute and rules PDFs (text from `pdftotext -enc UTF-8 -layout`, kept in cache/) into corpus.d parts,
one part per statute. Reads cache/ only; deterministic. Usage: python core_parts.py [name ...]"""
import collections, hashlib, json, re, sys
from pathlib import Path
here = Path(__file__).parent
BASE = 'https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/'
L41 = (' This compilation leaves out the amendments of Ley 41-2022, which the Title III court annulled on 3 March 2023'
       ' (In re: FOMB v. Pierluisi Urrutia), as the OGP states on its first page.')
ACTS = {
 'rpc': dict(part='30-reglas-procedimiento-criminal', slug='reglas-procedimiento-criminal', short='Reglas de Procedimiento Criminal',
   title='Reglas de Procedimiento Criminal de 1963 (según enmendadas)', url=BASE + 'Justicia/RPC/RPC.pdf', word='Regla',
   rev='2026-06-15', revtxt='Rev. 15 de junio de 2026',
   note='Oldest version available: the OGP compilation revised 15 June 2026 of the Rules of Criminal Procedure of 1963 (in force 30 July 1963), as amended by later laws.'),
 'revi': dict(part='31-reglas-evidencia', slug='reglas-evidencia', short='Reglas de Evidencia',
   title='Reglas de Evidencia de Puerto Rico de 2009 (según enmendadas)', url=BASE + 'Justicia/REVI/REVI.pdf', word='REGLA',
   rev='2024-04-15', revtxt='Rev. 15 de abril de 2024',
   note='Oldest version available: the OGP compilation revised 15 April 2024 of the Rules of Evidence adopted by the Supreme Court on 9 February 2009, as amended.'),
 'l80': dict(part='40-ley-80-1976-despidos', slug='ley-80-1976-despidos', short='Ley 80-1976',
   title='Ley sobre Despidos Injustificados (Ley 80 de 30 de mayo de 1976, según enmendada)', url=BASE + 'Trabajo/80-1976/80-1976.pdf', word='Artículo',
   rev='2024-04-15', revtxt='Rev. 15 de abril de 2024',
   note='Oldest version available: the OGP compilation revised 15 April 2024.' + L41),
 'l379': dict(part='41-ley-379-1948-jornada', slug='ley-379-1948-jornada', short='Ley 379-1948',
   title='Ley para Establecer la Jornada de Trabajo en Puerto Rico (Ley 379 de 15 de mayo de 1948, según enmendada)', url=BASE + 'Trabajo/379-1948.pdf', word='Artículo',
   rev='2024-04-15', revtxt='Rev. 15 de abril de 2024',
   note='Oldest version available: the OGP compilation revised 15 April 2024.' + L41),
 'l4': dict(part='42-ley-4-2017-flexibilidad-laboral', slug='ley-4-2017-flexibilidad-laboral', short='Ley 4-2017',
   title='Ley de Transformación y Flexibilidad Laboral (Ley 4-2017, según enmendada)', url=BASE + 'Trabajo/4-2017.pdf', word='Artículo',
   rev='2024-04-15', revtxt='Rev. 15 de abril de 2024',
   note='Oldest version available: the OGP compilation revised 15 April 2024.' + L41),
 'corp': dict(part='50-ley-general-corporaciones', slug='ley-general-corporaciones', short='Ley General de Corporaciones',
   title='Ley General de Corporaciones (Ley 164-2009, según enmendada)', url=BASE + 'Corporaciones%20Privadas/164-2009/164-2009.pdf', word='Artículo',
   rev='2025-07-31', revtxt='Rev. 31 de julio de 2025',
   note='Oldest version available: the OGP compilation revised 31 July 2025 of Ley 164 of 16 December 2009, as amended.'),
}
FOOT = re.compile(r'^\s*Rev\. .*www\.ogp\.pr\.gov.*Página \d+ de \d+\s*$')
HDG = re.compile(r'^(LIBRO|TÍTULO|TITULO|CAPÍTULO|CAPITULO|SUBCAPÍTULO|SUBCAPITULO|SUBPARTE|SECCIÓN|SUBSECCIÓN|PARTE|DISPOSICIONES|ÍNDICE)\b')
NOTE = re.compile(r'\[(Nota|Enmiendas|Renumerad[ao]s?)\b')
ROMAN = re.compile(r'^[IVXLC]+\. — [A-ZÁÉÍÓÚÑÜ ,;.()]+(\[Reglas? [0-9 a-z.-]+\])?$')
CITE = re.compile(r'\s*\(\d+ L\.P\.R\.A\.[^)]*\)')


def strip_notes(q):
    q = re.sub(r'\s*\[(Nota|Enmiendas|Renumerad[ao]s?)[^\]]*\]\s*(?=[.,;:])', '', q)
    return re.sub(r'\s*\[(Nota|Enmiendas|Renumerad[ao]s?)[^\]]*\]', '', q).strip()


def unit_re(word):
    if word.lower() == 'regla':
        return re.compile(r'^\[?(?:Regla|REGLA) (\d+)(?:\.(\d+))?(?:-?([A-Z]))?\.\s+(?:—\s*)?(.*)$', re.S)
    return re.compile(r'^\[?%s (\d+)(?:\.(\d+))?(?:-([A-Z]))?\.\s*—\s*(.*)$' % word, re.S)


def norm(s):
    s = s.replace('\xa0', ' ').replace('’', "'").replace('‘', "'").replace('​', '').replace('--', '—')
    return re.sub(r'[ \t]+', ' ', s).strip()


def source_lines(a):
    raw = (here / 'cache' / (a['name'] + '.txt')).read_text(encoding='utf8')
    lines = raw.replace('\f', '\n').split('\n')
    end = min([i for i in range(len(lines)) if lines[i].strip().upper() == 'TABLA DE CONTENIDO' and i > len(lines) // 2]
              + [i for i in range(len(lines)) if lines[i].strip().startswith('Nota. Este documento fue compilado')] + [len(lines)])
    lines = lines[:end]
    after = collections.Counter()
    for i, l in enumerate(lines):
        if FOOT.match(l):
            j = i + 1
            while j < len(lines) and not lines[j].strip(): j += 1
            if j < len(lines): after[lines[j].strip()] += 1
    head = after.most_common(1)[0][0]
    return lines, head


def parse(name):
    a = dict(ACTS[name], name=name)
    UNIT = unit_re(a['word'])
    lines, head = source_lines(a)
    blocks, cur, pb = [], [], False
    for l in lines:
        if FOOT.match(l) or l.strip() == head:
            if cur: blocks.append((' '.join(cur), pb)); cur = []
            pb = True; continue
        n = norm(l)
        ind = len(l) - len(l.lstrip(' '))
        if n and cur and (UNIT.match(n) or (HDG.match(n) and '—' in n[:60]) or re.match(r'^\((?:[a-z]{1,2}(?:\.\d)?|\d{1,2})\) ', n)
                          or re.match(r'^([A-Z]|\d{1,2})\. [A-ZÁÉÍÓÚÑ“"]', n) or (ind >= 3 and cur[-1][-1] in '.:;' and not n[0].islower())):
            blocks.append((' '.join(cur), pb)); cur = []; pb = False
        if not n:
            if cur: blocks.append((' '.join(cur), pb)); cur = []; pb = False
            continue
        cur.append(n)
    if cur: blocks.append((' '.join(cur), pb))
    paras = []
    for t, pbk in blocks:
        start = bool(UNIT.match(t) or HDG.match(t) or re.match(r'^\(?[0-9a-z]{1,3}[.)]|^\([^)]{1,6}\)', t))
        if paras and not start and not UNIT.match(paras[-1]) and (t[0].islower() or (pbk and paras[-1][-1] not in '.;:”"')):
            paras[-1] += ' ' + t; continue
        paras.append(t)
    paras = [q for q in (strip_notes(q) for q in paras) if q]
    units, key, skipping = {}, None, False
    lab_word = 'Regla' if a['word'].lower() == 'regla' else 'Art.'
    head_word = 'Regla' if a['word'].lower() == 'regla' else 'Artículo'
    for p in paras:
        m = UNIT.match(p)
        if m:
            n, minor, suf, title = int(m.group(1)), m.group(2), (m.group(3) or '').lower(), m.group(4)
            k = 'art-%04d' % n if lab_word == 'Art.' else 'regla-%04d' % n
            num = '%d' % n
            if minor is not None: k += '-' + minor; num += '.' + minor
            if suf: k += '-' + suf; num += '-' + suf.upper()
            lab = '%s %s' % (lab_word, num)
            rest = None
            mm = CITE.search(title)
            if mm:
                rest = title[mm.end():].strip().lstrip(']').strip() or None
                title = title[:mm.start()].strip()
            mo = NOTE.search(title)
            if mo and ']' not in title[mo.start():]:
                skipping = True; title = title[:mo.start()]
            title = re.sub(r'\s*\[(Nota|Enmiendas|Renumerad[ao]s?)[^\]]*\]', '', title).strip()
            if p.startswith('['): title = re.sub(r'\]\.?$', '', title).strip()
            if ' — ' in title:
                title, r2 = title.split(' — ', 1); rest = (r2 + ' ' + (rest or '')).strip()
            elif not mm and len(title) > 80:
                rest, title = title, ''
            title = title.strip().rstrip('—').strip()
            while k in units: k += 'x'
            tt = (' ' + title + ('' if title[-1:] in '.:;)]' else '.')) if title else ''
            units[k] = {'label': lab, 'kind': 'art', 'lines': ['# %s %s.%s' % (head_word, num, tt)]}
            if rest:
                rest = re.sub(r'\[(Nota|Enmiendas|Renumerad[ao]s?)[^\]]*\]', '', rest).strip()
                m2 = NOTE.search(rest)
                if m2:
                    skipping = ']' not in rest[m2.start():]; rest = rest[:m2.start()].strip()
                if rest: units[k]['lines'].append(rest)
            key = k; continue
        if key is None: continue
        if skipping:
            if ']' in p: skipping = False
            continue
        if NOTE.match(p):
            skipping = ']' not in p; continue
        if re.fullmatch(r'\(\d+ L\.P\.R\.A\.[^)]*\)', p): continue
        if re.match(r'^\[(Enmiendas|Nota|Ley)\b', p) and p.endswith(']'): continue
        if HDG.match(p) and ('—' in p[:60] or p.isupper()): continue
        if ROMAN.match(p): continue
        units[key]['lines'].append(p)
    for k, u in units.items():
        out, skip = [], False
        for l in u.pop('lines'):
            if skip:
                skip = ']' not in l; continue
            if NOTE.search(l):
                l2 = re.sub(r'\s*\[(Nota|Enmiendas|Renumerad[ao]s?)\b[^\]]*\]', '', l)
                m3 = NOTE.search(l2)
                if m3: skip = True; l2 = l2[:m3.start()]
                l2 = l2.strip()
                if l.startswith('# ') or (l2 and not re.fullmatch(r'\([a-z0-9.]{1,6}\)', l2)): out.append(l2)
                continue
            if re.fullmatch(r'\(\d+ L\.P\.R\.A\.[^)]*\)', l): continue
            out.append(l)
        u['text'] = '\n'.join(out) + '\n'
    return a, units


def verify(a, units):
    """Every body line must appear verbatim (spacing normalised) in the source text, in order."""
    lines, head = source_lines(a)
    src = ' '.join(norm(l) for l in lines if norm(l) and not FOOT.match(l) and l.strip() != head)
    src = strip_notes(re.sub(r'\s+', ' ', src))
    pos, bad = 0, []
    for k, u in units.items():
        for l in u['text'].splitlines()[1:]:
            i = src.find(l, pos)
            if i < 0:
                i = src.find(l)
                if i < 0: bad.append((k, l[:80])); continue
            pos = i
    return bad


def main(names):
    d = here / 'corpus.d'; d.mkdir(exist_ok=True)
    for name in names:
        a, units = parse(name)
        bad = verify(a, units)
        sha = hashlib.sha256((here / 'cache' / (name + '.pdf')).read_bytes()).hexdigest()
        act = {'slug': a['slug'], 'short': a['short'], 'title': a['title'], 'url': a['url'], 'first_law': None, 'earlier_laws': [],
               'versions': [{'from': a['rev'], 'source_url': a['url'], 'sha256': sha, 'units': units, 'credits': {}, 'note': a['note']}]}
        part = {'acts': [act],
                'sources': [{'name': 'OGP Biblioteca Virtual: ' + a['title'], 'url': a['url'], 'retrieved': '2026-10-30', 'licence': 'none stated',
                             'notes': 'Single PDF with a text layer, %s. The OGP states that the compilation is not official and may contain inadvertent errors.' % a['revtxt']}],
                'decisions': ['One version only for %s: the OGP compilation dated by its own revision date (%s); history before that is not reconstructed. '
                              'Front matter, chapter and title headings and the OGP amendment notes in brackets are left out; only the numbered %s are kept.'
                              % (a['slug'], a['rev'], 'rules' if a['word'].lower() == 'regla' else 'articles')],
                'ai_use': ['none']}
        p = d / (a['part'] + '.json'); t = p.with_suffix('.json.tmp')
        t.write_text(json.dumps(part, ensure_ascii=False, indent=1) + '\n', encoding='utf8', newline='\n')
        t.replace(p)
        print(name, len(units), 'units;', len(bad), 'lines not found in source', bad[:5])


if __name__ == '__main__':
    main(sys.argv[1:] or list(ACTS))
