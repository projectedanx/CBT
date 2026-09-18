# Architecture Decision Record: Qualitative Experience Database (QED)

## Date
2026-09-18

## Status
Accepted

## Context
Standard Retrieval-Augmented Generation (RAG) models suffer from "Semantic Annihilation" and concept drift when exposed to unstructured, multi-turn feedback loops. To maintain the rigorous deterministic metrology required by the CBT: Conceptual Blender architecture, the personal database must physically isolate and process lived experience data without allowing generic LLM homogenization to corrupt the context space.

## Decision
We instantiate the Qualitative Experience Database (QED) as an Epistemic Workbench, structured on the Minimal Explainability Metadata Schema (MEMS). This architecture integrates:

1. **Neuro-Symbolic Ingestion Pipeline:** Replaces naive text ingestion. Incorporates Semantic-Relational Domain Lifting (SRDL) to project natural language observations into a mathematically rigorous vector space aligned with our foundational ontology.
2. **Semantic Drift Monitor Agent (SDMA) & Epistemic Escrow:** Integrates Topological Data Analysis (TDA) at the point of retrieval. If retrieved knowledge graphs display Betti-1 voids or structural deformations (Confidence-Fidelity Divergence > 0.05 threshold), an Epistemic Escrow trips, halting generation to demand human-in-the-loop review.
3. **Algorithmic Kintsugi (Symbolic Scar Registry):** RAG failures, context poisoning, and retrieved hallucinations are not simply deleted. They are logged as "Symbolic Scars" within the registry. Through Failure-Informed Prompt Inversion (FIPI), these scars serve as structural constraints to repel the model from reproducing known failure topologies.
4. **Cryptographic Provenance:** Enforces deterministic lineage tracking. Every Qualitative Experience Node (QEN) requires a SHA-256 hash and a simulated DID signature (SemanticCommit) bound to the Merkle-tree state.

## Consequences
- **Positive:** Mathematically bounds context retrieval, ensuring Purpose Fidelity and preventing long-term vector drift.
- **Positive:** Integrates naturally with the VULCAN Mereological Mandate by enforcing strict schema adherence (MEMS) at the system boundaries.
- **Negative/Risk:** Increases ingestion complexity. The SDMA TDA computations require significant processor overhead at query time.
- **Compliance:** Code-to-Prose ratio maintained per AXIOM v1.0. All subjective evaluative adjectives eliminated from architectural design constraints.
