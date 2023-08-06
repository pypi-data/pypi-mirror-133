from spacy.language import Language 
from spacy.tokens import Doc

def _is_verb_like(e):
  return e.pos_ in ["VERB", "AUX"]

def _has_no_subject(e):
  children_deps = [x.dep_ for x in e.children]
  return all([subj not in children_deps for subj in ["nsubj", "nsubjpass"]])

def _get_predicate_range(p):
  start = p.i
  prt = [c.i for c in p.children if c.dep_ == "prt"]
  end  = max(prt)+1 if len(prt) > 0 else p.i+1
  return (start, end)

def _get_predicate(doc: Doc, nlp: Language):
  root = [r for r in doc if r.dep_=="ROOT"][0]
  p_conj = [e for e in root.children if e.dep_ == "conj" and _is_verb_like(e) and _has_no_subject(e)]
  predicates = sum([p_conj], [root])

  predicate_info = []
  predicate_related = []

  for p in predicates:
    start, end = p.i, p.i+1
    predicate_related.extend(range(start, end))
    _info = {
      "start": start,
      "end": end,
      "text": doc[start:end].text,
      "element": p.i,
      "is_root": True if p.dep_=="ROOT" else False,
    }
    predicate_info.append(_info)
  return (predicate_info, predicate_related)

def get_tree(doc: Doc, nlp: Language):
  store = []

  p_info, p_related = _get_predicate(doc, nlp)
  store.extend(p_info)

  roots = [doc[e["element"]] for e in p_info]
  children = [t for t in sum([list(r.children) for r in roots], []) if t.i not in p_related]

  for dc in children:
    dc_ranges = [e.i for e in dc.subtree]
    start, end = min(dc_ranges), max(dc_ranges)+1
    _info = {
      "start": start,
      "end": end,
      "text": doc[start:end].text,
      "element": dc.i, 
      "is_root": False,
    }
    store.append(_info)

  ordered_store = sorted(store, key=lambda d: d["start"]) 
  return ordered_store 


