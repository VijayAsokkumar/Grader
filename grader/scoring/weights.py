WEIGHTS = {
    "pass_rate": 0.25,
    "flaky_index": 0.15,
    "coverage_delta": 0.20,
    "duration_trend": 0.15,
    "suite_breadth": 0.15,
    "retry_rate": 0.10,
}
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9
