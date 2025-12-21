import pytest
from src.core.run_builder import build_full_run_structure

def test_full_run_structure_happy_path():
    run = {
        "run_id": "abc123",
        "model": "gpt-4o-mini",
        "input": "hi",
        "output": "hello",
        "tokens": 42,
        "cost": 0.001,
        "latency": 150,
        "status": "success",
        "error": None,
        "steps": [
            {
                "id": "1",
                "type": "root",
                "latency": 100,
                "tokens": 200,
                "error": None,
                "children": [
                    {
                        "id": "2",
                        "type": "child",
                        "latency": 50,
                        "tokens": 100,
                        "error": None,
                        "children": []
                    }
                ]
            }
        ]
    }

    result = build_full_run_structure(run)

    assert "run" in result
    assert "tree" in result
    assert "flags" in result
    assert "stats" in result

    # run summary presence
    assert result["run"]["run_id"] == "abc123"

    # tree structure
    tree = result["tree"]
    assert len(tree) == 1
    assert tree[0]["id"] == "1"
    assert len(tree[0]["children"]) == 1

    # step flags attached
    assert "flags" in tree[0]
    assert "is_slow_step" in tree[0]["flags"]
    assert "is_expensive_step" in tree[0]["flags"]

    # run flags
    flags = result["flags"]
    assert flags["has_error"] is False
    assert flags["has_slow_step"] in (True, False)
    assert flags["has_expensive_step"] in (True, False)

    # run stats
    stats = result["stats"]
    assert stats["total_steps"] == 2
    assert stats["max_depth"] == 1


def test_full_run_structure_invalid_run():
    with pytest.raises(ValueError):
        build_full_run_structure(None)


def test_full_run_structure_missing_steps():
    run = {
        "run_id": "abc",
        "model": "m",
        "input": "i",
        "output": "o",
        "status": "success",
        "steps": None
    }

    with pytest.raises(ValueError):
        build_full_run_structure(run)


def test_full_run_structure_empty_steps():
    run = {
        "run_id": "abc",
        "model": "m",
        "input": "i",
        "output": "o",
        "status": "success",
        "steps": []
    }

    with pytest.raises(ValueError):
        build_full_run_structure(run)


def test_full_run_structure_missing_step_id():
    run = {
        "run_id": "abc",
        "model": "m",
        "input": "i",
        "output": "o",
        "status": "success",
        "steps": [
            {
                "type": "root",
                "latency": 10,
                "tokens": 5,
                "error": None,
                "children": []
            }
        ]
    }

    with pytest.raises(ValueError):
        build_full_run_structure(run)
