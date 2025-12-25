# agents/compliance_agent/rules.py

def evaluate_compliance_rules(txn: dict) -> list:
    """
    Deterministic compliance checks.
    Returns a list of violated compliance rules.
    """

    violations = []

    amount = txn.get("amount", 0)
    txn_type = txn.get("type", "")
    is_new_account = txn.get("is_new_account", 0)
    txn_freq = txn.get("txn_frequency_1h", 0)

    old_bal = txn.get("oldbalanceOrg", 0)
    new_bal = txn.get("newbalanceOrig", 0)

    # Rule 1: High-value transaction from new account
    if is_new_account and amount > 20000:
        violations.append("High-value transaction from new account")

    # Rule 2: Rapid cash-out behavior
    if txn_type == "CASH_OUT" and txn_freq > 3:
        violations.append("Rapid cash-out behavior detected")

    # Rule 3: Account balance drained
    if old_bal > 0 and new_bal < 0.1 * old_bal:
        violations.append("Account balance rapidly depleted after transaction")

    # Rule 4: Structuring / burst behavior
    if txn_freq > 5:
        violations.append("Multiple high-frequency transactions in short time window")

    return violations
