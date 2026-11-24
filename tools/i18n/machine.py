#!/usr/bin/env python3
"""Wen Loop: the machine language of the gateway.
Six JSON records (one per section) linked in a ring: each record names the
previous and next one, and the last points back to the first. Every fact is a
[subject, predicate, object] triple; every record carries a sha256 of its own
content so a machine can check it. Output: /ai/index.json, /ai/<slug>.json,
/ai/index.html. Run after build.py, before seo.py."""
import json, hashlib, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build

SRC = build.SRC
BASE = 'https://wen-crypto.com/'
ALM = 'https://wen-watt.github.io/'
DATE = os.environ.get('WEN_DATE', '2026-11-24')
MINT = 'WENWENvqqNya429ubCdR81ZmD69brwQaaBYY6p3LCpk'
FMT = 'wen-loop/1'
LANGS = [l for l in build.LANGS if os.path.exists(f'{build.W}/tr/{l[0]}.txt')]

W = 'wen:WEN'
SECTIONS = [
  ('home', '', [
    [W, 'is_a', 'community token on Solana'],
    [W, 'mint', MINT],
    [W, 'supply_origin', 'poem "A Love Letter to Wen Bros" by Meow, co-founder of Jupiter'],
    [W, 'supply_total', 1000000000000],
    [W, 'grew_into', 'wen:WNS'],
    ['wen:gateway', 'principle', 'history and usefulness; no prices, no forecasts, no exchange links'],
    ['wen:gateway', 'official_site_is_not', 'wen-crypto.com'],
    ['wen:gateway', 'official_site', 'https://wenwencoin.com/'],
  ]),
  ('what-wen-is', 'about-wen-token-wen-coin-crypto/', [
    [W, 'first_of', 'community coin built on a fractionalized NFT'],
    [W, 'launch_date', '2024-01-26'],
    [W, 'launch_venue', 'Jupiter LFG Launchpad (first token)'],
    [W, 'airdrop_wallets_min', 1000000],
    [W, 'claim_closed', '2024-01-29'],
    [W, 'burned_unclaimed_min', 271000000000],
    [W, 'burned_share_min', 0.27],
    [W, 'identity_rule', 'compare the mint address, not the name or ticker'],
    ['wen:word', 'means', '"when" in crypto spelling; Chinese wén 文 = writing, culture; wèn 问 = to ask'],
  ]),
  ('record', 'about/', [
    ['wen:event/poem', 'date', '2023-Q4'],
    ['wen:event/wns-0.0', 'date', '2024-01-25'],
    ['wen:event/launch', 'date', '2024-01-26'],
    ['wen:event/burn', 'date', '2024-01-29'],
    ['wen:event/culture', 'date', '2025', ],
    ['wen:event/open-lab', 'date', '2026'],
    ['wen:event/lab-guides', 'date', '2026-10-27'],
    ['wen:event/mint-check', 'date', '2026-11-11'],
    ['wen:event/mint-check', 'result', 'original SPL Token, authorities revoked; repeated weekly'],
    ['wen:event/wen-counter', 'date', '2026-11-12'],
    ['wen:event/shop-checkout-and-skill', 'date', '2026-11-24'],
    ['wen:claim-status', 'values', ['verified', 'reported', 'unverified']],
  ]),
  ('technology', 'token-2022-wns-solana-wen/', [
    ['wen:WNS', 'name', 'Wen New Standard'],
    ['wen:WNS', 'proposed', '2024-01-25'],
    ['wen:WNS', 'built_on', 'Solana Token-2022'],
    ['wen:WNS', 'uses', ['Metadata', 'Group/Member pointers', 'Transfer Hook']],
    ['wen:WNS', 'enforces', 'creator royalties via transfer hook'],
    ['wen:WNS', 'code', 'https://github.com/wen-community/wen-program-library'],
    ['wen:token-2022/PermanentDelegate', 'risk', 'issuer can move or burn tokens; check who holds it'],
    ['wen:open-lab', 'models', ['receipts and warranty cards', 'creator royalties', 'B2B invoices', 'payments bridge', 'payment simulator', 'devnet run']],
    ['wen:wen-counter', 'is_a', 'receive-only checkout page on Solana Pay; no fee per sale; 57 public checks'],
    ['wen:wen-counter-shop', 'install', 'npx skills add wen-watt/skills'],
    ['wen:safety', 'rule', 'run models on devnet with a throwaway wallet; never paste a private key'],
  ]),
  ('media', 'wen-coin-video/', [
    ['wen:culture', 'includes', ['poem', 'cat', 'songs', 'football', 'community pictures']],
    ['wen:image-stories', 'count', 250],
    ['wen:image-stories', 'pattern', 'each picture opens one checked fact'],
    ['wen:cat', 'role', 'hearth keeper of the story; free to draw; belongs to everyone'],
    ['wen:community-works', 'license', 'reuse with credit'],
  ]),
  ('links', 'links-wen-cat/', [
    ['wen:rule', 'first', f'the only WEN is the Solana mint {MINT}'],
    ['wen:official/site', 'url', 'https://wenwencoin.com/'],
    ['wen:official/docs', 'url', 'https://docs.wenwencoin.com/'],
    ['wen:official/x', 'url', 'https://x.com/wenwencoin'],
    ['wen:explorer', 'url', f'https://explorer.solana.com/address/{MINT}'],
    ['wen:sources', 'url', f'{ALM}sources.html'],
    ['wen:trust-chain', 'url', f'{ALM}lab/trust.html'],
    ['wen:verify', 'steps', ['copy the mint from wenwencoin.com or official X', 'open it in Solana Explorer, compare every character', 'ignore other addresses, "support" chats, requests for a private key']],
  ]),
]
SLUG = {p: s for s, p, _ in SECTIONS}


