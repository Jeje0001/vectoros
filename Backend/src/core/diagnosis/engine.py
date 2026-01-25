from src.core.diagnosis.schema import DiagnosisResult
from src.core.run_builder import build_full_run_structure
from src.core.diagnosis.prompt import build_diagnosis_prompt
from src.core.diagnosis.llm import run_gpt_diagnosis



def find_first_error(node):
    if node.get("error"):
        return node

    for child in node.get("children", []):
        found = find_first_error(child)
        if found:
            return found

    return None


def collect_flagged_steps(node, flag_name, results):
    if node.get("flags", {}).get(flag_name) is True:
        results.append(node)

    for child in node.get("children", []):
        collect_flagged_steps(child, flag_name, results)


def diagnose_run(run: dict) -> DiagnosisResult:
    built = build_full_run_structure(run)

    tree = built["tree"]
    stats = built["stats"]
    flags = built["flags"]

    first_error = None
    slow_steps = []
    expensive_steps = []

    for root in tree:
        if first_error is None:
            first_error = find_first_error(root)

        collect_flagged_steps(root, "is_slow_step", slow_steps)
        collect_flagged_steps(root, "is_expensive_step", expensive_steps)

    root_cause = "success"
    explanation = "Run completed successfully."

    if first_error:
        root_cause = first_error.get("type") or "error"
        explanation = first_error.get("error") or "Unknown error"

    reliability_score = max(
        0.0,
        1.0 - (stats["error_count"] * 0.2)
    )

    COST_PER_1K_TOKENS = 0.002  # adjust later

    estimated_cost_usd = round(
        (stats["total_tokens"] / 1000) * COST_PER_1K_TOKENS,
        6
    )
    diagnosis_dict = {
    "root_cause": root_cause or "none",
    "explanation": explanation,
    "reliability_score": reliability_score,
    "cost_analysis": {
        "total_tokens": stats["total_tokens"],
        "estimated_cost_usd": estimated_cost_usd,
        "expensive_steps": [step.get("id") or step.get("type") for step in expensive_steps],
    },
}


    prompt = build_diagnosis_prompt(diagnosis_dict)
    suggested_fix = run_gpt_diagnosis(prompt)

    return DiagnosisResult(
        root_cause=root_cause,
        explanation=explanation,
        suggested_fix=suggested_fix,
        reliability_score=round(reliability_score, 2),
        cost_analysis=diagnosis_dict["cost_analysis"],
    )

