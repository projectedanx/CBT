import yaml
import json
import torch
import torch.nn as nn
from typing import Dict, Any, List

class LSeriesEpistemicCompiler:
    """
    Compiles the L-Series Ontology Schema into Verifiable Cognition Stack constraints.
    Maps epistemic concepts (L0-L11) into Differentiable Cache Augmentation boundaries.
    """

    def __init__(self, schema_path: str = 'pkm/L_Series_Conceptual_Hierarchy_v1.0.yaml'):
        self.schema_path = schema_path
        self.ontology = self._load_schema()

    def _load_schema(self) -> Dict[str, Any]:
        with open(self.schema_path, 'r') as f:
            return yaml.safe_load(f)

    def get_layer_constraint(self, layer_key: str) -> Dict[str, str]:
        """Returns the specific constraint definition for a given L-Series layer."""
        return self.ontology.get('layers', {}).get(layer_key, None)

    def generate_pytorch_loss_mask(self, active_layers: List[str], hidden_dim: int = 4096) -> torch.Tensor:
        """
        Generates a constraint mask tensor based on active L-Series layers.
        Used for Differentiable Cache Augmentation.

        Args:
            active_layers: List of layer keys (e.g., ['L8', 'L3.5'])
            hidden_dim: The dimensionality of the target KV-Cache or latent space.

        Returns:
            A boolean mask or continuous boundary tensor.
        """
        mask = torch.ones(hidden_dim, dtype=torch.float32)

        for layer in active_layers:
            constraint_data = self.get_layer_constraint(layer)
            if not constraint_data:
                continue

            c_type = constraint_data.get('constraint_type')

            # Simple heuristic mapping for demonstration of structural bounds
            if c_type == 'SymbolicScarDriftDetection': # L8
                # Stiffen the mask to reduce variance (enforce integrity)
                mask *= 0.5
            elif c_type == 'ThermodynamicContainment': # L3.5
                # Apply a strict truncation to simulate a firewall boundary
                mask[hidden_dim // 2:] = 0.0
            elif c_type == 'PhysicalSystemFoundation': # L1
                # Enforce physical grounding parameters
                mask = torch.clamp(mask, min=0.1, max=0.9)

        return mask

    def extract_vcp_ruleset(self) -> Dict[str, Any]:
        """
        Translates the entire L-Series schema into a JSON-serializable ruleset
        for consumption by the TS VerificationCoprocessorService.
        """
        ruleset = {}
        for layer_key, data in self.ontology.get('layers', {}).items():
            ruleset[layer_key] = {
                'constraint_id': data.get('constraint_type'),
                'description': data.get('description'),
                'active': True
            }
        return ruleset

if __name__ == "__main__":
    compiler = LSeriesEpistemicCompiler()
    rules = compiler.extract_vcp_ruleset()

    # Save the extracted ruleset for the TS services to consume
    with open('pkm/l_series_vcp_ruleset.json', 'w') as f:
        json.dump(rules, f, indent=2)

    print("Successfully compiled L-Series Epistemic Ruleset to JSON.")

    # Example tensor generation
    tensor_mask = compiler.generate_pytorch_loss_mask(['L8', 'L3.5'])
    print(f"Generated PyTorch Constraint Mask for L8 & L3.5. Shape: {tensor_mask.shape}, Active Elements: {tensor_mask.sum().item()}")
