def compute_run_flags(tree):
    has_error = False
    has_slow_step = False
    has_expensive_step = False

    def traverse(node):
        nonlocal has_error, has_slow_step, has_expensive_step

        # True error only if non-empty
        err = node.get("error")
        if err is not None and err != "":
            has_error = True

        flags = node.get("flags", {})

        if flags.get("is_slow_step") is True:
            has_slow_step = True

        if flags.get("is_expensive_step") is True:
            has_expensive_step = True

        for child in node.get("children", []):
            traverse(child)

    for root in tree:
        traverse(root)

    return {
        "has_error": has_error,
        "has_slow_step": has_slow_step,
        "has_expensive_step": has_expensive_step
    }
