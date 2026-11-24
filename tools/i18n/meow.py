#!/usr/bin/env python3
"""Meow: the gateway home page in cat language (a language still being
studied). Writes /meow/index.html. Run after build.py, before seo.py."""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build

SRC = build.SRC
BASE = 'https://wen-crypto.com/'
ALM = 'https://wen-watt.github.io/'
MINT = 'WENWENvqqNya429ubCdR81ZmD69brwQaaBYY6p3LCpk'
E = html.escape


def line(cat, human, tag='p', cls=''):
    c = f' class="{cls}"' if cls else ''
    return (f'<{tag}{c}><span class="cat" title="{E(human)}">{cat}</span>'
            f'<span class="gloss">{E(human)}</span></{tag}>')


DOORS = [
    ('about-wen-token-wen-coin-crypto/', 'mrrp? ⟨Wen⟩ =^.^=', 'What Wen is'),
    ('about/', 'mew↗ mew↗ mew↗ … prrr', 'The record, date by date'),
    ('token-2022-wns-solana-wen/', 'ek-ek-ek ⟨WNS⟩ 🐾', 'Technology and free tools'),
    ('wen-coin-video/', 'mrrow↗ =^ω^= =^ω^=', 'Media and culture'),
    ('links-wen-cat/', 'mew↗ ⟨official⟩ → mrrp ⟨community⟩', 'Links: official first'),
    ('ai/', '{ mew↗ } ⟳', 'Wen Loop, the machine language'),
]

DECODER = [
    ('mew↗ / mrrow↗', 'rising meow', 'asking, friendly, "yes please"',
     'Meows in positive, affiliative contexts tend to rise in pitch (Schötz, van de Weijer, Eklund; Lund University)'),
    ('mraow↘', 'falling meow', 'unhappy, careful, "no"',
     'Meows in negative contexts, such as the carrier or the vet, tend to fall (same studies)'),
    ('mrrp', 'trill', 'hello, follow me', 'A short rolling call cats use to greet people and other cats'),
    ('prrr', 'purr', 'content, close, calm', 'Usually contentment, but cats also purr when stressed or in pain, so read it with the face'),
    ('hsss', 'hiss', 'warning, stop', 'Between cats, sound is mostly hissing and growling over territory'),
    ('=^-.-^=', 'slow blink', 'I trust you', 'Friendly cat faces show closed or half-closed eyes and forward ears (Scott and Florkiewicz, 2023)'),
    ('ek-ek-ek', 'chatter', 'excited, "look at that!"', 'The fast clicking a cat makes at a bird behind the window'),
    ('⟨name⟩', 'borrowed word', 'proper names stay human', 'Cats have no word for Solana, so the page borrows it'),
]


