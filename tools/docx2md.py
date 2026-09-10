# -*- coding: utf-8 -*-
"""把《菲佣常见问题与应对办法（经验整理）.docx》转成 Markdown 源文件。
运行（需要 python-docx）：
  C:/Users/FRANKIE/.workbuddy/binaries/python/envs/default/Scripts/python.exe tools/docx2md.py
"""
import re, os
from docx import Document

SRC = os.environ.get('FDH_DOCX', r'C:/Users/FRANKIE/Desktop/菲佣/菲佣常见问题与应对办法（经验整理）.docx')
OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SOURCE.md'))

def esc(t):
    t = t.replace('\\', '\\\\')
    t = re.sub(r'(?m)^(\s*)(#{1,6})(\s)', r'\1\\\2\3', t)
    t = re.sub(r'(?m)^(\s*)(>)(\s)', r'\1\\\2\3', t)
    return t

def runs_to_md(runs, drop_bullet=False):
    out = []
    pending_drop = drop_bullet
    for r in runs:
        t = r.text
        if pending_drop:
            i = t.find('•')
            if i < 0:
                continue
            t = t[i + 1:].lstrip()
            pending_drop = False
        if not t:
            continue
        t = esc(t)
        if r.italic:
            out.append('*' + t + '*')
        elif r.bold:
            out.append('**' + t + '**')
        else:
            out.append(t)
    return ''.join(out)

def main():
    d = Document(SRC)
    lines = []
    for p in d.paragraphs:
        if not p.text.strip():
            continue
        style = p.style.name
        if style == 'Title':
            lines += ['# ' + runs_to_md(p.runs).strip(), '']
        elif style == 'Heading 1':
            lines += ['', '## ' + runs_to_md(p.runs).strip(), '']
        elif style == 'Heading 2':
            lines += ['', '### ' + runs_to_md(p.runs).strip(), '']
        else:
            all_italic = bool(p.runs) and all(r.italic for r in p.runs)
            is_bullet = p.text.lstrip().startswith('•')
            body = runs_to_md(p.runs, drop_bullet=is_bullet).strip()
            if all_italic:
                lines.append('> ' + body.strip('*'))
            elif is_bullet:
                lines.append('- ' + body)
            else:
                lines.append(body)
            lines.append('')
    md = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip() + '\n'
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(md)
    print('written:', OUT, len(md), 'chars,', md.count('\n'), 'lines')

if __name__ == '__main__':
    main()
