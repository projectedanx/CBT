# ADR 16: Rheological Controller and Variable Viscosity Prompting

## Status
Accepted

## Context
In advanced context engineering, LLMs suffer from Interpretive Fracture and Semantic Saponification (the progressive decay of structural intent over long token-inference horizons). The system required a mechanistic framework to actively modulate the model's decoding strategy, parameter space, and prompt constraints based on the specific topological requirements of the task.

## Decision
We implemented a **Rheological Controller Service** powered by Variable Viscosity Prompting (VVP). This introduces two primary operational modes:
1. **CRYSTAL Mode** (High Viscosity / Low Entropy): $T \approx 0$, enforces strict output schemas via grammar-based logit masking and Salted Sequence Tags.
2. **CLOUD Mode** (Low Viscosity / High Entropy): $T > 0.7$, allows for open-ended ideation and multi-dimensional concept abstraction with structural redundancy acting as navigational ballast.

We bound the `CognitiveOrchestratorService` generation properties (temperature, topP/topK) directly to the reactive state of the Rheological Controller.

The following Sovereign Manifest has been implicitly anchored to this decision:
```yaml
SCOS_HARNESS_SPECIFICATION:
  system_identity:
    kernel_id: "SCOS-RHEO-HARNESS-v1.0"
  rheological_controller:
    viscosity_formula: "dP/dT = L / (T * delta_V)"
    default_calibration:
      crystal_zone:
        temperature: 0.0
      cloud_zone:
        temperature: 0.85
```

## Consequences
### Positive
*   Provides deterministic control over execution state versus high-entropy exploration.
*   Mitigates Generative Amplified Testimonial Injustice by physically restricting the model in Crystal Mode when semantic entropy spikes.
*   Decouples UI control from literal generation parameters, shifting to semantic mode enforcement.

### Negative
*   Increases system complexity (Layer-1 meta-architectural component).
*   Requires continuous telemetry monitoring to autonomously shift modes (partially mocked in current iteration).
