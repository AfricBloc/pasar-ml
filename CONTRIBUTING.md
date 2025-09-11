---
# 🤝 Contributing to Pasar ML Agents

Welcome to the **Pasar ML Agents** project!
This repo contains the AI agents that power Pasar — **Xiara, Shogun, Resolute, and Xena**.
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
```

---

## 🚀 Developer Setup Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/AfricBloc/pasar-ml.git
cd pasar-ml
```

### 2️⃣ Create Your Virtual Environment

Use **Python 3.11** (recommended).

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Copy and Configure `.env`

```bash
cp .env.example .env
```

Fill in API keys, DB URLs, blockchain credentials as needed.

### 5️⃣ Run Services (Dev Mode)

Each agent is a FastAPI app:

```bash
cd xiara
uvicorn main:app --reload --port 8001
```

Repeat for **Shogun, Resolute, Xena** (ports 8002–8004).

### 6️⃣ Run via Docker Compose

```bash
docker-compose up --build
```

✅ Xiara → `http://localhost:8001`
✅ Shogun → `http://localhost:8002`
✅ Resolute → `http://localhost:8003`
✅ Xena → `http://localhost:8004`

### 7️⃣ Run Notebooks

```bash
jupyter notebook
```

Open `notebooks/` folder to experiment with ML.

---

## 🔀 Branch Workflow

- **`main`** → Production-ready code only.
- **`dev`** → Active development branch.

For new features:

```bash
git checkout dev
git pull origin dev
git checkout -b feature/<feature-name>
```

⚡ **Note:** All PRs into `dev` must pass **CI checks** before merge:

- ✅ Unit tests
- ✅ Linting (PEP8/Black)
- ✅ Docker build

---

## 📜 Commit Guidelines (Conventional Commits)

Use [Conventional Commit](https://www.conventionalcommits.org/) style:

- `feat:` → New feature
- `fix:` → Bug fix
- `docs:` → Documentation only
- `refactor:` → Code refactor
- `chore:` → Build/config/maintenance

**Examples:**

```bash
git commit -m "feat: add dispute analysis endpoint"
git commit -m "docs: update contributing guide"
```

---

## ✅ Code Style

- Follow **PEP8**
- Use **type hints** everywhere
- Use **Pydantic models** for request/response schemas

---

## 🔍 Pull Request Guidelines

1. Base branch = `dev`
2. Clear title + description (Conventional Commits)
3. Request review from another team member
4. Ensure all CI checks pass:

   - `pytest`
   - `flake8` + `black`
   - Docker build stage

5. After approval + passing CI → **Squash Merge** into `dev`

---

## 🛠 Useful Commands

```bash
make up         # Start all Docker services
make down       # Stop containers
make logs       # View logs
make rebuild    # Full rebuild
make test       # Run pytest suite
```

---

## 📬 Support

For questions or discussions:

- Open an issue on GitHub
- Or contact the team lead via Slack/Email

---

Thanks for contributing to **Pasar ML Agents**! 🚀

---
