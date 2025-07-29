

## 📄 **CONTRIBUTING.md**

# 🤝 Contributing to Pasar ML Agents

Welcome to the **Pasar ML Agents** project!  
This repo contains the AI agents that power Pasar — Xiara, Shogun, Resolute, and Xena.

---

## 📦 Project Structure

```

pasar-ml-agents/
├── xiara/         # Buyer conversational agent
├── shogun/        # Security & anomaly detection
├── resolute/      # Dispute resolution engine
├── xena/          # Smart wallet agent
├── shared/        # Shared settings, logging, auth
├── notebooks/     # Jupyter notebooks for ML experiments
├── docker/        # Dockerfiles for all agents
├── docker-compose.yml
├── requirements.txt
├── Makefile
└── CONTRIBUTING.md

````

---

## 🚀 Developer Setup Guide

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/AfricBloc/pasar-ml.git
cd pasar-ml
````

---

### 2️⃣ **Create Your Virtual Environment**

Use Python 3.11 (recommended).

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

---

### 3️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

(Dependencies include FastAPI, Pydantic, LangChain, Redis, etc.)

---

### 4️⃣ **Copy and Configure .env**

```bash
cp .env.example .env
```

* Add API keys, DB URLs, and blockchain credentials (if needed).

---

### 5️⃣ **Run Services (Development Mode)**

Each agent is a FastAPI app:

```bash
cd xiara
uvicorn main:app --reload --port 8001
```

Do the same for **Shogun, Resolute, Xena** (ports 8002–8004).

---

### 6️⃣ **Run via Docker Compose**

Make sure Docker is installed, then:

```bash
docker-compose up --build
```

✅ Xiara → `http://localhost:8001`
✅ Shogun → `http://localhost:8002`
✅ Resolute → `http://localhost:8003`
✅ Xena → `http://localhost:8004`

---

### 7️⃣ **Run Notebooks for ML Work**

```bash
jupyter notebook
```

Open `notebooks/` folder and start experimenting.

---

## 🔀 Branch Workflow

* **`main`** → Always production-ready code.
* **`dev`** → Active development branch.

**For new features:**

```bash
git checkout dev
git pull origin dev
git checkout -b feature/<feature-name>
```

---

## 📜 Commit Guidelines (Conventional Commits)

Use [Conventional Commit](https://www.conventionalcommits.org/) style:

* `feat:` → New feature (e.g. `feat: add dispute analysis endpoint`)
* `fix:` → Bug fix
* `docs:` → Documentation only
* `refactor:` → Code refactor without feature change
* `chore:` → Build, config, or maintenance

**Examples:**

```bash
git commit -m "feat: add login anomaly detection MVP"
git commit -m "docs: update contributing guide"
```

---

## ✅ Code Style

* **Python:** Follow **PEP8**
* Use **type hints** for all functions
* Use **Pydantic models** for request/response schemas in FastAPI

---

## 🔍 Pull Request Guidelines

1. **Base branch:** Always `dev`.
2. Write a **clear title & description**.
3. Request review from another team member.
4. Ensure all CI checks pass before merge.

---

## 🛠 Useful Commands

```bash
make up         # Start all Docker services
make down       # Stop containers
make logs       # View logs
make rebuild    # Full rebuild
```

(Use `Makefile` or run Docker Compose commands directly.)

---

## 📬 Support

For questions or discussions:

* Open an issue on GitHub
* Or contact the team lead via Slack/Email

---

Thanks for contributing to **Pasar ML Agents**! 🚀

```

---

✅ **This file does double duty:**  
- It’s a **Contributing Guide** for team members (how to work with the repo).  
- It’s also a **Developer Setup Guide** (clear steps to clone, install, run).

---
