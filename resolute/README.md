````markdown
# Resolute Engine – Dispute Resolution Agent (Pasar)

**Resolute Engine** is the automated dispute resolver for Pasar. It uses computer vision and NLP to analyze buyer/seller evidence and return fair verdicts.

---

## 📦 Features
- 🖼 Image Comparison: Checks if received product matches listing
- 📜 Text Discrepancy Analysis: Detects mismatched descriptions
- ⚖️ Automated Verdicts: Refund buyer, reject claim, or escalate

---

## 🚀 Run Locally

```bash
cd resolute
uvicorn main:app --reload --port 8003
````

---

## 🔌 API Endpoints

| Method | Endpoint          | Description                   |
| ------ | ----------------- | ----------------------------- |
| GET    | /                 | Health check endpoint         |
| POST   | /resolute/analyze | Submit dispute for evaluation |

---

## ⚙️ ML Models

* **SSIM + OpenCV** for image matching.
* **SpaCy + Transformers** for text analysis.
* **Rule-based engine** to combine evidence and output verdict.

---

## 🛠 Development Notes

* Media files handled via **Cloudinary** or IPFS.
* Verdicts sent back to backend → triggers escrow release/refund.

```
```
