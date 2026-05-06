# VULCAN_STRATEGY // Implementation Checklist

## Topological & Mereological Constraints
- [ ] Verify complete adherence to the Mereological Mandate: No state or network access transitivity exists between Part and Whole.
- [ ] Confirm zero cross-domain state mutation calls are present in the final architectural map.
- [ ] Ensure any database interactions strictly avoid the "Shared Database Pattern" (SCAR-002).
- [ ] Validate that all domain events utilize a message broker (e.g., Kafka/NATS) with independent read-model projections per consuming context.

## Epistemic Escrow & Constraints
- [ ] Verify that the CFDI brake threshold (0.15) is actively monitored during generation.
- [ ] Confirm execution halts immediately and issues a Justified Uncertainty Report if physical laws (e.g., CAP Theorem) are violated.
- [ ] Ensure the Bricolage Lens is applied: Remove any unwarranted complexity unless strict NFR Gate conditions are mathematically satisfied.

## Formatting & Generative Rigor
- [ ] Ensure all generated structural documents conform to `C4_Model_ADR_JSON`.
- [ ] Validate strict adherence to Draft-Conditioned Constrained Decoding (DCCD) schema enforcement.
- [ ] Verify that Adjectival Bounds are respected (no marketing terms, maximum of 0 subjective adjectives per entity).
- [ ] Confirm the use of the Hickam-OODA Recursive Loop JSON scaffold where applicable, followed by '---' and the final response.

## Prune-First & Sovereign Intent
- [ ] Verify all dependencies remain pinned with strict semantic boundaries (`^` or `~`).
- [ ] Ensure zero non-standard execution scripts (`.js`, `.py`, `.sh`) are introduced to the root namespace.
- [ ] Confirm all generated code and documentation maintain a dry, authoritative, and strictly causal tone.
- [ ] Update `.jules/superintendent.md` with infrastructure change logs utilizing the `<thinking>` and `<final_output>` tag structure.
