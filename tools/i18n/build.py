import json, re, hashlib, os, posixpath, copy
from bs4 import BeautifulSoup, Tag
import sys; sys.path.insert(0,'/home/claude/work/wc-i18n'); from seg import blocks, PAGES, LET
SRC='/home/claude/wen-crypto'; W='/home/claude/work/wc-i18n'
LANGS=[('zh','中文','zh-Hans','zh_CN','ltr'),('hi','हिन्दी','hi','hi_IN','ltr'),('es','Español','es','es_ES','ltr'),('ar','العربية','ar','ar_AR','rtl'),('fr','Français','fr','fr_FR','ltr'),('bn','বাংলা','bn','bn_BD','ltr'),('pt','Português','pt','pt_BR','ltr'),('id','Bahasa Indonesia','id','id_ID','ltr'),('ur','اردو','ur','ur_PK','rtl'),('de','Deutsch','de','de_DE','ltr'),('ja','日本語','ja','ja_JP','ltr'),('mr','मराठी','mr','mr_IN','ltr'),('vi','Tiếng Việt','vi','vi_VN','ltr'),('te','తెలుగు','te','te_IN','ltr'),('ha','Hausa','ha','ha_NG','ltr'),('tr','Türkçe','tr','tr_TR','ltr'),('pa','ਪੰਜਾਬੀ','pa','pa_IN','ltr'),('sw','Kiswahili','sw','sw_KE','ltr'),('tl','Tagalog','tl','tl_PH','ltr'),('ta','தமிழ்','ta','ta_IN','ltr'),('fa','فارسی','fa','fa_IR','rtl'),('ko','한국어','ko','ko_KR','ltr'),('th','ไทย','th','th_TH','ltr'),('jv','Basa Jawa','jv','jv_ID','ltr'),('it','Italiano','it','it_IT','ltr'),('gu','ગુજરાતી','gu','gu_IN','ltr'),('pl','Polski','pl','pl_PL','ltr')]
UNITS=json.load(open(f'{W}/units_ph.json'))
DONE=[l for l in LANGS if os.path.exists(f'{W}/tr/{l[0]}.txt')]; PH=json.load(open(f'{W}/ph_attrs.json'))
def h10(x): return hashlib.sha1(x.encode()).hexdigest()[:10]
def unit_key(inner):
    s=BeautifulSoup(inner,'html.parser'); kids=[c for c in s.contents if not (isinstance(c,str) and not c.strip())]
    v=inner
    if len(kids)==1 and getattr(kids[0],'name',None) in ('a','span') and len(list(kids[0].children))==1 and isinstance(next(kids[0].children),str):
        return h10(kids[0].get_text()), True
    v=v.replace('&amp;','&') if '<' not in v else v
    return h10(v), False
def restore(k,t):
    attrs=PH.get(k,[])
    for i,a in enumerate(attrs,1):
        t=t.replace(f'<a{i}>',f'<a {a}>').replace(f'</a{i}>','</a>')
    return t.replace('<b>','<strong>').replace('</b>','</strong>')
def page_url(p,lang=None):
    d=p[:-len('index.html')]
    return 'https://wen-crypto.com/'+(lang+'/' if lang else '')+d
TRANSLATED_DIRS={p[:-len('index.html')] for p in PAGES}
def fix_links(soup,p,lang):
    depth_src=p.count('/')
    for el in soup.find_all(True):
        for a in ('href','src'):
            u=el.get(a)
            if not u or re.match(r'^(#|https?:|mailto:|data:|//|javascript:)',u): continue
            path,_,frag=u.partition('#')
            tgt=posixpath.normpath(posixpath.join(posixpath.dirname(p),path))
            tgt='' if tgt=='.' else tgt
            tdir=(tgt+'/') if tgt and not tgt.endswith(('.html','.css','.js','.png','.ico','.txt','.xml','.jpg','.jpeg','.svg','.webmanifest')) else tgt
            if path.endswith('/') or path=='./' or path=='': tdir=(tgt+'/' if tgt else '')
            if tdir in TRANSLATED_DIRS:
                continue  # same structure inside /lang/
            el[a]='../'+u
def hreflang_block(p):
    out=[f'<link rel="alternate" hreflang="en" href="{page_url(p)}">']
    out+= [f'<link rel="alternate" hreflang="{l[2]}" href="{page_url(p,l[0])}">' for l in DONE]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{page_url(p)}">')
    return '\n'.join(out)
def switcher(p,cur):
    items=[('en','English',page_url(p))]+[(l[0],l[1],page_url(p,l[0])) for l in DONE]
    lis=''.join(f'<a href="{u}" hreflang="{c}" lang="{c}"'+(' aria-current="true"' if c==cur else '')+f'>{n}</a> ' for c,n,u in items)
    return f'<nav class="langs" aria-label="Languages">{lis.strip()}</nav>'
MISS=set()
def tr_text(T,v):
    k=h10(v.replace('&amp;','&') if '<' not in v else v)
    return T.get(k)
