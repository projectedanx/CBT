import torch
import torch.nn as nn
import torch.nn.functional as F

class MacroPolicy(nn.Module):
    """
    System 2: Strategic Planning (Low Frequency)
    Generates high-level desires and personality-driven biases.
    Runs at a lower temporal frequency (e.g., once per conversational day/round).
    """
    def __init__(self, state_dim: int, bias_dim: int, hidden_dim: int = 256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, bias_dim)
        )

    def forward(self, macro_state: torch.Tensor) -> torch.Tensor:
        """
        Args:
            macro_state (Tensor): The high-level environmental/conversational state.
        Returns:
            Tensor: Macro-bias vector conditioning the micro-policy.
        """
        # Output could represent log-probabilities or a continuous latent bias
        return self.net(macro_state)

class MicroPolicy(nn.Module):
    """
    System 1: Execution (High Frequency)
    Generates immediate dialogue actions conditioned on the macro-bias.
    Runs at a high frequency (turn-by-turn).
    """
    def __init__(self, state_dim: int, bias_dim: int, action_dim: int, hidden_dim: int = 256):
        super().__init__()
        self.fc1 = nn.Linear(state_dim + bias_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.action_head = nn.Linear(hidden_dim, action_dim)

    def forward(self, micro_state: torch.Tensor, macro_bias: torch.Tensor) -> torch.Tensor:
        """
        Args:
            micro_state (Tensor): The immediate, local conversational state.
            macro_bias (Tensor): The conditioning vector from the MacroPolicy.
        Returns:
            Tensor: Action logits for the current turn.
        """
        # Concatenate state and bias
        x = torch.cat([micro_state, macro_bias], dim=-1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        action_logits = self.action_head(x)
        return action_logits

class TimeHCRLTrainer:
    """
    Temporal-aware Hierarchical Cognitive Reinforcement Learning (TimeHC-RL)
    Integrates Macro (System 2) and Micro (System 1) policies to prevent
    the 'CoT deliberation penalty' in fast-moving social interactions.
    """
    def __init__(self, macro_policy: MacroPolicy, micro_policy: MicroPolicy):
        self.macro_policy = macro_policy
        self.micro_policy = micro_policy

    def get_action(self, macro_state: torch.Tensor, micro_state: torch.Tensor, macro_step: bool = False) -> torch.Tensor:
        """
        Determines the action, conditionally updating the macro-bias based on temporal frequency.

        Args:
            macro_state (Tensor): High-level state.
            micro_state (Tensor): Turn-level state.
            macro_step (bool): Whether to update the macro-policy on this step.

        Returns:
            Tensor: The chosen action logits.
        """
        if macro_step or not hasattr(self, 'current_macro_bias'):
            # Expensive System 2 deliberation
            self.current_macro_bias = self.macro_policy(macro_state)

        # Fast System 1 execution conditioned on System 2 bias
        action_logits = self.micro_policy(micro_state, self.current_macro_bias)
        return action_logits
