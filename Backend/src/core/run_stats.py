def compute_run_stats(roots):
    total_steps=0
    total_tokens=0
    total_latency=0
    error_count=0
    max_depth=0

    def dfs(node,depth):
        nonlocal total_steps,total_tokens,total_latency,error_count,max_depth

        total_steps+=1

        if node.get("tokens") is not None:
            total_tokens+=node["tokens"]
        
        if node.get("latency") is not None:
            total_latency+=node["latency"]
        
        if node.get("error") not in (None,""):
            error_count+=1
        if depth > max_depth:
            max_depth=depth
        
        for child in node["children"]:
            dfs(child,depth + 1)
    
    for root in roots:
        dfs(root,depth=0)
    
    return {
        "total_steps":total_steps,
        "total_tokens":total_tokens,
        "total_latency":total_latency,
        "error_count":error_count,
        "max_depth":max_depth
    }


