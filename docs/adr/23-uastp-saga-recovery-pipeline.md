# ADR 23: UASTP Saga Recovery Pipeline via Isomorphic GitHub Actions AST

## 1. Title and Context
- **Title:** Isomorphic Mapping of UASTP Cognitive Contracts to GitHub Actions ASTs
- **Status:** Approved
- **Context:** SCOS requires translating high-entropy Unified Agentic Skill & Tool Protocol (UASTP) declarative contracts into zero-entropy GitHub Actions workflows. Probabilistic agent decisions introduce stateful deviations leading to Catastrophic State Drift and Topological Tearing.

## 2. Decision
We have compiled the UASTP state machine into the GitHub Actions runner runtime via an isomorphic mapping.
- Forward Transactions ($T_f$) map to explicit state validation gates.
- Compensating Transactions ($T_c$) map to idempotent rollback steps gated by `if: failure()`.
- Verification Gates ($\mathcal{V}$) map to automated testing blocks.
- Unresolved validation failures or CFDI breaches trigger the rollback block.

We enforce:
- The Least-Privilege Identity Rule (`[G⁻.1]`) using OIDC.
- Supply-Chain Commit Pinning to prevent Slopsquatting and Injection Weaknesses.
- Read-Only/Write-Only Decoupling separating epistemic audits from stateful deployments.
- Continuous falsification testing to detect 'Lost Compensation' dilemmas resulting in Epistemic Escrow.

## 3. Consequences
- **Positive:** Reduces Epistemic Crash Rate (ECR) to 0%. Mitigates Semantic Saponification and Chronological Saponification. Stabilizes CI/CD pipelines under probabilistic generation.
- **Negative:** Introduces a Thermodynamic Latency Tax (45-90 seconds) per pipeline run.

## 4. Compliance
- Adheres to AXIOM v1.0 and AGS-A standards.
- Reifies the "Prune-First Protocol" (explicit SHA pinning on GitHub Actions dependencies).
