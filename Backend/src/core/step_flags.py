from .thresholds import SLOW_STEP_LATENCY_MS,EXPENSIVE_STEP_TOKENS

def compute_step_flags(step):
    flags={
        "is_slow_step":False,
        "is_expensive_step":False
    }

    if step.get("latency") is not None and step.get("latency") > SLOW_STEP_LATENCY_MS:
        flags["is_slow_step"]=True
    
    
    if step.get("tokens") is not None and step.get("tokens") > EXPENSIVE_STEP_TOKENS:
        flags["is_expensive_step"]=True
    
    
    return flags
    


def attach_step_flags(roots):
    def dfs(node):
        flags=compute_step_flags(node)

        node["flags"]=flags

        for child in node["children"]:
            dfs(child)
    for root in roots:
        dfs(root)

