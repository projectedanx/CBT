"""
Parsimonious Architecture Protocol (PAP) - Occam Loss Compiler

This module programmatically compiles competing scientific theories into
Directed Acyclic Graphs (DAGs) and computes an "Occam Loss Score" that penalizes
model complexity at the structural level.

Adheres strictly to the AXIOM v1.0 manifest: Deterministic, causally rigorous,
schema-compliant, and devoid of sycophancy or subjective adjectives.
"""

import json
import math
from typing import Dict, List, Any, Optional
import jsonschema
from pydantic import BaseModel, Field, ValidationError

# ---------------------------------------------------------------------------
# 1. ONTOLOGICAL COMMITMENT SCHEMA
# ---------------------------------------------------------------------------

ONTOLOGICAL_COMMITMENT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "theory_name": {"type": "string"},
        "variables": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "observable": {"type": "boolean"}
                },
                "required": ["name", "observable"]
            }
        },
        "free_parameters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "fine_tuned": {"type": "boolean"},
                    "dimension": {"type": "integer", "minimum": 1}
                },
                "required": ["name", "fine_tuned", "dimension"]
            }
        },
        "foundational_assumptions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "description": {"type": "string"},
                    "prior_probability": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                    "dependencies": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["id", "prior_probability", "dependencies"]
            }
        },
        "prediction_error_sigma": {"type": "number", "minimum": 0.0}
    },
    "required": ["theory_name", "variables", "free_parameters", "foundational_assumptions", "prediction_error_sigma"]
}

class Assumption(BaseModel):
    id: str
    description: Optional[str] = None
    prior_probability: float = Field(..., ge=0.0, le=1.0)
    dependencies: List[str]

class Parameter(BaseModel):
    name: str
    fine_tuned: bool
    dimension: int = Field(..., ge=1)

class Variable(BaseModel):
    name: str
    observable: bool

class OntologicalCommitment(BaseModel):
    theory_name: str
    variables: List[Variable]
    free_parameters: List[Parameter]
    foundational_assumptions: List[Assumption]
    prediction_error_sigma: float

# ---------------------------------------------------------------------------
# 2. QUANTITATIVE COMPLEXITY METRIC C(G)
# ---------------------------------------------------------------------------

class OccamLossCompiler:
    """
    Computes the complexity score and validates structural parsimony.
    """

    @staticmethod
    def compute_assumption_joint_probability(assumptions: List[Assumption]) -> float:
        """
        Calculates P(T) = \\prod P(A_i).
        Assumes conditional independence for simplification, or independent
        priors if dependencies are structured hierarchically.
        """
        p_t = 1.0
        for assumption in assumptions:
            p_t *= assumption.prior_probability
        return p_t

    @staticmethod
    def compute_structural_complexity(commitment: OntologicalCommitment) -> float:
        """
        Computes C(G) based on parameter dimensionality and assumption density.
        C(G) = -ln(\\prod P(A_i)) + \\lambda * \\sum (dim(P_j) * (2 if fine_tuned else 1))
        """
        # Penalty for assumptions (Information Shannon Entropy equivalent)
        p_t = OccamLossCompiler.compute_assumption_joint_probability(commitment.foundational_assumptions)
        assumption_penalty = -math.log(p_t) if p_t > 0 else float('inf')

        # Penalty for free parameters
        parameter_penalty = 0.0
        for param in commitment.free_parameters:
            weight = 2.0 if param.fine_tuned else 1.0
            parameter_penalty += param.dimension * weight

        return assumption_penalty + parameter_penalty

# ---------------------------------------------------------------------------
# 3. PARETO OPTIMIZATION (Simplest Adequate Approximation)
# ---------------------------------------------------------------------------

