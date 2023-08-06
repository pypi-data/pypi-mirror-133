import sys
from pathlib import Path
from .utils import *
from .data_reader import equation_reader, code_reader

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
    process_table(fp)       #d
    process_figure(fp)      #d
    process_listing(fp)     #d
    process_equations(fp)   #d
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


def process_citation(fp):
    with open(fp, encoding="utf-8") as f:
        f = f.read()
    for i, pat in enumerate(PAT_CITE):
        while pat.search(f) is not None:
            m = pat.search(f)
            citekey = CITE_REPL[i](m[1])
            f = pat.sub(citekey, f, count=1)
    write_file(f, fp)


def process_table(fp):
    """Insert dummpy tables before table anchors. 
       Work in conjunction with insertTables.lua
    """
    new_file = []
    for line in read_file_gen(fp):
        if line.startswith('Table: ') and PAT_TABLE.match(line):
            line = '\n{}\n{}'.format(DUMMY_TALBE, line)
        new_file.append(line)
    write_file(''.join(new_file), fp)

        
def process_figure(fp, fig_dir="figures/"):
    fig_dir = Path(str(fig_dir))  # to do: arbitrary file ext.
    new_file = []
    for line in read_file_gen(fp):
        if line.startswith('FIGURE: '):
            m = PAT_IMG.match(line)
            if m is None: continue
            caption, id_ = m[1], m[2]
            fig_path = list(fig_dir.glob("{id_}*"))[0]
            img = "![{}]({})".format(caption.strip(), fig_path)
            meta = '{#fig:' + id_ + '}\n\n'
            line = img + meta
        new_file.append(line)
    write_file(''.join(new_file), fp)


def process_listing(fp, code_path="data/code.md"):
    CODEBLOCKS = code_reader(code_path)
    new_file = []
    for line in read_file_gen(fp):
        if line.startswith('CODE: '):
            m = PAT_CODE.match(line)
            if m is None: continue
            caption, id_ = m[1], m[2]
            code = CODEBLOCKS.get(id_, {})
            code, lang, attrs = code.get('code'), code.get('lang'), code.get('attrs')
            meta = f'#lst:{id_} {lang} caption="{caption}"'
            line = '\n```{' + meta + '}\n' + code + '\n```\n'
        new_file.append(line)
    write_file(''.join(new_file), fp)


def process_equations(fp, equation_path="data/equations"):
    EQUATIONS = equation_reader(equation_path)
    new_file = []
    for line in read_file_gen(fp):
        if line.startswith('EQUATION: '):
            m = PAT_EQUATION.match(line)
            if m is None: continue
            id_ = m[1]
            line = '\n\n' + EQUATIONS[id_] + '\n\n'
        new_file.append(line)
    write_file(''.join(new_file), fp)
