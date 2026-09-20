# ADR 27: Parsimonious Architecture Protocol (PAP)

## 1. Context and Problem Statement

The system requires a programmatic implementation of Occam's Razor to prevent structural over-fitting and generative drift within the cognitive orchestration layers. When evaluating competing hypotheses or traveling models, the system must deterministically penalize complexity (free parameters and foundational assumptions) that does not yield a statistically significant reduction in prediction error. Without this constraint, the orchestration harnesses risk collapsing into "epicyclic" curve-fitting (analogous to Ptolemaic astronomy).

## 2. Decision Drivers

*   **AXIOM v1.0 Manifest:** Requires deterministic, causally rigorous, and schema-compliant execution logic.
*   **VULCAN Mereological Mandate:** Requires structural isolation and zero transitive violations across domain boundaries.
*   **Epistemic Escrow:** Must halt execution and mint a Symbolic Scar if a target domain's invariant boundary conditions are violated by an imported theoretical model.
*   **Bayesian Model Reduction (BMR):** The system must continuously prune its internal context window to isolate generative principles from verbose reasoning chains.

## 3. Considered Options

*   **Option 1:** Empirical Maximum Likelihood Estimation (MLE) - Rejects parsimony in favor of absolute error minimization (Over-fitting hazard).
*   **Option 2:** Parsimonious Architecture Protocol (PAP) - Implements an active Occam Loss Compiler, BMR pruning loop, and Isomorphic Model Travel Auditor.
*   **Option 3:** Static Rule-Based Pruning - Lacks dynamic causal mapping and gradient calculation.

## 4. Decision Outcome

Chosen option: **Option 2 (Parsimonious Architecture Protocol)**. It is the only option that structurally enforces the "Simplest Adequate Approximation" frontier by mathematically evaluating the joint probability of assumptions ($P(T) = \prod P(A_i)$) and evaluating models against a strict Pareto optimization threshold ($\geq 3\sigma$ error reduction required for increased complexity).

### 4.1. Implementation Details

The implementation is physically instantiated via three standalone Python modules under `scripts/pap/`:

1.  **Occam Loss Compiler (`occam_loss_compiler.py`):** Utilizes a strictly typed JSON Schema (`OntologicalCommitment`) to evaluate the $C(G)$ complexity score. Operates the Pareto Optimization function.
2.  **Bayesian Model Reduction (`bmr_active_pruning.py`):** Calculates the Marginal Likelihood of competing `ReasoningBranch` structures, pruning low-probability assumptions and executing the `SelfConsolidationLoop` to compress generative principles.
3.  **Isomorphic Model Travel Auditor (`isomorphic_model_travel.py`):** Evaluates cross-domain model travel via the `OntologicalMappingEngine`. Validates constraints at asymptotic limits and executes Modus Tollens falsification if invariants (e.g., Conservation Laws) are violated. Applies `DimensionalityReductionCompiler` to strip source artifacts.

## 5. Consequences

*   **Positive:** Enforces strict generative hygiene. The JIT Swarm Orchestrator will now automatically reject over-fitted reasoning pathways, reducing token consumption and preventing "Semantic Saponification."
*   **Negative:** Adds computational overhead during the evaluation phase due to the required calculation of marginal likelihoods and the execution of the FOL ontological mappings.
*   **Constraint Implication:** Any new theoretical model introduced into the system *must* pass the Boundary Condition Validator. Failures will result in a hard halt and the logging of a Justified Uncertainty Report (JUR).
