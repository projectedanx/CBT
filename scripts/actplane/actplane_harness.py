#!/usr/bin/env python3
"""
ActPlane Harness: Userspace Parent Orchestrator
Simulates the loading of the BPF maps and the ring buffer delta submission process for child sub-agents.
"""
import sys
import ctypes
import os

# Mock structures corresponding to the eBPF maps for the simulation
class PolicyDomain(ctypes.Structure):
    _fields_ = [
        ("parent_domain_id", ctypes.c_uint32),
        ("inherited_rules", ctypes.c_uint64),
        ("inherited_labels", ctypes.c_uint64),
        ("local_rules", ctypes.c_uint64),
        ("active_labels", ctypes.c_uint64)
    ]

# Simulated eBPF maps
pid_domain_map = {}
domain_registry = {}

def initialize_root_domain():
    """Initializes the root domain (Parent Orchestrator) with strict invariants."""
    print("[ActPlane] Initializing Root Domain 0...")
    root_domain = PolicyDomain(
        parent_domain_id=0,
        inherited_rules=0x01, # e.g., Bit 0 = block writes to system targets
        inherited_labels=0x00,
        local_rules=0x00,
        active_labels=0x00
    )
    domain_registry[0] = root_domain

def spawn_child_agent(pid: int, child_domain_id: int, parent_domain_id: int):
    """Spawns a child agent, assigning it to a new domain inheriting from the parent."""
    print(f"[ActPlane] Spawning Child Agent PID {pid} in Domain {child_domain_id} (Parent: {parent_domain_id})")

    if parent_domain_id not in domain_registry:
        raise ValueError("Parent domain not found.")

    parent = domain_registry[parent_domain_id]

    # Monotonic inheritance
    child_domain = PolicyDomain(
        parent_domain_id=parent_domain_id,
        inherited_rules=parent.inherited_rules | parent.local_rules,
        inherited_labels=parent.inherited_labels | parent.active_labels,
        local_rules=0x00,
        active_labels=0x00
    )

    domain_registry[child_domain_id] = child_domain
    pid_domain_map[pid] = child_domain_id

    print(f"[ActPlane] Child Domain {child_domain_id} inherited rules: {hex(child_domain.inherited_rules)}")

def submit_runtime_delta(pid: int, new_local_rule: int):
    """
    Child agent attempts to submit a runtime delta.
    The Authority Checker intercepts to ensure inherited gates aren't masked.
    """
    if pid not in pid_domain_map:
        print(f"[ActPlane] PID {pid} is unmonitored.")
        return

    domain_id = pid_domain_map[pid]
    domain = domain_registry[domain_id]

    print(f"[ActPlane] PID {pid} (Domain {domain_id}) submitting delta rule: {hex(new_local_rule)}")

    # Falsification Defense (The Kernel Authority Checker)
    # Ensure the delta does not attempt to clear or mask an inherited rule.
    # In a real bitmask, we might use specific bits for 'allow' vs 'deny'.
    # Here, we simulate a simple check: cannot submit a delta that conflicts with inherited invariants.
    # For simplicity, we just add local rules. If a child tries to clear a rule, it fails.

    # Simulate: If the child tries to set a bit that is already enforced by the parent, it's redundant but okay.
    # If the child tries to "unset" an inherited rule (which it can't mathematically do here due to | operator),
    # the architecture prevents it.

    domain.local_rules |= new_local_rule
    print(f"[ActPlane] Delta accepted. Domain {domain_id} local rules now: {hex(domain.local_rules)}")

def simulate_file_write(pid: int, filepath: str):
    """Simulates the BPF-LSM file_permission hook."""
    if pid not in pid_domain_map:
        return 0 # Unmonitored

    domain_id = pid_domain_map[pid]
    domain = domain_registry[domain_id]

    active_rules = domain.inherited_rules | domain.local_rules

    print(f"[BPF-LSM] Intercepting write to '{filepath}' by PID {pid}...")

    if filepath.startswith("/usr/bin/"):
        if active_rules & 0x01:
            print(f"[BPF-LSM] ActPlane Domain Intercept: Blocked write by PID {pid}")
            return -1 # -EPERM

    print(f"[BPF-LSM] Write to '{filepath}' allowed.")
    return 0

def run_simulation():
    print("=== ActPlane Sovereignty-Enforcement Split Simulation ===")
    initialize_root_domain()

    child_pid = 2048
    spawn_child_agent(child_pid, child_domain_id=1, parent_domain_id=0)

    # Child attempts to write to a system binary
    result = simulate_file_write(child_pid, "/usr/bin/python")

    if result == -1:
        print("[Harness] Catching -EPERM, mapping to userspace rule metadata.")
        print("[Harness] Semantic Feedback: Blocked: Cannot write to system binaries. Use /workspace/tmp.")

        # Agent plans recovery and redirects writes
        simulate_file_write(child_pid, "/workspace/tmp/python")

    print("=======================================================")

if __name__ == "__main__":
    run_simulation()
