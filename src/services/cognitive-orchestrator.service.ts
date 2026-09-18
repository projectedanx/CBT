import { Injectable, signal, WritableSignal, inject } from '@angular/core';
import { GeminiService } from './gemini.service';
import { HistoryService } from './history.service';
import { AppState, GenericSpaceResult, BlendResult, BlendedConcept } from '../types';

/**
 * Service responsible for orchestrating the Petzold Loop.
 * Decoupled from the UI component to satisfy the VULCAN Mereological Mandate.
 */
@Injectable({
  providedIn: 'root'
})
export class CognitiveOrchestratorService {
  private gemini = inject(GeminiService);
  private historyService = inject(HistoryService);

  /** Represents the current phase of the cognitive processing loop. */
  state: WritableSignal<AppState> = signal('idle');
  /** System error notifications and feedback. */
  errorMessage: WritableSignal<string | null> = signal(null);

  /** The extracted structural mapping between inputs. */
  genericSpace: WritableSignal<GenericSpaceResult | null> = signal(null);
  /** The generative synthesis output from the Gemini API. */
  blendResult: WritableSignal<BlendResult | null> = signal(null);

  /** The operative blending strategy. */
  blendType: WritableSignal<'composition' | 'completion' | 'elaboration'> = signal('composition');
  /** Variance parameter for generation. */
  temperature: WritableSignal<number> = signal(0.8);
  /** Distribution limit for generation. */
  topK: WritableSignal<number> = signal(40);

  /**
   * Triggers the primary Petzold Loop. Begins Phase 1: Mapping the Generic Space.
   */
  async startAnalysis(conceptA: string, conceptB: string) {
    this.state.set('analyzing');
    this.errorMessage.set(null);
    this.genericSpace.set(null);
    this.blendResult.set(null);
    this.historyService.currentHistoryItemId.set(null);

    try {
      const resultA = await this.gemini.analyzeGenericSpace(conceptA, conceptB);
      this.genericSpace.set(resultA);

      await this.performBlend(conceptA, conceptB);

    } catch (e) {
      this.state.set('error');
      this.errorMessage.set('Analysis failed. The alchemist could not stabilize the inputs.');
      console.error(e);
    }
  }

  /**
   * Executes Phase 2 of the loop: Conceptual Blend Synthesis.
   */
  async performBlend(conceptA: string, conceptB: string) {
    const gs = this.genericSpace();
    if (!gs) return;

    this.state.set('blending');
    const currentType = this.blendType();

    try {
      const resultB = await this.gemini.runConceptualBlend(
        conceptA,
        conceptB,
        gs,
        currentType,
        this.temperature(),
        this.topK()
      );
      this.blendResult.set(resultB);
      this.state.set('complete');
      this.historyService.addToHistory(conceptA, conceptB, resultB, gs, currentType);
    } catch (e) {
      this.state.set('error');
      this.errorMessage.set('Blending synthesis failed.');
      console.error(e);
    }
  }

  /**
   * Mutates the cognitive blending strategy directive. Re-triggers synthesis if a valid mapping exists.
   */
  setBlendType(type: 'composition' | 'completion' | 'elaboration', conceptA: string, conceptB: string) {
    this.blendType.set(type);
    if (this.genericSpace()) {
      this.performBlend(conceptA, conceptB);
    }
  }

  /**
   * Purges the volatile active context window.
   */
  reset() {
    this.state.set('idle');
    this.genericSpace.set(null);
    this.blendResult.set(null);
    this.historyService.currentHistoryItemId.set(null);
  }
}
