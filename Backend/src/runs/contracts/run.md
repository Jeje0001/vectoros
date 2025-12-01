1. Overview

A run represents a single execution of an AI model or agent inside VectorOS. It captures the full lifecycle of that execution, including input/output data, performance metrics, execution steps, and any associated errors or state changes. The run contract defines the exact structure that every run must follow across ingestion, storage, retrieval, memory, SDKs, and the UI. Consistency in this contract prevents schema drift and ensures all components of VectorOS interpret run data the same way. Any deviation breaks ingestion, retrieval, diagnosis, and future memory systems.
 
2. Field Definitions 

    run_id

        Type: UUID (string-formatted)

        Required: No

        Default: Auto-generated UUID v4 on ingestion

        Description: A globally unique identifier for the run. Used to track, retrieve, and correlate executions across ingestion, memory, diagnosis, and SDK layers.

        Normalization Rules:

            If absent: backend generates a UUID.

            If provided as a UUID object: converted to string.

            If provided as a string: stored as-is if valid.

    model

        Type: String

        Required: Yes

        Default: None

        Description: Identifies which AI model or agent executed this run (e.g., "gpt-4.1", "claude-3.5", "internal-routing-agent-v2"). Used for routing, benchmarking, analytics, and debugging.

        Normalization Rules:

            Trim surrounding whitespace

            Must be a non-empty string
    
    input

        Type: String

        Required: Yes

        Default: None

        Description: Raw input payload sent to the model or agent. This may contain text, prompts, serialized JSON, or any user-provided request body. Stored exactly as received for traceability, debugging, and memory systems.

        Normalization Rules:

            Converted to string if not already.

            Empty strings are allowed.

            No validation of structure (VectorOS does not assume specific prompt formats).

    output

        Type: String

        Required: No

        Default: None

        Description: Raw output returned by the model or agent after execution. Used for UI display, debugging, and memory extraction. Stored exactly as returned.

        Normalization Rules:

            Converted to string if provided.

            No assumptions about structure, formatting, or model type.

            May be null for incomplete, failed, or streaming runs.
    tokens

        Type: Integer

        Required: No

        Default: None

        Description: Total number of tokens consumed during the run (input + output, or model-specific definition). Used for analytics, cost estimation, performance benchmarking, and anomaly detection.

        Normalization Rules:

            Must be an integer if provided

            Converted to int if possible

            Reject negative values

    cost

        Type: Float

        Required: No

        Default: None

        Description: Monetary cost of the run based on model pricing or internal rate definitions. Used for analytics, billing, and optimization systems.

        Normalization Rules:

            Must be numeric

            Converted to float if possible

            Reject negative values
    
    latency

        Type: Float

        Required: No

        Default: None

        Description: Total execution time of the run, measured in seconds. Calculated as the difference between started_at and the time the run completed. Used for performance analytics and anomaly detection.

        Normalization Rules:

            Must be numeric

            Convert to float if possible

            Reject negative values
    
    status

        Type: String

        Required: Yes

        Default: None

        Description: The execution state of the run. Indicates whether the run completed successfully, failed with an error, is still in progress, or exceeded defined timeout limits.

        Normalization Rules:

            Must be a string

            Normalize to lowercase

            Must be one of: "success", "error", "running", "timeout"

    
    error
        Type: String

        Required: No

        Default: None

        Description: Optional error message describing what caused the failure. Only present when status is "error". Used for debugging and diagnosis.

        Normalization Rules:

            Must be a string if provided

            Trim whitespace

            Empty string becomes None
    


    steps

        Type: List of dictionaries

        Required: No

        Default: `[]`

        Description: `steps` captures the *execution trace* of an agent run.
        Each step represents a meaningful sub-action performed during the run.
        Steps can be nested because complex agents perform hierarchical operations. This field is the backbone of the trace viewer (Phase 3 + Phase 4) and the diagnosis engine (Phase 5).


        Structure of a Single Step: Each step **must** be a dictionary with the following normalized fields:
         ```
        {
            "type":      str,
            "metadata":  dict,
            "children":  list[dict]
        }
        ```

        Field Definitions for Each Step:

            #### **type**

            * The category of the step
            Examples: `"tool_call"`, `"model_call"`, `"parse"`, `"decision"`, `"http_request"`
            * Must be a string
            * Default: `"unknown"`

            #### **metadata**

            * Arbitrary key–value data about the step
            * Must be a dictionary
            * Default: `{}`
            * This is where things like:

            * tokens used
            * tool name
            * input/output snippets
            * endpoint called
            * intermediate model thoughts (if relevant)
                go.

            #### **children**

            * A list of *sub-steps*
            * Must be a list
            * Default: `[]`
            * Every child must obey the **same structure as the parent**
            (recursive contract)



        ## **Normalization Rules**

            ### 1. Acceptable incoming shapes for `steps`:

            * `None`
            * `""`
            * `{}`
            * `{...}`
            * `[...]` (list of dicts)

            Anything else → immediately reject.

            ### 2. Normalization behavior:

            * `None`, `""`, `{}`, `[]`  → `[]`
            * A dictionary → wrap into list and normalize each field
            * A list → validate each item is a dictionary, then normalize each item

            ### 3. Per-step normalization:

            * If `"type"` missing → set `"type": "unknown"`
            * If `"metadata"` missing → set `"metadata": {}`
            * If `"children"` missing → set `"children": []`
            * `"type"` must become `str(...)`
            * `"metadata"` must remain a dict or error
            * `"children"` must remain a list or error
            * Each child must itself be validated with the same rules (recursive)

            ### 4. Final guaranteed shape:

            ```
            steps = [
                {
                    "type": str,
                    "metadata": dict,
                    "children": [same structure...]
                },
                ...
            ]
            ```

