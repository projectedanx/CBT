import { Injectable, signal } from '@angular/core';

/**
 * @interface AstNode
 * @description Simplified representation of an Abstract Syntax Tree node for static analysis.
 */
export interface AstNode {
    nodeType: 'Calculation' | 'Assignment' | 'Invocation' | 'SecurityRule';
    moduleOrigin: string;
    targetReference: string;
    lineRef: number;
}

/**
 * @interface ScannerResult
 * @description Output of the SRP Violation analysis.
 */
export interface ScannerResult {
    violationsDetected: number;
    bleedingModules: string[];
    refactoringRecommendations: string[];
}

/**
 * @class SrpViolationScannerService
 * @description Architectural scanning harness designed to detect business logic bleed within polyglot BFF repositories.
 * Enforces the Single Responsibility Principle by identifying misplaced domain calculations.
 */
@Injectable({
    providedIn: 'root'
})
export class SrpViolationScannerService {
    public scanResults = signal<ScannerResult | null>(null);

    /**
     * @method executeStaticAnalysis
     * @description Parses AST nodes to identify state-changing calculations and domain rule evaluations inside BFF codebases.
     * @param astTree Simulated array of parsed Abstract Syntax Tree nodes from the BFF repository.
     * @returns ScannerResult detailing the detected violations and mitigation plans.
     */
    public executeStaticAnalysis(astTree: AstNode[]): ScannerResult {
        let violations = 0;
        const bleeding: string[] = [];
        const recommendations: string[] = [];

        astTree.forEach(node => {
            if (node.nodeType === 'Calculation' || node.nodeType === 'SecurityRule') {
                violations++;
                if (!bleeding.includes(node.moduleOrigin)) {
                    bleeding.push(node.moduleOrigin);
                }

                const recommendation = `SRP Violation at ${node.moduleOrigin}:${node.lineRef}. Target reference '${node.targetReference}' implies domain logic bleed. Safely migrate this calculation back to the appropriate downstream microservice domain.`;
                recommendations.push(recommendation);
            }
        });

        const result: ScannerResult = {
            violationsDetected: violations,
            bleedingModules: bleeding,
            refactoringRecommendations: recommendations
        };

        this.scanResults.set(result);
        return result;
    }
}