def page():
    en = open(f'{SRC}/index.html').read()
    head = re.search(r'<head>(.*?)</head>', en, re.S).group(1)
    head = re.sub(r'<title>.*?</title>', '<title>Meow: Wen in Cat Language (Experimental)</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="The Wen gateway in cat language: rising meows, purrs, trills and slow blinks, with a decoder built on real cat research. A language still being studied. Use it freely.">', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{BASE}meow/">', head)
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', head)
    head = re.sub(r'\n?<link rel="alternate" type="application/json"[^>]*>', '', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    head = re.sub(r'<meta property="og:(url|title|description)" content="[^"]*">', '', head)
    head = re.sub(r'(href|src)="(assets/|llms\.txt)', r'\1="../\2', head)
    head = re.sub(r'<script[^>]*src="[^"]*site\.js[^"]*"[^>]*></script>', '', head)
    head += '''
<style>
.meowwrap{max-width:860px;margin:0 auto;padding:28px 20px 40px}
.meow-note{border:1px solid rgba(224,164,68,.55);border-radius:12px;padding:12px 16px;margin:0 0 22px;font-size:.95rem}
.meowwrap .cat{display:block;font-size:1.15rem;letter-spacing:.01em}
.meowwrap h1 .cat{font-size:2.1rem;line-height:1.25}
.meowwrap .gloss{display:none;font-size:.85rem;opacity:.7;margin-top:2px}
#subs:checked ~ .meowwrap .gloss{display:block}
.subs-toggle{position:sticky;top:8px;z-index:5;display:inline-block;margin:10px 20px 0;padding:6px 14px;border:1px solid rgba(255,255,255,.25);border-radius:999px;cursor:pointer;font-size:.9rem;background:rgba(10,12,20,.85)}
#subs{position:absolute;opacity:0}
#subs:focus-visible + .subs-toggle{outline:2px solid #e0a444}
.meow-doors{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.meow-doors a{display:block;padding:14px;border:1px solid rgba(255,255,255,.15);border-radius:12px;text-decoration:none}
.decoder{width:100%;border-collapse:collapse;font-size:.9rem}
.decoder th,.decoder td{border-bottom:1px solid rgba(255,255,255,.12);padding:8px 6px;text-align:left;vertical-align:top}
.decoder td:first-child{white-space:nowrap;font-weight:600}
.meowwrap code{word-break:break-all}
</style>
'''
    parts = []
    w = parts.append
    w('<p class="meow-note"><b>Meow (experimental).</b> This page is written in cat language, a language that '
      'scientists are still studying. Nobody speaks it perfectly, not even cats talking to each other: adult cats '
      'mostly meow at people. Use it freely, share it, and switch on human subtitles if you get lost.</p>')
    w(line('mrrp! ⟨Solana⟩ prrr =^.^=', 'A community almanac on Solana', cls='kicker'))
    w(line('mew-mew mrrow↗, mrrow =^.^=, =^.^= prrr↗ ⟨standard⟩!', 'A poem became a cat, the cat became a standard.', tag='h1'))
    w(line('⟨Meow⟩ ⟨Jupiter⟩ mew-mew-mew ♡ prrr. mew ×1 000 000 000 000 … mew↗ 👛 ×1 000 000 … prrr↗ ⟨WNS⟩. '
           'mrrow↗ ⟨history⟩, mrrow↗ ⟨use⟩, hsss ⟨price⟩.',
           'Wen began as a love letter written by Meow of Jupiter. It was split into a trillion pieces, sent to a million '
           'wallets and grew into WNS, an open way to build NFTs. Kept as history and usefulness, never as a price.'))
    w(f'<p class="hero-actions"><a class="btn primary" href="{ALM}" title="Open the Wen Almanac">mrrp → ⟨Almanac⟩</a> '
      f'<a class="btn" href="{BASE}" title="Back to the English gateway">mraow↘ ← ⟨English⟩</a></p>')
    w(line('mew↗ mew↗ mew↗ … 🚪×6', 'Six doors into the story', tag='h2'))
    w('<ul class="meow-doors">' + ''.join(
        f'<li><a href="{BASE}{p}"><span class="cat" title="{E(h)}">{c}</span><span class="gloss">{E(h)}</span></a></li>'
        for p, c, h in DOORS) + '</ul>')
    w(line('=^-.-^= mew↗ ⟨address⟩, hsss ⟨name⟩', 'The one real WEN: compare the address, not the name.', tag='h2'))
    w(f'<p><code>{MINT}</code></p>')
    w(line('hsss! ⟨private key⟩ ✕ hsss! ⟨devnet⟩ 👛 mew↗ prrr.',
           'Never paste a private key anywhere. Test on devnet with a new, empty wallet.'))
    w(line('ek-ek-ek! ⟨Wen Counter⟩ mew↗ 🪙 → 🏪 prrr. ⟨WooCommerce⟩ prrr. ⟨AI⟩ 🐾 prrr.',
           'Free tools: a till that only receives, a shop checkout and an AI skill. Free, open, checked.', tag='h2'))
    w(line('mraow↘ … ⟨local rules⟩? mrrp → 🔎 → prrr.',
           'In some countries paying for goods with crypto assets is banned or needs a licence. Check your local rules before you use Wen Counter.'))
    w(line('hsss ⟨price⟩. hsss ⟨forecast⟩. hsss ⟨100x⟩. prrr ⟨what happened⟩.',
           'No prices, no forecasts, no "next 100x". Only what happened, how the technology works and how to check it yourself.', tag='h2'))
    w('<h2>Decoder: how to read cat</h2>')
    w('<table class="decoder"><thead><tr><th>Written</th><th>Sound</th><th>Meaning here</th><th>What research says</th></tr></thead><tbody>'
      + ''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>' for a, b, c, d in DECODER)
      + '</tbody></table>')
    w('<h2>What science knows so far</h2><ul>'
      '<li>Meow melody carries mood: in a study of 780 meows from 40 cats, positive contexts mostly gave rising contours and negative ones falling contours (Schötz, van de Weijer and Eklund, Lund University). People with cat experience recognise the difference better.</li>'
      '<li>Cats have 276 distinct facial expressions built from 26 movements; friendly ones often show closed eyes and forward ears (Scott and Florkiewicz, Behavioural Processes, 2023).</li>'
      '<li>Adult cats rarely meow to each other: the meow is mainly a cat-to-human channel.</li>'
      '<li>AI tools now turn meows into spectrograms and sort them by intent, and some apps claim very high accuracy; these claims are early and not independently confirmed.</li>'
      '</ul>')
    w(f'<p class="small">Sources are named in the text; links are on the almanac\'s <a href="{ALM}sources.html">sources page</a>. '
      'This page is a playful experiment, not a scientific translation. Educational, not financial advice.</p>')
    w(f'<p class="small langs-title">Read in your language</p>{build.switcher("index.html", "meow")}')
    body = ('<input type="checkbox" id="subs"><label for="subs" class="subs-toggle">🐾 Human subtitles</label>'
            '<main class="meowwrap" lang="en">' + ''.join(parts) + '</main>')
    out = f'<!DOCTYPE html>\n<html lang="en">\n<head>{head}</head>\n<body>{body}\n</body>\n</html>\n'
    os.makedirs(f'{SRC}/meow', exist_ok=True)
    open(f'{SRC}/meow/index.html', 'w').write(out)
    print('meow page written')


if __name__ == '__main__':
    page()
