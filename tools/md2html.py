# -*- coding: utf-8 -*-
"""极简 Markdown → 单文件 HTML（仅用标准库，GitHub Actions 里也能跑）。

用法：
    python tools/md2html.py SOURCE.md index.html --repo frankiezeng6-ai/fdh-employer-guide
生成的 HTML 自带 CSS/JS，零外部依赖。
"""
import re, sys, html, argparse

CSS = """
:root{--bg:#f6f7f9;--panel:#fff;--fg:#1f2328;--muted:#656d76;--line:#d8dee4;--acc:#0969da;--acc-soft:#ddf4ff;
--quote:#57606a;--quotebg:#f6f8fa;--tag:#8250df;--tagbg:#fbefff}
html[data-theme=dark]{--bg:#0d1117;--panel:#161b22;--fg:#e6edf3;--muted:#8b949e;--line:#30363d;--acc:#58a6ff;
--acc-soft:#0c2d6b;--quote:#8b949e;--quotebg:#1c2128;--tag:#d2a8ff;--tagbg:#2b2140}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI",
"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;-webkit-font-smoothing:antialiased}
.wrap{display:flex;max-width:1240px;margin:0 auto;gap:28px;padding:0 20px}
aside{width:270px;flex:none;position:sticky;top:0;align-self:flex-start;max-height:100vh;overflow:auto;
padding:24px 0 60px}
aside h4{font-size:12px;letter-spacing:.08em;color:var(--muted);margin:18px 0 8px;text-transform:uppercase}
#q{width:100%;padding:9px 11px;border:1px solid var(--line);border-radius:8px;background:var(--panel);
color:var(--fg);font-size:14px}
.toc a{display:block;padding:5px 10px;margin:1px 0;border-radius:6px;color:var(--muted);text-decoration:none;
font-size:13.5px;line-height:1.5}
.toc a.sub{padding-left:22px;font-size:13px}
.toc a:hover{background:var(--acc-soft);color:var(--acc)}
main{flex:1;min-width:0;padding:24px 0 80px}
.top{position:sticky;top:0;z-index:5;background:var(--bg);padding:14px 0 10px;border-bottom:1px solid var(--line);
margin-bottom:22px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.btn{border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:8px;padding:7px 12px;
font-size:13.5px;cursor:pointer;text-decoration:none;display:inline-block;white-space:nowrap}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{opacity:.88;color:#fff}
.spacer{flex:1}
h1{font-size:30px;line-height:1.35;margin:6px 0 6px;letter-spacing:-.01em}
h2{font-size:22px;margin:44px 0 14px;padding-bottom:8px;border-bottom:2px solid var(--line)}
h3{font-size:17.5px;margin:28px 0 10px;color:var(--acc)}
p{margin:9px 0}
ul{margin:9px 0;padding-left:22px}
li{margin:5px 0}
blockquote{margin:10px 0;padding:9px 14px;border-left:3px solid var(--line);background:var(--quotebg);
color:var(--quote);font-size:14.5px;border-radius:0 6px 6px 0}
code{background:var(--quotebg);padding:1px 5px;border-radius:4px;font-size:.92em}
hr{border:0;border-top:1px solid var(--line);margin:26px 0}
.sub{color:var(--muted);font-size:14px}
.meta{color:var(--muted);font-size:13px;margin-top:6px}
.note{background:var(--acc-soft);border:1px solid var(--acc);border-radius:10px;padding:12px 14px;font-size:14px;
margin:16px 0}
.hidden{display:none!important}
#cnt{position:fixed;right:16px;bottom:16px;background:var(--panel);border:1px solid var(--line);
border-radius:20px;padding:5px 12px;font-size:12.5px;color:var(--muted);box-shadow:0 2px 10px rgba(0,0,0,.08)}
mark{background:#fff3a3;color:#000;border-radius:2px}
html[data-theme=dark] mark{background:#5b4c00;color:#fff}
@media(max-width:900px){.wrap{display:block}aside{position:static;width:auto;max-height:none;padding:16px 0 0}
#tocbox{max-height:230px;overflow:auto;border:1px solid var(--line);border-radius:10px;padding:8px;margin-top:8px}}
@media print{aside,.top,.btn,#cnt{display:none!important}body{background:#fff}main{padding:0}}
"""

