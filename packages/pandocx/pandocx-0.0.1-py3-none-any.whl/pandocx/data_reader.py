#%%
import re
from utils import to_ast, read_file_gen
from pprint import pprint

PAT_EQ_END = re.compile(r'\$\$ ?{#eq:([a-zA-Z0-9-]+)}')


def equation_reader(fp="data/equations.md"):
    in_eq = False
    blocks = {}
    content = ""
    for line in read_file_gen(fp):
        if line.strip() == '$$':
            in_eq = True
            content += line
            continue
        end_label = PAT_EQ_END.match(line.strip())
        if end_label:
            in_eq = False
            content += line
            id_ = end_label[1]
            blocks[id_] = content
            content = ""
            continue
        if in_eq:
            content += line
    return blocks
    

def code_reader(fp='data/code.md'):
    ast = to_ast(fp)
    blocks = {}
    for bl in ast.get('blocks', []):
        if bl.get('t') != 'CodeBlock': continue
        c = bl.get('c', [])
        if len(c) != 2: continue
        meta, code = c[0], c[1]
        lst_id = meta[0]
        attrs = meta[1]
        lang = ""
        if len(attrs) >= 1:
            lang = attrs[0].replace('#lst:', '')
        blocks[lst_id] = {
            'lang': lang,
            'attrs': attrs,
            'code': code
        }
    return blocks


# %%

# %%
ast = eq

blocks = {}
for bl in ast.get('blocks', []):
    if bl.get('t') != 'Para': continue
    Para = bl.get('c', [])
    for bl in Para:



    if bl.get('t') != 'DisplayMath': continue
    c = bl.get('c', [])
    if len(c) != 2: continue
    meta, code = c[0], c[1]
    lst_id = meta[0]
    attrs = meta[1]
    lang = ""
    if len(attrs) >= 1:
        lang = attrs[0]
    blocks[lst_id] = {
        'lang': lang,
        'attrs': attrs,
        'code': code
    }
return blocks