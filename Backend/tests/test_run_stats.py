import pytest
from src.core.run_stats import compute_run_stats

def test_empty_tree_has_zero_counts():
    roots = []
    stats = compute_run_stats(roots)

    assert stats["total_steps"] == 0
    assert stats["total_tokens"] == 0
    assert stats["total_latency"] == 0
    assert stats["error_count"] == 0
    assert stats["max_depth"] == 0


def test_single_step_with_metrics():
    roots = [
        {
            "id": "s1",
            "tokens": 50,
            "latency": 100,
            "error": "",
            "children": []
        }
    ]

    stats = compute_run_stats(roots)

    assert stats["total_steps"] == 1
    assert stats["total_tokens"] == 50
    assert stats["total_latency"] == 100
    assert stats["error_count"] == 0
    assert stats["max_depth"] == 0


def test_nested_steps_depth_and_totals():
    roots = [
        {
            "id": "root",
            "tokens": 100,
            "latency": 200,
            "error": None,
            "children": [
                {
                    "id": "child1",
                    "tokens": 50,
                    "latency": 50,
                    "error": "",
                    "children": [
                        {
                            "id": "child2",
                            "tokens": 30,
                            "latency": 20,
                            "error": "boom",
                            "children": []
                        }
                    ]
                }
            ]
        }
    ]

    stats = compute_run_stats(roots)

    assert stats["total_steps"] == 3
    assert stats["total_tokens"] == 180
    assert stats["total_latency"] == 270
    assert stats["error_count"] == 1
    assert stats["max_depth"] == 2


def test_missing_metrics_are_ignored():
    roots = [
        {
            "id": "x1",
            "children": [
                {"id": "x2", "children": []}
            ]
        }
    ]

    stats = compute_run_stats(roots)

    assert stats["total_steps"] == 2
    assert stats["total_tokens"] == 0
    assert stats["total_latency"] == 0
    assert stats["error_count"] == 0
    assert stats["max_depth"] == 1