3. Timestamps

    VectorOS stores two timestamps for every run:

        created_at

            Type: Timestamp

            Required: No

            Default: NOW() (database-level)

            Description: The moment the run was inserted into the database.

            Normalization Rules:

                Handled entirely by PostgreSQL

                Backend should never override it

                Read-only field

        started_at

            Type: Timestamp

            Required: No

            Default: NOW() (database-level)

            Description: The moment the model began execution.

            Importance:

                Used by Phase 3 for latency computation

                Used for diagnosis (Phase 5)

                Used for reliability scoring (Phase 6–7)

            Normalization Rules:

                If user provides a timestamp → reject

                If missing → DB uses NOW()

                Must never be modified by the backend

                Read-only field

        Timestamp Integrity Rules


            Backend does not accept manual timestamps

            Backend does not generate timestamps

            Only PostgreSQL provides the timestamps

            All components (SDK, UI, diagnosis engine) must treat these as immutable

            If a user tries to send timestamps in payload, they must be ignored or rejected
4. Global Validation Rules

    These rules apply to the entire run payload before insertion into the database.

    1. Unknown Fields Are Rejected

        If a client sends fields that are not part of the contract:

            reject the request

            return a 400 Validation Error

        VectorOS must enforce strict schemas.

    2. Required Fields Must Exist

        The following fields must be present:

            model

            input

            status

        Missing any of these → validation failure.

    3. Type Enforcement

        All types must match the contract:

            Strings must be strings

            Numbers must be numeric

            UUIDs must be UUID-compatible

            steps must follow the step-structure rules

        If a field cannot be coerced to the correct type → reject.

    4. Status Must Be One of the Allowed Values

        Must be:

            success

            error

            running

            timeout

        Case-insensitive normalization is allowed.
        Invalid status → reject.

    5. Error Field Consistency

        If status == "error":

            error message must exist (string)

        If status != "error":

            error must be None or omitted.

        This keeps diagnosis clean.

    6. Steps Must Be Valid

        Steps must always be normalized to:

            [
            {
                "type": str,
                "metadata": dict,
                "children": [...nested steps...]
            }
            ]


        Invalid shapes → reject.

    7. No Timestamps in Payload

        Reject payloads containing:

            created_at

            started_at

        Only DB generates these.

    8. No Silent Coercion

        VectorOS never “guesses” when data is malformed.
        It either:

            normalizes safely

            rejects

        Never silently accept broken payloads.

        9. Final Output Shape Must Match DB

            The returned run object must match the database row:

                The normalized input fields

                PLUS timestamps from DB

            This ensures UI and diagnosis engine receive consistent data.