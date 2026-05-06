# VIPER_STRATEGY // Implementation Checklist

## Metric 1: Adjectival Dilution Score (ADS) Constraints
- [ ] Verify ADS < 0.15 threshold is enforced to prevent Attention Dilution and norm collapse.
- [ ] Ensure automatic re-run of Phase 2 (DENOISE) triggers if ADS exceeds 0.15.
- [ ] Confirm adherence to the Banned Token Protocol (no "masterpiece", "cinematic", "epic", etc.).

## Metric 2: Hardware Grounding Index (HGI) Mandate
- [ ] Ensure HGI target is exactly 100% (binary: present or absent).
- [ ] Verify every output contains explicitly defined hardware optical parameters (Lens, Aperture/Film_Stock, Lighting).
- [ ] For multi-subject scenes (≥3 subjects), ensure a full lighting diagram annotation is generated.

## Metric 3: Spatial Collision Rate (SCR) Prevention
- [ ] Verify target SCR is 0% over rolling 10-generation windows.
- [ ] Confirm RCC-8 topological bindings are applied for every prompt containing multiple interacting subjects.
- [ ] Ensure the Scar Archivist correctly maps and stores failure geometries as Symbolic Scars for FIPI application.

## Workflow & Formatting Integrity
- [ ] Ensure all generation outputs conform strictly to the Optical State Matrix (OSM) format (Diagnostic block followed by JSON target).
- [ ] Validate adherence to Draft-Conditioned Constrained Decoding (DCCD) schema enforcement.
- [ ] Verify the absence of any conversational prose, sycophancy, or summarization in the OSM output (Rule 4: No Semantic Saponification).

## Prune-First & Sovereign Intent
- [ ] Verify all dependencies remain pinned with strict semantic boundaries (`^` or `~`).
- [ ] Ensure zero non-standard execution scripts (`.js`, `.py`, `.sh`) are introduced to the root namespace.
- [ ] Confirm all generated documentation maintains a clinical, authoritative tone.
- [ ] Update `.jules/superintendent.md` with infrastructure change logs utilizing the `<thinking>` and `<final_output>` tag structure.
