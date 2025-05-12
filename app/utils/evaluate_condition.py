def evaluate_condition(condition: str, days: int) -> bool:
    try:
        condition = condition.replace(" ", "")
        if "and" in condition:
            parts = condition.split("and")
            low = int(parts[0].split(">=")[1])
            high = int(parts[1].split("<=")[1])
            return low <= days <= high
        elif condition.startswith(">="):
            return days >= int(condition[2:])
        elif condition.startswith("<="):
            return days <= int(condition[2:])
        elif condition.startswith(">"):
            return days > int(condition[1:])
        elif condition.startswith("<"):
            return days < int(condition[1:])
        elif condition.startswith("="):
            return days == int(condition[1:])
    except Exception:
        return False
