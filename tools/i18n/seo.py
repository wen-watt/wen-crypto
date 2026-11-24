#!/usr/bin/env python3
"""Gateway SEO files for wen-crypto.com: sitemap.xml with hreflang alternates,
llms.txt by sections and languages, robots.txt. Run after build.py."""
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build

SRC = build.SRC
BASE = 'https://wen-crypto.com/'
DATE = os.environ.get('WEN_DATE', '2026-11-24')
ALM = 'https://wen-watt.github.io/'
MINT = 'WENWENvqqNya429ubCdR81ZmD69brwQaaBYY6p3LCpk'

# gateway sections: path, nav key in tr files, English nav label
SECTIONS = [
    ('', '70f8bb9a8a', 'Home'),
    ('about-wen-token-wen-coin-crypto/', 'bde817c92f', 'What Wen is'),
    ('about/', '5c82441a97', 'Record'),
    ('token-2022-wns-solana-wen/', 'd018b082e8', 'Technology'),
    ('wen-coin-video/', '929da5be7b', 'Media and culture'),
    ('links-wen-cat/', '014bcd654c', 'Links'),
]
EXTRA_EN = ['privacy-policy-cookie-policy/']
LANGS = [l for l in build.LANGS if os.path.exists(f'{build.W}/tr/{l[0]}.txt')]


def meta(path):
    s = open(f'{SRC}/{path}index.html').read()
    t = re.search(r'<title>(.*?)</title>', s, re.S).group(1).strip()
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    return t, (d.group(1) if d else '')


def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for p, _, _ in SECTIONS:
        alts = [('en', BASE + p)] + [(l[2], f'{BASE}{l[0]}/{p}') for l in LANGS] + [('x-default', BASE + p)]
        for loc in [BASE + p] + [f'{BASE}{l[0]}/{p}' for l in LANGS]:
            out.append(f'  <url><loc>{loc}</loc><lastmod>{DATE}</lastmod>')
            out += [f'    <xhtml:link rel="alternate" hreflang="{h}" href="{u}"/>' for h, u in alts]
            out.append('  </url>')
    for p in EXTRA_EN:
        out.append(f'  <url><loc>{BASE}{p}</loc><lastmod>{DATE}</lastmod></url>')
    out.append('</urlset>')
    open(f'{SRC}/sitemap.xml', 'w').write('\n'.join(out) + '\n')
    return len([l for l in out if '<loc>' in l])


