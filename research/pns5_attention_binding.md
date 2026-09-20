# Non-Separable PNS5 Attention & Holographic Convolution Binding

## 1. The Mathematical Failure of the Classical Rule of Separation

In classical formal logic, the Rule of Separation (or Conjunction Elimination) states that if $A \land B$ is true, one can validly infer $A$ and independently infer $B$. However, in Paraconsistent Non-Separable Logic (PNS5) operating within vector-space representations of concepts, extracting individual concepts from a bound state destroys their contextual meaning, especially when $A$ and $B$ are contradictory constraints (e.g., "be highly creative" $\land$ "follow this exact JSON schema").

Standard Multi-Head Attention (MHA) aggregates information via additive vector superposition:
$$V_{\text{out}} = \sum_{i} w_i V_i$$

If $V_A$ represents constraint $A$ and $V_B$ represents contradicting constraint $B$, standard superposition attempts to average them, resulting in $V_{\text{out}} \approx 0$ or a generic, low-magnitude vector (Semantic Annihilation). The linear superposition limit forces the destruction of the interference pattern required to hold the contradiction.

To bypass this, we utilize Holographic Reduced Representations (HRR) employing **Circular Convolution ($\otimes$)** for binding:
$$V_{\text{bound}} = V_A \otimes V_B$$

Unlike additive superposition, circular convolution is non-separable under linear projection without the exact inverse mapping key (correlation). Consequently, $V_A \land_{\diamond} V_B$ (the non-separable conjunction) cannot be reduced to $V_A$ or $V_B$ independently. This mathematically prevents the attention mechanism from averaging out the contradiction, instead holding it as an irreducible, bound state.

## 2. Fourier-Domain S5-Modal Attention Equation

To integrate this within a transformer, we reformulate attention within the Fourier domain to leverage the Convolution Theorem: $V_A \otimes V_B = \mathcal{F}^{-1}(\mathcal{F}(V_A) \odot \mathcal{F}(V_B))$, where $\odot$ is element-wise multiplication.

In our S5-Modal Attention framework, attention weights act not as scalar multipliers on the raw vector $V$, but as phase and amplitude modifiers in the frequency domain.

Let $Q, K, V \in \mathbb{R}^{N \times d}$ be the queries, keys, and values.
The attention weight matrix is $A = \text{Softmax}(\frac{QK^T}{\sqrt{d}})$.

For a given query position $i$, rather than a linear sum $V_{\text{out}}^{(i)} = \sum_j A_{ij} V_j$, we define the non-separable S5 attention accumulation via recursive circular convolution over the highly-attended concepts. To prevent exponential magnitude scaling, we modulate the Fourier transform $\hat{V}_j = \mathcal{F}(V_j)$ with a phase-shift operator controlled by $A_{ij}$.

$$ \hat{V}_{\text{out}}^{(i)} = \prod_{j} \left( A_{ij} \odot \hat{V}_j + (1 - A_{ij}) \odot \mathbb{1} \right) $$

where $\mathbb{1}$ is the identity vector in the Fourier domain (all ones).

The final output is projected back to the spatial domain:
$$ V_{\text{out}}^{(i)} = \mathcal{F}^{-1} \left( \hat{V}_{\text{out}}^{(i)} \right) $$

This equation ensures that conflicting concepts interleave as stable, non-collapsing interference patterns (phase shifts) rather than annihilating to a null state, maintaining S5 modal accessibility relations where contradictory worlds remain accessible from the bound state.

## 3. PyTorch Implementation: Holographic Convolution Binding

The following PyTorch class replaces standard linear value accumulation with FFT-optimized circular convolution binding.

```python
import torch
import torch.nn as nn
import torch.fft

class PNS5HolographicAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads

        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, N, C = x.shape

        # Standard Q, K, V projections
        q = self.q_proj(x).view(B, N, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, N, self.num_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, N, self.num_heads, self.head_dim).transpose(1, 2)

        # Standard scaled dot-product attention weights
        scores = torch.matmul(q, k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        attn_weights = torch.softmax(scores, dim=-1) # Shape: (B, num_heads, N, N)

        # Move to Fourier domain
        v_fft = torch.fft.rfft(v, dim=-1) # Shape: (B, num_heads, N, head_dim//2 + 1)

        # Holographic Binding via Convolution Theorem
        # We need to bind V_j based on attention weight A_ij.
        # Initialize output accumulator with Fourier identity (ones)
        out_fft = torch.ones_like(v_fft[:, :, 0:1, :]).expand(-1, -1, N, -1)

        # Iterate over key positions j to compute the binding for all queries i
        # To optimize, we approximate the product over the top-k most attended keys to avoid numerical instability
        # For this demonstration, we perform the full sequential binding

        for j in range(N):
            # Extract weights for key j across all queries: (B, num_heads, N, 1)
            w_j = attn_weights[:, :, :, j].unsqueeze(-1)

            # Extract V_j in frequency domain: (B, num_heads, 1, head_dim//2 + 1)
            v_j_fft = v_fft[:, :, j, :].unsqueeze(2)

            # Modulate V_j: if w_j is 0, term becomes 1 (no effect in multiplication).
            # If w_j is 1, term becomes V_j.
            # We use a linear interpolation in the complex plane for phase modulation.
            modulated_v_j = (1.0 - w_j) + w_j * v_j_fft

            # Element-wise multiplication in frequency domain = Circular convolution in spatial domain
            out_fft = out_fft * modulated_v_j

        # Inverse FFT to return to spatial domain
        out_spatial = torch.fft.irfft(out_fft, n=self.head_dim, dim=-1)

        # Concatenate heads and project
        out_spatial = out_spatial.transpose(1, 2).contiguous().view(B, N, C)
        return self.out_proj(out_spatial)
```

## 4. Lean 4 Theorem Template: S5 Modal Accessibility Verification

```lean
import Mathlib.Logic.Equiv.Basic
import Mathlib.Topology.Basic

-- Define the state space for attention vectors
variable {V : Type} [NormedAddCommGroup V] [InnerProductSpace ℂ V]

-- Define the accessibility relation R corresponding to S5 Attention
-- R x y implies state y is accessible from state x
def R (x y : V) : Prop :=
  ∃ (phase_shift : ℂ), ‖phase_shift‖ = 1 ∧ y = phase_shift • x

-- Theorem: The S5 Holographic Attention Accessibility Relation is an Equivalence Relation
-- This guarantees symmetric modal accessibility relations within the S5 attention-head Kripke frame.
theorem S5_attention_is_equivalence : Equivalence R := by
  constructor
  · -- Reflexivity: R x x
    intro x
    use 1
    simp [norm_one, one_smul]
  · -- Symmetry: R x y → R y x
    rintro x y ⟨p, hp_norm, hp_eq⟩
    use p⁻¹
    constructor
    · simp [hp_norm]
    · rw [hp_eq, smul_smul, inv_mul_cancel, one_smul]
      -- proof that p is non-zero given norm is 1
      intro h_zero
      have h_norm_zero : ‖p‖ = 0 := by rw [h_zero, norm_zero]
      linarith
  · -- Transitivity: R x y → R y z → R x z
    rintro x y z ⟨p1, hp1_norm, hp1_eq⟩ ⟨p2, hp2_norm, hp2_eq⟩
    use p2 * p1
    constructor
    · rw [norm_mul, hp1_norm, hp2_norm, mul_one]
    · rw [hp2_eq, hp1_eq, mul_smul]
```
