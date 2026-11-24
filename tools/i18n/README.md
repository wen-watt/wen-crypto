# Static translations of wen-crypto.com

`units_ph.json`: English units (links as <aN> placeholders, restored from `ph_attrs.json`). `tr/<lang>.txt`: one `key|translation` per line. `python3 build.py` (paths at top) rebuilds `/<lang>/` pages, hreflang and the language switcher. Translated by the Wen community with AI help; English is the reference.

## SEO files

After `build.py`, run `seo.py`: it regenerates `sitemap.xml` (every section URL with xhtml:link hreflang alternates for all languages and x-default), `llms.txt` (sections and languages map) and `robots.txt`.
