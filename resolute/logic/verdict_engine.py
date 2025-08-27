from typing import List, Tuple
from resolute.api.schemas import ImageAnalysisResult, VerdictEnum

def make_verdict(
    image_results: List[ImageAnalysisResult],
    text_res: dict
) -> Tuple[VerdictEnum, float, str]:
    """
    Combine image + text analysis results into a verdict.

    Args:
        image_results: List of ImageAnalysisResult objects (ssim, resnet, etc.)
        text_res: Dict from TextAnalysisResult

    Returns:
        verdict: one of REFUND_BUYER | RELEASE_SELLER | ESCALATE_ADMIN
        confidence: float [0.0, 1.0]
        report: str (human-readable reasoning)
    """

    # ----  Flags ----
    image_mismatches = [res for res in image_results if res.mismatch]
    text_discrepancy = text_res.get("discrepancy", False)

    # ---- Confidence logic ----
    confidence = 0.5  # base

    if image_mismatches:
        confidence += 0.2
    if text_discrepancy:
        confidence += 0.2
    if len(image_mismatches) == len(image_results) and text_discrepancy:
        confidence += 0.1  # strong signal if *everything* disagrees

    confidence = min(confidence, 1.0)

    # ---- Verdict ----
    if image_mismatches and text_discrepancy:
        verdict = "REFUND_BUYER"
    elif not image_mismatches and not text_discrepancy:
        verdict = "RELEASE_SELLER"
    else:
        verdict = "ESCALATE_ADMIN"

    # ---- Report ----
    img_parts = [
        f"{res.method}: score={res.score:.3f}, mismatch={res.mismatch}"
        for res in image_results
    ]
    txt_part = f"text: sim={text_res.get('similarity', 0):.3f}, discrepancy={text_discrepancy}"
    report = " | ".join(img_parts + [txt_part])

    return verdict, confidence, report
