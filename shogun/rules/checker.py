def simple_fraud_check(data: dict) -> dict:
    amount = data.get("amount", 0)
    country = data.get("country", "").lower()

    fraud = False
    reasons = []

    # Rule 1: Check if amount exceeds $1000
    if amount > 1000:
        fraud = True
        reasons.append("Amount exceeds $1000")

    # Rule 2: Check for Foreign transactions
    if country != "nigeria":
        fraud = True
        reasons.append("Transaction outside Nigeria")


    # Rule 3: Invalid user ID
    if not data["userId"] or len(data["userId"]) < 3:
        reasons.append("User ID is too short or missing")
    
    return {
        "fraud": fraud,
        "reasons": reasons
    }
