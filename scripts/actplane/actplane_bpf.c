#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

/* Domain Node Definition */
struct policy_domain {
    __u32 parent_domain_id;
    __u64 inherited_rules;   /* Read-only rule bitmask from higher authority */
    __u64 inherited_labels;  /* Read-only inherited safety labels */
    __u64 local_rules;       /* Locally authored rules (agent deltas) */
    __u64 active_labels;     /* Dynamic IFC labels currently in this domain */
};

/* PID to Domain Mapping Map */
struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, __u32); /* Process TGID/PID */
    __type(value, __u32); /* Domain ID */
    __uint(max_entries, 10240);
} pid_domain_map SEC(".maps");

/* Domain Registry Map */
struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, __u32); /* Domain ID */
    __type(value, struct policy_domain);
    __uint(max_entries, 128);
} domain_registry SEC(".maps");

/* Synchronous Pre-Operation Enforcement Hook (BPF-LSM) */
SEC("lsm/file_permission")
int BPF_PROG(enforce_domain_boundary, struct file *file, int mask) {
    __u32 pid = bpf_get_current_pid_tgid() >> 32;
    __u32 *domain_id = bpf_map_lookup_elem(&pid_domain_map, &pid);

    if (!domain_id) {
        return 0; /* Unmonitored process space */
    }

    struct policy_domain *dom = bpf_map_lookup_elem(&domain_registry, domain_id);
    if (!dom) {
        return 0;
    }

    /* Bitwise comparison: Evaluate inherited and local rules */
    __u64 active_rules = dom->inherited_rules | dom->local_rules;

    /* If a write occurs on a restricted target, assert rules */
    if (mask & MAY_WRITE) {
        if (active_rules & 0x01) { /* Assuming Bit 0 represent write locks on system targets */
            bpf_printk("ActPlane Domain Intercept: Blocked write by PID %d\n", pid);
            return -EPERM; /* Return EPERM to trigger harness semantic feedback loop */
        }
    }

    return 0;
}
