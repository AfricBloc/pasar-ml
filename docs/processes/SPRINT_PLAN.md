#  Pasar ML  Team Sprint Plan (Updated)

This sprint plan reflects our **current repo state** (scaffold already done) and the **teams decision** to work together on each agent first.

---

##  Sprint 1 (Week 12)  Xiara MVP Foundations
 **Goal:** Get Xiara (the buyer-facing agent) responding to simple queries end-to-end.

- ?? **Tasks**
  - Implement GET /ping and POST /query endpoints in **Xiara**.
  - Set up a **very simple LangChain prompt** for product query handling (static responses at first).
  - Build 12 **unit tests** for endpoints.
  - All engineers **mob-program** in VS Code Live Share.

-  **Learning**
  - 1 day deep-dive on **FastAPI** (routing, dependency injection).
  - 1 day intro to **LangChain** basics (prompt templates, chains).

---

## ?? Sprint 2 (Week 3–4) – Shogun MVP (Security)
?? **Goal:** Start Shogun’s rule-based fraud detection.

- ?? **Tasks**
  - Add GET /ping and POST /check to **Shogun**.
  - Implement **basic hard-coded rules** (e.g., flag transactions over \).
  - Shared **test suite** for Shoguns endpoints.

-  **Learning**
  - 12 days reviewing **basic ML anomaly detection concepts** (IsolationForest, threshold rules).
  - Agree on **how Shogun will evolve** into an ML-based detector in later sprints.

---

##  Sprint 3 (Week 56)  Resolute MVP (Dispute Resolution)
 **Goal:** Enable Resolute to take dispute evidence.

-  **Tasks**
  - Add GET /ping and POST /dispute.
  - Start with **keyword spotting** in dispute text (“broken,” “wrong size,” etc.).
  - Plan for future **NLP model integration** (SpaCy pipeline).

-  **Learning**
  - Explore **SpaCy or Hugging Face** basics for NLP.
  - Discuss approach for handling **image evidence** later.

---

##  Sprint 4 (Week 78)  Xena MVP (Wallet Agent)
 **Goal:** Xena can simulate transactions.

-  **Tasks**
  - Add GET /ping and POST /transaction.
  - Implement a **mock ledger** (store balances in Redis for now).
  - Add unit tests for transaction endpoints.

-  **Learning**
  - Learn **Web3.py basics** (future smart wallet integration).
  - Discuss how escrow contracts will link with Xena.

---

##  Beyond Sprint 4
-  All agents have **working MVP endpoints**.
-  Team has learned **FastAPI + LangChain + NLP/ML basics** together.
-  Ready to **split into feature teams** for Sprint5 and beyond.

---
