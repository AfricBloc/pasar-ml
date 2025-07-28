````markdown
# Shared Module – Pasar ML Agents

This folder contains code shared by all Pasar agents (Xiara, Shogun, Resolute, Xena).

---

## 📦 Components
- 🛠 config/ – Loads `.env` variables into a central `Settings` class.
- 📜 logging/ – Consistent logger for all agents.
- 🔐 auth/ – Verifies internal service tokens for API-to-API calls.
- 📂 utils/ – Optional helper functions (e.g., date formatters, response builders).

---

## 🧑‍💻 How to Use

Example – Load configs:
```python
from shared.config.settings import settings
print(settings.REDIS_URL)
````

Example – Use logger:

```python
from shared.logging.logger import logger
logger.info("Xiara started.")
```

Example – Secure endpoint:

```python
from shared.auth.auth_utils import verify_internal_token
verify_internal_token(request)
```

---

📌 This module keeps code DRY and ensures all agents use the same settings, logging style, and security.

```
```
