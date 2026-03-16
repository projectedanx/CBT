import { Injectable } from '@angular/core';
import { GoogleGenAI, Type } from '@google/genai';
import { GenericSpaceResult, BlendResult, BlendedConcept } from '../types';

@Injectable({
  providedIn: 'root'
})
export class GeminiService {
  private ai: GoogleGenAI;

  constructor() {
    this.ai = new GoogleGenAI({ apiKey: process.env['API_KEY'] || '' });
  }

  async analyzeGenericSpace(conceptA: string, conceptB: string): Promise<GenericSpaceResult> {
    const model = 'gemini-2.5-flash';
    const prompt = `
      Act as a Cognitive Scientist specializing in Conceptual Blending Theory (Fauconnier & Turner).
      Analyze the two input spaces: "${conceptA}" and "${conceptB}".
      Identify the "Generic Space" - the abstract structural commonalities and mappings between them.
      
      Also, calculate a "Similarity Score" (0-100) that represents the degree of structural alignment and overlap between the two concepts. 
      - 0 means completely disjoint/orthogonal.
      - 100 means they are isomorphic or nearly identical structurally.
      
      Return the result in JSON format.
    `;

    const schema = {
      type: Type.OBJECT,
      properties: {
        commonStructure: {
          type: Type.ARRAY,
          items: { type: Type.STRING },
          description: "List of abstract structures shared by both concepts (e.g., 'hierarchy', 'container', 'cycle')."
        },
        mappings: {
          type: Type.ARRAY,
          items: { type: Type.STRING },
          description: "List of direct counterparts (e.g., 'The CEO in A maps to the Queen in B')."
        },
        similarityScore: {
          type: Type.NUMBER,
          description: "A score (0-100) indicating the strength of structural alignment."
        }
      },
      required: ["commonStructure", "mappings", "similarityScore"]
    };

    try {
      const response = await this.ai.models.generateContent({
        model,
        contents: prompt,
        config: {
          responseMimeType: 'application/json',
          responseSchema: schema,
          temperature: 0.3 // Low temperature for analytical precision
        }
      });

      const text = response.text || '{}';
      return JSON.parse(text) as GenericSpaceResult;
    } catch (e) {
      console.error('Error analyzing generic space:', e);
      throw e;
    }
  }

  async runConceptualBlend(
    conceptA: string, 
    conceptB: string, 
    genericSpace: GenericSpaceResult, 
    focus: 'composition' | 'completion' | 'elaboration',
    temperature: number = 0.8,
    topK: number = 40
  ): Promise<BlendResult> {
    const model = 'gemini-2.5-flash';
    
    // Construct a prompt that enforces the specific CBT operation
    let focusInstruction = "";
    if (focus === 'composition') {
      focusInstruction = "Focus on COMPOSITION: Combine elements from both spaces directly to create immediate relations.";
    } else if (focus === 'completion') {
      focusInstruction = "Focus on COMPLETION: Bring in background knowledge or frames to fill out the pattern.";
    } else {
      focusInstruction = "Focus on ELABORATION: Run the simulation of the blend mentally to see what new properties emerge dynamically.";
    }

    const prompt = `
      Perform a Conceptual Blend of "${conceptA}" and "${conceptB}".
      
      Context (Generic Space):
      - Structure: ${genericSpace.commonStructure.join(', ')}
      - Mappings: ${genericSpace.mappings.join(', ')}
      
      Directive: ${focusInstruction}
      
      Goal: Generate 3 novel, sophisticated concepts that emerge from this blend. They should not be simple portmanteaus, but functional conceptual tools or scenarios. Include a detailed explanation of the mechanics for each.
      Output JSON.
    `;

    const schema = {
      type: Type.OBJECT,
      properties: {
        analysis: { type: Type.STRING, description: "Brief explanation of how the blend was achieved." },
        blends: {
          type: Type.ARRAY,
          items: {
            type: Type.OBJECT,
            properties: {
              name: { type: Type.STRING },
              description: { type: Type.STRING, description: "A short, high-level summary." },
              detailedExplanation: { type: Type.STRING, description: "A comprehensive explanation of how the concept functions in practice." },
              rationale: { type: Type.STRING, description: "Why this works according to CBT." },
              noveltyScore: { type: Type.NUMBER, description: "A score from 1-100 indicating how surprising this blend is." }
            },
            required: ["name", "description", "detailedExplanation", "rationale", "noveltyScore"]
          }
        }
      },
      required: ["analysis", "blends"]
    };

    try {
      const response = await this.ai.models.generateContent({
        model,
        contents: prompt,
        config: {
          responseMimeType: 'application/json',
          responseSchema: schema,
          temperature: temperature,
          topK: topK
        }
      });

      const text = response.text || '{}';
      return JSON.parse(text) as BlendResult;
    } catch (e) {
      console.error('Error running blend:', e);
      throw e;
    }
  }
}