import pytest
from src.core.tree_builder import build_step_tree

# ----------------------------
# 1. Duplicate ID
# ----------------------------
def test_duplicate_ids():
    steps = [
        {"id": "1", "parent_id": None},
        {"id": "1", "parent_id": None},
    ]

    with pytest.raises(ValueError):
        build_step_tree(steps)

# ----------------------------
# 2. Missing parent
# ----------------------------
def test_missing_parent():
    steps = [
        {"id": "1", "parent_id": "999"}
    ]

    with pytest.raises(ValueError):
        build_step_tree(steps)

# ----------------------------
# 3. No root
# ----------------------------
def test_no_root():
    steps = [
        {"id": "2", "parent_id": "1"}
    ]

    with pytest.raises(ValueError):
        build_step_tree(steps)

# ----------------------------
# 4. Cycle detection
# ----------------------------
def test_cycle_detection():
    steps = [
        {"id": "A", "parent_id": "B"},
        {"id": "B", "parent_id": "A"},
    ]

    with pytest.raises(ValueError):
        build_step_tree(steps)

# ----------------------------
# 5. Multiple roots
# ----------------------------
def test_multiple_roots():
    steps = [
        {"id": "1", "parent_id": None},
        {"id": "2", "parent_id": None},
    ]

    roots = build_step_tree(steps)
    assert isinstance(roots, list)
    assert len(roots) == 2
    assert roots[0]["children"] == []
    assert roots[1]["children"] == []

# ----------------------------
# 6. Simple valid chain
# ----------------------------
def test_simple_tree_chain():
    steps = [
        {"id": "A", "parent_id": None},
        {"id": "B", "parent_id": "A"},
        {"id": "C", "parent_id": "B"},
    ]

    roots = build_step_tree(steps)
    assert len(roots) == 1

    A = roots[0]
    assert A["id"] == "A"
    assert len(A["children"]) == 1

    B = A["children"][0]
    assert B["id"] == "B"
    assert len(B["children"]) == 1

    C = B["children"][0]
    assert C["id"] == "C"
    assert len(C["children"]) == 0
