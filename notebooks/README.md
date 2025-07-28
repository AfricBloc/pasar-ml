# 📓 Pasar ML – Notebooks

This folder contains **Jupyter notebooks** for experimentation, prototyping, and model testing across the Pasar ML agents.

---

## 📂 Structure & Purpose

### ✅ **00_pasar_ml_starter.ipynb**
- Main starter notebook for quick setup, shared utilities, and initial experiments.

### 🤖 **01_xiara_experiments.ipynb**
- Experiments for **Xiara**, the conversational agent.
- LLM prompts, RAG memory tests, product search prototypes.

### 🛡 **02_shogun_anomaly.ipynb**
- Security and anomaly detection experiments for **Shogun**.
- Isolation Forest, XGBoost, and fraud pattern testing.

### ⚖️ **03_resolute_disputes.ipynb**
- CV/NLP experiments for **Resolute**.
- Image matching (OpenCV, SSIM) and text discrepancy analysis.

### 💸 **04_xena_wallet.ipynb**
- Blockchain & wallet experiments for **Xena**.
- Smart contract calls, wallet commands, and transaction simulations.

---

## 📝 Notebook Guidelines

✅ **1. Use the Right Notebook:**  
Each agent has its own file to keep work organized.

✅ **2. Keep Outputs Clean:**  
Clear heavy cell outputs before committing:
```

Cell → All Output → Clear

```

✅ **3. Data Storage:**  
Do **not** store large datasets or model weights in this folder. Use `/data` or external storage.

✅ **4. New Notebooks:**  
Name new notebooks with a prefix:
```

05\_agentname\_topic.ipynb

```
Example:
```

05\_xiara\_prompt\_tuning.ipynb

````

✅ **5. Git Hygiene:**  
Notebook checkpoints (`.ipynb_checkpoints`) are ignored in `.gitignore`.

---

## 🚀 How to Run Notebooks

From repo root:
```bash
jupyter notebook
````

Or open them directly in **VS Code** (with the Jupyter extension).

```

---
