````markdown
# Xiara – Conversational Agent (Pasar)

**Xiara** is the buyer-facing conversational AI agent for the Pasar platform. It helps buyers search products, negotiate deals, and initiate payments securely.

---

## 📦 Features
- 💬 Conversational Commerce: Natural language product search
- 💰 Price Negotiation: Uses LLM + rules for basic negotiation
- 🗂 Vector Search: Retrieves product info via Weaviate or Pinecone
- 🧠 Memory: Session context managed by Redis or LangChain
- 🔗 Payment Triggers: Can call backend APIs to initiate payments

---

## 🚀 Run Locally

```bash
cd xiara
uvicorn main:app --reload --port 8001
````

📌 **Note**: Ensure `.env` file exists (copy from `.env.example`).

---

## 🔌 API Endpoints

| Method | Endpoint    | Description                      |
| ------ | ----------- | -------------------------------- |
| GET    | /           | Health check endpoint            |
| POST   | /xiara/chat | Accepts user prompt and responds |

---

## 🧠 LLM Setup

* Uses Hugging Face LLMs (e.g. `llama-2-7b`).
* Managed via `LangChain` for prompt orchestration.

---

## 🛠 Development Notes

* Loads settings via `shared/config/settings.py`.
* Uses logger from `shared/logging/logger.py`.
* Supports future extensions (multi-lingual chat, RAG memory).

```
```
