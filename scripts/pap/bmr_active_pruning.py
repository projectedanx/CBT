"""
Parsimonious Architecture Protocol (PAP) - Bayesian Model Reduction (BMR)

This module operationalizes BMR during complex multi-agent workflows, serving as
an active inference reasoning harness. It evaluates candidate hypotheses and prunes
superfluous parameters to find simpler, more generalizable explanations,
minimizing complexity while maintaining accuracy.

Adheres strictly to the AXIOM v1.0 manifest.
"""

import math
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# STRUCTURES
# ---------------------------------------------------------------------------

class ReasoningNode(BaseModel):
    id: str
    description: str
    is_assumption: bool = False
    prior_probability: float = Field(1.0, ge=0.0, le=1.0)
    complexity_weight: float = Field(1.0, ge=0.0) # E.g., length of explanation or cognitive load

class ReasoningBranch(BaseModel):
    id: str
    nodes: List[ReasoningNode]
    explanatory_power: float = Field(..., ge=0.0, le=1.0) # Accuracy/Likelihood of explaining the anomaly

    @property
    def assumption_count(self) -> int:
        return sum(1 for node in self.nodes if node.is_assumption)

# ---------------------------------------------------------------------------
# 1. THEORY-BUILDING PHASE
# ---------------------------------------------------------------------------

class TheoryBuilder:
    """
    Simulates the abductive reasoning and analogical mapping phase to generate
    competing candidate hypotheses (Reasoning Branches) for a given anomaly.
    """

    @staticmethod
    def generate_hypotheses(anomaly_description: str) -> List[ReasoningBranch]:
        """
        Mock implementation generating competing reasoning branches.
        In production, this interfaces with the LLM abductive generator.
        """
        # Complex Branch: High explanatory power, many assumptions
        branch_a = ReasoningBranch(
            id="Complex_AdHoc",
            nodes=[
                ReasoningNode(id="n1", description="Observation matches pattern X", is_assumption=False),
                ReasoningNode(id="n2", description="Assume external interference by agent Y", is_assumption=True, prior_probability=0.2),
                ReasoningNode(id="n3", description="Assume sensor malfunction simultaneously", is_assumption=True, prior_probability=0.1),
                ReasoningNode(id="n4", description="Resulting cascade causes anomaly", is_assumption=False)
            ],
            explanatory_power=0.99
        )

        # Parsimonious Branch: Good explanatory power, few assumptions
        branch_b = ReasoningBranch(
            id="Parsimonious_Causal",
            nodes=[
                ReasoningNode(id="n1", description="Observation matches pattern X", is_assumption=False),
                ReasoningNode(id="n2", description="Assume standard thermal degradation", is_assumption=True, prior_probability=0.8),
                ReasoningNode(id="n3", description="Thermal limit reached, triggering failsafe (anomaly)", is_assumption=False)
            ],
            explanatory_power=0.92
        )

        return [branch_a, branch_b]

# ---------------------------------------------------------------------------
# 2. AXIOMATIC PRUNING MODULE
# ---------------------------------------------------------------------------

class AxiomaticPruningModule:
    """
    Calculates a marginal likelihood score for each reasoning branch,
    penalizing paths that introduce unverified assumptions or ad-hoc explanations.
    """

    @staticmethod
    def calculate_marginal_likelihood(branch: ReasoningBranch, lambda_penalty: float = 2.0) -> float:
        """
        Calculates the approximate evidence: Evidence ≈ Accuracy - Complexity.
        Complexity is derived from assumption priors and node weights.
        """
        accuracy = branch.explanatory_power

        # Calculate complexity (KL divergence approximation)
        # We penalize low-probability assumptions heavily.
        complexity = 0.0
        for node in branch.nodes:
            if node.is_assumption:
                # -ln(P) gives high penalty for low probability
                penalty = -math.log(node.prior_probability) if node.prior_probability > 0 else float('inf')
                complexity += penalty * node.complexity_weight
            else:
                # Minor penalty for general verbosity/chain length
                complexity += 0.1 * node.complexity_weight

        # Normalize or scale complexity
        # Evidence = log(Accuracy) - lambda * Complexity
        log_accuracy = math.log(accuracy) if accuracy > 0 else float('-inf')
        marginal_likelihood = log_accuracy - (lambda_penalty * complexity)

        return marginal_likelihood

    @staticmethod
    def select_best_branch(branches: List[ReasoningBranch]) -> ReasoningBranch:
        """
        Selects the branch with the highest marginal likelihood (Occam's Razor).
        """
        best_branch = None
        best_score = float('-inf')

        for branch in branches:
            score = AxiomaticPruningModule.calculate_marginal_likelihood(branch)
            if score > best_score:
                best_score = score
                best_branch = branch

        return best_branch

# ---------------------------------------------------------------------------
# 3. SELF-CONSOLIDATION LOOP
# ---------------------------------------------------------------------------

class SelfConsolidationLoop:
    """
    Compresses internal prompt context windows, replacing verbose step-by-step
    logic with concise, elegant "fictive principles" that preserve maximum
    explanatory power.
    """

    @staticmethod
    def consolidate(branch: ReasoningBranch) -> str:
        """
        Compresses the winning branch into a summarized generative principle.
        """
        # In a real system, this would use LLM summarization bounded by the
        # semantic tokens of the nodes. Here we mock the compilation.

        assumptions = [n.description for n in branch.nodes if n.is_assumption]
        conclusions = [n.description for n in branch.nodes if not n.is_assumption]

        principle = f"PRINCIPLE [{branch.id}]: Given {', '.join(assumptions)}, it follows that {', '.join(conclusions)}."
        return principle

# ---------------------------------------------------------------------------
# EXECUTION HARNESS
# ---------------------------------------------------------------------------

def run_bmr_harness():
    print("=== BAYESIAN MODEL REDUCTION (BMR) HARNESS ===")

    anomaly = "System failure occurred simultaneously with anomalous sensor readings at Sector 7."
    print(f"\n[ANOMALY]: {anomaly}")

    # Phase 1: Theory-Building
    hypotheses = TheoryBuilder.generate_hypotheses(anomaly)
    print(f"\n[THEORY-BUILDING]: Generated {len(hypotheses)} competing hypotheses.")

    # Phase 2: Axiomatic Pruning
    print("\n[AXIOMATIC PRUNING]: Calculating Marginal Likelihoods...")
    for branch in hypotheses:
        score = AxiomaticPruningModule.calculate_marginal_likelihood(branch)
        print(f"  - Branch '{branch.id}' | Explanatory Power: {branch.explanatory_power:.2f} | Assumptions: {branch.assumption_count} | Marginal Likelihood: {score:.4f}")

    winning_branch = AxiomaticPruningModule.select_best_branch(hypotheses)
    print(f"\n[PRUNING DECISION]: Selected Branch -> {winning_branch.id}")

    # Phase 3: Self-Consolidation
    consolidated_principle = SelfConsolidationLoop.consolidate(winning_branch)
    print("\n[SELF-CONSOLIDATION LOOP]: Context Window Compressed.")
    print(f"  -> {consolidated_principle}")

if __name__ == "__main__":
    run_bmr_harness()
