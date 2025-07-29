## 📄 **`docs/architecture/Architecture_Overview.md`**

```markdown
# 🏗 Pasar ML Agents – Architecture Overview

This document explains **how all components of Pasar work together** – from the ML agents to infrastructure services.

---

## 🔹 Core Components

### 🤖 **ML Agents**
- **Xiara** – Conversational LLM-powered assistant (buyer-facing).
- **Shogun** – Security & anomaly detection agent.
- **Resolute** – Dispute resolution engine (uses CV/NLP).
- **Xena** – Smart wallet & blockchain transaction handler.

Each agent is a **FastAPI service** running in its own Docker container.

---

## 🟢 **Supporting Services**

- **Redis** → In-memory cache + pub/sub queue for fast communication between agents.
- *(Future)* **PostgreSQL** → Persistent store for transactions, user info, etc.
- *(Future)* **Weaviate (or other Vector DB)** → Semantic search & embedding store for Xiara.

---

## 🔀 **System Flow**

1. **Buyer talks to Xiara** → Xiara answers questions, fetches product info, or triggers tasks.
2. **Xiara calls Shogun** → For security checks (e.g., suspicious login or fraud detection).
3. **Xiara calls Xena** → To initiate wallet transactions or payments.
4. **Shogun flags anomalies** → Alerts Xiara or Resolute if disputes arise.
5. **Resolute resolves disputes** → Uses NLP & CV to compare buyer claims with seller data.

---

## 🐳 **Container Setup**

Each agent has:
- Its own **Dockerfile** (in `/docker/`)
- Runs on a **unique port** (Xiara: 8001, Shogun: 8002, Resolute: 8003, Xena: 8004)
- All orchestrated by **`docker-compose.yml`**.

---

## 🗂 **Folder Mapping to Architecture**

- **/xiara, /shogun, /resolute, /xena** → Individual microservices.
- **/shared** → Common code for all services (logging, config, auth).
- **/infra** → Deployment configs (Kubernetes, Terraform, etc.).
- **/migrations** → Database versioning (for backend team).
- **/docs** → Diagrams, specs, dev processes.

---

## 📊 **High-Level Diagram**

```

\[Buyer] → (Xiara)
↘ calls Shogun (Security checks)
↘ calls Xena (Wallet actions)
↘ calls Resolute (Dispute resolution)
Redis ←→ (Cache + Pub/Sub for agents)
PostgreSQL (future)

---




**This overview should always stay updated** as the system evolves.
```