def build(p,lang,T):
    code=[l for l in LANGS if l[0]==lang][0]
    soup=BeautifulSoup(open(f'{SRC}/{p}').read(),'html.parser')
    for old in soup.select('p.langs-title, nav.langs'): old.decompose()
    if p=='index.html':
        sh=soup.find('section',class_='shorts')
        if sh: sh.decompose()
    for el in blocks(soup):
        inner=el.decode_contents().strip(); k,single=unit_key(inner)
        if k not in T: MISS.add(k); continue
        if single:
            child=[c for c in el.children if isinstance(c,Tag)][0]; child.string=T[k]
        else:
            frag=BeautifulSoup(restore(k,T[k]),'html.parser'); el.clear()
            for c in list(frag.contents): el.append(c)
    for m in soup.find_all('meta'):
        c=m.get('content')
        if c and (m.get('name') in ('description','twitter:title','twitter:description') or m.get('property') in ('og:title','og:description','og:image:alt')):
            t=tr_text(T,c)
            if t: m['content']=re.sub('<[^>]+>','',t)
            else: MISS.add(h10(c))
    if soup.title:
        t=tr_text(T,soup.title.string)
        if t: soup.title.string=t
    for im in soup.find_all('img'):
        if im.get('alt'):
            t=tr_text(T,im['alt'])
            if t: im['alt']=re.sub('<[^>]+>','',t)
    for el in soup.find_all(attrs={'aria-label':True}):
        t=tr_text(T,el['aria-label'])
        if t: el['aria-label']=t
    fix_links(soup,p,lang)
    soup.html['lang']=code[2]; soup.html['dir']=code[4]
    can=soup.find('link',rel='canonical'); can['href']=page_url(p,lang)
    for m in soup.find_all('meta',property='og:url'): m['content']=page_url(p,lang)
    for m in soup.find_all('link',rel='alternate',hreflang=True): m.decompose()
    ogl=soup.find('meta',property='og:locale')
    if ogl: ogl['content']=code[3]
    else: soup.head.append(BeautifulSoup(f'<meta property="og:locale" content="{code[3]}">','html.parser'))
    can.insert_after(BeautifulSoup('\n'+hreflang_block(p),'html.parser'))
    if p in ('index.html','about-wen-token-wen-coin-crypto/index.html'):
        ld={"@context":"https://schema.org","@type":"FAQPage","inLanguage":code[2],"mainEntity":[{"@type":"Question","name":T['faq_q'],"acceptedAnswer":{"@type":"Answer","text":T['faq_a']}}]}
        sc=soup.new_tag('script',type='application/ld+json'); sc.string=json.dumps(ld,ensure_ascii=False); soup.head.append(sc)
    for sc in soup.find_all('script',type='application/ld+json'):
        try: d=json.loads(sc.string)
        except: continue
        def walk(o):
            if isinstance(o,dict):
                for k2,v in list(o.items()):
                    if k2=='inLanguage' and v=='en': o[k2]=code[2]
                    elif k2 in ('url','@id') and isinstance(v,str) and v.startswith('https://wen-crypto.com/') and '/'+lang+'/' not in v:
                        rest=v[len('https://wen-crypto.com/'):]
                        if rest.split('#')[0] in TRANSLATED_DIRS: o[k2]='https://wen-crypto.com/'+lang+'/'+rest
                    elif isinstance(v,str):
                        t=tr_text(T,v)
                        if t and k2 in ('name','headline','description','alternativeHeadline','caption'): o[k2]=re.sub('<[^>]+>','',t)
                    else: walk(v)
            elif isinstance(o,list):
                for x in o: walk(x)
        walk(d); sc.string=json.dumps(d,ensure_ascii=False)
    foot=soup.find('footer') or soup.find('aside',class_='gate')
    note=soup.new_tag('p',attrs={'class':'small trnote'}); note.string=T['trnote']
    sw=BeautifulSoup(f'<p class="small langs-title">{T["langs"]}</p>'+switcher(p,lang),'html.parser')
    tgt=soup.find('footer') or soup.body
    tgt.append(note); tgt.append(sw)
    out=f'{SRC}/{lang}/{p}'; os.makedirs(os.path.dirname(out),exist_ok=True)
    open(out,'w').write(str(soup))
def add_en_alternates():
    for p in PAGES:
        s=open(f'{SRC}/{p}').read()
        s=re.sub(r'\n<link rel="alternate" hreflang="[^"]*" href="[^"]*">','',s)
        s=re.sub(r'<p class="small langs-title">.*?</nav>','',s,flags=re.S)
        m=re.search(r'<link rel="canonical" href="[^"]*">',s)
        s=s[:m.end()]+'\n'+hreflang_block(p)+s[m.end():]
        blk='<p class="small langs-title">Read in your language</p>'+switcher(p,'en')
        if '</footer>' in s: s=s.replace('</footer>',blk+'</footer>',1)
        else: s=s.replace('</body>',blk+'</body>',1)
        open(f'{SRC}/{p}','w').write(s)

def load(lang):
    return dict(l.split('|',1) for l in open(f'{W}/tr/{lang}.txt').read().strip().split('\n'))
def check(lang):
    t=load(lang); u=UNITS
    miss=[k for k in u if k not in t]
    bad=[k for k in u if k in t and sorted(re.findall(r'</?a\d>|<code>|<b>|<span>',u[k]))!=sorted(re.findall(r'</?a\d>|<code>|<b>|<span>',t[k]))]
    return miss,bad
def build_all():
    for l in DONE:
        m,b=check(l[0])
        if m or b: print('SKIP',l[0],m[:5],b[:5]); continue
        T=load(l[0])
        for p in PAGES: build(p,l[0],T)
    add_en_alternates()
    print('built',[l[0] for l in DONE],'miss',len(MISS))
if __name__=='__main__': build_all()
