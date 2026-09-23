# 30. Anomaly Learning Agent (ALA)

Date: 2026-03-30

## Status
Accepted

## Context
Within advanced neuro-symbolic security architectures designed to monitor autonomous agent workflows, the **Anomaly Learning Agent (ALA)** serves as a meta-learning system that adapts the defensive posture of a system in real time. The core of its perception engine is the **Statistical Anomaly Score**, which quantifies the predictability of an agent’s behavior to preemptively flag **"grey-zone misuse"**—actions that are individually authorized but whose sequence and intent indicate malicious or misaligned processes.

The Statistical Anomaly Score is not a simple heuristic; it is the output of a multi-layered, hybrid neural-symbolic calculation that combines sequence probability modeling, information-theoretic entropy tracking, and dynamic Bayesian inference.

## Decision
We will implement the Anomaly Learning Agent (ALA) as the primary safety and alignment harness, wrapping state-of-the-art continuous latent reasoning models. The ALA calculates its Statistical Anomaly Score by executing parallel mathematical evaluations over a sliding window of recent actions:

1. **Neural Sequence Modeling (System 1):** A Recurrent Neural Network (RNN) or Transformer computes the probability of the token sequence. $S_{\text{neural}} = 1 - P(tool_t \mid tool_{<t}, \text{Context})$
2. **First-Order Markov Transition Probability:** Computes transition probabilities $P(tool_j \mid tool_i)$ between adjacent tool calls to establish a low-latency baseline.
3. **Toolchain Entropy Gradient Mapping:** Applies Shannon information entropy to quantify "behavioral surprise". The rate of change (gradient) flags rapid shifts to chaotic actions.
4. **Relative Entropy (Kullback-Leibler Divergence):** Computes $D_{KL}(P \mid\mid Q)$ between observed tool-transition frequencies and a task-specific baseline.
5. **Probabilistic Action-Behavior Model (PABM):** Evaluates sequences via a Dynamic Bayesian Network (DBN), computing joint probability using inference algorithms like the Viterbi algorithm.

### The ALA Guard Verification Loop
The ALA executes a Run-Time Verification Loop Algorithm:
1.  **Extract State:** Ingest tool, arguments, and execution trace into Action Vector $V_{\text{action}}$.
2.  **Verify watchlists:** Check against the `Affordance Watchlist` ($W_{\text{watch}}$). Watchlisted tools trigger the full NeSy ALA suite. Non-watchlisted tools use the instantaneous Toolchain Entropy Gradient (threshold $\le 0.40$ for laminar pass).
3.  **Execute NeSy ALA Synthesis:** Compute $S_{\text{neural}}$, $F_{\text{symbolic}}$ (BICM Intent Divergence $S_{BICM}$ from SEPAO Graph), and $S_{\text{recon}}$ (Graph Autoencoder Reconstruction Error).
4.  **Synthesize Risk:** $\text{RiskScore} = w_1 S_{\text{neural}} + w_2 S_{BICM} + w_3 S_{\text{recon}} + w_4 F_{\text{symbolic}}$
5.  **Evaluate Thresholds:** If $\ge 0.80$, halt synchronously, generate Ontological Traceback, present for HITL triage, log as Symbolic Scar, and feed gradient to ALA RL policy.

### Threshold Dynamics Simulation
The ALA detection threshold $\theta(t)$ models a dynamic physical system:
$$\frac{d\theta(t)}{dt} = -\alpha \cdot \text{Grad}_{\theta}\mathcal{L}_{\text{FalsePositive}}(t) + \beta \cdot \text{Grad}_{\theta}\mathcal{L}_{\text{TruePositive}}(t) - \eta \cdot \theta(t)$$
Targeting a Critically Damped (Homeostatic Balance) profile to avoid "Sycophantic Blindness" (Under-Damped) and "Semantic Ossification" (Over-Damped).

### Isomorphic Formalization (PROV-AGENT Schema)
Anomaly detections, HITL interventions, and parameter updates must compile to a strictly typed, verifiable record governed by the PROV-AGENT Schema, preserving causal lineage.

## Consequences
*   **Positive:** Dynamic mapping of the optimal boundary, permitting constructive, high-entropy exploration under low-risk contexts while applying absolute preemption when high-impact watchlist tools are accessed anomalously. Generative Adversarial Resilience (GAR) via automated Failure Generator red-teaming.
*   **Negative:** Fusing deep sequential models with GNN-based graph ontological traversals introduces computational and memory latency. Mitigated by Epistemic Triage: running full evaluations only when entropy gradients cross warning thresholds or watchlisted tools are invoked.
