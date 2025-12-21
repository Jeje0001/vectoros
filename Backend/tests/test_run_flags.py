import pytest
from src.core.run_flags import compute_run_flags

def test_empty_tree_has_no_flags():
    tree = []
    flags = compute_run_flags(tree)

    assert flags["has_error"] is False
    assert flags["has_slow_step"] is False
    assert flags["has_expensive_step"] is False


def test_single_step_no_flags():
    tree = [
        {
            "id": "s1",
            "error": "",
            "flags": {
                "is_slow_step": False,
                "is_expensive_step": False
            },
            "children": []
        }
    ]

    flags = compute_run_flags(tree)

    assert flags["has_error"] is False
    assert flags["has_slow_step"] is False
    assert flags["has_expensive_step"] is False


def test_error_propagates():
    tree = [
        {
            "id": "root",
            "error": "",
            "flags": {"is_slow_step": False, "is_expensive_step": False},
            "children": [
                {
                    "id": "child",
                    "error": "boom",
                    "flags": {"is_slow_step": False, "is_expensive_step": False},
                    "children": []
                }
            ]
        }
    ]

    flags = compute_run_flags(tree)

    assert flags["has_error"] is True
    assert flags["has_slow_step"] is False
    assert flags["has_expensive_step"] is False


def test_slow_and_expensive_detection():
    tree = [
        {
            "id": "A",
            "error": "",
            "flags": {"is_slow_step": True, "is_expensive_step": False},
            "children": [
                {
                    "id": "B",
                    "error": "",
                    "flags": {"is_slow_step": False, "is_expensive_step": True},
                    "children": []
                }
            ]
        }
    ]

    flags = compute_run_flags(tree)

    assert flags["has_error"] is False
    assert flags["has_slow_step"] is True
    assert flags["has_expensive_step"] is True


def test_flags_exist_even_nested_deeply():
    tree = [
        {
            "id": "root1",
            "error": "",
            "flags": {"is_slow_step": False, "is_expensive_step": False},
            "children": [
                {
                    "id": "lvl1",
                    "error": "",
                    "flags": {"is_slow_step": False, "is_expensive_step": True},
                    "children": [
                        {
                            "id": "lvl2",
                            "error": "",
                            "flags": {"is_slow_step": True, "is_expensive_step": False},
                            "children": []
                        }
                    ]
                }
            ]
        }
    ]

    flags = compute_run_flags(tree)

    assert flags["has_error"] is False
    assert flags["has_slow_step"] is True
    assert flags["has_expensive_step"] is True
