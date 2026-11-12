"""Story kit: write a campaign once, in English and Spanish side by side.

Every player-visible text is a pair (english, spanish). build.py turns the story modules in this folder into
datafiles/data/campaign.json (English) and merges the Spanish into datafiles/data/lang/es.json.
Steps and goal types are documented in scripts/scr_campaign/scr_campaign.gml; the canon in docs/STORIES.md.
"""
ES = {}          # english -> spanish, filled as texts are declared
ITEMS = []       # story items
NPCS = []        # story characters
ENEMIES = []     # story boss ships

def _t(pair):
    if pair is None: return None
    en, es = pair
    ES[en] = es
    return en

def say(npc, text, ok, name=None):
    d = {"do": "say", "npc": npc, "text": _t(text), "ok": _t(ok)}
    if name: d["name"] = _t(name)
    return d

def goal(type_, text, **kw):
    d = {"do": "goal", "type": type_}
    d.update(kw)
    d["text"] = _t(text)
    return d

def log(text): return {"do": "log", "text": _t(text)}
def get(item): return {"do": "get", "item": item}
def give(item): return {"do": "give", "item": item}
def reward(cash): return {"do": "reward", "cash": cash}
def unlock(good): return {"do": "unlock_good", "good": good}
def take(good, n): return {"do": "take", "good": good, "amount": n}
END = {"do": "end"}

def chapter(id_, title, level, vars_, steps):
    return {"id": id_, "title": _t(title), "level": level, "vars": vars_, "steps": steps}

def campaign(id_, title, year, intro, ending_title, ending_text, chapters):
    return {"id": id_, "title": _t(title), "year": year, "intro": _t(intro),
            "ending_title": _t(ending_title), "ending_text": _t(ending_text), "chapters": chapters}

def item(id_, name, desc, effect=""):
    ITEMS.append({"id": id_, "name": _t(name), "kind": "quest", "effect": effect, "desc": _t(desc)})

def npc(id_, name, role, female, seed, portrait="portrait_sailor"):
    NPCS.append({"id": id_, "name": _t(name), "portrait": portrait, "look": {"role": role, "female": female, "seed": seed}})

def enemy(id_, name, hp, guns, reload, thaco, booty, sprite, acc=8):
    ENEMIES.append({"id": id_, "name": _t(name), "hp": hp, "guns": guns, "reload": reload, "thaco": thaco, "booty": booty,
                    "level": 99, "sprite": sprite, "behavior": "relentless", "unique": True, "acc": acc})
