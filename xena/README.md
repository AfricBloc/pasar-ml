````markdown
# Xena – Smart Wallet Agent (Pasar)

**Xena** is the seller-facing wallet assistant for Pasar. It parses text or voice commands to manage funds and generate reports.

---

## 📦 Features
- 🎙 Voice/Text Commands: “Send 50 USDC to supplier.”
- 💸 Smart Wallet Control: Initiates transactions securely.
- 📊 Sales Reports: Generates seller dashboards and analytics.

---

## 🚀 Run Locally

```bash
cd xena
uvicorn main:app --reload --port 8004
````

---

## 🔌 API Endpoints

| Method | Endpoint      | Description                       |
| ------ | ------------- | --------------------------------- |
| GET    | /             | Health check endpoint             |
| POST   | /xena/command | Parse wallet command (text/voice) |

---

## ⚙️ ML Models

* Hugging Face LLM for command parsing.
* Wav2Vec2 for voice-to-text (optional).
* LangChain for tool orchestration.

---

## 🛠 Development Notes

* Uses `web3.py` or `ethers.js` for blockchain calls.
* Requires `.env` for Infura/Alchemy keys and smart contract addresses.

```
```
