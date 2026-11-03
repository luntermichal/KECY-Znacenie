import re, html, json, pathlib, urllib.parse
import xml.etree.ElementTree as ET

ROOT = pathlib.Path('.')
E = html.escape
def url(p):
    return '/'.join(urllib.parse.quote(s) for s in pathlib.PurePosixPath(p).parts)
def thumb(p):
    return 'prehlad-img/' + url(p.replace('/', '__').replace(' ', '_')[:-4] + '.png')
def flink(p, label=None):
    return f'<a href="{url(p)}" target="_blank">{E(label or p)}</a>'

ZN = {1: ('zelená', '#3cc954'), 2: ('žltá', '#f5c400'), 3: ('červená', '#e8505b'), 4: ('modrá', '#3b8fd9')}
def ztags(zs):
    return ''.join(f'<span class="zt z{z}">Z{z}</span>' for z in zs)

# ---------- trails ----------
TR = [
 ('DržHubu', 1, 'drzhubu', 'drzhubu.pdf', '1120 m', 'medium', '#2e7d32'),
 ('Lesmír', 1, 'lesmir', 'lesmir.pdf', '1550 m', 'difficult', '#9ccc65'),
 ('Zlatokopka', 1, 'zlatokopka', 'zlatokopka.pdf', '1400 m', 'difficult', '#66bb6a'),
 ('Bufet', 1, 'bufet', 'bufet.pdf', '650 m', 'výšľap', '#e53935'),
 ('Cez prameň invalidov', 1, 'pramen', 'invalid.pdf', '3400 m', 'výšľap (zóna 1 a 2)', '#c2185b'),
 ('SuRAWy', 2, 'surawy', 'surawy.pdf', '750 m', 'difficult', '#555555'),
 ('Davidoff', 2, 'davidoff', 'Davidoff.pdf', '1460 m', 'difficult', '#ffa000'),
 ('Hupiky', 2, 'hupiky', 'hupiky.pdf', '1700 m', 'medium', '#a1662f'),
 ('Kamenný', 2, 'kamenny', 'kamenny.pdf', '0 m (!)', 'medium / difficult (?)', '#ef6c00'),
 ('Bedľa', 2, 'bedla', 'bedla.pdf', '2630 m', 'difficult', '#fdd835'),
 ('Jahoda', 3, 'jahoda', 'jahoda.pdf', '2630 m', 'medium', '#e53935'),
 ('Michalkov', 3, 'michalkov', 'michalkov.pdf', '3690 m', 'medium', '#7b1e3a'),
 ('Mravenisko', 4, 'mravenisko', 'mravenisko.pdf', '400 m', 'easy', '#26c6da'),
 ('Natural', 4, 'natural', 'natural.pdf', '1400 m', 'medium', '#1a237e'),
 ('Flow trail', 4, 'flow', 'flowtrail.pdf', '2100 m', 'medium', '#1e88e5'),
 ('Hriešny', 4, 'hriesny', 'hriesny.pdf', '4900 m', 'medium (značka) / výšľap (mapa)', '#5c9ded'),
]
ISS = {
 'DržHubu': ['Na štartovej značke je „Medium“ s veľkým M, ostatné majú malé písmená.', 'Štart na mape je ťažko nájsť (Peťo D.).', 'Dokresliť prepojku na Bankov (Veronika).'],
 'Lesmír': ['Na značke je len „Difficult“ po anglicky (Peťo D.).', 'Dvojitá tabuľa na ČB nefunguje: ponechať smerovanie Lesmír → ČB, alebo smerovať na Huberta? (Rišo)'],
 'Zlatokopka': ['V PDF značkách je názov už správne „Zlatokopka“. Preklep „Zlatoklopka“ na mape treba overiť.', 'Križuje starší lokálny chodník, treba na to upozorniť (Rišo).', 'Lavica na konci: označiť lavicu aj bezpečnú obchádzku (Rišo).', 'Infotabuľa o prechode Zlatokopka ↔ DržHubu (Rišo).'],
 'Bufet': ['Obojsmerný, alebo len výšľap? (Veronika)'],
 'Cez prameň invalidov': ['Prechod medzi zónami je na mape rozpoznaný len približne.'],
 'SuRAWy': ['Na mape chýba „ý“ (Peťo D.).'],
 'Davidoff': ['Chce 2 nástupy (Veronika).', 'Začiatok flowtrailu dať ako ľahký? (Veronika)', 'Doplniť časť Natural pod cestou (PaloG).'],
 'Hupiky': ['Opraviť štart (vedľa LC Flowy alebo od aktuálnej smerovej tabule) (Tomáš).'],
 'Kamenný': ['Štartová značka uvádza dĺžku 0 m, treba doplniť skutočnú dĺžku.', 'Značka uvádza medium, legenda mapy difficult: treba rozhodnúť.', 'Dokresliť prepojku na červenú magistrálu (Veronika).', 'Posunúť zóny, aby bol celý v zóne 2 (PaloG).'],
 'Bedľa': ['Rovnaká dĺžka ako Jahoda (2630 m): overiť.', 'Chce 2 nástupy (Veronika).', 'Prepojenie z konca na Bankov cez lúky, žltá cyklotrasa Sedlo → Jahodná (Veronika, DK).'],
 'Jahoda': ['Rovnaká dĺžka ako Bedľa (2630 m): overiť.', 'Na mape označiť ako obojsmerný trail, doplniť nadmorské výšky (Gabi M.).'],
 'Michalkov': ['Označiť ako obojsmerný, doplniť nadmorské výšky, prípadne zakresliť od Psieho cintorína (Gabi M.).', 'Infotabuľa pri Psom cintoríne: je tam ešte? (Rišo)'],
 'Mravenisko': [],
 'Natural': [],
 'Flow trail': ['Súbor štartu je flowtrail.pdf, smerovníky sú „flow“.'],
 'Hriešny': ['Na štartovej značke je medium, na mape bodkovaný výšľap: treba zjednotiť.', 'Tabule začiatku sú zmätočné (celkový Hriešny + Mravenisko + Natural + Flow), pre výšľap tabuľa nie je (Veronika).', 'Výšlap na Hrešnú: už sa nedá ísť na vrch lúky, treba ísť okolo pozemku (Tomáš).'],
}
ALIAS = {'Flow': 'Flow trail', 'Hriešny Flow': 'Flow trail', 'Hriešny Natural': 'Natural', 'Hriešny Mravenisko': 'Mravenisko',
         'Hriešny Výšlap': 'Hriešny', 'Prameň invalidov': 'Cez prameň invalidov', 'Hriešny Výšlap/Flow': 'Hriešny'}
