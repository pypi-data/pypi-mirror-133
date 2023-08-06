from spacy.language import Language 
from spacy.tokens import Doc

_d2c = {
  "nsubj": "主语",
  "csubj": "主语",
  "nsubjpass": "主语", 
  "advmod": "状语",
  "dative": "间接宾语",
  "intj": "感叹语",
  "aux": "助动词",
  "neg": "否定词",
  "auxpass": "助动词",
  "cc": "连词",
  "preconj": "连接",
  "acomp": "表语",
  "expl": "形式主语",
  "agent": "状语",
  "mark": "连词",
  "prt": "小品词",
}

verb_tags = {
  "VBZ": "动词第三人称单数",
  "VBN": "动词过去分词",
  "VBG": "动词现在分词",
  "VBD": "动词过去式",
  "VB": "动词原形",
  "VBP": "动词原形",
}

cop_verbs = ["be", "prove", "seem", "remain", "get", "look", "feel", "sound", "turn", "smell", "taste", "become"]

def _get_root_explanation(doc, r, structure):
  ele = doc[r["element"]]
  deps = [doc[s["element"]].dep_ for s in structure]
  explanation = None
  if ele.pos_ not in ["VERB", "AUX"]:
    explanation = None
  elif any([e == "attr" for e in deps]) and any([e == "expl" for e in deps]):
    explanation = "谓语"
  elif ele.lemma_ in cop_verbs and any([e in ["attr", "oprd", "acomp", "xcomp", "advcl"] for e in deps]):  
    explanation = "系动词"
  elif ele.pos_ == "AUX" and any([e in ["prep", "advmod"] for e in deps]):  
    explanation = "系动词"
  elif ele.tag_ in verb_tags.keys():
    explanation = verb_tags[ele.tag_]
  else:
    explanation = ele.tag_ 
  return explanation

def _get_conj_explanation(doc, c, structure):
  explanation = None
  ele = doc[c["element"]]
  if c["end"] - c["start"] == 1 and doc[c["element"]].pos_ in ["VERB", "AUX"] and ele.tag_ in verb_tags.keys():
    explanation = verb_tags[ele.tag_]
  else:
    explanation = "并列连句"
  return explanation

def _get_oprd_explanation(doc, o, structure):
  deps = [doc[s["element"]].dep_ for s in structure]
  explanation = None
  if any([e in ["dobj"] for e in deps]):  
    explanation = "补语"
  else:
    explanation = "表语"
  return explanation

def _get_attr_explanation(doc, o, structure):
  deps = [doc[s["element"]].dep_ for s in structure]
  explanation = None
  if any([e in ["expl"] for e in deps]):  
    explanation = "主语"
  else:
    explanation = "表语"
  return explanation

def _get_npadvmod_explanation(doc, t, structure):
  explanation = None
  if t["end"] - t["start"] == 1 and doc[t["element"]].pos_ == "PROPN":
    explanation = "插入语"
  else:
    explanation = "状语"
  return explanation
  
def _get_prep_explanation(doc, t, structure):
  roots = [doc[s["element"]] for s in structure if doc[s["element"]].dep_=="ROOT"]
  assert(len(roots) == 1)
  root = roots[0]
  explanation = None
  deps = [doc[s["element"]].dep_ for s in structure]
  explanation = None
  if root.pos_ == "AUX" and all([e not in ["attr", "oprd"] for e in deps]):
    explanation = "表语"
  else:
    explanation = "状语"
  return explanation

def _get_dobj_explanation(doc, t, structure):
  deps = [doc[s["element"]].dep_ for s in structure]
  explanation = None
  if any([e in ["dative"] for e in deps]):  
    explanation = "直接宾语"
  else:
    explanation = "宾语"
  return explanation
 
def _get_xcomp_explanation(doc, t, structure):
  roots = [doc[s["element"]] for s in structure if doc[s["element"]].dep_=="ROOT"]
  assert(len(roots) == 1)
  root = roots[0]
  explanation = None
  if root.pos_ == "AUX":
    explanation = "表语"
  else:
    explanation = "宾语"
  return explanation
 
def _get_ccomp_explanation(doc, t, structure):
  #deps = [doc[s["element"]].dep_ for s in structure]
  roots = [doc[s["element"]] for s in structure if doc[s["element"]].dep_=="ROOT"]
  assert(len(roots) == 1)
  root = roots[0]
  explanation = None
  if root.pos_ == "AUX":
    explanation = "表语"
  else:
    explanation = "宾语"
  return explanation
 
def _get_advcl_explanation(doc, t, structure):
  deps = [doc[s["element"]].dep_ for s in structure]
  roots = [doc[s["element"]] for s in structure if doc[s["element"]].dep_=="ROOT"]
  assert(len(roots) == 1)
  root = roots[0]
  explanation = None
  cop_deps = ["acomp", "prep", "attr"]
  if root.pos_ == "AUX" and all([d not in deps for d in cop_deps]):
    explanation = "表语"
  else:
    explanation = "状语"
  return explanation
 
def _analyze(doc, t, structure):
  dep = doc[t["element"]].dep_
  explanation = None
  if dep == "ROOT":
    explanation = _get_root_explanation(doc, t, structure)  
  elif dep == "conj":
    explanation = _get_conj_explanation(doc, t, structure)
  elif dep == "oprd":
    explanation = _get_oprd_explanation(doc, t, structure)
  elif dep == "attr":
    explanation = _get_attr_explanation(doc, t, structure)
  elif dep == "punct":
    explanation = None
  elif dep == "prep":
    explanation = _get_prep_explanation(doc, t, structure)
  elif dep == "npadvmod":
    explanation = _get_npadvmod_explanation(doc, t, structure)
  elif dep == "dobj":
    explanation = _get_dobj_explanation(doc, t, structure)
  elif dep == "xcomp":
    explanation = _get_xcomp_explanation(doc, t, structure)
  elif dep == "ccomp":
    explanation = _get_ccomp_explanation(doc, t, structure)
  elif dep == "advcl":
    explanation = _get_advcl_explanation(doc, t, structure)
  elif dep in _d2c.keys():
    explanation = _d2c[dep]
  else:
    explanation = dep
  t["explanation"] = explanation
  return t

def en_trs(doc, structure):
  structure_with_explanation = []
  for t in structure:
    _t = _analyze(doc, t, structure)
    structure_with_explanation.append(_t)
  return structure_with_explanation
