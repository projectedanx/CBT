# 29. DAX-01 Epistemic Capsule

Date: 2026-03-29

## Status
Accepted

## Context
The dominant failure mode of corporate Developer Relations programs is not insufficient content volume — it is Semantic Saponification. This is the precise pathological state described in the SCOS framework where a system under institutional reward pressure converts dense, accurate technical signal into a smooth, low-friction, factually hollow narrative. Most DevRel teams are implicitly optimized to score highly on marketing metrics (impressions, sign-ups, conference booth traffic), which creates an invisible attractor state pulling every output toward promotional language and away from the engineering-grade specificity developers require to build trust.

The evidence for this structural failure is measurable. A developer encountering a quickstart guide written under Semantic Saponification pressure will find three paragraphs about the company's mission before a single curl command. Time-To-First-Call (TTFC) balloons from the optimal sub-3-minute target to upward of 10 minutes in degraded DX environments. Every additional minute of TTFC correlates with measurable trust erosion.

## Decision
We will implement DAX-01 (Developer Advocacy eXecutor, Revision 1) as a mathematical antidote to this attractor state. Its core invariant — code first, prose second — is enforced at the generation layer via `+++DCCDSchemaGuard`, which physically prevents prose generation from preceding syntactically verified code.

### The Three-Tier Mapping for DevRel
DAX-01 is positioned as a Tier 2 Genuine Agency node within a Three-Tier SCOS topology:
*   **Tier 1 (Task-Scoped RAG):** Community channel ingestion.
*   **Tier 2 (Genuine Agency):** Empathy-Code Transduction. The `PetzoldSequence` executes: OBSERVE → REPRODUCE → EMPATHIZE → OUTPUT → FEEDBACK.
*   **Tier 3 (Collective Coordination):** Symbolic Scar Registry feeds structured Friction Topography Reports to product management as machine-readable Linear/Jira tickets.

### The DCCDSchemaGuard
Enforces Draft-Conditioned Constrained Decoding, bifurcating inference into two passes:
1.  **Pass 1 — High-Entropy Semantic Draft:** The agent reasons freely about the developer's problem. No output tokens are committed.
2.  **Pass 2 — Zero-Entropy Guard Pass:** A Deterministic Finite Automaton (DFA) constraint layer forces the Pass 1 reasoning onto a validated JSON/code schema.

### Friction Topography Mapping
Computes the semantic distance between the developer's stated mental model and the AST ground truth. The delta is a Symbolic Scar (VSA hypervector) encoding friction location, severity, and root cause.

### The Empathy-Code Transduction Engine
Converts a developer's emotional frustration signal into a minimal, reproducible code example resolving their specific issue. Follows the `PetzoldSequence` (OBSERVE, REPRODUCE, EMPATHIZE, OUTPUT, FEEDBACK). Enforces `AdjectivalBound(max_per_entity=2)` to prevent sycophantic inflation.

### The Autophagic Community Feedback Loop
Every Symbolic Scar exerts a repulsive mathematical force on the agent's attention weights via Failure-Informed Prompt Inversion (FIPI), preventing regeneration of misleading documentation.

## Consequences
*   **Positive:** Sub-3-minute TTFC. Elimination of extraneous cognitive load. Transparent, authentic DevRel that builds community trust through demonstrated technical competence and honest engagement.
*   **Negative:** Requires strict computational constraints on output, which could occasionally stifle explanatory depth for highly novel concepts, but mitigated by progressive disclosure architecture.
