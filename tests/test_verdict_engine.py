from resolute.logic.verdict_engine import make_verdict
from resolute.api.schemas import ImageAnalysisResult

def test_verdict_refund_buyer():
    img_res = [ImageAnalysisResult(method="ssim", score=0.3, mismatch=True)]
    text_res = {"similarity": 0.2, "discrepancy": True}
    verdict, conf, _ = make_verdict(img_res, text_res)
    assert verdict == "REFUND_BUYER"
    assert conf >= 0.7

def test_verdict_release_seller():
    img_res = [ImageAnalysisResult(method="ssim", score=0.9, mismatch=False)]
    text_res = {"similarity": 0.9, "discrepancy": False}
    verdict, conf, _ = make_verdict(img_res, text_res)
    assert verdict == "RELEASE_SELLER"

def test_verdict_escalate_admin():
    img_res = [ImageAnalysisResult(method="ssim", score=0.4, mismatch=True)]
    text_res = {"similarity": 0.8, "discrepancy": False}
    verdict, conf, _ = make_verdict(img_res, text_res)
    assert verdict == "ESCALATE_ADMIN"
