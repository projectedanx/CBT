import { Injectable, signal, WritableSignal } from '@angular/core';
import { LogicViolationReport, SemanticIntegrityConstraint, SymbolicScar } from '../types';
import { v4 as uuidv4 } from 'uuid';

/**
 * Service implementing the Reflexive Repair Loop, bridging probabilistic generation with deterministic verification.
 * Enforces the VULCAN Epistemic Escrow mandate.
 */
@Injectable({
  providedIn: 'root'
})
export class ReflexiveRepairLoopService {
  /** Maximum number of reflexive repair attempts before triggering Epistemic Escrow */
  private readonly MAX_REPAIR_ATTEMPTS = 3;

  /** Current state of the escrow tripwire */
  public escrowTripped: WritableSignal<boolean> = signal(false);

  /** Temporary in-memory log of Symbolic Scars for the current session */
  public scarArchive: WritableSignal<SymbolicScar[]> = signal([]);

  /**
   * Evaluates a generated payload against a set of constraints.
   * System 2 Interdiction phase.
   *
   * @param payload The generated output from the LLM
   * @param constraints Array of Semantic Integrity Constraints to check
   * @returns A LogicViolationReport if a constraint is violated, or null if all pass.
   */
  public executeDeterministicVerification(payload: any, constraints: SemanticIntegrityConstraint[]): LogicViolationReport | null {
    for (const constraint of constraints) {
      if (!constraint.validationLogic(payload)) {
        return this.generateLogicViolationReport(payload, constraint);
      }
    }
    return null;
  }

  /**
   * Generates a structured Logic Violation Report from a failed constraint.
   */
  private generateLogicViolationReport(payload: any, constraint: SemanticIntegrityConstraint): LogicViolationReport {
    return {
      timestamp: new Date().toISOString(),
      violatedConstraintId: constraint.constraintId,
      erroneousPayload: payload,
      rejectionReason: constraint.description
    };
  }

  /**
   * Executes the reflexive repair loop, querying the generator and validating until success or escrow.
   *
   * @param generatorFn The async function that calls the LLM and returns the candidate payload
   * @param constraints The invariants that must be upheld
   * @param initialPromptVectorId Context ID for tracking
   * @param modulePath Originating module path
   * @returns The validated payload, or throws an error if Escrow is triggered
   */
  public async executeReflexiveRepair<T>(
    generatorFn: (previousLvr?: LogicViolationReport) => Promise<T>,
    constraints: SemanticIntegrityConstraint[],
    initialPromptVectorId: string,
    modulePath: string
  ): Promise<T> {
    let attempts = 0;
    let lvr: LogicViolationReport | null = null;
    let candidatePayload: T;

    while (attempts < this.MAX_REPAIR_ATTEMPTS) {
      attempts++;
      try {
        candidatePayload = await generatorFn(lvr || undefined);
        lvr = this.executeDeterministicVerification(candidatePayload, constraints);

        if (!lvr) {
            // Success! If there were previous failures, log a resolved Scar.
            if (attempts > 1) {
                 this.logSymbolicScar({
                     scar_id: `err_${Date.now()}_${uuidv4().substring(0,6)}`,
                     timestamp: new Date().toISOString(),
                     failure_mode: "LOGICAL_CONTRADICTION_RESOLVED",
                     module_path: modulePath,
                     trauma_context: {
                         initial_prompt_vector_id: initialPromptVectorId,
                         erroneous_output: "See previous attempts", // Simplified for brevity
                         constraint_violation: "MULTIPLE_CONSTRAINTS"
                     },
                     reparation_delta: {
                         successful_repair_output: JSON.stringify(candidatePayload),
                         attempts_to_resolution: attempts,
                         failure_utility_loss_tokens: 0 // Mock metric
                     }
                 });
            }
            return candidatePayload;
        }
        console.warn(`[REFLEXIVE LOOP] Attempt ${attempts} failed constraint: ${lvr.violatedConstraintId}. Re-injecting prompt.`);
      } catch (error) {
        // Generation itself failed catastrophically (e.g. network error)
        throw error;
      }
    }

    // Max attempts reached. Trigger Escrow.
    const finalLvr = lvr!;
    this.triggerEpistemicEscrow(finalLvr, initialPromptVectorId, modulePath, attempts);
    throw new Error(`[EPISTEMIC ESCROW TRIPPED] Maximum repair attempts (${this.MAX_REPAIR_ATTEMPTS}) exceeded for constraint: ${finalLvr.violatedConstraintId}`);
  }

  /**
   * Halts the autonomous agent execution and logs a permanent Symbolic Scar.
   */
  private triggerEpistemicEscrow(lvr: LogicViolationReport, promptVectorId: string, modulePath: string, attempts: number): void {
    this.escrowTripped.set(true);

    const scar: SymbolicScar = {
        scar_id: `err_${Date.now()}_${uuidv4().substring(0, 6)}`,
        timestamp: new Date().toISOString(),
        failure_mode: "UNRESOLVED_CONSTRAINT_VIOLATION",
        module_path: modulePath,
        trauma_context: {
            initial_prompt_vector_id: promptVectorId,
            erroneous_output: JSON.stringify(lvr.erroneousPayload),
            constraint_violation: lvr.violatedConstraintId
        },
        reparation_delta: {
            successful_repair_output: null,
            attempts_to_resolution: attempts,
            failure_utility_loss_tokens: 0
        }
    };

    this.logSymbolicScar(scar);
    console.error(`[EPISTEMIC ESCROW] Halting downstream execution. Scar logged: ${scar.scar_id}`);
  }

  private logSymbolicScar(scar: SymbolicScar): void {
      this.scarArchive.update(scars => [...scars, scar]);
  }
}
