def build_step_tree(steps: list[dict]) -> list[dict]:
    if not isinstance(steps, list):
        raise ValueError("steps must be a list")
    if len(steps) == 0:
        raise ValueError("steps list cannot be empty")

    id_map = {}
    roots = []

    # First pass: build nodes from provided steps
    for step in steps:
        if "id" not in step:
            raise ValueError("Step missing id")

        sid = step["id"]
        if sid in id_map:
            raise ValueError("Duplicate step id")

        node = {k: v for k, v in step.items() if k != "children"}
        node["children"] = []
        id_map[sid] = node

    # Second pass: attach inline children and create missing nodes
    def process_inline_children(parent_dict):
        parent_node = id_map[parent_dict["id"]]
        inline_children = parent_dict.get("children", [])

        if not isinstance(inline_children, list):
            raise ValueError("children must be a list if present")

        for child_dict in inline_children:
            cid = child_dict.get("id")
            if not cid:
                raise ValueError("inline child missing id")

            # If child wasn't declared at top level, create it now
            if cid not in id_map:
                node = {k: v for k, v in child_dict.items() if k != "children"}
                node["children"] = []
                id_map[cid] = node

            child_node = id_map[cid]
            parent_node["children"].append(child_node)

            process_inline_children(child_dict)

    for step in steps:
        process_inline_children(step)

    # Determine roots (anything without parent_id)
    for step in steps:
        if step.get("parent_id") is None:
            roots.append(id_map[step["id"]])

    if not roots:
        raise ValueError("No root steps found")

    # Attach parent_id format
    for step in steps:
        pid = step.get("parent_id")
        if pid is not None:
            if pid not in id_map:
                raise ValueError("Missing parent")
            parent = id_map[pid]
            parent["children"].append(id_map[step["id"]])

    # DFS cycle detection
    visited = set()

    def dfs(node, path):
        nid = node["id"]
        if nid in path:
            raise ValueError("Cycle detected")
        if nid in visited:
            return

        path.add(nid)
        for child in node["children"]:
            dfs(child, path)
        path.remove(nid)
        visited.add(nid)

    for r in roots:
        dfs(r, set())

    return roots