TNAMES = {t[0] for t in TR}

# ---------- GPS ----------
ns = '{http://www.opengis.net/kml/2.2}'
kml = ET.parse('gps/nortysp-ke.cy-zona-2.kml')
pts = []
for zf in kml.getroot().iter(ns + 'Folder'):
    if zf.find(ns + 'Folder') is None: continue
    z = int(re.search(r'Zóna (\d)', zf.findtext(ns + 'name')).group(1))
    for sf in zf.findall(ns + 'Folder'):
        cat = re.sub(r'^\d+ | \(\d+\)$', '', sf.findtext(ns + 'name'))
        for p in sf.findall(ns + 'Placemark'):
            d = p.findtext(ns + 'description') or ''
            obs = re.search(r'Obsah:\n(.*?)\n(?:Poznámka|⚠|GPS)', d, re.S)
            items = [x.strip(' •') for x in obs.group(1).splitlines()] if obs else []
            g = lambda k: (re.search(k + r': (.*)', d) or [None, ''])[1]
            pts.append(dict(n=len(pts) + 1, z=z, cat=cat, name=p.findtext(ns + 'name') or '', items=items,
                            note=g('Poznámka'), warn='⚠' in d, gps=g('GPS'), orig=g('Pôvodný názov')))
cnt = {t: {'start': 0, 'L': 0, 'P': 0, 'F': 0, 'K': 0, 'pts': []} for t in TNAMES}
other = {}
tot = {z: {'MC': 0, 'MZ': 0, 'PRE': 0, 'KRI': 0, 'PROT': 0, 'ZAK': 0, 'VYS': 0, 'nedopl': 0} for z in ZN}
for p in pts:
    for it in p['items']:
        m = re.match(r'(Začiatok trailu|Tabuľa trailu|Smerovník (vľavo|vpravo|vpred)|Koniec trailu): (.+)', it)
        if m:
            t = ALIAS.get(m.group(3), m.group(3))
            if t not in cnt:
                other.setdefault(t, []).append(p['n']); continue
            k = {'vľavo': 'L', 'vpravo': 'P', 'vpred': 'F'}.get(m.group(2)) or ('K' if m.group(1).startswith('Koniec') else 'start')
            cnt[t][k] += 1
            if p['n'] not in cnt[t]['pts']: cnt[t]['pts'].append(p['n'])
        tz = tot[p['z']]
        if it.startswith('Mapa celku'): tz['MC'] += 1
        if it.startswith('Mapa zóny'): tz['MZ'] += 1
        if it.startswith('Prechod'): tz['PRE'] += 1
        if it.startswith('Križovanie'): tz['KRI'] += 1
        if it == 'Protismer': tz['PROT'] += 1
        if it.startswith('Zákaz'): tz['ZAK'] += 1
        if it.startswith('Upozornenie'): tz['VYS'] += 1
        if 'nedoplnený' in it: tz['nedopl'] += 1
