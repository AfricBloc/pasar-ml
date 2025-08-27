from fastapi import APIRouter, Header, HTTPException, Depends, Request
from typing import Optional, List
from .schemas import (
    AnalyzeRequest, AnalyzeResponse, SubmitVerdictRequest,
    ImageAnalysisResult, TextAnalysisResult, EvidenceItem, VerdictEnum
)
from resolute.logic.verdict_engine import make_verdict
from resolute.api.evidence_fetcher import load_local_images
from resolute.analyzers.image_analyzer import ssim_compare_images, resnet_cosine_pair
from resolute.analyzers.text_checker import analyze_claim_vs_description
from shared.auth.auth_utils import verify_internal_token    
from shared.logging.logger import logger

router = APIRouter()

def auth_guard(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    mock_request = Request(scope={"type": "http", "headers": [(b"authorization", f"Bearer {token}".encode())]})
    if not verify_internal_token(mock_request):
        raise HTTPException(status_code=403, detail="Invalid token")
    return True

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest, request: Request = Depends(auth_guard)):
    logger.info("Analyze request received", extra={"orderId": req.orderId, "productId": req.productId})

    try:
        buyer_items, seller_items = load_local_images(
            req.disputeDetails.buyer_image_paths, 
            req.disputeDetails.seller_image_paths
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))

    image_results: List[ImageAnalysisResult] = []

    if buyer_items and seller_items:
        # SSIM
        ssim_score = ssim_compare_images(buyer_items[0].path, seller_items[0].path)
        image_results.append(ImageAnalysisResult(
            method="ssim",
            score=ssim_score,
            mismatch=ssim_score < 0.5
        ))

        # ResNet cosine
        try:
            cos_score = resnet_cosine_pair(buyer_items[0].path, seller_items[0].path)
            image_results.append(ImageAnalysisResult(
                method="resnet",
                score=cos_score,
                mismatch=cos_score < 0.7
            ))
        except Exception as e:
            logger.warning("ResNet skipped", extra={"reason": str(e)})

    text_res = analyze_claim_vs_description(
        req.disputeDetails.claim_text, 
        req.disputeDetails.product_description
    )

    # pass dicts to verdict engine
    verdict, confidence, report = make_verdict(image_results, text_res.dict())

    resp = AnalyzeResponse(
        orderId=req.orderId,
        productId=req.productId,
        verdict=verdict,
        confidenceScore=confidence,
        imageAnalysis=image_results,
        textAnalysis=text_res,
        analysisReport=report,
        buyerEvidence=buyer_items,
        sellerEvidence=seller_items
    )

    logger.info("Analyze completed", extra={
        "orderId": req.orderId,
        "verdict": verdict,
        "confidence": confidence
    })
    return resp

@router.post("/verdict")
def submit_verdict(req: SubmitVerdictRequest, _: None = Depends(auth_guard)):
    logger.info("Verdict submitted", extra=req.dict())
    return {"status": "accepted", "orderId": req.orderId}
