# resolute/analyzers/text_checker.py
from typing import List, Tuple
from ._keywords import COLOR_WORDS, CONDITION_WORDS

def _load_spacy():
    import spacy
    try:
        return spacy.load("en_core_web_md")
    except Exception:
        # fallback to sm if md isn't installed; warn in notes
        return spacy.load("en_core_web_sm")

def _extract_aspects(text: str) -> List[str]:
    t = text.lower()
    hits = []
    for c in COLOR_WORDS:
        if c in t:
            hits.append(f"color:{c}")
    for c in CONDITION_WORDS:
        if c in t:
            hits.append(f"condition:{c}")
    return hits

def _aspect_conflict(claim_aspects: List[str], desc_aspects: List[str]) -> bool:
    # conflict if claim mentions a specific aspect that contradicts description
    # e.g., claim says color:red but description says color:blue
    claim_colors = {a.split(":")[1] for a in claim_aspects if a.startswith("color:")}
    desc_colors  = {a.split(":")[1] for a in desc_aspects  if a.startswith("color:")}
    if claim_colors and desc_colors and not claim_colors.intersection(desc_colors):
        return True
    # condition mismatch heuristic: claim contains 'scratched/damaged' while desc has 'new'
    claim_cond = {a.split(":")[1] for a in claim_aspects if a.startswith("condition:")}
    desc_cond  = {a.split(":")[1] for a in desc_aspects  if a.startswith("condition:")}
    if "scratched" in claim_cond and ("new" in desc_cond or "mint" in desc_cond):
        return True
    return False

def analyze_claim_vs_description(claim_text: str, product_description: str):
    nlp = _load_spacy()
    doc_claim = nlp(claim_text)
    doc_desc  = nlp(product_description)
    sim = float(doc_claim.similarity(doc_desc))

    claim_aspects = _extract_aspects(claim_text)
    desc_aspects  = _extract_aspects(product_description)
    conflict = _aspect_conflict(claim_aspects, desc_aspects)

    discrepancy = (sim < 0.65) or conflict  # starting threshold
    notes = None
    if nlp.meta.get("name") == "en_core_web_sm":
        notes = "spaCy sm model has weak vectors; consider en_core_web_md or Sentence-Transformers."

    from resolute.api.schemas import TextAnalysisResult
    return TextAnalysisResult(
        similarity=sim,
        discrepancy=discrepancy,
        matched_aspects=sorted(set(claim_aspects + desc_aspects)),
        notes=notes
    )
