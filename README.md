# 🛍️ Pasar ML Agents

Pasar is an **AI-powered marketplace infrastructure** designed for the next generation of commerce.
This repository contains the **machine learning (ML)** and **agentic services** that power Pasar’s smart, automated platform.

---

## 🌟 Overview

Pasar is built on a **multi-agent architecture**, where each agent handles a critical part of the marketplace:

* 🤖 **Xiara** – Conversational AI for buyers (product search, negotiation)
* 🛡 **Shogun** – Security & anomaly detection (logins, fraud detection)
* ⚖️ **Resolute** – Automated dispute resolution (image & text evidence analysis)
* 💸 **Xena** – Smart wallet assistant for sellers (funds management & reports)

These agents connect to the **Pasar backend services** (orders, products, disputes, wallet) and interact with **smart contracts** for escrow, access management, and wallet control.

---

## 🏗 Architecture

```
Buyer/Seller/Admin
│
Frontend (Web/Mobile)
│
Backend Services (Orders, Products, Wallet)
│
┌─────────────────────────────────────┐
│    Pasar ML Agent Services (this repo) │
│   • Xiara   • Shogun   • Resolute   • Xena │
└─────────────────────────────────────┘
│
Smart Contracts (Escrow, Access Manager, Wallet)
Redis (Cache & Pub/Sub)
PostgreSQL (Future DB Layer)
```

---

## 📦 Features by Agent

### 🤖 **Xiara** – Conversational AI Agent

* Product discovery & natural language search
* Negotiation using rules + LLM prompts
* Triggers payment flows

### 🛡 **Shogun** – Security Agent

* Detects suspicious logins & transactions
* Can flag users or pause escrow contracts

### ⚖️ **Resolute** – Dispute Resolution Engine

* Uses CV + NLP to assess disputes
* Returns verdicts (refund buyer, reject, escalate)

### 💸 **Xena** – Smart Wallet Manager

* Parses text/voice commands from sellers
* Handles transactions & generates reports

---

## 🚀 Getting Started

### 1️⃣ **Clone the Repository**

```bash
git clone https://github.com/yourusername/pasar-ml-agents.git
cd pasar-ml-agents
```

### 2️⃣ **Create Environment File**

```bash
cp .env.example .env
```

Edit `.env` and add your API keys, DB URLs, and blockchain credentials.

### 3️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Agents

Each agent is a **FastAPI service**.

Run them individually:

```bash
cd xiara
uvicorn main:app --reload --port 8001
```

```bash
cd shogun
uvicorn main:app --reload --port 8002
```

```bash
cd resolute
uvicorn main:app --reload --port 8003
```

```bash
cd xena
uvicorn main:app --reload --port 8004
```

✅ Assign different ports for each agent.
✅ Use `--reload` during development for hot reload.

Or run everything via Docker Compose:

```bash
docker-compose up --build
```

---

## 📂 Repo Structure

```
pasar-ml-agents/
├── xiara/           # Buyer conversational agent
├── shogun/          # Security & anomaly detection
├── resolute/        # Dispute resolution engine
├── xena/            # Smart wallet agent
├── shared/          # Shared config, logging, auth
├── scripts/         # Dev utility scripts
├── tests/           # Unit/integration tests
├── data/            # Sample datasets
├── infra/           # Deployment configs (Docker/K8s/Terraform)
├── docs/            # Documentation hub
├── requirements.txt
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## 🔗 Key Technologies

* **FastAPI** – API framework for all agents
* **LangChain + Hugging Face** – LLM orchestration for Xiara & Xena
* **OpenCV + SpaCy** – CV/NLP dispute resolution for Resolute
* **Scikit-learn + XGBoost** – Anomaly detection for Shogun
* **Redis + Celery** – Caching & async tasks
* **Web3.py** – Smart wallet & escrow contract control
* **Docker & Docker Compose** – Local and production orchestration
* **GitHub Actions** – CI/CD workflow

---

## 🧪 Development Notes

* ✅ All agents load environment variables from `.env` via `shared/config/settings.py`.
* ✅ Consistent logging is handled by `shared/logging/logger.py`.
* ✅ Internal API calls are protected by a shared token (`shared/auth/auth_utils.py`).
* ✅ Placeholder tests in `/tests` ensure CI runs cleanly.

---

## 🛠 Contribution Guide

1. **Create a feature branch**

   ```bash
   git checkout -b feature/<name>
   ```
2. **Follow Conventional Commits**

   * `feat:` new feature
   * `fix:` bug fix
   * `chore:` setup, dependencies
3. **Write tests** for new endpoints and modules.
4. **Open a Pull Request** to `dev` branch for review.

See [CONTRIBUTING.md](CONTRIBUTING.md) for full contributor guidelines.

---

## 📜 License

This project is currently private and under active development.
Future licensing will be defined at launch.