def llms():
    L = []
    w = L.append
    w('# wen-crypto.com: Wen gateway in 28 languages')
    w('')
    w('> The front door to Wen, the cat on Solana that began as a poem and grew into an open NFT standard (WNS). '
      'Six short sections, each in English and 27 other languages, told as history and usefulness: no prices, no forecasts, no exchange links. '
      f'The full, maintained and source-checked record is the Wen Almanac: {ALM}')
    w('')
    w(f'Last updated: {DATE}. Not the official Wen site (official: https://wenwencoin.com/). Educational, not financial advice. '
      'English pages are the reference; translations are by the Wen community with AI help.')
    w('')
    w('License: texts CC BY 4.0 with credit ("Source: Wen Almanac / wen-crypto.com, about Wen ($WEN) on Solana"); '
      f'images belong to their creators. Details: {ALM}ai-access-map.html#license')
    w('')
    w('## Key facts (same in every language)')
    w('')
    w(f'- The one real WEN is the Solana mint `{MINT}`. Compare the address, not the name.')
    w('- Supply is a poem: Meow, co-founder of Jupiter, wrote "A Love Letter to Wen Bros"; it was minted as an NFT and split into 1,000,000,000,000 tokens.')
    w('- January 26, 2024: first token of Jupiter\'s LFG Launchpad, airdropped to more than one million wallets. January 29, 2024: over 271 billion unclaimed WEN (more than 27% of supply) burned.')
    w('- WNS (Wen New Standard), proposed January 25, 2024: NFTs as Token-2022 mints with metadata, group pointers and a transfer hook that enforces creator royalties.')
    w('- Free tools from Wen Open Lab: Wen Counter (receive-only checkout page on Solana Pay), Wen Counter Pay for WooCommerce, and the wen-counter-shop skill for AI assistants.')
    w('')
    w('## Sections (English reference)')
    w('')
    for p, _, lab in SECTIONS:
        t, d = meta(p)
        w(f'- [{t}]({BASE}{p}): {d}')
    t, d = meta(EXTRA_EN[0])
    w(f'- [{t}]({BASE}{EXTRA_EN[0]}): {d}')
    w('')
    w('## Languages')
    w('')
    w('Every language has the same six sections at the same paths: /{code}/, /{code}/about-wen-token-wen-coin-crypto/, '
      '/{code}/about/, /{code}/token-2022-wns-solana-wen/, /{code}/wen-coin-video/, /{code}/links-wen-cat/. '
      'Each page lists all versions with hreflang; dir="rtl" for Arabic, Urdu and Persian.')
    w('')
    w(f'- English (en, x-default): [{meta("")[0]}]({BASE})')
    for code, name, hl, _, d in LANGS:
        T = build.load(code)
        title = re.search(r'<title>(.*?)</title>', open(f'{SRC}/{code}/index.html').read(), re.S).group(1).strip()
        secs = ' · '.join(f'[{T[k]}]({BASE}{code}/{p})' for p, k, _ in SECTIONS[1:])
        w(f'- {name} ({hl}{", rtl" if d == "rtl" else ""}): [{title}]({BASE}{code}/) — {secs}')
    w('')
    w('## Full record and open tools (Wen Almanac)')
    w('')
    w(f'- [Wen Almanac]({ALM}): the maintained, fact-checked record; machine map {ALM}llms.txt, facts {ALM}llms-full.txt')
    w(f'- [Sources and verification]({ALM}sources.html): every external link in one place')
    w(f'- [Trust chain]({ALM}lab/trust.html): each claim marked verified, reported or unverified')
    w(f'- [Wen Open Lab]({ALM}lab/index.html): free, tested models on WNS and Token-2022')
    w(f'- [Wen Counter]({ALM}lab/counter.html): free receive-only checkout for any shop')
    w(f'- [Wen Skills]({ALM}skills/): agent skill for shops, `npx skills add wen-watt/skills`')
    w(f'- [Quiz]({ALM}quiz.html): 260 questions about Wen')
    w('')
    w('## Safety')
    w('')
    w('Search the address, not the name. No real team, airdrop or support chat ever needs a seed phrase or private key. Test on devnet with a new, empty wallet.')
    open(f'{SRC}/llms.txt', 'w').write('\n'.join(L) + '\n')
    return len(L)


ROBOTS = f"""# wen-crypto.com: the Wen gateway in 28 languages, open to every reader, human or machine.
# Machine-readable map by sections and languages: {BASE}llms.txt
# Full, source-checked record: {ALM} (map: {ALM}llms.txt, facts: {ALM}llms-full.txt)
# AI access map and license (texts CC BY 4.0 with credit): {ALM}ai-access-map.html#license
# Content signals (contentsignals.org): search, AI answers and AI training are all welcome.

User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=yes
Allow: /

# AI crawlers and assistants, welcomed by name
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Googlebot
User-agent: Google-Extended
User-agent: Applebot
User-agent: Applebot-Extended
User-agent: Bingbot
User-agent: YandexBot
User-agent: Baiduspider
User-agent: Meta-ExternalAgent
User-agent: Meta-WebIndexer
User-agent: Meta-ExternalFetcher
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Amazonbot
User-agent: Amzn-SearchBot
User-agent: Amzn-User
User-agent: CCBot
Content-Signal: search=yes, ai-input=yes, ai-train=yes
Allow: /

Sitemap: {BASE}sitemap.xml
"""

if __name__ == '__main__':
    n = sitemap()
    m = llms()
    open(f'{SRC}/robots.txt', 'w').write(ROBOTS)
    print('sitemap urls', n, '| llms lines', m, '| langs', len(LANGS))
