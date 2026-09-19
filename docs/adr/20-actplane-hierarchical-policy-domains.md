# 20. ActPlane Hierarchical Policy Domains

Date: 2026-09-20

## Status

Accepted

## Context

To engineer a production-grade AI system, systems architects must invert the traditional, model-centric development paradigm. An LLM is a probabilistic next-token generator; it possesses no intrinsic capability to securely execute sequential operations, enforce runtime safety, or maintain durable state across time. Instead, the surrounding **harness** acts as the operating system for cognitive workloads, converting non-deterministic reasoning into verifiable system behavior.

At the core of this engineering discipline lies a fundamental division of control: **Hierarchical Policy Domains**. By nesting security boundaries within the process tree and enforcing them natively in the operating system kernel, this architecture guarantees that no downstream sub-agent or generated script can ever weaken, disable, or bypass parent-imposed invariants.

## Decision

We will implement the **ActPlane Sovereignty-Enforcement Split** using eBPF LSM integration.

### The Four Pillars of Policy Domain Specification Planning

1.  **Automated Discovery and Constraint Mining:**
    *   **Invariant Mining (Parent Constraints):** Static, non-negotiable core policies (e.g., "never expose credentials") are loaded into a higher-authority constraint ring before agent execution. These are inherited monotonically by child domains and are read-only.
    *   **Soft Target Discovery:** Child agents can author runtime policy deltas (e.g., restricting specific paths based on context), which are submitted and validated by the parent.
2.  **Isomorphic Formalization (From Rules to Bitmasks):**
    *   Policy domains are formalized as **in-kernel eBPF maps**.
    *   A `pid_domain_map` links PIDs to domains.
    *   A `domain_registry` stores metadata: `parent_domain_id`, `inherited_rules`, `inherited_labels`, `local_rules`, and `active_labels`.
    *   **Monotonic Label Propagation (IFC State Machine):** Cryptographic-style information-flow control (IFC) labels are attached to OS objects and propagate monotonically: $\text{Label}_{\text{target}} \gets \text{Label}_{\text{target}} \lor \text{Label}_{\text{source}}$.
3.  **Parametric Trade-off Modeling:**
    *   ActPlane domain hierarchy adds minimal latency ($\approx 1.9\%$ overhead) via BPF-LSM and tracepoint hooks, offering high isolation without the latency of hardware-virtualization.
    *   **Mitigation for Label Creep:** Spawning a fresh subprocess clears inherited file-read labels, bounding taint accumulation.
4.  **Continuous Falsification and Edge-Case Stress Testing:**
    *   **Gate-Bypassing Defense:** An in-kernel **Authority Checker** intercepts runtime deltas and rejects any that mask inherited gates.
    *   **Laid-back Defense (Privilege Scoping):** Declassification authority is strictly bound to the domain that authored the rule. Child domains cannot clear inherited labels.

## Consequences

*   **Security:** Provides a verifiable zero-trust cross-harness state execution environment.
*   **Performance:** Maintains low latency for high-speed agentic loops compared to full containerization.
*   **Complexity:** Requires maintenance of eBPF kernel C code and strict adherence to monotonic label propagation logic.
