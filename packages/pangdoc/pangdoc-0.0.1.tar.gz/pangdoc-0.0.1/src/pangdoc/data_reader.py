#%%
import json
import pypandoc


def code_reader(fp='data/code.md'):
    ast = pypandoc.convert_file(fp, 'json', format='md')
    ast = json.loads(ast)

    code_blocks = {}
    for bl in ast.get('blocks', []):
        if bl.get('t') != 'CodeBlock': continue
        c = bl.get('c', [])
        if len(c) != 2: continue
        meta, code = c[0], c[1]
        lst_id = meta[0]
        attrs = meta[1]
        lang = ""
        if len(attrs) >= 1:
            lang = attrs[0]
        code_blocks[lst_id] = {
            'lang': lang,
            'attrs': attrs,
            'code': code
        }
    return code_blocks


# %%

# %%
