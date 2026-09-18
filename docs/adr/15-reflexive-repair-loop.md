# Architecture Decision Record: Reflexive Repair Loop Integration

## Date
2026-09-18

## Status
Accepted

## Context
Standard AI generation pipelines treat logical failure or constraint violation as terminal states requiring human intervention, or worse, quietly pass invalid states downstream. To maintain the rigorous deterministic metrology required by the CBT: Conceptual Blender and adhere to the VULCAN Epistemic Escrow mandate, we must introduce an autonomous, bounded self-correction mechanism bridging probabilistic generation (System 1) with deterministic verification (System 2).

## Decision
We implement the **Reflexive Repair Loop** as a core service (`ReflexiveRepairLoopService`).

1.  **Deterministic Verification (System 2):** All generated payloads are intercepted and validated against explicit `SemanticIntegrityConstraint` definitions before state release.
2.  **Logic Violation Reporting:** Failures generate structured `LogicViolationReport` (LVR) artifacts, capturing the exact constraint breached.
3.  **Bounded Iteration:** The loop executes Failure-Informed Prompt Inversion (F-IPI), re-prompting the generator with the LVR to repel it from the failure vector. This loop is strictly bounded to a maximum of 3 attempts to prevent resource exhaustion and thrashing.
4.  **Epistemic Escrow:** If the constraint remains unresolved after 3 attempts, the system halts. It logs a `SymbolicScar` in the Scar Tissue Archive (STA) and triggers the Epistemic Escrow tripwire, blocking all downstream execution and demanding Human-In-The-Loop (HITL) resolution.

## Consequences
*   **Positive:** Dramatically increases generation reliability and prevents logical contradictions (Semantic Saponification) from polluting the application state.
*   **Positive:** Enforces the VULCAN mandate by refusing to compromise on physical/architectural constraints.
*   **Negative/Risk:** Increases generation latency due to potential multi-pass API calls.
*   **Compliance:** Code-to-Prose ratio maintained per AXIOM v1.0. All subjective evaluative adjectives eliminated from architectural design constraints.
