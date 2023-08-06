import re

# IPA{nʲihoN}
PAT_IPA = re.compile(r'IPA{([^{}]+)}')
# FIGURE: Caption. {#fig:radicals-given-word}
PAT_IMG = re.compile(r'FIGURE: (.+?) {#fig:([a-zA-Z0-9-]+)}')
# CODE: Caption. {#lst:code-blcok}
PAT_CODE = re.compile(r'CODE: (.+?) {#lst:([a-zA-Z0-9-]+)}')
# Table: Caption. {#tbl:some-table}
PAT_TABLE = re.compile(r'Table: (.+?) {#tbl:([a-zA-Z0-9-]+)}')


PAT_CITE = [
    r'\\\[-\\(@[a-z]+[0-9]+[a-z]?)\\\]',
    r'\\\[\\(@[a-z]+[0-9]+[a-z]?(; ?\\@[a-z]+[0-9]+[a-z]?)*; ?\\@[a-z]+[0-9]+[a-z]?)\\\]',
    r'\\\[\\(@[a-z]+[0-9]+[a-z]?; ?\\@[a-z]+[0-9]+[a-z]?)\\\]',
    r'\\\[\\(@[a-z]+[0-9]+[a-z]?)\\\]',
    r'\\(@[a-z]+[0-9]+[a-z]? \\\[pp?\. ?[0-9-]+\\\])',
    r'\\(@[a-z]+[0-9]+[a-z]?)',
    r'\\(@(tbl|lst|eq|sec|fig):[a-z0-9-]+)',
    r'\\\[\\([a-zA-Z ]*@[a-z]+[0-9]+[a-z]?, p\. ?\d{1,})\\\]',
    r'\\\[\\([a-zA-Z ]*@[a-z]+[0-9]+[a-z]?, pp\. ?\d{1,}-\d{1,})\\\]',
]
PAT_CITE = [ re.compile(x) for x in PAT_CITE ]
CITE_REPL = [
    lambda x: "[-{}]".format(x),
    lambda x: "[{}]".format(x),
    lambda x: "[{}]".format(x),
    lambda x: "[{}]".format(x),
    lambda x: "{}".format(x.replace(r'\[', '[').replace(r'\]', ']')),
    lambda x: x,
    lambda x: x,
    lambda x: "[{}]".format(x),
    lambda x: "[{}]".format(x),
]

DUMMY_TALBE = """
| Placeholder | Table |
|-------------|-------|
| a           | b     |""".strip()


def read_file_gen(fp):
    with open(fp, encoding="utf-8") as f:
        for l in f: yield l


def read_file(fp):
    with open(fp, encoding="utf-8") as f:
        return f.read()


def write_file(s, fp):
    with open(fp, "w", encoding="utf-8") as f:
        f.write(s)
