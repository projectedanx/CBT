import { Injectable } from '@angular/core';
import { GeometricDirective, SceneTopology, MSIParameters } from '../types';

/**
 * PHASE 1: GEOMETRIC COGNITION
 * Service responsible for parsing the Unified Meta-Prompting API directives
 * and translating them into prompt constraints that manipulate "Phantom Dimensions".
 * Enforces strict VULCAN and VIPER protocols.
 */
@Injectable({
  providedIn: 'root'
})
export class UnifiedPromptingService {

  /**
   * Compiles the GeometricDirective into a strictly formatted Meta-Prompt constraint string.
   * Maps high-level topologies to granular parameter adjustments.
   *
   * @param {GeometricDirective} directive - The geometric parameters defining the latent space.
   * @param {MSIParameters} [msi] - Optional Multispectral Imaging parameters.
   * @returns {string} The compiled constraint block to be injected into the prompt.
   */
  compilePromptConstraints(directive: GeometricDirective, msi?: MSIParameters): string {
    let constraints = `\n[OPTICAL STATE MATRIX // GEOMETRIC DIRECTIVE]\n`;
    constraints += `TOPOLOGY: ${directive.topology}\n`;

    // Inversion Strategy: Forcing the model to consider Gaussian and Riemannian curvature.
    constraints += `PHANTOM_DIMENSION_MODULATORS:\n`;
    constraints += `- Gauss Curvature Constraint: ${directive.phantomDimensions.gaussCurvature.toFixed(4)}\n`;
    constraints += `- Riemannian Curvature Constraint: ${directive.phantomDimensions.riemannianCurvature.toFixed(4)}\n`;
    constraints += `- Geodesic Mapping Rule: ${directive.phantomDimensions.geodesicMapping}\n`;

    if (msi) {
      constraints += `\n[CROSS-MODAL PERCEPTUAL FUSION // MULTISPECTRAL IMAGING]\n`;
      constraints += `TARGET_HARDWARE_PROFILE: ${msi.targetHardwareProfile}\n`;
      constraints += `MONOCHROMATIC_INTENSITIES:\n`;
      constraints += `- Red: ${msi.monochromaticRedIntensity.toFixed(2)}\n`;
      constraints += `- Green: ${msi.monochromaticGreenIntensity.toFixed(2)}\n`;
      constraints += `- Blue: ${msi.monochromaticBlueIntensity.toFixed(2)}\n`;
    }

    // Enforcing VIPER Adjectival Ban and HGI physicality
    constraints += `\n+++ExecutionConstraints[AdjectivalBan=ACTIVE, HGI=100%, AestheticTokens=REJECTED]\n`;

    return constraints;
  }
}