JS = """
(function(){
 var root=document.documentElement;
 try{var t=localStorage.getItem('fdh-theme');if(t){root.setAttribute('data-theme',t);}}catch(e){}
 var btn=document.getElementById('theme');
 if(btn){btn.onclick=function(){var cur=root.getAttribute('data-theme')==='dark'?'light':'dark';
   root.setAttribute('data-theme',cur);try{localStorage.setItem('fdh-theme',cur);}catch(e){}};}
 var q=document.getElementById('q'), items=[].slice.call(document.querySelectorAll('main .srch')), n=0;
 function clearMarks(){[].forEach.call(document.querySelectorAll('mark'),function(m){
   m.parentNode.replaceChild(document.createTextNode(m.textContent),m);});}
 if(q){q.oninput=function(){var k=q.value.trim().toLowerCase();clearMarks();n=0;
   var lastH=null;
   items.forEach(function(el){
     if(!k){el.classList.remove('hidden');n++;return;}
     var ok=el.textContent.toLowerCase().indexOf(k)>=0;
     el.classList.toggle('hidden',!ok);
     if(ok){n++;if(!el.dataset.hl){el.dataset.hl='1';
        var re=new RegExp('('+k.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')+')','gi');
        el.innerHTML=el.innerHTML.replace(/<[^>]*>|[^<]+/g,function(s){
          return s.charAt(0)==='<'?s:s.replace(re,'<mark>$1</mark>')});
     }}else{el.dataset.hl='';}
   });
   document.getElementById('cnt').textContent=k?('命中 '+n+' 条'):('共 '+items.length+' 段');
 };q.oninput();}
})();
"""

INLINE = [
    (re.compile(r'`([^`]+)`'), r'<code>\1</code>'),
    (re.compile(r'\[([^\]]+)\]\(([^)]+)\)'), r'<a href="\2" target="_blank" rel="noopener">\1</a>'),
    (re.compile(r'\*\*([^*]+)\*\*'), r'<strong>\1</strong>'),
    (re.compile(r'(?<!\*)\*([^*\n]+)\*(?!\*)'), r'<em>\1</em>'),
]

def inline_md(t):
    t = html.escape(t, quote=False)
    for rx, rep in INLINE:
        t = rx.sub(rep, t)
    return t

def slug(text, used):
    s = re.sub(r'[^\w\u4e00-\u9fff]+', '-', text).strip('-').lower() or 's'
    base, i = s, 2
    while s in used:
        s = base + '-' + str(i); i += 1
    used.add(s)
    return s

