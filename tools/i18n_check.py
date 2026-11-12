#!/usr/bin/env python3
"""Lists player-visible English texts that have no entry in a language table.

Usage: python3 tools/i18n_check.py [es] [--all]
  Scans the GML scripts (string literals that read like text) and the translatable fields of
  datafiles/data/*.json (the same field list as I18N_DATA_FIELDS in scr_i18n.gml).
  --all prints every text found instead of only the missing ones (as JSON, ready to translate).
"""
import json, re, sys, glob, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'game', 'ExchangeTides')
FIELDS = {"name", "desc", "title", "text", "intro", "ok", "bio", "closed_reason", "greeting", "months", "ship_names", "ship_name", "pirate_names", "label", "role"}
SKIP_SCRIPTS = {"scr_selftest", "scr_i18n"}
# Literals the scan picks up that are not player-visible (comments, examples, internal keys).
NOT_TEXT = {"bring it here", "by end of February", "high month", "low month", "G", "PORT_LAYOUTS", "SETTINGS",
            "Storms -50%, Your gunnery +15", "Customs seizures 10%", "Missing data file: ", "March 1702", "Week 2, March 1702"}
LIT = re.compile(r'"((?:[^"\\]|\\.)*)"')

def code_texts():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'scripts', '*', '*.gml'))):
        if os.path.basename(os.path.dirname(f)) in SKIP_SCRIPTS:
            continue
        for line in open(f, encoding='utf-8'):
            code = line.split('//')[0] if '"' not in line.split('//')[0][-1:] else line
            for m in LIT.finditer(line):
                s = m.group(1)
                # prose: has a letter and either a space or a capital; not a sprite/file/id
                if not re.search(r'[A-Za-z]', s): continue
                if not (' ' in s.strip() or re.match(r'[A-Z]', s)): continue
                if re.fullmatch(r'[a-z0-9_|:.,/ -]+', s) and not ' ' in s.strip(): continue
                if s.endswith('.json') or s.endswith('.png') or s.startswith('[SELFTEST]'): continue
                out.append(s.encode().decode('unicode_escape') if '\\' in s else s)
    return out

def data_texts():
    out = []
    def walk(o, key=None):
        if isinstance(o, dict):
            for k, v in o.items(): walk(v, k)
        elif isinstance(o, list):
            for v in o:
                if isinstance(v, str):
                    if key in FIELDS: out.append(v)
                else: walk(v, key)
        elif isinstance(o, str) and key in FIELDS:
            out.append(o)
    for f in sorted(glob.glob(os.path.join(ROOT, 'datafiles', 'data', '*.json'))):
        if f.endswith('routes.json') or f.endswith('npc_parts.json'): continue
        walk(json.load(open(f, encoding='utf-8')))
    parts = json.load(open(os.path.join(ROOT, 'datafiles', 'data', 'npc_parts.json'), encoding='utf-8'))
    for r in parts.get('roles', {}).values():
        if isinstance(r, dict) and 'title' in r: out.append(r['title'])
    return out

def main():
    lang = next((a for a in sys.argv[1:] if not a.startswith('--')), 'es')
    texts = list(dict.fromkeys(code_texts() + data_texts()))
    if '--all' in sys.argv:
        print(json.dumps(texts, ensure_ascii=False, indent=1)); return
    table = json.load(open(os.path.join(ROOT, 'datafiles', 'data', 'lang', lang + '.json'), encoding='utf-8'))
    same = set(table.get("_same", []))   # names that stay as they are in this language
    missing = [t for t in texts if t not in table and t not in same and t not in NOT_TEXT]
    for t in missing: print(repr(t))
    print(f"{len(missing)} of {len(texts)} texts missing from {lang}.json", file=sys.stderr)
    sys.exit(1 if missing else 0)

if __name__ == '__main__':
    main()
