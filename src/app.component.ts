import { Component, signal, computed, inject } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormControl, Validators } from '@angular/forms';
import { GeminiService } from './services/gemini.service';
import { ConceptGraphComponent } from './components/concept-graph.component';
import { AppState, GenericSpaceResult, BlendResult, BlendedConcept, GraphData, ConceptNode, ConceptLink, HistoryItem, EpistemicOverride } from './types';

/**
 * The sovereign controller of the Conceptual Blender architecture.
 * Manages the Petzold Loop of ingestion, structural mapping, and dialectic synthesis.
 */
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, ConceptGraphComponent, DatePipe],
  templateUrl: './app.component.html'
})
export class AppComponent {
  /** Reference to the cognitive engine handling external Gemini API synthesis. */
  private gemini = inject(GeminiService);

  /** Represents the current phase of the cognitive processing loop. */
  state = signal<AppState>('idle');
  /** Form control representing the first input conceptual domain (Space Alpha). */
  conceptA = new FormControl('Mycelium Network', [Validators.required]);
  /** Form control representing the second input conceptual domain (Space Beta). */
  conceptB = new FormControl('Corporate Hierarchy', [Validators.required]);
  
  /** The specific cognitive strategy applied to force the convergence of disparate domains. */
  blendType = signal<'composition' | 'completion' | 'elaboration'>('composition');
  
  /** The thermodynamic variance applied to the generator. Higher means more entropy/novelty. */
  temperature = signal<number>(0.8);
  /** The sampling restraint threshold governing token generation variance. */
  topK = signal<number>(40);
  /** Flag to toggle visibility of advanced cognitive constraints. */
  showSettings = signal<boolean>(false);
  
  /** Signal holding the extracted structural commonalities between domains. */
  genericSpace = signal<GenericSpaceResult | null>(null);
  /** Signal holding the resulting conceptual artifacts from the blending phase. */
  blendResult = signal<BlendResult | null>(null);
  /** Volatile signal capturing critical failures in the cognitive engine. */
  errorMessage = signal<string | null>(null);
  /** Volatile signal providing transient feedback on ledger or mutation actions. */
  notification = signal<string | null>(null);
  
  /** The local temporal archive storing previously generated operations. */
  history = signal<HistoryItem[]>([]);
  /** Pointer to the specific historical artifact currently loaded into the context window. */
  currentHistoryItemId = signal<string | null>(null);

  /** Tracks which blend is currently being annotated with a Golden Scar. */
  activeOverrideBlend = signal<string | null>(null);


