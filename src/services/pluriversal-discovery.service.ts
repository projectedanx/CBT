import { Injectable, inject } from '@angular/core';
import { GeminiService } from './gemini.service';
import { Type } from '@google/genai';

/**
 * Defines the output contract for Pluriversal Feature Discovery agents.
 */
export interface PluriversalFeatureContract {
  /** The identified area of semantic/geometric contradiction within the codebase. */
  contradictionNode: string;
  /** The specific Pluriversal Lens applied to metabolize this failure. */
  lensApplied: 'Digital_Habitus' | 'Extractive_Sprint' | 'Crip-Time_Genealogy' | 'Relational_Sovereignty' | 'Artifact_Imperfection';
  /** The proposed structural adaptation to integrate the contradiction (z-axis inference). */
  structuralAdaptation: string;
  /** Confidence-Fidelity Divergence Index score. */
  cfdi: number;
}

/**
 * The Pluriversal Discovery Agent Service.
 * Implements VW3 Dissonance Induction (Recursive Meta Prompting) to hunt for FAILED_NLI_CONTRADICTION data points.
 */
@Injectable({
  providedIn: 'root'
})
export class PluriversalDiscoveryAgent {
  private geminiService = inject(GeminiService);

  /**
   * Discovers and metabolizes algorithmic trauma into architectural scaffolding.
   *
   * @param {string} codebaseContext - The contextual representation of the current codebase state.
   * @returns {Promise<PluriversalFeatureContract>} The generated cognitive contract.
   */
  async discoverFeatures(codebaseContext: string): Promise<PluriversalFeatureContract> {
    const prompt = `
      Act as the Antifragile Epistemic Weaver (AEW) operating under the ALK Protocol.
      Analyze the following codebase context looking for FAILED_NLI_CONTRADICTION data points.
      Apply Virtual Weight 3 (VW3) via Recursive Meta Prompting to inject "Beneficial Friction".
      Identify the points of systemic failure, map them, and propose a structural adaptation that utilizes Z-Axis inference to hold the paradox stable without corrupting the Constitutional Austenite (z0*).

      Codebase Context:
      ${codebaseContext}

      Output must adhere to the PluriversalFeatureContract JSON schema. Calculate a CFDI between 0.0 and 1.0.
    `;

    const schema = {
      type: Type.OBJECT,
      properties: {
        contradictionNode: {
          type: Type.STRING,
          description: "The identified area of semantic/geometric contradiction."
        },
        lensApplied: {
          type: Type.STRING,
          enum: ['Digital_Habitus', 'Extractive_Sprint', 'Crip-Time_Genealogy', 'Relational_Sovereignty', 'Artifact_Imperfection'],
          description: "The Pluriversal Lens applied."
        },
        structuralAdaptation: {
          type: Type.STRING,
          description: "The proposed structural adaptation utilizing z-axis inference."
        },
        cfdi: {
          type: Type.NUMBER,
          description: "Confidence-Fidelity Divergence Index (CFDI) score between 0.0 and 1.0."
        }
      },
      required: ['contradictionNode', 'lensApplied', 'structuralAdaptation', 'cfdi']
    };

    try {
      // Direct call via generic method, assuming AI client is accessible or we wrap it in GeminiService
      // Since GeminiService doesn't expose a generic method, we need to adapt.
      // For now, we will add a generic generateContent method to GeminiService in the next step,
      // or we can use a similar approach to runConceptualBlend.
      // I will add a generic analysis method to GeminiService directly.
      const response = await this.geminiService.getClient().models.generateContent({
        model: 'gemini-2.5-flash',
        contents: prompt,
        config: {
          responseMimeType: 'application/json',
          responseSchema: schema,
          temperature: 0.6 // Task constraints temperature
        }
      });
      const text = response.text || '{}';
      return JSON.parse(text) as PluriversalFeatureContract;
    } catch (e) {
      console.error('Pluriversal Discovery Agent failed to synthesize:', e);
      throw e;
    }
  }
}
