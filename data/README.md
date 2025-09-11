# 📊 Pasar Data Folder

This folder stores **datasets, sample files, and reference data** used for Pasar ML agents.

---

## 📂 Structure & Usage

- **raw/** → Original datasets (do not modify)
- **processed/** → Cleaned or transformed data
- **samples/** → Tiny CSV/JSON files for tests & demos

---

## ⚠️ Guidelines

- ❌ **DO NOT commit large files** (over ~50MB).
- ❌ **DO NOT commit production secrets** or private user data.
- ✅ Use `.gitignore` to exclude heavy datasets.
- ✅ Store big files on cloud storage (e.g., S3, GDrive) and document the download path here.

---

## 📜 Example

```

data/
├── raw/
│   └── sample\_transactions.csv
├── processed/
│   └── cleaned\_users.csv
└── samples/
└── tiny\_orders.json

```

data/
├── buyer/ # Buyer-uploaded evidence (mock images, claims, etc.)
├── seller/ # Seller listing evidence (mock images, descriptions, etc.)
├── samples/ # Small demo/test assets safe to commit
├── raw/ # Large unprocessed datasets (ignored in git)
└── processed/ # Preprocessed datasets (ignored in git)

---

## ✅ Notes

- Any ML notebooks should reference files **relative to the repo root**:

```python
df = pd.read_csv("data/samples/tiny_orders.json")
```
