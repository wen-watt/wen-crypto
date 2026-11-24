import hashlib, re, json
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
SRC='/home/claude/wen-crypto'
PAGES=['index.html','about-wen-token-wen-coin-crypto/index.html','about/index.html','token-2022-wns-solana-wen/index.html','wen-coin-video/index.html','links-wen-cat/index.html']
INLINE={'a','b','strong','em','i','code','span','small','sup','sub','br','abbr','time','q','cite','mark','u','s'}
SKIP={'script','style','svg','noscript','template','canvas'}
LET=re.compile(r'[A-Za-z]{2,}')
def h(x): return hashlib.sha1(x.encode()).hexdigest()[:12]
def blocks(soup):
    out=[]
    for el in soup.body.find_all(True):
        if el.name in SKIP or any(p.name in SKIP for p in el.parents if isinstance(p,Tag)): continue
        if el.get('class') and 'reel' in el.get('class'): continue
        if any(isinstance(p,Tag) and p.get('class') and 'reel' in p.get('class') for p in el.parents): continue
        leafish = el.name not in INLINE and not any(isinstance(d,Tag) and d.name not in INLINE for d in el.descendants)
        span_leaf = el.name=='span' and el.get('class') and set(el['class'])&{'dt','dd'}
        if not (leafish or span_leaf or el.name=='button'): continue
        if el.name in INLINE and not span_leaf: continue
        inner=el.decode_contents().strip()
        txt=''.join(str(d) for d in el.descendants if isinstance(d,NavigableString) and not isinstance(d,Comment) and not any(p.name=='code' for p in d.parents if isinstance(p,Tag)))
        if not LET.search(txt): continue
        out.append(el)
    return out
def attrs(soup):
    res=[]
    if soup.title: res.append(('title',soup.title.string))
    for m in soup.find_all('meta'):
        if m.get('name') in ('description',) or m.get('property') in ('og:title','og:description','og:image:alt') or m.get('name') in ('twitter:title','twitter:description'):
            res.append(('meta',m.get('content','')))
    for im in soup.find_all('img'):
        if im.get('alt') and LET.search(im['alt']) and not any(isinstance(p,Tag) and p.get('class') and 'reel' in p.get('class') for p in im.parents): res.append(('alt',im['alt']))
    for el in soup.find_all(attrs={'aria-label':True}):
        if LET.search(el['aria-label']): res.append(('aria',el['aria-label']))
    return res
if __name__=='__main__':
    segs={}
    for p in PAGES:
        s=BeautifulSoup(open(f'{SRC}/{p}').read(),'html.parser')
        for el in blocks(s): x=el.decode_contents().strip(); segs[h(x)]=x
        for k,v in attrs(s):
            if v: segs['a'+h(v)]=v
    json.dump(segs,open('/home/claude/work/wc-i18n/en.json','w'),ensure_ascii=False,indent=0)
    words=sum(len(re.sub('<[^>]+>',' ',v).split()) for v in segs.values())
    print(len(segs),'segments',words,'words')
