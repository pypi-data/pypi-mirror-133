import sys
from pathlib import Path
from .utils import *

"""
## Need external data
    Equations
    Tables
    code block (parse markdown)

## Independent
    IPA
    Citation
    Figure (specify folder)

## Custom process
"""



def main():
    fp = sys.argv[1]
    process_citation(fp)
    process_dummy_table(fp)
    process_figure(fp)
    process_listing(fp)
    insert_equations(fp)
    process_ipa(fp)
    chapter_specific_manipulations(fp)


def process_ipa(fp):
    with open(fp, encoding="utf-8") as f:
        f = f.read()
    m = PAT_IPA.search(f)   
    while m is not None:
        ipa = m[1]
        anchor = m[0]
        ipa_html = f'`<span>{ipa}</span>`' + '{=html}' 
        ipa_tex = r'\ipatext{' + ipa + '}'
        repl = ipa_html + ipa_tex
        f = f.replace(anchor, repl)
        m = PAT_IPA.search(f)
    write_file(f, fp)



# Chapter specific function
def chapter_specific_manipulations(fp):
    if '03_system' in fp:
        with open(fp, encoding="utf-8") as f:
            f = f.read()
        f = f\
            .replace(r'\`', '`')\
            .replace(r'\[', '[')\
            .replace(r'\]', ']')\
            .replace(r'\"', '"')\
            .replace(r'\|', '|')\
            .replace(r'ALPHA', r'$\alpha$')\
            .replace(r'BETA', r'$\beta$')
        write_file(f, fp)


def insert_equations(fp):
    global EQUATIONS
    new_file = []
    for line in read_file_gen(fp):
        if line.startswith('EQ.'):
            line = '\n\n' + EQUATIONS[line.strip()] + '\n\n'
        new_file.append(line)
    write_file(''.join(new_file), fp)


def process_citation(fp):
    with open(fp, encoding="utf-8") as f:
        f = f.read()
    for i, pat in enumerate(PAT_CITE):
        while pat.search(f) is not None:
            m = pat.search(f)
            citekey = CITE_REPL[i](m[1])
            f = pat.sub(citekey, f, count=1)
    write_file(f, fp)
        

def process_figure(fp):
    new_file = []
    for line in read_file_gen(fp):
        if line.startswith('FIGURE: ') and line.rstrip().endswith('}'):
            fig_id = PAT_IMG.search(line.strip())[2]
            caption = PAT_IMG.search(line.strip())[1]
            fig_path = f"figures/{fig_id}.png"
            img = "![{}]({})".format(caption.strip(), fig_path)
            meta = '{#fig:' + fig_id + '}\n\n'
            line = img + meta
        new_file.append(line)
    write_file(''.join(new_file), fp)


def process_listing(fp):
    new_file = []
    for line in read_file_gen(fp):
        if line.startswith('CODE: ') and line.rstrip().endswith('}'):
            lst_id = PAT_CODE.search(line.strip())[2]
            caption = PAT_CODE.search(line.strip())[1]
            code, ext = CODEBLOCKS.get(lst_id, ["Code Block Not Found!", None ])
            meta = f'#lst:{lst_id} {ext} caption="{caption}"'
            line = '\n```{' + meta + '}\n' + code + '\n```\n'
        new_file.append(line)
    write_file(''.join(new_file), fp)


def process_dummy_table(fp):
    new_file = []
    for line in read_file_gen(fp):
        if 'TABLE.DUMMY' in line:
            line = line.replace('TABLE.DUMMY', DUMMY_TALBE)
        new_file.append(line)
    write_file(''.join(new_file), fp)
