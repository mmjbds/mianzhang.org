"""Check local public link targets without changing the research archive."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, unquote

ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag in ('a','link','img','script'):
            value=d.get('href',d.get('src',''))
            if value:self.links.append(value)

def main():
    bad=[];pages=0
    for file in ROOT.rglob('*.html'):
        if '.git' in file.parts:continue
        pages+=1;p=Links();p.feed(file.read_text(encoding='utf-8'))
        for link in p.links:
            url=urlparse(urljoin('https://mianzhang.org/'+file.relative_to(ROOT).as_posix(),link))
            if url.netloc!='mianzhang.org':continue
            rel=unquote(url.path).lstrip('/');target=ROOT/rel
            if not rel or url.path.endswith('/'):target=target/'index.html'
            if not target.exists():bad.append((str(file.relative_to(ROOT)),link))
    print({'pages':pages,'missing':bad})
    return bool(bad)
if __name__=='__main__':raise SystemExit(main())
