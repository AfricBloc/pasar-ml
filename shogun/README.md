````markdown
# Shogun – Security & Anomaly Detection Agent (Pasar)

**Shogun** is the security brain of Pasar. It detects unusual logins, suspicious transactions, and can trigger account or escrow contract locks.

---

## 📦 Features
- 🔐 Login Monitoring: Detects geo/IP anomalies
- 💸 Transaction Scoring: Flags high-risk transactions
- 🚨 Real-time Alerts: Can call backend to suspend users or pause smart contracts

---

## 🚀 Run Locally

```bash
cd shogun
uvicorn main:app --reload --port 8002
````

---

## 🔌 API Endpoints

| Method | Endpoint                  | Description                        |
| ------ | ------------------------- | ---------------------------------- |
| GET    | /                         | Health check endpoint              |
| POST   | /shogun/event/login       | Send login event for anomaly check |
| POST   | /shogun/event/transaction | Send transaction event for review  |

---

## ⚙️ ML Models

* **Isolation Forest** for login anomaly detection.
* **XGBoost** for transaction scoring.
* Future: Graph Neural Networks for fraud ring detection.

---

## 🛠 Development Notes

* Loads sensitive configs from `.env`.
* Uses `shared.auth.auth_utils` to verify internal API tokens.
* Logs all events to Redis for monitoring dashboards.

```
```