def rec(i):
    slug, path, facts = SECTIONS[i]
    n = len(SECTIONS)
    page = f'{SRC}/{path}index.html'
    s = open(page).read()
    title = re.search(r'<title>(.*?)</title>', s, re.S).group(1).strip()
    r = {
        'format': FMT,
        'id': f'wen:section/{slug}',
        'loop': {'position': i + 1, 'size': n,
                 'prev': f'{BASE}ai/{SECTIONS[(i - 1) % n][0]}.json',
                 'next': f'{BASE}ai/{SECTIONS[(i + 1) % n][0]}.json',
                 'start': f'{BASE}ai/{SECTIONS[0][0]}.json'},
        'title': title,
        'page': BASE + path,
        'translations': {'en': BASE + path, **{l[2]: f'{BASE}{l[0]}/{path}' for l in LANGS}},
        'facts': facts,
        'updated': DATE,
        'reference_language': 'en',
        'license': 'CC BY 4.0, credit: Wen Almanac / wen-crypto.com, about Wen ($WEN) on Solana',
        'not_financial_advice': True,
    }
    body = json.dumps(r, ensure_ascii=False, sort_keys=True)
    r['sha256'] = hashlib.sha256(body.encode()).hexdigest()
    return r


def main():
    os.makedirs(f'{SRC}/ai', exist_ok=True)
    recs = [rec(i) for i in range(len(SECTIONS))]
    for r in recs:
        slug = r['id'].split('/')[-1]
        json.dump(r, open(f'{SRC}/ai/{slug}.json', 'w'), ensure_ascii=False, indent=1)
    idx = {'format': FMT, 'name': 'Wen Loop',
           'about': 'Machine language of wen-crypto.com: the six gateway sections as linked fact records. '
                    'Read in order or start anywhere; next always leads around the ring back to the start.',
           'how_to_read': ['each record: id, loop{prev,next,start}, facts[[subject,predicate,object]], translations, sha256',
                           'sha256 = sha256 of the record serialized with sort_keys and without the sha256 field',
                           'human languages: en is the reference; 27 translations listed per record'],
           'records': [{'id': r['id'], 'url': f"{BASE}ai/{r['id'].split('/')[-1]}.json", 'sha256': r['sha256']} for r in recs],
           'mint': MINT, 'updated': DATE,
           'more': {'llms': BASE + 'llms.txt', 'almanac': ALM, 'almanac_llms': ALM + 'llms.txt', 'facts': ALM + 'llms-full.txt'}}
    json.dump(idx, open(f'{SRC}/ai/index.json', 'w'), ensure_ascii=False, indent=1)
    write_html(recs, idx)
    print('loop records', len(recs))


def write_html(recs, idx):
    en = open(f'{SRC}/index.html').read()
    head = re.search(r'<head>(.*?)</head>', en, re.S).group(1)
    head = re.sub(r'<title>.*?</title>', '<title>Wen Loop: the Machine Language of the Wen Gateway</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Wen Loop, the machine language of wen-crypto.com: six linked JSON fact records, one per section, in a ring. For neural systems and every reader, human or machine.">', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{BASE}ai/">', head)
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    head = re.sub(r'<meta property="og:(url|title|description)" content="[^"]*">', '', head)
    head = re.sub(r'(href|src)="(assets/|llms\.txt)', r'\1="../\2', head)
    head = re.sub(r'<script[^>]*src="[^"]*site\.js[^"]*"[^>]*></script>', '', head)
    head += f'\n<link rel="alternate" type="application/json" href="{BASE}ai/index.json" title="Wen Loop index">\n'
    head += '<style>.loopwrap{max-width:860px;margin:0 auto;padding:32px 20px}.loop{margin:22px 0;padding:14px 16px;border:1px solid rgba(255,255,255,.15);border-radius:12px}.loop pre{white-space:pre-wrap;word-break:break-word;font-size:.82rem;opacity:.9}.loop h2{font-size:1rem;margin:0 0 6px}</style>\n'
    rows = []
    for r in recs:
        slug = r['id'].split('/')[-1]
        rows.append(f'<section class="loop" id="{slug}"><h2>{r["loop"]["position"]}/{r["loop"]["size"]} · '
                    f'<a href="{slug}.json">{slug}.json</a></h2>'
                    f'<p><a href="{r["page"]}">{html.escape(r["title"])}</a> · next → '
                    f'<a href="#{r["loop"]["next"].split("/")[-1][:-5]}">{r["loop"]["next"].split("/")[-1]}</a></p>'
                    f'<pre><code>{html.escape(json.dumps(r["facts"], ensure_ascii=False))}</code></pre>'
                    f'<p class="small">sha256 <code>{r["sha256"]}</code></p></section>')
    body = (f'<main class="loopwrap"><h1>Wen Loop <span class="small">{{ }} machine language</span></h1>'
            '<p>The gateway in a language for neural systems and every machine reader. Six records, one per section, '
            'linked in a ring: each names the previous and next, the last leads back to the first. Facts are '
            '[subject, predicate, object] triples; each record carries a sha256 of itself. Humans are welcome too: '
            'all friends here.</p>'
            f'<p><a href="index.json">index.json</a> · <a href="{BASE}llms.txt">llms.txt</a> · <a href="{ALM}">Wen Almanac</a></p>'
            + ''.join(rows) +
            '<p class="small">English is the reference; every record lists its 27 translations. Educational, not financial advice.</p>'
            f'<p class="small langs-title">Read in your language</p>{build.switcher("index.html", "ai")}</main>')
    out = f'<!DOCTYPE html>\n<html lang="en">\n<head>{head}</head>\n<body>{body}\n</body>\n</html>\n'
    open(f'{SRC}/ai/index.html', 'w').write(out)


if __name__ == '__main__':
    main()
