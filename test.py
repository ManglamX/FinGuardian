from agents.credit_agent.inference import assess_credit

user_profile = {
    "txn_count": 65,
    "avg_transaction_amount": 1800,
    "avg_txn_frequency": 2,
    "balance_stability": 0.8,
}

print(assess_credit(user_profile))
