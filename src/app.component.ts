import { Component, signal, computed, inject } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormControl, Validators } from '@angular/forms';
import { GeminiService } from './services/gemini.service';
import { SymbioticTensorMesh } from './services/tensor-mesh.service';
import { HistoryService } from './services/history.service';
import { CognitiveOrchestratorService } from './services/cognitive-orchestrator.service';

import { ConceptGraphComponent } from './components/concept-graph.component';
import { AppState, GenericSpaceResult, BlendResult, BlendedConcept, GraphData, ConceptNode, ConceptLink, HistoryItem, EpistemicOverride, PluriversalLens, StakeholderDissonance } from './types';

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
  public orchestrator = inject(CognitiveOrchestratorService);
  public historyService = inject(HistoryService);
  private tensorMesh = inject(SymbioticTensorMesh);

  /** Represents the current phase of the cognitive processing loop. */
  /** Form control representing the first input conceptual domain (Space Alpha). */
  conceptA = new FormControl('Mycelium Network', [Validators.required]);
  /** Form control representing the second input conceptual domain (Space Beta). */
  conceptB = new FormControl('Corporate Hierarchy', [Validators.required]);
  notification = signal<string | null>(null);
  
  /** The specific cognitive strategy applied to force the convergence of disparate domains. */
  
  /** The thermodynamic variance applied to the generator. Higher means more entropy/novelty. */
  /** The sampling restraint threshold governing token generation variance. */
  /** Flag to toggle visibility of advanced cognitive constraints. */
  showSettings = signal<boolean>(false);
  
  /** Signal holding the extracted structural commonalities between domains. */
  /** Signal holding the resulting conceptual artifacts from the blending phase. */
  /** Volatile signal capturing critical failures in the cognitive engine. */
  /** Volatile signal providing transient feedback on ledger or mutation actions. */
  
  /** The local temporal archive storing previously generated operations. */
  /** Pointer to the specific historical artifact currently loaded into the context window. */

  /** Tracks which blend is currently being annotated with a Golden Scar. */

  activeOverrideBlend = signal<string | null>(null);
  activeDissonanceBlend = signal<string | null>(null);
  pluriversalLenses: PluriversalLens[] = ['Digital_Habitus', 'Extractive_Sprint', 'Crip-Time_Genealogy', 'Relational_Sovereignty', 'Artifact_Imperfection'];



  /**
   * Bootstraps the primary controller and attempts to rehydrate the temporal archive from local storage.
   */
  constructor() {

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
    const gs = this.orchestrator.genericSpace();
    const br = this.orchestrator.blendResult();

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
        let nodeGravity: number | undefined;
        if (b.epistemicOverride && typeof b.epistemicOverride.contradictionRetentionScore === 'number' && !isNaN(b.epistemicOverride.contradictionRetentionScore)) {
          nodeGravity = this.tensorMesh.calculateGravity(b.epistemicOverride.contradictionRetentionScore);
        }
        nodes.push({ id, label: b.name, type: 'blend', group: 4, gravity: nodeGravity });
        
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
    this.orchestrator.temperature.set(val);
  }

  /**
   * Intercepts DOM range input events to mutate the engine's Top-K limit.
   * @param {Event} event - The raw DOM input event.
   */
  updateTopK(event: Event) {
    const val = parseInt((event.target as HTMLInputElement).value, 10);
    this.orchestrator.topK.set(val);
  }

  /**
   * Triggers the primary Petzold Loop. Begins Phase 1: Mapping the Generic Space.
   * On successful structural extraction, automatically delegates to Phase 2 (Synthesis).
   * @returns {Promise<void>}
   */

  async startAnalysis() {
    if (this.conceptA.invalid || this.conceptB.invalid) return;
    await this.orchestrator.startAnalysis(this.conceptA.value!, this.conceptB.value!);
  }


  async performBlend() {
    await this.orchestrator.performBlend(this.conceptA.value!, this.conceptB.value!);
  }


  setBlendType(type: 'composition' | 'completion' | 'elaboration') {
    this.orchestrator.setBlendType(type, this.conceptA.value!, this.conceptB.value!);
  }


  reset() {
    this.orchestrator.reset();
  }


  saveBlend(blend: BlendedConcept) {
    const gs = this.orchestrator.genericSpace();
    if (!gs) return;
    this.historyService.saveBlend(blend, this.conceptA.value!, this.conceptB.value!, gs, this.orchestrator.blendType());
    this.notification.set(`Artifact "${blend.name}" successfully archived.`);
    setTimeout(() => this.notification.set(null), 3000);
  }

  injectStakeholderDissonance(blend: BlendedConcept, lens: string, tensionScore: number) {
    const topoDerivative = this.tensorMesh.calculateTopologicalDerivative(tensionScore);
    const dissonance: StakeholderDissonance = {
      lens: lens as PluriversalLens,
      tensionScore: tensionScore,
      topologicalDerivative: topoDerivative
    };

    const currentResult = this.orchestrator.blendResult();
    if (currentResult) {
      const updatedBlends = currentResult.blends.map(b =>
        b.name === blend.name ? { ...b, stakeholderDissonance: dissonance } : b
      );
      this.orchestrator.blendResult.set({ ...currentResult, blends: updatedBlends });
    }
    this.activeDissonanceBlend.set(null);
  }

  injectEpistemicOverride(blend: BlendedConcept, annotation: string, score: number) {
    const override: EpistemicOverride = {
      annotation,
      contradictionRetentionScore: score,
      timestamp: Date.now()
    };

    const currentResult = this.orchestrator.blendResult();
    if (currentResult) {
      const updatedBlends = currentResult.blends.map(b =>
        b.name === blend.name ? { ...b, epistemicOverride: override } : b
      );
      this.orchestrator.blendResult.set({ ...currentResult, blends: updatedBlends });
    }

    const currentId = this.historyService.currentHistoryItemId();
    if (currentId) {
      this.historyService.history.update(items => items.map(item => {
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
      this.historyService.persistHistory();
    }

    this.activeOverrideBlend.set(null);
    this.notification.set(`Golden Scar Protocol injected into "${blend.name}". Tension stabilized.`);
    setTimeout(() => this.notification.set(null), 3000);
  }

  rateBlend(blend: BlendedConcept, rating: 'like' | 'dislike') {
    const newRating = blend.userRating === rating ? undefined : rating;
    
    const currentResult = this.orchestrator.blendResult();
    if (currentResult) {
      const updatedBlends = currentResult.blends.map(b => 
        b.name === blend.name ? { ...b, userRating: newRating } : b
      );
      this.orchestrator.blendResult.set({ ...currentResult, blends: updatedBlends });
    }

    const currentId = this.historyService.currentHistoryItemId();
    if (currentId) {
      this.historyService.history.update(items => items.map(item => {
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
      this.historyService.persistHistory();
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


  loadHistory(item: HistoryItem) {
    this.orchestrator.state.set('complete');
    this.conceptA.setValue(item.conceptA);
    this.conceptB.setValue(item.conceptB);
    this.orchestrator.blendType.set(item.blendType);
    this.orchestrator.genericSpace.set(item.genericSpace);
    this.orchestrator.blendResult.set(item.blendResult);
    this.historyService.currentHistoryItemId.set(item.id);
  }


  clearHistory() {
    this.historyService.clearHistory();
  }

}
