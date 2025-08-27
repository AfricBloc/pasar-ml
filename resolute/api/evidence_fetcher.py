import os
import hashlib
import datetime
from typing import List, Tuple
from resolute.api.schemas import EvidenceItem
from shared.logging.logger import logger

def _file_metadata(path: str, file_type: str) -> EvidenceItem:
    stats = os.stat(path)
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        sha256.update(f.read())
    return EvidenceItem(
        path=path,
        type=file_type,
        size_bytes=stats.st_size,
        created_at=datetime.datetime.fromtimestamp(stats.st_ctime),
        sha256=sha256.hexdigest()
    )

def load_local_images(buyer_paths: List[str], seller_paths: List[str]) -> Tuple[List[EvidenceItem], List[EvidenceItem]]:
    missing = [p for p in (buyer_paths + seller_paths) if not os.path.exists(p)]
    if missing:
        logger.error("Missing evidence files", extra={"missing": missing})
        raise FileNotFoundError(f"Missing evidence files: {missing}")

    buyer_items = [_file_metadata(p, "image") for p in buyer_paths]
    seller_items = [_file_metadata(p, "image") for p in seller_paths]

    logger.info("Evidence loaded", extra={
        "buyerEvidence": [b.dict() for b in buyer_items],
        "sellerEvidence": [s.dict() for s in seller_items]
    })

    return buyer_items, seller_items

