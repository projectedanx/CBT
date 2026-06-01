import { Injectable } from '@angular/core';

/**
 * Service responsible for the Symbiotic Tensor Mesh.
 * Translates human deterministic constraints (Golden Scar Protocol) into physical
 * topological forces (D3 gravity) to bound AI latent space exploration.
 */
@Injectable({
  providedIn: 'root'
})
export class SymbioticTensorMesh {

  /** The baseline gravitational constant for the force-directed graph. */
  private readonly BASE_G = 0.1;

  /** The Golden Ratio, used as the maximum scaling factor for severe contradictions. */
  private readonly PHI = 1.618;

  constructor() { }

  /**
   * Calculates the localized gravitational force multiplier based on the human's
   * Contradiction Retention Score (CRS).
   *
   * [∇] Uncertainty: The exact polynomial curve for CRS to Gravity scaling is
   * a heuristic. Currently using linear scaling mapped to the Golden Ratio (Φ) max constraint.
   *
   * @param {number} crs - The Contradiction Retention Score (0-100).
   * @returns {number} The calculated gravity value for D3 force simulation.
   */
  public calculateGravity(crs: number): number {
    // Sanitize input boundaries
    const boundedCrs = Math.max(0, Math.min(100, crs));

    // Scale from BASE_G up to (BASE_G * PHI) linearly based on CRS
    const scaleFactor = 1 + ((this.PHI - 1) * (boundedCrs / 100));

    return this.BASE_G * scaleFactor;
  }
}
