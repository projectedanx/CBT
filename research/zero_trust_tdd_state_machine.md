# RESEARCH BLUEPRINT 1: Isomorphic Multi-Agent State Machine for Zero-Trust TDD Isolation
# AUTHOR: VULCAN / AXIOM v1.0
# STATUS: DRAFT-CONDITIONED

## 1. Operational Decoupling: State Graph Definition

The execution environment defines two non-overlapping agent containers: the Test Architect and the Implementer Agent. They share state strictly through an immutable event log. Direct memory sharing is prohibited.

```typescript
// State definition enforcing Agent boundary isolation
export interface TDDState {
  ticket_id: string;
  test_spec_path: string;
  target_src_path: string;
  current_phase: 'ARCHITECT' | 'IMPLEMENTER' | 'VERIFICATION';
  test_result_log: Array<{
    timestamp: number;
    exit_code: number;
    stderr: string;
  }>;
}

// Graph definition demonstrating state transitions
import { StateGraph, START, END } from '@langchain/langgraph';

const workflow = new StateGraph({
  channels: {
    ticket_id: { value: (x, y) => y ? y : x },
    test_spec_path: { value: (x, y) => y ? y : x },
    target_src_path: { value: (x, y) => y ? y : x },
    current_phase: { value: (x, y) => y ? y : x },
    test_result_log: { value: (x, y) => x.concat(y) }
  }
});

workflow.addNode('TestArchitect', executeTestArchitect);
workflow.addNode('ImplementerAgent', executeImplementerAgent);
workflow.addNode('SandboxRunner', executeSandboxRunner);
```

The `TestArchitect` writes to `./__tests__/`. The `ImplementerAgent` writes to `./src/`. The OS enforces these permissions.

## 2. Dynamic Environment Sandboxing

The `gemini-cli-sandbox` operates via Docker with zero-trust networking and restricted syscalls.

```yaml
# docker-compose.test.yml definition for isolated sandbox
version: '3.8'
services:
  gemini-cli-sandbox:
    image: alpine-node-sandbox:v22
    read_only: true
    network_mode: none
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    volumes:
      - type: bind
        source: ./src
        target: /app/src
        read_only: false
      - type: bind
        source: ./__tests__
        target: /app/__tests__
        read_only: true
    command: ["npm", "run", "test:isolated"]
```

Network socket connection attempts during execution return `ENETUNREACH`. The container terminates after a `max_duration` limit of 30 seconds.

## 3. Structured State Schemas

System stderr output is raw and non-deterministic. The harness normalizes this into a JSON schema before passing it back to the agent state machine.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SanitizedTestResult",
  "type": "object",
  "properties": {
    "exit_code": { "type": "integer" },
    "failing_tests": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "file": { "type": "string" },
          "assertion": { "type": "string" },
          "expected": { "type": "string" },
          "actual": { "type": "string" }
        },
        "required": ["file", "assertion", "expected", "actual"]
      }
    }
  },
  "required": ["exit_code", "failing_tests"]
}
```

This prevents prompt injection via hallucinated test output and normalizes parsing context.

## 4. Symbolic Scar Integration

If an agent attempts a Sandbox Escape or Sycophantic Mocking, the execution immediately halts.

```yaml
# SSR-20261012-001
trigger: "Agent B (Implementer) attempted to modify read-only test definitions."
failure_mode: "EACCES: permission denied, open '/app/__tests__/target.spec.ts'"
prevention_directive: "Implementer agent has ZERO write access to __tests__. Do not attempt. Edit src/ only."
severity: "CRITICAL"
```

The registry entry is injected into the Agent B system prompt for the remainder of the session.