  /**
   * Bootstraps the primary controller and attempts to rehydrate the temporal archive from local storage.
   */
  constructor() {
    const saved = localStorage.getItem('cbt_history');
    if (saved) {
      try {
        this.history.set(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse history', e);
      }
    }
  }

  /**
   * Computed topographical data structure consumed by the D3.js visualizer.
   * Maps current signals (Input A, Input B, Generic Space, and Blends) into a linked force graph.
   */
  graphData = computed<GraphData>(() => {
    const nodes: ConceptNode[] = [];
    const links: ConceptLink[] = [];
    
    const cA = this.conceptA.value;
    const cB = this.conceptB.value;
    const gs = this.genericSpace();
    const br = this.blendResult();

    if (!cA || !cB) return { nodes: [], links: [] };

    // 1. Input Spaces
    nodes.push({ id: 'a', label: cA, type: 'input-a', group: 1 });
    nodes.push({ id: 'b', label: cB, type: 'input-b', group: 2 });

    // 2. Generic Space (if available)
    if (gs) {
      nodes.push({ id: 'g', label: 'Generic Space', type: 'generic', group: 3 });
      
      gs.commonStructure.slice(0, 3).forEach((s, i) => {
        const id = `g-${i}`;
        nodes.push({ id, label: s, type: 'generic', group: 3 });
        links.push({ source: 'g', target: id, value: 1 });
      });

      links.push({ source: 'a', target: 'g', value: 0.5 });
      links.push({ source: 'b', target: 'g', value: 0.5 });
    }

    // 3. Blend Space (if available)
    if (br) {
      br.blends.forEach((b, i) => {
        const id = `blend-${i}`;
        nodes.push({ id, label: b.name, type: 'blend', group: 4 });
        
        links.push({ source: 'a', target: id, value: 2 });
        links.push({ source: 'b', target: id, value: 2 });
        if (gs) {
           links.push({ source: 'g', target: id, value: 1 });
        }
      });
    }

    return { nodes, links };
  });

  /**
   * Toggles the UI overlay for adjusting generator constraints (temperature/topK).
   */
  toggleSettings() {
    this.showSettings.update(v => !v);
  }

  /**
   * Intercepts DOM range input events to mutate the engine's temperature.
   * @param {Event} event - The raw DOM input event.
   */
  updateTemperature(event: Event) {
    const val = parseFloat((event.target as HTMLInputElement).value);
    this.temperature.set(val);
  }

  /**
   * Intercepts DOM range input events to mutate the engine's Top-K limit.
   * @param {Event} event - The raw DOM input event.
   */
  updateTopK(event: Event) {
    const val = parseInt((event.target as HTMLInputElement).value, 10);
    this.topK.set(val);
  }

  /**
   * Triggers the primary Petzold Loop. Begins Phase 1: Mapping the Generic Space.
   * On successful structural extraction, automatically delegates to Phase 2 (Synthesis).
   * @returns {Promise<void>}
   */
  async startAnalysis() {
    if (this.conceptA.invalid || this.conceptB.invalid) return;
    
    this.state.set('analyzing');
    this.errorMessage.set(null);
    this.genericSpace.set(null);
    this.blendResult.set(null);
    this.currentHistoryItemId.set(null);

    try {
      const resultA = await this.gemini.analyzeGenericSpace(this.conceptA.value!, this.conceptB.value!);
      this.genericSpace.set(resultA);
      
      await this.performBlend();
      
    } catch (e) {
      this.state.set('error');
      this.errorMessage.set('Analysis failed. The alchemist could not stabilize the inputs.');
      console.error(e);
    }
  }

  /**
   * Executes Phase 2 of the loop: Conceptual Blend Synthesis based on the established Generic Space mapping.
   * Archives the resultant operation to the temporal ledger on completion.
   * @returns {Promise<void>}
   */
  async performBlend() {
    const gs = this.genericSpace();
    if (!gs) return;

    this.state.set('blending');
    const currentType = this.blendType();

    try {
      const resultB = await this.gemini.runConceptualBlend(
        this.conceptA.value!,
        this.conceptB.value!,
        gs,
        currentType,
        this.temperature(),
        this.topK()
      );
      this.blendResult.set(resultB);
      this.state.set('complete');
      this.addToHistory(resultB, gs, currentType);
    } catch (e) {
      this.state.set('error');
      this.errorMessage.set('Blending synthesis failed.');
      console.error(e);
    }
  }

  /**
   * Mutates the cognitive blending strategy directive. Re-triggers synthesis if a valid mapping exists.
   * @param {'composition' | 'completion' | 'elaboration'} type - The newly selected cognitive focus.
   */
  setBlendType(type: 'composition' | 'completion' | 'elaboration') {
    this.blendType.set(type);
    if (this.genericSpace()) {
      this.performBlend();
    }
  }

  /**
   * Purges the volatile active context window, returning the controller to an idle baseline.
   */
  reset() {
    this.state.set('idle');
    this.genericSpace.set(null);
    this.blendResult.set(null);
    this.currentHistoryItemId.set(null);
  }

  /**
   * Promotes a specific generated artifact into a specialized, manually preserved historical record.
   * @param {BlendedConcept} blend - The specific artifact to archive permanently.
   */
  saveBlend(blend: BlendedConcept) {
    const gs = this.genericSpace();
    if (!gs) return;

    const specificResult: BlendResult = {
      analysis: `Archived Artifact: ${blend.name}`,
      blends: [blend]
    };

    const newItem: HistoryItem = {
      id: Math.random().toString(36).substring(2, 9),
      timestamp: Date.now(),
      conceptA: this.conceptA.value!,
      conceptB: this.conceptB.value!,
      genericSpace: gs,
      blendResult: specificResult,
      blendType: this.blendType(),
      isManualSave: true
    };

    this.history.update(h => [newItem, ...h].slice(0, 30));
    this.persistHistory();

    this.notification.set(`Artifact "${blend.name}" successfully archived.`);
    setTimeout(() => this.notification.set(null), 3000);
  }

  /**
   * Mutates the user-feedback tensor for a specific generated concept, updating both volatile memory and persistent history.
   * @param {BlendedConcept} blend - The generated artifact receiving feedback.
   * @param {'like' | 'dislike'} rating - The binary sentiment value.
   */

  /**
   * Injects a deterministic human contradiction (Epistemic Override) into a probabilistic artifact.
   * This physicalizes the Golden Scar Protocol, resolving Algorithmic Shame by holding tension.
   *
   * [PARACONSISTENT LOGIC ENFORCEMENT]
   * Ensures the resulting epistemic override operates within the ϵ-band of computational superposition.
   * Treats the architectural state simultaneously as Boundary, Interior, and Exterior.
   *
   * @param {BlendedConcept} blend - The artifact receiving the override.
   * @param {string} annotation - The deterministic human judgment.
   * @param {number} score - The Contradiction Retention Score (0-100), bounded to maintain ∣∇d∣=1.
   */
  injectEpistemicOverride(blend: BlendedConcept, annotation: string, score: number) {
    const override: EpistemicOverride = {
      annotation,
      contradictionRetentionScore: score,
      timestamp: Date.now()
    };

    const currentResult = this.blendResult();
    if (currentResult) {
      const updatedBlends = currentResult.blends.map(b =>
        b.name === blend.name ? { ...b, epistemicOverride: override } : b
      );
      this.blendResult.set({ ...currentResult, blends: updatedBlends });
    }

    const currentId = this.currentHistoryItemId();
    if (currentId) {
      this.history.update(items => items.map(item => {
        if (item.id === currentId) {
          const updatedBlends = item.blendResult.blends.map(b =>
            b.name === blend.name ? { ...b, epistemicOverride: override } : b
          );
          return {
            ...item,
            blendResult: {
              ...item.blendResult,
              blends: updatedBlends
            }
          };
        }
        return item;
      }));
      this.persistHistory();
    }

    this.activeOverrideBlend.set(null);
    this.notification.set(`Golden Scar Protocol injected into "${blend.name}". Tension stabilized.`);
    setTimeout(() => this.notification.set(null), 3000);
  }

  rateBlend(blend: BlendedConcept, rating: 'like' | 'dislike') {
    const newRating = blend.userRating === rating ? undefined : rating;
    
    const currentResult = this.blendResult();
    if (currentResult) {
      const updatedBlends = currentResult.blends.map(b => 
        b.name === blend.name ? { ...b, userRating: newRating } : b
      );
      this.blendResult.set({ ...currentResult, blends: updatedBlends });
    }

    const currentId = this.currentHistoryItemId();
    if (currentId) {
      this.history.update(items => items.map(item => {
        if (item.id === currentId) {
          const updatedBlends = item.blendResult.blends.map(b => 
            b.name === blend.name ? { ...b, userRating: newRating } : b
          );
          return {
            ...item,
            blendResult: {
              ...item.blendResult,
              blends: updatedBlends
            }
          };
        }
        return item;
      }));
      this.persistHistory();
    }
  }

  /**
   * Recycles an emergent artifact into the primary input nodes, facilitating recursive iteration (Phase 2 capability).
   * @param {string} name - The label of the generated artifact.
   * @param {'A' | 'B'} target - The destination vector to inject the artifact.
   */
  useAsInput(name: string, target: 'A' | 'B') {
    if (target === 'A') {
      this.conceptA.setValue(name);
    } else {
      this.conceptB.setValue(name);
    }
    
    this.notification.set(`Injecting Artifact "${name}" into Input ${target === 'A' ? 'Alpha' : 'Beta'}.`);
    setTimeout(() => this.notification.set(null), 3000);
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  /**
   * Appends the output of a completed cognitive loop to the persistent temporal ledger.
   *
   * @param {BlendResult} result - The output payload containing the generated artifacts.
   * @param {GenericSpaceResult} generic - The abstract topology linking the inputs.
   * @param {'composition' | 'completion' | 'elaboration'} type - The methodological constraint used.
   */
  private addToHistory(
    result: BlendResult, 
    generic: GenericSpaceResult, 
    type: 'composition' | 'completion' | 'elaboration'
  ) {
    const id = Math.random().toString(36).substring(2, 9);
    const newItem: HistoryItem = {
      id,
      timestamp: Date.now(),
      conceptA: this.conceptA.value!,
      conceptB: this.conceptB.value!,
      genericSpace: generic,
      blendResult: result,
      blendType: type
    };

    this.currentHistoryItemId.set(id);
    this.history.update(h => [newItem, ...h].slice(0, 30));
    this.persistHistory();
  }

  /**
   * Rehydrates a preserved historical record back into the active context window.
   * @param {HistoryItem} item - The temporal ledger entry to load.
   */
  loadHistory(item: HistoryItem) {
    this.state.set('complete'); 
    this.conceptA.setValue(item.conceptA);
    this.conceptB.setValue(item.conceptB);
    this.blendType.set(item.blendType);
    this.genericSpace.set(item.genericSpace);
    this.blendResult.set(item.blendResult);
    this.currentHistoryItemId.set(item.id);
  }

  /**
   * Irreversibly purges the temporal ledger from local storage and volatile memory.
   */
  clearHistory() {
    this.history.set([]);
    this.persistHistory();
    this.currentHistoryItemId.set(null);
  }

  /**
   * Flushes volatile ledger structures into static browser storage.
   */
  private persistHistory() {
    localStorage.setItem('cbt_history', JSON.stringify(this.history()));
  }
}
