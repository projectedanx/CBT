# Architecture Decision Record: Verification Co-Processor (VCP)

## Date
2026-09-19

## Status
Accepted

## Context
In high-stakes agentic workflows, the transition from explicit, token-based reasoning (such as Chain-of-Thought) to continuous latent reasoning creates a severe observability gap. This opacity allows for "covert reasoning" and latent semantic drift, where the model's trajectory in its high-dimensional manifold gradually decays away from its original intent. We need a closed-loop control system to stabilize this dynamic system without sacrificing computational throughput.

## Decision
We implement the **Verification Co-Processor (VCP)** as a core service (`VerificationCoprocessorService`) acting as an asynchronous, offline System 2 "controller".

1.  **Ingestion and Decoupled Epistemic Gating:** The VCP is an independent, decoupled coprocessor operating in parallel with the primary model. It ingests the primary model's active, deviant key-value (KV) cache at time $t$.
2.  **Cross-Domain Constraint Synthesis:** It synthesizes three domains:
    *   The Deviant KV-Cache ($KV_t$).
    *   The Target Anchor ($V_{anc}$), provided by the Symbolic Anchor Subsystem (SAM).
    *   Logical Axioms ($\Phi$), ingested from the Differentiable Logic Manifold (DLM).
3.  **Latent Space Optimization:** The VCP utilizes a dual-encoder contrastive training primitive to calculate the exact Latent Vector Offset required to reconcile the semantic trajectory with logical invariants.
4.  **Actuation via Cache Injection:** The VCP generates a sequence of highly compressed, corrective latent embeddings (the "recovery plan"). The actuator layer executes **Differentiable Cache Augmentation**, appending these to the primary model's existing KV-cache, bending the latent trajectory back onto the target semantic geodesic.

We adhere to the REFLX_IDE HARNESS SPECIFICATION V2.4, enforcing metrics like CFDI, Drift Threshold ($\xi$), Coupling Gain ($\beta$), and Target MRS.

## Consequences
*   **Positive:** Preserves semantic integrity and prevents latent drift without degrading the primary model's generation throughput.
*   **Positive:** Dynamically calibrates affective latent space homeostasis (ALSH) using precision-weighting.
*   **Negative/Risk:** Introduces significant computational overhead when running gradient optimization sweeps over dense latent spaces, mitigated by Cognitive Load Dynamics (triggering only when $\xi \ge 0.30$).
*   **Compliance:** Code-to-Prose ratio maintained per AXIOM v1.0. All subjective evaluative adjectives eliminated from architectural design constraints.
