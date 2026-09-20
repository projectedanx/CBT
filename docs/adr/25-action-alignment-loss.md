# 25. Action-Alignment Loss (Regret Minimization)

Date: 2024-05-24

## Status

Accepted

## Context

To align an artificial agent's internal cognitive modeling with its external strategic execution, we must resolve the **thought-action gap**. Standard behavioral cloning and next-token prediction objectives often decouple descriptive representation (**Literal Theory of Mind**) from utility-maximizing action (**Functional Theory of Mind**).

When prompted to interact in sequential multi-agent games (such as Rock, Paper, Scissors), models equipped with perfect predictors of opponent behavior (Head A) still default to unexploitative, high-entropy **Nash equilibria** (Head B). They fail to translate their descriptive beliefs into optimal strategic policy.

By applying structured modeling to the cognitive boundary of transformer activations, we specify a mathematically rigorous **Action-Alignment Loss** to causally bind the predicted belief state to policy optimization.

## Decision

We have implemented an **Action-Alignment Loss** module (`scripts/sae/action_alignment.py`) in PyTorch. This module computes a bounded regret objective representing the distance between the expected utility of the selected policy and the expected utility of the optimal best response.

We introduced the **Boltzmann Best-Response Approximation** using LogSumExp to restore smooth gradient flow across all possible actions, ensuring dense gradient flow and preventing premature local minima trapping.

## Consequences

1.  **Bridged Thought-Action Gap:** The agent's policy (Head B) is mathematically penalized if it deviates from the optimal Best Response calculated based on its descriptive prediction of the opponent's strategy (Head A).
2.  **Mitigated Nash Trap:** In zero-sum competitive settings against predictable opponents, the agent is forced to play the optimal counter-strategy rather than collapsing into an unexploitative Nash equilibrium.
3.  **Smooth Gradient Landscape:** The Boltzmann approximation ensures dense gradient flow, prioritizing precise best-response enforcement at low temperatures and preventing instability during early phases of reinforcement learning at higher temperatures.
