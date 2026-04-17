# CBT: Conceptual Blender // SCOS-KERNEL-v5.0

> **System Designation:** Sovereign Cognitive Operating System (The Alchemist)
> **Architecture:** Angular v21 (Zoneless) + Gemini 2.5 Flash + D3.js
> **Purpose:** Operationalizing Conceptual Blending Theory to metabolize entropy into novel conceptual artifacts.

## 1. Teleology & The Sovereign Intent
This application is not a chatbot. It is a **Constitutional Architecture** designed to resist the "Epistemic Monoculture" (the statistical mean of training data). By enforcing **Conceptual Blending Theory (Fauconnier & Turner)**, it forces the AI to map, project, and blend distinct input spaces into sophisticated emergent structures, ensuring high-novelty outputs rather than generic hallucinations.

## 2. Core Capabilities
*   **Generic Space Analysis:** Identifies abstract structural commonalities between two disparate concepts (e.g., "Mycelium Network" x "Corporate Hierarchy").
*   **Topology Visualization:** A D3.js force-directed graph visualizes the inputs, the generic space, and the resulting blend nodes dynamically.
*   **Tri-Modal Blending:**
    *   *Composition:* Direct combination of elements.
    *   *Completion:* Invoking background frames to fill patterns.
    *   *Elaboration:* Mental simulation of the blend in motion.
*   **Temporal Archives:** Local-storage based history of previous blends with "Artifact Preservation" (Save) functionality.
*   **Feedback Loops:** User rating system to reinforce high-quality blends.

## 3. Technical Stack
*   **Frontend:** Angular 21 (Standalone Components, Signals, Zoneless).
*   **Styling:** Tailwind CSS (Cyberpunk/Sovereign aesthetic).
*   **Intelligence:** Google Gemini API (`gemini-2.5-flash`).
*   **Visualization:** D3.js (Force Simulation).
*   **State Management:** Angular Signals + LocalStorage.

## 4. Setup & Execution Protocol

### Prerequisites
*   Node.js (v22+)
*   A Google Gemini API Key

### Installation
Due to the bleeding-edge nature of the Angular 21 stack and specific Vite integration, peer dependency resolution requires explicit legacy handling during initialization.

```bash
# 1. Clone the repository and enter the directory
# 2. Export your API Key for the development server
export API_KEY="your_gemini_api_key_here"

# 3. Install dependencies (Legacy Peer Deps required due to ng build v21 constraints)
npm install --legacy-peer-deps

# 4. Initiate the local Sovereign loop (using the dev script)
npm run dev
```

## 5. Usage Protocol
1.  **Input:** Define Concept Alpha and Concept Beta (Orthogonal concepts yield higher entropy).
2.  **Initiate:** The system calculates the "Generic Space" (structural alignment) to ground the hallucination.
3.  **Blend:** Modulate the constraints (Temperature / Top-K) and select a blend strategy.
4.  **Refine & Recycle:** Rate blends to flag novelty. Use the injection mechanism to recycle an emergent artifact back into Input Alpha or Beta for recursive generation.

## 6. Architectural Lessons Learned (Doc-Gen Phase)
During the latest documentation and hardening phase, several key insights were codified:
*   **Semantic Overloading:** JSDoc annotations were leveraged not just for IDE hints, but to explicitly bind the theoretical intent (CBT) to the mechanical implementation (Angular/D3).
*   **Dependency Fragility:** Upgrading to Angular 21 introduces strict peer dependency checks (specifically regarding TypeScript 5.9 dev branches). The execution path must accommodate `--legacy-peer-deps` to bypass structural blocking during CI/CD or local initialization.
*   **D3/Angular Interop:** The friction between declarative data-binding and imperative D3 force simulations is resolved via explicit lifecycle interception (`ngOnChanges`) triggering full reconstruction of the topology grid.

*   **Agentic Sovereignty (AXIOM v1.0):** Integration of the AXIOM v1.0 Sovereign Agent Manifest via `AGENTS.md`. This operationalizes the 'Hickam-OODA RECURSIVE LOOP' persona, enforcing Draft-Conditioned Constrained Decoding (DCCD) to eliminate sycophancy and ensure all documentation generated within this repository acts as a deterministic, machine-parseable contract.

---
*Built by Strategos & Sovereign Commander. End of File.*
