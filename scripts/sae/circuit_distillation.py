import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Tuple

class MechanisticLookbackCircuitDistillation(nn.Module):
    """
    Implements Mechanistic Lookback Circuit Distillation.

    This module computes a composite loss to transfer the causal belief-tracking
    'lookback circuit' from a larger teacher model to a smaller student model,
    addressing the 'thought-action gap' by binding beliefs directly to the policy
    execution.

    Attributes:
        lambda_cka (float): Weight for the Centered Kernel Alignment (CKA) loss.
        paired_heads (List[Tuple[str, str]]): List of tuples mapping student head names
                                              to teacher head names.
    """
    def __init__(self, lambda_cka: float = 0.5, paired_heads: List[Tuple[str, str]] = None):
        super().__init__()
        self.lambda_cka = lambda_cka
        self.paired_heads = paired_heads or []

    def _cka_loss(self, K_s: torch.Tensor, K_t: torch.Tensor) -> torch.Tensor:
        """
        Computes the Centered Kernel Alignment (CKA) representational similarity loss.
        CKA(K_s, K_t) = ||K_s^T K_t||_F^2 / (||K_s^T K_s||_F * ||K_t^T K_t||_F)
        Loss = 1 - CKA to minimize divergence.

        Args:
            K_s (Tensor): Student activation map (batch_size, seq_len, head_dim)
            K_t (Tensor): Teacher activation map (batch_size, seq_len, head_dim)

        Returns:
            Tensor: Scalar loss value (1 - CKA).
        """
        # Flatten spatial dimensions
        batch_size = K_s.size(0)
        K_s_flat = K_s.view(batch_size, -1)
        K_t_flat = K_t.view(batch_size, -1)

        # Center the representations
        def center(x):
            mean = x.mean(dim=1, keepdim=True)
            return x - mean

        K_s_c = center(K_s_flat)
        K_t_c = center(K_t_flat)

        # Compute dot products
        dot_st = torch.sum(K_s_c * K_t_c, dim=1)
        dot_ss = torch.sum(K_s_c * K_s_c, dim=1)
        dot_tt = torch.sum(K_t_c * K_t_c, dim=1)

        # Add epsilon to prevent division by zero
        eps = 1e-8
        cka = dot_st / (torch.sqrt(dot_ss * dot_tt) + eps)

        # Loss is 1 - average CKA across batch
        return 1.0 - cka.mean()

    def forward(
        self,
        student_logits: torch.Tensor,
        target_labels: torch.Tensor,
        student_activations: Dict[str, torch.Tensor],
        teacher_activations: Dict[str, torch.Tensor]
    ) -> torch.Tensor:
        """
        Computes the composite loss: L_task + lambda * Sum(L_CKA)

        Args:
            student_logits (Tensor): Output logits of the student model.
            target_labels (Tensor): Ground truth labels for the downstream task.
            student_activations (Dict[str, Tensor]): Dictionary of internal activations
                                                     from the student's mapped heads.
            teacher_activations (Dict[str, Tensor]): Dictionary of internal activations
                                                     from the teacher's mapped heads.

        Returns:
            Tensor: The total composite loss.
        """
        # 1. Downstream Task Loss (Cross Entropy)
        # Assuming classification/autoregressive task
        loss_task = F.cross_entropy(
            student_logits.view(-1, student_logits.size(-1)),
            target_labels.view(-1)
        )

        # 2. Circuit Distillation Loss (CKA)
        loss_cka_total = 0.0
        if self.paired_heads:
            for s_head, t_head in self.paired_heads:
                if s_head in student_activations and t_head in teacher_activations:
                    K_s = student_activations[s_head]
                    K_t = teacher_activations[t_head]
                    loss_cka_total += self._cka_loss(K_s, K_t)

        total_loss = loss_task + (self.lambda_cka * loss_cka_total)
        return total_loss
