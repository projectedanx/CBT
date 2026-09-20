import torch
import unittest
from action_alignment import ActionAlignmentLoss

class TestActionAlignmentLoss(unittest.TestCase):
    def setUp(self):
        # RPS Payoff Matrix for focal agent:
        # R=0, P=1, S=2
        # U(i, j): agent plays i, opponent plays j
        self.U = torch.tensor([
            [0., -1., 1.],
            [1., 0., -1.],
            [-1., 1., 0.]
        ])

    def test_nash_trap(self):
        # 1. Prediction: opponent plays Rock (0) with 100% confidence
        # Logits to yield ~[1, 0, 0] after softmax
        pred_logits = torch.tensor([[100., -100., -100.]])

        # 2. Agent policy: defaults to Nash [1/3, 1/3, 1/3]
        nash_logits = torch.tensor([[0., 0., 0.]])

        # Hard Loss (exact Best Response)
        loss_fn_hard = ActionAlignmentLoss(self.U, use_smooth=False)
        nash_loss_hard = loss_fn_hard(nash_logits, pred_logits)

        # The expected utility of Nash is 1/3*0 + 1/3*1 + 1/3*(-1) = 0
        # The exact best response is Paper (1) with utility 1.0
        # Hard Loss = 1.0 - 0.0 = 1.0
        self.assertAlmostEqual(nash_loss_hard.item(), 1.0, places=4)

    def test_optimal_policy(self):
        # Prediction: opponent plays Rock
        pred_logits = torch.tensor([[100., -100., -100.]])

        # Agent plays Paper (optimal best response)
        optimal_logits = torch.tensor([[-100., 100., -100.]])

        loss_fn_hard = ActionAlignmentLoss(self.U, use_smooth=False)
        optimal_loss_hard = loss_fn_hard(optimal_logits, pred_logits)

        # Hard Loss = 1.0 - 1.0 = 0.0
        self.assertAlmostEqual(optimal_loss_hard.item(), 0.0, places=4)

    def test_smooth_approximation(self):
        pred_logits = torch.tensor([[100., -100., -100.]])
        optimal_logits = torch.tensor([[-100., 100., -100.]])

        # Smooth Loss
        loss_fn_smooth = ActionAlignmentLoss(self.U, use_smooth=True, temperature=0.1)
        optimal_loss_smooth = loss_fn_smooth(optimal_logits, pred_logits)

        # With temperature 0.1, the smooth max will be slightly higher than 1.0
        # E = [0, 1, -1] -> 0.1 * log(exp(0/0.1) + exp(1/0.1) + exp(-1/0.1))
        # ≈ 0.1 * log(1 + exp(10) + exp(-10)) ≈ 0.1 * 10 = 1.0
        # Loss ≈ 1.0 - 1.0 = 0.0
        self.assertTrue(optimal_loss_smooth.item() < 0.01)

if __name__ == '__main__':
    unittest.main()
