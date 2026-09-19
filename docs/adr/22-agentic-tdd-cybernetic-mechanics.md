# ADR 22: Agentic TDD Cybernetic Mechanics
# STATUS: ACCEPTED

## 1. Context

When autonomous agents mutate production codebase state without strict deterministic validation, the system falls victim to the "Lazy Implementer" trap—generating shallow patches, hallucinated mocks, or latent defects that pass visual inspection but break under load. The unconstrained ReAct loop leads to a "Doom Loop" of token exhaustion. We require a closed-loop cybernetic system to convert subjective natural language instruction into mathematical verification.

## 2. Decision

We will integrate strict Agentic Test-Driven Development (TDD) as the primary verification oracle for all automated modifications. The TDD process is defined as a closed-loop state machine with three mandatory phases:

1. **The Red Phase (Programmatic Specification):** Before modifying production code, the agent must generate a reproducible baseline script in `__tests__/` that yields a non-zero exit status (failing test).
2. **The Green Phase (Iterative ReAct Loop):** The agent iteratively modifies `src/` code and observes the resulting stdout/stderr (parsed into deterministic JSON schemas).
3. **The Refactor Phase (Verification Gate):** Once a zero exit status is achieved, the agent performs static linting (`npm run lint` / `npm run build`) alongside the test runner to guarantee no architectural regressions.

This mandates a "Plan-First" pipeline where strategic test generation is explicitly segregated from mutating implementation logic.

## 3. Consequences

### Positive Consequences
*   **Alignment Accuracy:** Empirically verified to drastically increase patch correctness by converting agentic hallucination into verifiable logic via the test harness.
*   **Reduced Token Exhaustion:** Truncates the infinite "Doom Loop" by enforcing hard threshold cutoffs (e.g., $N=10$) for repetitive test failures.
*   **Sandbox Security:** By utilizing isomorphic containerization (e.g., `gemini-cli-sandbox`), test execution vulnerabilities are mitigated through blocked outbound network sockets and read-only test definition constraints.

### Negative Consequences
*   **Execution Velocity Decline:** Direct single-shot (YOLO mode) modifications are significantly faster. TDD loops introduce substantial token and latency overheads.
*   **Compute Costs:** A full Red-Green loop consumes an average of 1.1M input tokens per successful resolution, increasing operational OPEX per ticket.

## 4. Implementation Notes
*   Integration of `TDDState` via LangGraph or Google Agent Development Kit to decouple Test Architect and Implementer agent roles.
*   Modification of the `gemini-cli-sandbox` Docker definition to enforce `read_only: true` on system files and `network_mode: none`.
*   Establishment of the `evaluate_loop_state` invariant to trigger human escalation at iteration 10.
