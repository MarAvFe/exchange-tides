"""Tolerant converter for Tradewinds 2 XML-ish config files -> JSON.

The game's parser accepts things strict XML rejects: tag names starting with
digits, attributes without separating spaces, duplicate attributes (last wins),
'<' inside quoted attribute values, and // line comments.
Output: element -> dict of attributes + children; repeated child tags become
lists; text-only elements become strings; mixed text goes to "#text".
usage: xml2json.py IN_DIR OUT_DIR"""
import json, os, re, sys

TOKEN = re.compile(r'<!--.*?-->|<(/?)([^\s/>"]+)((?:[^>"]|"[^"]*")*?)(/?)>', re.S)
ATTR = re.compile(r'([^\s=/"]+)\s*=\s*"([^"]*)"')

def parse(s):
    s = re.sub(r'(^|[\s>])//[^\n]*', r'\1', s)
    root = {'tag': '#root', 'attrs': {}, 'kids': [], 'text': []}; stack = [root]; pos = 0
    for m in TOKEN.finditer(s):
        stack[-1]['text'].append(s[pos:m.start()]); pos = m.end()
        if m.group(0).startswith('<!--'): continue
        close, tag, attrs, selfclose = m.groups()
        if close:
            # pop to the matching open tag; tolerate stray closers
            for i in range(len(stack) - 1, 0, -1):
                if stack[i]['tag'] == tag: del stack[i:]; break
            continue
        node = {'tag': tag, 'attrs': dict(ATTR.findall(attrs)), 'kids': [], 'text': []}
        stack[-1]['kids'].append(node)
        if not selfclose: stack.append(node)
    stack[-1]['text'].append(s[pos:])
    return root

def conv(n):
    d = dict(n['attrs'])
    for k in n['kids']:
        v = conv(k)
        if k['tag'] in d:
            if not isinstance(d[k['tag']], list) or k['tag'] in n['attrs']: d[k['tag']] = [d[k['tag']]]
            d[k['tag']].append(v)
        else: d[k['tag']] = v
    t = ''.join(n['text']).strip()
    if not d: return t
    if t: d['#text'] = t
    return d

if __name__ == '__main__':
    src, dst = sys.argv[1:3]; os.makedirs(dst, exist_ok=True)
    for f in sorted(os.listdir(src)):
        if f.endswith('.txt'):
            out = conv(parse(open(os.path.join(src, f), encoding='latin1').read()))
            json.dump(out, open(os.path.join(dst, f[:-4] + '.json'), 'w'), indent=1, ensure_ascii=False)
    print('converted', len(os.listdir(dst)), 'files ->', dst)
