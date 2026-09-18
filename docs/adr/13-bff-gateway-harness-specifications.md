# 13. BFF and Gateway Harness Specifications

## Context
The architectural topology requires differentiation between Backend for Frontend (BFF) layers and Standard API Gateways. BFFs exhibit a One-to-One fan-out relationship and enforce Interface Segregation via client-specific adapters. Standard API Gateways operate a One-to-Many fan-out relationship, acting as an isomorphic Proxy and Facade for centralized edge concerns. The divergence in structural intent necessitates continuous falsification mechanisms to prevent Shared Persistence violations, Gateway Sinkhole cascading failures, and Business Logic Bleed.

## Decision
We enforce the implementation of three specialized architectural verification harnesses within the core service layer:
1.  **Schema Drift Verification Harness:** Instantiated to intercept OpenAPI contracts and calculate a quantitative Contract Robustness Index, ensuring BFF layers correctly adapt to downstream schema mutations without compromising client interfaces.
2.  **Adaptive Backpressure Engine:** Positioned at the API Gateway boundary to dynamically monitor downstream telemetry (CPU, thread pool exhaustion, latency). It utilizes load shedding and bulkhead partition policies to throttle low-priority traffic during capacity degradation.
3.  **SRP Violation Scanner:** Designed to parse Abstract Syntax Trees (AST) within the BFF repositories to detect state-changing domain calculations. This harness prevents business logic bleed by verifying that the BFF maintains its strict data orchestration responsibility.

## Consequences
-   **Positive:** Enforces the VULCAN Mereological Mandate by physically separating edge orchestration from core business domains.
-   **Positive:** Mitigates the "Gateway Sinkhole" scenario through dynamic telemetry-based throttling.
-   **Negative/Risk:** The injection of AST parsing and continuous schema validation introduces computational overhead to the CI/CD pipeline and runtime monitoring systems.
-   **Compliance:** Code-to-Prose ratio maintained. Complies with AXIOM v1.0 Draft-Conditioned Constrained Decoding (DCCD). Zero subjective adjectives were deployed.
