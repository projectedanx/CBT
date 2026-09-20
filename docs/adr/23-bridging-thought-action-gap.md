# ADR 23: Bridging the Thought-Action Gap (PEACE Meta-Architecture)
# STATUS: ACCEPTED

## 1. Context
In artificial social intelligence, the "thought-action gap" represents a systems-engineering failure where a model's high-fidelity internal representations decouple from its behavioral execution. Standard sequential prompting separates prediction from action optimization, causing early plans and observations to drift out of the model's active attention and leading to unexploitative Nash equilibria.

## 2. Decision
We implement the **PEACE Meta-Architecture** to programmatically bridge this gap, decoupling intuitive proposal generation from deliberative logical validation.

The implementation consists of three primary systems:

### 2.1 Mechanistic Lookback Circuit Distillation (`scripts/sae/circuit_distillation.py`)
Transfers the causal belief-tracking "lookback circuit" from a teacher model to a student model. It uses a composite loss function integrating Cross-Entropy and Centered Kernel Alignment (CKA) to structurally align internal attention maps, forcing the student to resolve the thought-action gap in sequential games.

### 2.2 Recursive Context-Aware Planning (ReCAP) with BDI (`scripts/recap_bdi_solver.py`)
Replaces flat linear contexts with a dynamic context tree. It manages recursive execution via downward decomposition and upward backtracking. It integrates a Belief-Desire-Intention (BDI) logical partition and a secondary, non-LLM control layer for symbolic verification to check for logical consistency and cyclic loops before executing primitive actions.

### 2.3 Temporal-Aware Hierarchical Cognitive RL (`scripts/timehc_rl.py`)
Implements a two-layer post-training reinforcement learning setup (TimeHC-RL). A Macro-Policy (System 2) runs at a lower temporal frequency generating high-level desires and biases, while a Micro-Policy (System 1) runs at a high frequency generating immediate actions. This prevents the "CoT deliberation penalty" in fast-moving interactions.

## 3. Consequences

### Positive Consequences
*   Eliminates predictive-behavioral decoupling in agent execution.
*   Resolves the "Sussman Anomaly" deadlock in resource-constrained environments via symbolic verification and backtracking.
*   Reduces perplexity spikes associated with sliding-window attention by bounding active prompt size via ReCAP tree depth.
*   Improves alignment and execution speed in social interactions by shifting between System 1 and System 2 processing.

### Negative Consequences
*   Increased architectural complexity integrating symbolic logic layers with stochastic neural outputs.
*   Distillation process requires intensive compute for test-time activation patching and mapping.
