"""Pure analysis functions: values in, results out. No files, no printing."""


def count_above(values, threshold):
    """Count values strictly greater than the threshold (>, not >=)."""
    return sum(value > threshold for value in values)  # True counts as 1

    # The same logic as an explicit loop:
    # count = 0
    # for value in values:
    #     if value > threshold:
    #         count += 1
    # return count


def summarize(values, threshold):
    """Return n, mean, and the number of values above the threshold."""
    if not values:
        raise ValueError("No measurements to summarize")
    return {
        "n": len(values),
        "mean": sum(values) / len(values),
        "n_above": count_above(values, threshold),
        "threshold": threshold,
    }
