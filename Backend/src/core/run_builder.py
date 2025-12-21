from .tree_builder import build_step_tree
from .step_flags import attach_step_flags
from .run_stats import compute_run_stats
from .run_flags import compute_run_flags


def build_full_run_structure(run: dict):
    if not isinstance(run,dict):
        raise ValueError("The run is not a dictionary")
    steps = run.get("steps", [])
    if  not isinstance(steps,list):
        raise ValueError("The steps is not a list")
    if len(steps) == 0:
        raise ValueError("Steps Cannot be Empty")
    
    for step in steps:
        if "id" not in step:
            raise ValueError("ID is not in step")
    roots = build_step_tree(steps)

    attach_step_flags(roots)
    def verify(node):
        if "flags" not in node:
            raise ValueError("Step flags missing")
        
        for child in node["children"]:
            verify(child)
    
    for root in roots:
        verify(root)
    run_flags = compute_run_flags(roots)
    run_stats = compute_run_stats(roots)


    return {
        "run": {
            "run_id": run.get("run_id"),
            "model": run.get("model"),
            "input": run.get("input"),
            "output": run.get("output"),
            "tokens": run.get("tokens"),
            "cost": run.get("cost"),
            "latency": run.get("latency"),
            "status": run.get("status"),
            "error": run.get("error")
        },
        "tree": roots,
        "flags": run_flags,
        "stats": run_stats
    }