nwarn = sum(p['warn'] for p in pts)

# ---------- markdown ----------
def inline(s):
    s = s.replace('\\*', '&#42;').replace('\\-', '-').replace('\\\\', '\\')
    keep = []
    s = re.sub(r'</?mark>', lambda m: keep.append(m.group(0)) or f'\x00{len(keep)-1}\x00', s)
    s = E(s, quote=False)
    s = re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)\*(?!\w)', r'<i>\1</i>', s)
    s = re.sub(r'(https?://[^\s<]+)', r'<a href="\1" target="_blank">\1</a>', s)
    return s
def md(text):
    out, lines, i = [], text.splitlines(), 0
    para = []
    def flush():
        if para: out.append('<p>' + inline(' '.join(para)) + '</p>'); para.clear()
    while i < len(lines):
        l = lines[i]
        if l.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i + 1]):
            flush(); rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            h = ''.join(f'<th>{inline(c)}</th>' for c in rows[0])
            b = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows[2:])
            out.append(f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'); continue
        m = re.match(r'^(#{1,6})\s+(.*)', l)
        if m:
            flush(); lv = min(len(m.group(1)) + 2, 6); out.append(f'<h{lv}>{inline(m.group(2))}</h{lv}>')
        elif re.match(r'^\s*[-*]\s+', l) or re.match(r'^\s*\d+\.\s+', l):
            flush(); items = []
            while i < len(lines) and (re.match(r'^\s*([-*]|\d+\.)\s+', lines[i]) or (lines[i].startswith('  ') and lines[i].strip() and items)):
                if re.match(r'^\s*([-*]|\d+\.)\s+', lines[i]):
                    ind = len(lines[i]) - len(lines[i].lstrip())
                    t = re.sub(r'^\s*([-*]|\d+\.)\s+', '', lines[i])
                    t = re.sub(r'^\[ \]', '☐', re.sub(r'^\[x\]', '☑', t))
                    items.append(f'<li class="i{min(ind // 2, 3)}">{inline(t)}</li>')
                else:
                    items[-1] = items[-1][:-5] + ' ' + inline(lines[i].strip()) + '</li>'
                i += 1
            out.append('<ul>' + ''.join(items) + '</ul>'); continue
        elif re.match(r'^-{3,}$|^\*{3,}$', l.strip()):
            flush(); out.append('<hr>')
        elif not l.strip():
            flush()
        else:
            para.append(l.strip())
        i += 1
    flush()
    return '\n'.join(out)

MD = [
 ('ke.cy znacenie-facebook message.md', 'Pripnuté správy a komunikácia (postup prieskumu, kódy, Zoran 22. 10. 2025)'),
 ('mesenger-vystupy/Upravy mapy.md', 'Pôvodný zber pripomienok k mape'),
 ('mesenger-vystupy/prehlad-pripomienok-po-osobach.md', 'Pripomienky zoradené po osobách + opakujúce sa témy'),
 ('KECY mapy/ke.cy-mapy.md', 'Popis máp, zón a trailov'),
 ('KECY znacky/start trailu/nazvy-trailov.md', 'Názvy, dĺžky a obtiažnosť trailov'),
 ('gps/nortysp-ke.cy-zona-2-sumar.md', 'Súhrn GPS bodov (99) podľa zón'),
 ('mail/FNPCR.md', 'Mail: financovanie z výzvy FNPCR'),
 ('informacie-o-suboroch.md', 'Prehľad súborov a účastníkov'),
]

# ---------- tasks ----------
# (id, skupina, text, zóny, kto, zdroj)
TASKS = [
 ('t01', 'Mapa a legenda', 'Pridať Rypak a Diviak (už legálne) do mapy, legendy a značenia. Zistiť dĺžku, obtiažnosť a typ.', [1, 2], '', 'KECY mapy/ke.cy-mapy.md'),
 ('t02', 'Mapa a legenda', 'Zistiť, či je Johanka legálna.', [2], '', 'KECY mapy/ke.cy-mapy.md'),
 ('t03', 'Mapa a legenda', 'Rozhodnúť, ako zobraziť nelegálne Lentil core flowy, Veveričku a Miňonku.', [2, 3], '', 'KECY mapy/ke.cy-mapy.md'),
 ('t04', 'Mapa a legenda', 'Legenda: „ilegal“ zmeniť na „ostatné“ a presunúť pod „nachádzaš sa tu“.', [], 'PaloG, Tomáš', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t05', 'Mapa a legenda', 'Rozlíšiť čiary obtiažnosti (ľahký a stredný sú obaja plnou čiarou).', [], 'Veronika', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t06', 'Mapa a legenda', 'Zjednotiť obtiažnosť SK/EN (ťažký / difficult) na mape aj značkách.', [], 'Peťo D.', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t07', 'Mapa a legenda', 'Doplniť popisy Jahodná, Alpinka, Bankov, Ovečka.', [], 'úvod, Veronika, Tomáš', 'mesenger-vystupy/Upravy mapy.md'),
 ('t08', 'Mapa a legenda', 'Doplniť piktogramy parkovísk (P) a prameňov (zóna 1: vodojem pod parkoviskom, studnička pod kaplnkou).', [1], 'Gabi M., Peťo D., Veronika, Rišo', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t09', 'Mapa a legenda', 'Odstrániť Girbeš bistro (zaniklo).', [2], 'DK', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t10', 'Mapa a legenda', 'Posunúť hranice zón: celý Kamenný (aj Diviak/Rypak) v zóne 2, celá Miňonka v zóne 3.', [2, 3], 'PaloG', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t11', 'Mapa a legenda', 'Doplniť Huberta a Prepadák (prípadne SuRAWy 3, 4, 5 sivou).', [], 'PaloG, Tomáš', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t12', 'Mapa a legenda', 'Dokresliť prepojenia: Bedľa → Bankov, Kamenný → červená magistrála, DržHubu → Bankov, žltá cyklotrasa Sedlo → Jahodná, Čermeľská dolina → Hrešná, Veverička → Michalkov, Miňonka → Veverička.', [1, 2, 3, 4], 'Veronika, PaloG, Gabi M., DK', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t13', 'Mapa a legenda', 'Jahoda a Michalkov ako obojsmerné, nadmorské výšky aj pri Miňonke a Veveričke.', [3], 'Gabi M.', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t14', 'Mapa a legenda', 'Opraviť štart Hupikov a výšlap na Hrešnú.', [2, 4], 'Tomáš', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t15', 'Mapa a legenda', 'Značka „nachádzaš sa tu“: ako ju urobiť trvácnu, iná farba.', [], 'PaloG', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t16', 'Mapa a legenda', 'Nefunkčný QR kód. Miesto pre QR na stiahnutie mapy, logá partnerov a reklamu podnikov.', [], 'Veronika, Tomáš', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t17', 'Mapa a legenda', 'Overiť preklep „Zlatoklopka“ na mape (v PDF značkách je už „Zlatokopka“) a „SuRAWý“.', [1, 2], 'Peťo D., Veronika', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t20', 'Značky', 'Štartové značky: preklep „LENGHT“ → „LENGTH“ na všetkých 16 tabuliach.', [], 'zistené z PDF', 'KECY znacky/start trailu/bedla.pdf'),
 ('t21', 'Značky', 'Kamenný: doplniť dĺžku (je 0 m) a rozhodnúť obtiažnosť (medium vs difficult).', [2], '', 'KECY znacky/start trailu/nazvy-trailov.md'),
 ('t22', 'Značky', 'Overiť dĺžku Bedle a Jahody (obe 2630 m).', [2, 3], '', 'KECY znacky/start trailu/nazvy-trailov.md'),
 ('t23', 'Značky', 'Hriešny: zjednotiť obtiažnosť (značka medium, mapa výšľap) a rozhodnúť delenie štartových tabúľ.', [4], 'Veronika', 'KECY znacky/start trailu/hriesny.pdf'),
 ('t24', 'Značky', 'Vyrobiť výstražné tabule pred náročnými úsekmi (zatiaľ neexistujú) a vybrať úseky.', [], 'Zoran, PaloG, Tomáš', 'ke.cy znacenie-facebook message.md'),
 ('t25', 'Značky', 'Všeobecná smerovka „návrat na traily“ za koncom trailu.', [], 'Zoran', 'ke.cy znacenie-facebook message.md'),
 ('t26', 'Značky', 'Rozhodnúť o 2 nástupoch na Bedľu a Davidoff a či je Bufet obojsmerný.', [1, 2], 'Veronika', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t27', 'Značky', 'Rozhodnúť o značke zákazu pre peších (hlavne zóna 1).', [1], 'Peťo D.', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t30', 'Terén a GPS', f'Rozhodnúť {nwarn} GPS bodov s ⚠ (otáznik alebo alternatíva v pôvodnom popise).', [1, 2, 3, 4], '', 'gps/nortysp-ke.cy-zona-2-sumar.md'),
 ('t31', 'Terén a GPS', f'Zóna 3: doplniť trail pri smerovníkoch bez trailu ({sum(t["nedopl"] for t in tot.values())}×).', [3], '', 'gps/nortysp-ke.cy-zona-2-sumar.md'),
 ('t32', 'Terén a GPS', 'Odfotiť miesta osadenia (viditeľnosť, pravá strana, nezavadzať ťažbe).', [1, 2, 3, 4], 'Zoran', 'ke.cy znacenie-facebook message.md'),
 ('t33', 'Terén a GPS', 'Mapa celku na Hornom Bankove: za rampou na konci čipu lesa (pretlak tabúľ pri parkovisku).', [1], 'Rišo', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t34', 'Terén a GPS', 'Zlatokopka: upozorniť na križovanie chodníka, lavica + obchádzka, prechod na DržHubu.', [1], 'Rišo', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t35', 'Terén a GPS', 'Overiť infotabuľu pri Psom cintoríne (smer Michalkov).', [3], 'Rišo', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('t40', 'Financie', 'Cenová ponuka výroby a osadenia podľa počtu tabúľ (sekcia Počty tabúľ).', [], 'Zoran', 'ke.cy znacenie-facebook message.md'),
 ('t41', 'Financie', 'Zvážiť výzvu FNPCR (do 500 000 €, 90 %, značenie a mapové tabule sú oprávnené).', [], '', 'mail/FNPCR.md'),
]
DONE = [
 ('Mapa celku a mapy 4 zón (PDF + PNG)', 'KECY mapy/kecy celok.pdf'),
 ('Štartové tabule pre všetkých 16 trailov', 'KECY znacky/start trailu/bedla.pdf'),
 ('Smerovníky vľavo, vpravo a vpred pre 16 trailov (48 PDF)', 'KECY znacky/Smerovniky/smerovníky vlavo/L bedla.pdf'),
 ('Tabule Koniec trailu, Protismer a Prechod medzi zónami', 'KECY znacky/koniec.pdf'),
 ('Preklep Zlatokopka je v PDF značkách opravený', 'KECY znacky/start trailu/zlatokopka.pdf'),
 (f'GPS: {len(pts)} navrhovaných miest značenia v zónach 1–4, zoradených do priečinkov', 'gps/nortysp-ke.cy-zona-2.kml'),
 ('Pripomienky k mape od 7 členov, zoradené po osobách', 'mesenger-vystupy/prehlad-pripomienok-po-osobach.md'),
 ('Princíp zón a farieb, kódy značenia (MC, MZ, T, SĽ, SP, SR, K, KP, !)', 'ke.cy znacenie-facebook message.md'),
]

# ---------- build ----------
def card_img(p, cap):
    return (f'<figure class="sg{" tall" if "start trailu" in p else ""}"><a href="{url(p)}" target="_blank" data-img="{thumb(p)}">'
            f'<img loading="lazy" src="{thumb(p)}" alt="{E(cap)}"></a><figcaption>{E(cap)}</figcaption></figure>')

S = []  # sections: (id, title, html)

# overview
nopen = len(TASKS)
signs_needed = sum(c['start'] + c['L'] + c['P'] + c['F'] + c['K'] for c in cnt.values())
S.append(('stav', 'Stav projektu', f'''
<div class="stats">
 <div class="st"><b>{len(DONE)}</b><span>hotové / jasné</span></div>
 <div class="st"><b id="openN">{nopen}</b><span>otvorené úlohy</span></div>
 <div class="st"><b>{len(pts)}</b><span>GPS bodov</span></div>
 <div class="st warn"><b>{nwarn}</b><span>bodov s ⚠</span></div>
 <div class="st"><b>{signs_needed}</b><span>trailových tabúľ podľa GPS</span></div>
</div>
<h3>Hotové / jasné</h3>
<ul class="done">{''.join(f'<li>✔ {E(t)} <small>{flink(s, "→ súbor")}</small></li>' for t, s in DONE)}</ul>'''))

# tasks
groups = {}
for t in TASKS: groups.setdefault(t[1], []).append(t)
th = '<div class="bar"><label><input type="checkbox" id="hideDone"> skryť odškrtnuté</label> <button id="resetT">zrušiť odškrtnutia</button></div>'
for g, ts in groups.items():
    th += f'<h3>{E(g)}</h3><ul class="tasks">'
    for tid, _, txt, zs, who, src in ts:
        th += (f'<li class="task f" data-z="{" ".join(map(str, zs)) or "all"}" data-id="{tid}"><label><input type="checkbox"> '
               f'<span>{E(txt)}</span></label> {ztags(zs)} <small>{E(who)} · {flink(src, "zdroj")}</small></li>')
    th += '</ul>'
S.append(('ulohy', 'Čo treba dorobiť', th))

# trails
th = '<p class="hint">Ku každému trailu sú zobrazené jeho tabule a počet tabúľ potrebných podľa GPS bodov. Klik na obrázok ho zväčší, odkaz otvorí PDF.</p>'
for z in ZN:
    th += f'<h3 class="f" data-z="{z}"><span class="zt z{z}">Zóna {z}</span> {ZN[z][0]}</h3><div class="trails f" data-z="{z}">'
    for name, tz, slug, sf, ln, df, col in [t for t in TR if t[1] == z]:
        c = cnt[name]
        imgs = card_img(f'KECY znacky/start trailu/{sf}', 'štart') + \
               card_img(f'KECY znacky/Smerovniky/smerovníky vlavo/L {slug}.pdf', 'vľavo') + \
               card_img(f'KECY znacky/Smerovniky/smerovniky vpravo/P {slug}.pdf', 'vpravo') + \
               card_img(f'KECY znacky/Smerovniky/smerovniky vpred/F {slug}.pdf', 'vpred')
        iss = ''.join(f'<li>{E(x)}</li>' for x in ISS.get(name, []))
        plinks = ' '.join(f'<a href="#p{n}" class="pl">#{n}</a>' for n in c['pts'])
        th += f'''<details class="trail" id="tr-{slug}" open><summary><i class="sw" style="background:{col}"></i><b>{E(name)}</b>
 <span class="meta">{E(ln)} · {E(df)}</span>{' <span class="badge">' + str(len(ISS.get(name, []))) + ' na riešenie</span>' if iss else ''}</summary>
 <div class="imgs">{imgs}</div>
 <table class="mini"><tr><th>Štart</th><th>SĽ</th><th>SP</th><th>SV</th><th>Koniec</th></tr>
 <tr><td>{c["start"]}</td><td>{c["L"]}</td><td>{c["P"]}</td><td>{c["F"]}</td><td>{c["K"]}</td></tr></table>
 <div class="pts">GPS body: {plinks or '<i>žiadne</i>'}</div>
 {'<ul class="iss">' + iss + '</ul>' if iss else '<p class="ok">Bez otvorených pripomienok.</p>'}</details>'''
    th += '</div>'
if other:
    th += '<h3>Ciele bez vlastnej tabule (v GPS sa na ne smeruje)</h3><ul>' + ''.join(
        f'<li><b>{E(k)}</b>: ' + ' '.join(f'<a href="#p{n}">#{n}</a>' for n in v) + '</li>' for k, v in other.items()) + '</ul>'
S.append(('traily', 'Traily a ich tabule', th))

# counts
rows = ''
for z in ZN:
    zt = [t[0] for t in TR if t[1] == z]
    s = lambda k: sum(cnt[t][k] for t in zt)
    o = tot[z]
    rows += (f'<tr class="f" data-z="{z}"><td><span class="zt z{z}">Z{z}</span></td><td>{o["MC"]}</td><td>{o["MZ"]}</td><td>{s("start")}</td><td>{s("L")}</td>'
             f'<td>{s("P")}</td><td>{s("F")}</td><td>{s("K")}</td><td>{o["PROT"]}</td><td>{o["PRE"]}</td><td>{o["KRI"]}</td><td>{o["ZAK"]}</td><td>{o["VYS"]}</td></tr>')
S.append(('pocty', 'Počty tabúľ (podklad pre cenovú ponuku)', f'''
<p class="hint">Spočítané z obsahu GPS bodov v <code>gps/nortysp-ke.cy-zona-2.kml</code>. Trailové tabule sú priradené k zóne trailu, ostatné k zóne bodu. Body s ⚠ ešte nie sú rozhodnuté, preto sú to len orientačné počty.</p>
<div class="tw"><table><thead><tr><th>Zóna</th><th>Mapa celku</th><th>Mapa zóny</th><th>Štart</th><th>SĽ</th><th>SP</th><th>SV</th><th>Koniec</th><th>Protismer</th><th>Prechod zón</th><th>Križovanie</th><th>Zákaz</th><th>Výstraha</th></tr></thead>
<tbody>{rows}</tbody></table></div>'''))

# maps
mp = ['kecy celok', 'zona 1', 'zona 2', 'zona 3', 'zona 4']
th = '<div class="maps">' + ''.join(
    f'<figure class="map f" data-z="{m[-1] if m[-1].isdigit() else "all"}"><a href="{url("KECY mapy/PNG/" + m + ".png")}" data-img="{url("KECY mapy/PNG/" + m + ".png")}">'
    f'<img loading="lazy" src="{thumb("KECY mapy/" + m + ".pdf")}"></a><figcaption>{E(m)} · {flink("KECY mapy/" + m + ".pdf", "PDF")} · {flink("KECY mapy/PNG/" + m + ".png", "PNG")}</figcaption></figure>'
    for m in mp) + '</div>'
S.append(('mapy', 'Mapy', th))

# other signs
th = '<div class="imgs big">' + card_img('KECY znacky/koniec.pdf', 'Koniec trailu (K)') + card_img('KECY znacky/protismer.pdf', 'Protismer (KP)') + \
     card_img('KECY znacky/Smerovniky/Prechod medzi zonami/smerovniky medzi zonami.pdf', 'Prechod medzi zónami') + '</div>'
th += '<details><summary>Všetky smerovníky podľa smeru</summary>'
for d, folder, pre in [('vľavo (SĽ)', 'smerovníky vlavo', 'L'), ('vpravo (SP)', 'smerovniky vpravo', 'P'), ('vpred (SV / SR)', 'smerovniky vpred', 'F')]:
    th += f'<h4>Smerovníky {d}</h4><div class="imgs">' + ''.join(
        card_img(f'KECY znacky/Smerovniky/{folder}/{pre} {t[2]}.pdf', t[0]) for t in TR) + '</div>'
th += '</details>'
S.append(('znacky', 'Ostatné značky a všetky smerovníky', th))

# GPS
cats = sorted({p['cat'] for p in pts})
th = ('<div class="bar"><select id="catF"><option value="">všetky kategórie</option>' + ''.join(f'<option>{E(c)}</option>' for c in cats) +
      '</select> <label><input type="checkbox" id="warnF"> iba ⚠</label></div><div class="tw"><table id="gps"><thead><tr><th>#</th><th>Zóna</th><th>Kategória</th><th>Názov</th><th>Obsah</th><th>Poznámka</th><th>GPS</th></tr></thead><tbody>')
for p in pts:
    ll = p['gps'].replace(' ', '')
    th += (f'<tr id="p{p["n"]}" class="f{" w" if p["warn"] else ""}" data-z="{p["z"]}" data-cat="{E(p["cat"])}"><td>{p["n"]}</td><td><span class="zt z{p["z"]}">Z{p["z"]}</span></td>'
           f'<td>{E(p["cat"])}</td><td>{E(p["name"])}<br><small>pôv.: {E(p["orig"])}</small></td><td>{"<br>".join(E(x) for x in p["items"])}</td>'
           f'<td>{"⚠ " if p["warn"] else ""}{E(p["note"])}</td><td><a href="https://maps.google.com/?q={ll}" target="_blank">{E(p["gps"])}</a></td></tr>')
th += '</tbody></table></div>'
S.append(('gps', f'GPS body ({len(pts)})', th))

# docs
th = '<p class="hint">Obsah projektových .md súborov. Každý sa dá rozbaliť, odkaz otvorí originál.</p>'
for p, desc in MD:
    txt = (ROOT / p).read_text(encoding='utf8')
    th += f'<details class="doc"><summary><b>{E(p)}</b> <span class="meta">{E(desc)}</span> {flink(p, "otvoriť")}</summary><div class="md">{md(txt)}</div></details>'
S.append(('dokumenty', 'Dokumenty (.md)', th))

# files
files = sorted(x.as_posix() for x in ROOT.rglob('*') if x.is_file() and not x.as_posix().startswith(('prehlad-img', '.')) and x.name != 'prehlad.html')
byd = {}
for f in files: byd.setdefault(str(pathlib.PurePosixPath(f).parent), []).append(f)
th = ''.join(f'<details><summary>{E(d)} <span class="meta">({len(v)})</span></summary><ul class="files">' +
             ''.join(f'<li>{flink(f, pathlib.PurePosixPath(f).name)}</li>' for f in v) + '</ul></details>' for d, v in byd.items())
S.append(('subory', f'Všetky súbory ({len(files)})', th))

nav = ''.join(f'<li><label><input type="checkbox" checked data-sec="{i}"></label><a href="#{i}">{E(t)}</a></li>' for i, t, _ in S)
body = ''.join(f'<section id="{i}"><h2>{E(t)}</h2>{h}</section>' for i, t, h in S)
zbtn = '<button data-zf="all" class="on">Všetky</button>' + ''.join(f'<button data-zf="{z}" class="zb z{z}">Z{z} {ZN[z][0]}</button>' for z in ZN)

tpl = pathlib.Path(__file__).with_name('tpl.html').read_text(encoding='utf8')
out = tpl.replace('{{NAV}}', nav).replace('{{BODY}}', body).replace('{{ZBTN}}', zbtn)
(ROOT / 'prehlad.html').write_text(out, encoding='utf8')
print('ok', len(out), len(pts), nwarn, signs_needed, sorted(other))
