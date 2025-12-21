import pytest
from src.core.step_flags import compute_step_flags, SLOW_STEP_LATENCY_MS, EXPENSIVE_STEP_TOKENS

def test_step_with_no_latency_or_tokens():
    step = {}
    flags = compute_step_flags(step)
    assert flags["is_slow_step"] is False
    assert flags["is_expensive_step"] is False

def test_step_with_fast_latency():
    step = {"latency": SLOW_STEP_LATENCY_MS - 1}
    flags = compute_step_flags(step)
    assert flags["is_slow_step"] is False

def test_step_with_slow_latency():
    step = {"latency": SLOW_STEP_LATENCY_MS + 10}
    flags = compute_step_flags(step)
    assert flags["is_slow_step"] is True

def test_step_with_small_token_usage():
    step = {"tokens": EXPENSIVE_STEP_TOKENS - 1}
    flags = compute_step_flags(step)
    assert flags["is_expensive_step"] is False

def test_step_with_expensive_token_usage():
    step = {"tokens": EXPENSIVE_STEP_TOKENS + 10}
    flags = compute_step_flags(step)
    assert flags["is_expensive_step"] is True

def test_step_with_both_slow_and_expensive():
    step = {
        "latency": SLOW_STEP_LATENCY_MS + 100,
        "tokens": EXPENSIVE_STEP_TOKENS + 100,
    }
    flags = compute_step_flags(step)
    assert flags["is_slow_step"] is True
    assert flags["is_expensive_step"] is True
