from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import datetime

VerdictEnum = Literal["REFUND_BUYER", "RELEASE_SELLER", "ESCALATE_ADMIN"]

class DisputeEvidence(BaseModel):
    buyer_image_paths: List[str] = Field(default_factory=list)
    seller_image_paths: List[str] = Field(default_factory=list)
    claim_text: str
    product_description: str
    buyer_submitted_at: Optional[str] = None
    seller_listed_at: Optional[str] = None

class AnalyzeRequest(BaseModel):
    orderId: str
    productId: str
    disputeDetails: DisputeEvidence

class ImageAnalysisResult(BaseModel):
    method: str   # "ssim" | "resnet"
    score: float
    mismatch: bool
    notes: Optional[str] = None

class TextAnalysisResult(BaseModel):
    similarity: float
    discrepancy: bool
    matched_aspects: List[str] = []
    notes: Optional[str] = None

class EvidenceItem(BaseModel):
    path: str
    type: str   # "image" | "text"
    size_bytes: Optional[int]
    created_at: Optional[datetime.datetime]
    sha256: Optional[str]

class AnalyzeResponse(BaseModel):
    orderId: str
    productId: str
    verdict: VerdictEnum
    confidenceScore: float
    imageAnalysis: List[ImageAnalysisResult] = []  
    textAnalysis: Optional[TextAnalysisResult] = None
    analysisReport: str
    buyerEvidence: List[EvidenceItem] = []
    sellerEvidence: List[EvidenceItem] = []

class SubmitVerdictRequest(BaseModel):
    orderId: str
    verdict: VerdictEnum
    confidenceScore: float
