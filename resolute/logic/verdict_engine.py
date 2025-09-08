from typing import List, Tuple
from resolute.api.schemas import ImageAnalysisResult, VerdictEnum

def make_verdict(
    image_results: List[ImageAnalysisResult],
    text_res: dict
) -> Tuple[VerdictEnum, float, str]:
    """
    Combine image + text analysis results into a verdict.

    Args:
        image_results: List of ImageAnalysisResult objects (ssim, resnet, color, etc.)
        text_res: Dict from TextAnalysisResult

    Returns:
        verdict: one of REFUND_BUYER | RELEASE_SELLER | ESCALATE_ADMIN
        confidence: float [0.0, 1.0]
        report: str (human-readable reasoning)
    """

    # ---- Extract mismatches ----
    mismatches = {res.method: res for res in image_results if res.mismatch}
    text_discrepancy = text_res.get("discrepancy", False)

    # ---- Confidence base ----
    confidence = 0.5
    verdict = "ESCALATE_ADMIN"

    # ---- Image weighting ----
    if "color_histogram" in mismatches:
        confidence += 0.3  # strong signal: buyer says "wrong color"
    if "ssim" in mismatches:
        confidence += 0.2  # scratches/structural issues
    if "resnet" in mismatches:
        confidence += 0.2  # deeper feature-level mismatch

    # ---- Text weighting ----
    if text_discrepancy:
        confidence += 0.2

    confidence = min(confidence, 1.0)

    # ---- Verdict logic ----
    if mismatches and text_discrepancy:
        verdict = "REFUND_BUYER"
    elif mismatches and not text_discrepancy:
        # If only color mismatch but text matches → still refund buyer
        if "color_histogram" in mismatches:
            verdict = "REFUND_BUYER"
        else:
            verdict = "ESCALATE_ADMIN"
    elif not mismatches and text_discrepancy:
        verdict = "REFUND_BUYER"
    else:
        verdict = "RELEASE_SELLER"

    # ---- Report ----
    img_parts = [
        f"{res.method}: score={res.score:.3f}, mismatch={res.mismatch}"
        for res in image_results
    ]
    txt_part = f"text: sim={text_res.get('similarity', 0):.3f}, discrepancy={text_discrepancy}"
    report = " | ".join(img_parts + [txt_part])

    return verdict, confidence, report
