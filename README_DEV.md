
## 📄 **README\_DEV.md**


# 🛠 Pasar ML Agents – Developer Notes

This file is **for the team only** — scratch notes, local setup quirks, and tips for building Pasar ML agents.

---

## ⚙️ Local Development Quickstart

### ✅ **1. Start Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
````

### ✅ **2. Install Requirements**

```bash
pip install -r requirements.txt
```

### ✅ **3. Run an Agent Locally**

```bash
cd xiara
uvicorn main:app --reload --port 8001
```

### ✅ **4. Spin Up Everything via Docker**

```bash
make up
```

(or `docker-compose up --build`)

---

## 🚩 Gotchas

* **.env File** – Required for all agents. Copy from `.env.example`:

  ```bash
  cp .env.example .env
  ```
* **Redis Must Be Running** – Xiara, Shogun, and others expect Redis on `localhost:6379`.
* **Model Weights** – Don’t commit `.pt`, `.h5`, `.pkl`, etc. (they’re already in `.gitignore`).

---

## 📓 Notebooks Workflow

* All ML experiments live in `/notebooks`
* Clear heavy outputs before commit:

  ```
  Cell → All Output → Clear
  ```
* Check `.ipynb_checkpoints` stays ignored.

---

## 📦 Docker Tips

* Rebuild everything from scratch:

  ```bash
  make rebuild
  ```
* Stop and remove containers & volumes (careful!):

  ```bash
  make reset
  ```

---

## 🔀 Branching Tips

* **`main`** – Stable / production.
* **`dev`** – Active development.
* **Feature branches** – Start from `dev`:

  ```bash
  git checkout dev
  git pull origin dev
  git checkout -b feature/<feature-name>
  ```

---

## ✅ Things To Do Next

* 🔹 Hook Xiara up to LangChain for real LLM responses.
* 🔹 Add anomaly detection logic to Shogun.
* 🔹 Build first CV pipeline in Resolute.
* 🔹 Connect Xena to a testnet wallet (Infura/Alchemy).

---

> **Note:** This file is **team-facing only**. Keep it lean — delete old notes once they’re in real docs or tickets.

```

---

📌 **Purpose of this file:**  
- **Quick reference** for **team-only dev notes** (not for external users).  
- Keeps “scratch notes” out of the main `README.md`.  

---

