import numpy as np
from pydantic import BaseModel, Field
from typing import List, Dict, Set, Optional

# ==============================================================================
# COGNITIVE ARCHITECTURE COMPILER
# Purpose: Formalizes the transition from propositional fact-gathering to
#          holistic causal understanding using Fictive Principles and Grasping Metrics.
# ==============================================================================

class FictivePrinciple(BaseModel):
    """Ontology of idealized assumptions used in scientific modeling."""
    id: str
    name: str
    description: str
    is_strictly_true: bool = False
    computational_utility_score: float = Field(..., ge=0.0, le=1.0)
    explanatory_power_score: float = Field(..., ge=0.0, le=1.0)

class CognitiveModel(BaseModel):
    """A framework of understanding applied to a specific domain."""
    name: str
    fictive_principles: List[FictivePrinciple]
    causal_dependencies: Dict[str, List[str]] # Node -> [Dependencies]

    def calculate_understanding_score(self, target_domain_complexity: float) -> float:
        """
        Calculate the 'Grasping Metric'.
        Understanding is high when explanatory power is high and computational cost is manageable,
        even if the underlying principles are strictly false.
        """
        avg_utility = np.mean([p.computational_utility_score for p in self.fictive_principles])
        avg_power = np.mean([p.explanatory_power_score for p in self.fictive_principles])

        # Grasping metric is a function of explanatory power, utility, penalized by domain complexity
        grasping_score = (avg_utility * 0.4 + avg_power * 0.6) / max(1.0, np.log1p(target_domain_complexity))
        return grasping_score

def simulate_understanding_scenario():
    print("=== INITIALIZING COGNITIVE ARCHITECTURE COMPILER ===")

    # 1. Define Fictive Principles for Newtonian Gravity
    p1 = FictivePrinciple(
        id="FP_001",
        name="Absolute Space and Time",
        description="Space and time are rigid, uniform, and independent of observer state.",
        is_strictly_true=False, # Defeated by Special Relativity
        computational_utility_score=0.95, # Extremely easy to compute
        explanatory_power_score=0.85      # Explains most low-velocity phenomena
    )

    p2 = FictivePrinciple(
        id="FP_002",
        name="Instantaneous Action at a Distance",
        description="Gravity propagates infinitely fast between point masses.",
        is_strictly_true=False, # Defeated by General Relativity (speed of light limit)
        computational_utility_score=0.98, # Trivial vector addition
        explanatory_power_score=0.90      # Highly accurate for solar system orbital mechanics
    )

    p3 = FictivePrinciple(
        id="FP_003",
        name="Point Mass Idealization",
        description="Massive bodies are treated as zero-dimensional points at their center of mass.",
        is_strictly_true=False, # Planets are extended bodies
        computational_utility_score=0.99,
        explanatory_power_score=0.95
    )

    # 2. Construct the Newtonian Model
    newtonian_model = CognitiveModel(
        name="Newtonian Gravitational Framework",
        fictive_principles=[p1, p2, p3],
        causal_dependencies={
            "Force": ["Mass_1", "Mass_2", "Distance"],
            "Acceleration": ["Force", "Mass_target"],
            "Trajectory": ["Acceleration", "Initial_Velocity", "Absolute_Time"]
        }
    )

    # 3. Apply to Domain: Solving an Astrophysical Trajectory (e.g., Apollo Moon Mission)
    # The domain is complex but mostly low-velocity, weak gravity.
    domain_complexity = 2.5

    print(f"\nEvaluating Model: {newtonian_model.name}")
    print("Injecting Fictive Principles (Strictly False but Computationally Potent):")
    for fp in newtonian_model.fictive_principles:
        print(f"  - {fp.name}: Factive={fp.is_strictly_true}, Utility={fp.computational_utility_score}")

    score = newtonian_model.calculate_understanding_score(target_domain_complexity=domain_complexity)

    print("\n--- GRASPING METRIC RESULTS ---")
    print(f"Target Domain Complexity: {domain_complexity}")
    print(f"Calculated Understanding Score: {score:.3f} (Max ~1.0 for given complexity)")

    print("\n[EPISTEMIC CONCLUSION]")
    print("The agent retains a high Understanding Score by leveraging non-factive")
    print("idealizations (Fictive Principles). Strict truth (factivity) is not required")
    print("for high causal understanding in localized domains, demonstrating the")
    print("parsimony of the Newtonian framework despite General Relativistic defeaters.")
    print("=== COMPILATION COMPLETE ===")

if __name__ == "__main__":
    simulate_understanding_scenario()