def render(md, repo=None, srcfile='SOURCE.md'):
    lines = md.replace('\r\n', '\n').split('\n')
    # 去掉 bullet 之间的空行，合并成一个列表
    compact = []
    for ln in lines:
        if not ln.strip() and compact and compact[-1].lstrip().startswith('- '):
            nxt = lines.index(ln) + 1 if ln in lines else -1
            pass
        compact.append(ln)
    # 逐个 block 处理：空行分隔
    blocks, cur = [], []
    for ln in lines:
        if ln.strip() == '':
            if cur: blocks.append(cur); cur = []
        else:
            cur.append(ln)
    if cur: blocks.append(cur)

    used = set()
    body, toc = [], []
    title = '文档'
    for blk in blocks:
        first = blk[0]
        if first.startswith('# ') and title == '文档':
            title = first[2:].strip()
            body.append('<h1 id="top">%s</h1>' % inline_md(title))
            continue
        if first.startswith('## '):
            t = first[3:].strip(); sid = slug(t, used)
            body.append('<h2 id="%s">%s</h2>' % (sid, inline_md(t)))
            toc.append(('h2', sid, t))
            for extra in blk[1:]:
                if extra.strip():
                    body.append('<p class="srch">%s</p>' % inline_md(extra.strip()))
            continue
        if first.startswith('### '):
            t = first[4:].strip(); sid = slug(t, used)
            body.append('<h3 id="%s">%s</h3>' % (sid, inline_md(t)))
            toc.append(('h3', sid, t))
            for extra in blk[1:]:
                if extra.strip():
                    body.append('<p class="srch">%s</p>' % inline_md(extra.strip()))
            continue
        if first.startswith('> '):
            t = ' '.join(x[2:] if x.startswith('> ') else x for x in blk).strip()
            body.append('<blockquote class="srch">%s</blockquote>' % inline_md(t))
            continue
        if first.startswith('---'):
            body.append('<hr>')
            continue
        if first.lstrip().startswith('- '):
            items = []
            for x in blk:
                s = x.lstrip()
                if s.startswith('- '):
                    items.append(s[2:].strip())
                elif items:
                    items[-1] += ' ' + s.strip()
            body.append('<ul>' + ''.join('<li class="srch">%s</li>' % inline_md(i) for i in items) + '</ul>')
            continue
        body.append('<p class="srch">%s</p>' % inline_md(' '.join(x.strip() for x in blk)))

    toc_html = ''.join('<a class="%s" href="#%s">%s</a>' % ('sub' if k == 'h3' else '', sid, html.escape(t))
                       for k, sid, t in toc)
    edit = ''
    raw = ''
    if repo:
        edit = ('<a class="btn primary" target="_blank" rel="noopener" '
                'href="https://github.com/%s/edit/main/%s">✏️ 在 GitHub 上編輯此頁</a>' % (repo, srcfile))
        raw = ('<a class="btn" target="_blank" rel="noopener" '
               'href="https://github.com/%s/raw/main/菲佣常见问题与应对办法（经验整理）.docx">⬇️ 下載 Word 原件</a>'
               % repo)

    tpl = """<!DOCTYPE html>
<html lang="zh-Hans"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{title} · 香港菲傭（外傭）管理經驗整理 · GitHub Pages 公開版">
<style>{css}</style></head><body>
<div class="wrap">
<aside>
  <h4>搜索全文</h4>
  <input id="q" placeholder="例：出糧 / 匯款 / Alipay / 解僱" autocomplete="off">
  <div id="tocbox"><h4>目錄</h4><div class="toc">{toc}</div></div>
</aside>
<main>
  <div class="top">
    {edit}{raw}
    <a class="btn" href="#top">↑ 回到頂部</a>
    <span class="spacer"></span>
    <button class="btn" id="theme">🌓 深/淺色</button>
    <button class="btn" onclick="window.print()">🖨 列印／存 PDF</button>
  </div>
  <div class="note">
    本頁由 <code>SOURCE.md</code> 自動生成。想改內容？點右上角「在 GitHub 上編輯此頁」直接改 Markdown，
    提交後 GitHub Actions 會在一分鐘內重建本頁。<b>附三</b>列出所有尚未核實的事項，使用前請自行向勞工處／入境處核對。
  </div>
  {body}
  <hr>
  <p class="meta">本文件為微信群友經驗整理，不是法律意見。涉及金額、天數、法例條文者，以香港勞工處／入境處最新公告及《標準僱傭合約》正本為準。</p>
</main>
</div>
<div id="cnt"></div>
<script>{js}</script>
</body></html>"""
    return tpl.format(title=html.escape(title), css=CSS, js=JS, toc=toc_html, body='\n'.join(body),
                      edit=edit, raw=raw)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--repo', default=None)
    ap.add_argument('--srcfile', default='SOURCE.md')
    a = ap.parse_args()
    md = open(a.src, encoding='utf-8').read()
    html_out = render(md, a.repo, a.srcfile)
    open(a.out, 'w', encoding='utf-8').write(html_out)
    print('generated:', a.out, len(html_out), 'chars')

if __name__ == '__main__':
    main()
