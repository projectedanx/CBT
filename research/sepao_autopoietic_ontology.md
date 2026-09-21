# Designing an Autopoietic Self-Healing Ontology Engine using Static AST Analysis and Failure-Informed Prompt Inversion

## 1. The Environment Scanner

The SEPAO (Self-Evolving Plugin Affordance Ontology) engine requires continuous situational awareness of its operating environment. This is achieved via a background worker that monitors the codebase.

### Operation
1.  **File System Monitoring:** A watcher process (e.g., using Python's `watchdog` library) monitors critical directories for file modification events.
2.  **AST Parsing:** When a change is detected in source files (e.g., Python or TypeScript), the scanner parses the file into an Abstract Syntax Tree (AST).
3.  **Entity Extraction:** It extracts function signatures, class definitions, decorators, and type hints to reconstruct the current local schema.

## 2. Semantic Delta Mapping

Extracted schema information is maintained as a unified knowledge graph $G = (V, E)$, where $V$ are entities (e.g., functions, endpoints) and $E$ are relationships (e.g., calls, depends_on).

### Semantic Drift Calculation
Let $G_t$ be the ontology graph at time $t$ and $G_{t+1}$ be the updated graph after a scan. We compute the Graph Edit Distance (GED) or a structural embedding distance to quantify the drift.

Using embedding models (e.g., SentenceTransformers for docstrings and GraphSAGE for structure), let $\mathbf{v}_i^{(t)}$ be the embedding of node $i$ at time $t$. The Semantic Drift Delta for node $i$ is:

$$ \Delta S_i = 1 - \frac{\mathbf{v}_i^{(t)} \cdot \mathbf{v}_i^{(t+1)}}{||\mathbf{v}_i^{(t)}|| \cdot ||\mathbf{v}_i^{(t+1)}||} $$

**Ontological Conflict:**
If $\Delta S_i > \tau_{drift}$, an "Ontological Conflict" is declared, signaling that the environment has mutated beyond the agent's current understanding.

## 3. Failure-Informed Prompt Inversion (F-IPI)

When the agent executes code that fails a test suite or compiler check, F-IPI is triggered to mutate the agent's core constitution (`GEMINI.md`).

### Pipeline
1.  **Isolation:** The stack trace is parsed to isolate the failing line range.
2.  **Scar Generation:** A 'Symbolic Scar' JSON object is minted containing the error context and AST diff.
3.  **Prompt Mutation:** A gradient-free optimization process (e.g., using an LLM as a mutator) is given the Scar and tasked with proposing a rule addition to `GEMINI.md` that explicitly forbids or handles the failed state.

### Metadata Structure (`scar_schema.json`)
```json
{
  "scar_id": "SCAR_49A8F",
  "timestamp": "2024-05-20T14:32:00Z",
  "triggering_module": "auth_middleware.py",
  "error_type": "TypeError",
  "semantic_drift_delta": 0.45,
  "stack_trace_snippet": "TypeError: verify_token() missing 1 required positional argument: 'audience'",
  "proposed_fipi_rule": "MANDATE: All calls to verify_token must explicitly pass the 'audience' kwarg."
}
```

## 4. Metamorphic Invariance Verification

Before committing a proposed F-IPI rule to `GEMINI.md`, it must be verified to prevent "Scar-Induced Rigidity."

### Procedure
1.  **Paraphrasing:** The proposed rule is semantically paraphrased into $N$ variations.
2.  **Simulation:** The agent runs a suite of unrelated sub-tasks (regression tests) with the modified constitution.
3.  **Invariance Check:** If the agent's behavior changes negatively on the unrelated tasks (e.g., it stops using functions it used previously), the rule fails the metamorphic check and is rejected.

## Appendix: Executable Demonstration

```python
import ast
import numpy as np

class SimpleScanner:
    def parse_file(self, file_path):
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        functions = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                functions[node.name] = args
        return functions

def calculate_drift(old_schema, new_schema):
    drift_score = 0
    for func, args in old_schema.items():
        if func not in new_schema:
            drift_score += 1.0 # Function deleted
        elif args != new_schema[func]:
            drift_score += 0.5 # Signature changed

    for func in new_schema:
        if func not in old_schema:
            drift_score += 0.2 # New function added

    return drift_score

def trigger_fipi(error_msg, diff_context):
    # Simulated FIPI generation
    print(f"[F-IPI] Analyzing Error: {error_msg}")
    print(f"[F-IPI] Generating constraint for GEMINI.md...")
    return f"ASSERT: Prevent {error_msg.split(':')[0]} in {diff_context}"

if __name__ == "__main__":
    # Simulate V1 of a file
    with open("temp_target.py", "w") as f:
        f.write("def auth(user, password):\n    pass\n")

    scanner = SimpleScanner()
    schema_v1 = scanner.parse_file("temp_target.py")

    # Simulate V2 of a file (API breaking change)
    with open("temp_target.py", "w") as f:
        f.write("def auth(token):\n    pass\n")

    schema_v2 = scanner.parse_file("temp_target.py")

    drift = calculate_drift(schema_v1, schema_v2)
    print(f"Schema V1: {schema_v1}")
    print(f"Schema V2: {schema_v2}")
    print(f"Calculated Drift Delta: {drift}")

    if drift > 0.4:
        print("Ontological Conflict Detected!")
        new_rule = trigger_fipi("TypeError: missing required argument", "auth()")
        print(f"Proposed Rule: {new_rule}")
```