class ParetoOptimizer:
    """
    Evaluates the 'Simplest Adequate Approximation' between competing models.
    Rejects models that add parameters without >= 3 sigma decrease in error.
    """

    @staticmethod
    def evaluate_models(base_model: OntologicalCommitment, challenger_model: OntologicalCommitment) -> str:
        """
        Selects the optimal model based on the Occam boundary constraints.
        Returns the theory_name of the selected model.
        """
        c_base = OccamLossCompiler.compute_structural_complexity(base_model)
        c_challenger = OccamLossCompiler.compute_structural_complexity(challenger_model)

        e_base = base_model.prediction_error_sigma
        e_challenger = challenger_model.prediction_error_sigma

        delta_c = c_challenger - c_base
        delta_e = e_base - e_challenger # Positive means challenger has lower error

        # If challenger is more complex, it MUST reduce error by >= 3 sigma
        if delta_c > 0:
            if delta_e >= 3.0:
                return challenger_model.theory_name
            else:
                return base_model.theory_name
        # If challenger is simpler, it must not increase error by >= 3 sigma
        elif delta_c < 0:
            if delta_e > -3.0:
                return challenger_model.theory_name
            else:
                return base_model.theory_name
        # If complexity is equal, pick the one with lower error
        else:
            if delta_e > 0:
                return challenger_model.theory_name
            else:
                return base_model.theory_name

# ---------------------------------------------------------------------------
# 4. SIMULATED WALK-THROUGH (Copernican vs Ptolemaic)
# ---------------------------------------------------------------------------

def run_simulation():
    """
    Simulates the theory selection using Galileo's observations of Venus.
    """

    ptolemaic_data = {
        "theory_name": "Ptolemaic Geocentrism",
        "variables": [{"name": "Planetary Position", "observable": True}],
        "free_parameters": [
            {"name": "Deferent Radius", "fine_tuned": True, "dimension": 1},
            {"name": "Epicycle Radius", "fine_tuned": True, "dimension": 1},
            {"name": "Equant Offset", "fine_tuned": True, "dimension": 1}
        ],
        "foundational_assumptions": [
            {"id": "A1", "description": "Earth is stationary center", "prior_probability": 0.5, "dependencies": []},
            {"id": "A2", "description": "Perfect circular motion", "prior_probability": 0.3, "dependencies": ["A1"]}
        ],
        # Ptolemaic model cannot easily explain the full phases of Venus observed by Galileo
        "prediction_error_sigma": 15.0
    }

    copernican_data = {
        "theory_name": "Copernican Heliocentrism",
        "variables": [{"name": "Planetary Position", "observable": True}],
        "free_parameters": [
            {"name": "Orbital Radius", "fine_tuned": False, "dimension": 1}
        ],
        "foundational_assumptions": [
            {"id": "A1", "description": "Sun is stationary center", "prior_probability": 0.8, "dependencies": []}
        ],
        # Heliocentric naturally predicts full phases of Venus
        "prediction_error_sigma": 1.0
    }

    # Validate against Schema
    jsonschema.validate(instance=ptolemaic_data, schema=ONTOLOGICAL_COMMITMENT_SCHEMA)
    jsonschema.validate(instance=copernican_data, schema=ONTOLOGICAL_COMMITMENT_SCHEMA)

    # Load into Pydantic models
    ptolemaic = OntologicalCommitment(**ptolemaic_data)
    copernican = OntologicalCommitment(**copernican_data)

    print(f"[{ptolemaic.theory_name}]")
    print(f"  Complexity Score C(G): {OccamLossCompiler.compute_structural_complexity(ptolemaic):.4f}")
    print(f"  Prediction Error: {ptolemaic.prediction_error_sigma} sigma\n")

    print(f"[{copernican.theory_name}]")
    print(f"  Complexity Score C(G): {OccamLossCompiler.compute_structural_complexity(copernican):.4f}")
    print(f"  Prediction Error: {copernican.prediction_error_sigma} sigma\n")

    winner = ParetoOptimizer.evaluate_models(ptolemaic, copernican)
    print(f"[PARETO OPTIMAL SELECTION]: {winner}")

if __name__ == "__main__":
    run_simulation()
