"""
System Assurance Agent (SAA) for the Temporal Blending Engine (TBE).
Calculates Causal Path Integrity (CPI) and strictly bounds cascading contradictions.
"""

from typing import List, Dict, Any, Set

class SystemAssuranceAgent:
    """
    Evaluates state-action traces against the Causal Path Integrity (CPI) constraint.
    """

    def __init__(self, threshold: float = 0.95):
        self.cpi_threshold = threshold

    def _frame_operator_holds(self, s_k: Dict[str, Any], s_k_plus_1: Dict[str, Any], a_k_eff: Dict[str, Any]) -> bool:
        """
        Validates that fluents NOT in the action's effects remain invariant.
        """
        all_keys = set(s_k.keys()).union(set(s_k_plus_1.keys()))
        effect_keys = set(a_k_eff.keys())

        for k in all_keys:
            if k not in effect_keys:
                if s_k.get(k) != s_k_plus_1.get(k):
                    return False
        return True

    def _preconditions_met(self, s_k: Dict[str, Any], a_k_pre: Dict[str, Any]) -> bool:
        """
        Validates that state s_k satisfies the preconditions of action a_k.
        """
        for k, v in a_k_pre.items():
            if s_k.get(k) != v:
                return False
        return True

    def _effects_applied(self, s_k_plus_1: Dict[str, Any], a_k_eff: Dict[str, Any]) -> bool:
        """
        Validates that state s_k+1 accurately reflects the effects of action a_k.
        """
        for k, v in a_k_eff.items():
            if s_k_plus_1.get(k) != v:
                return False
        return True

    def evaluate_trace(self, trace: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates a discrete trace of states and actions.
        Trace format expected: [s_1, a_1, s_2, a_2, ..., s_N]
        Where s_i is a state dict, and a_i is an action dict with 'pre' and 'eff'.
        """
        if not trace or len(trace) < 3 or len(trace) % 2 == 0:
            return {"cpi": 0.0, "status": "INVALID_TRACE_FORMAT", "passed": False}

        N = (len(trace) + 1) // 2
        valid_transitions = 0

        for k in range(N - 1):
            s_k = trace[2 * k]
            a_k = trace[2 * k + 1]
            s_k_plus_1 = trace[2 * k + 2]

            pre = a_k.get('pre', {})
            eff = a_k.get('eff', {})

            holds = (self._preconditions_met(s_k, pre) and
                     self._effects_applied(s_k_plus_1, eff) and
                     self._frame_operator_holds(s_k, s_k_plus_1, eff))

            if holds:
                valid_transitions += 1

        cpi = valid_transitions / (N - 1)
        passed = cpi >= self.cpi_threshold

        status = "RELEASE_STATE" if passed else "EPISTEMIC_ESCROW"

        return {
            "cpi": cpi,
            "status": status,
            "passed": passed,
            "details": f"Valid transitions: {valid_transitions} / {N - 1}"
        }
