import { Component, signal, computed, inject } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormControl, Validators } from '@angular/forms';
import { GeminiService } from './services/gemini.service';
import { ConceptGraphComponent } from './components/concept-graph.component';
import { AppState, GenericSpaceResult, BlendResult, BlendedConcept, GraphData, ConceptNode, ConceptLink, HistoryItem } from './types';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, ConceptGraphComponent, DatePipe],
  templateUrl: './app.component.html'
})
export class AppComponent {
  private gemini = inject(GeminiService);

  // State
  state = signal<AppState>('idle');
  conceptA = new FormControl('Mycelium Network', [Validators.required]);
  conceptB = new FormControl('Corporate Hierarchy', [Validators.required]);
  
  blendType = signal<'composition' | 'completion' | 'elaboration'>('composition');
  
  // Hyperparameters
  temperature = signal<number>(0.8);
  topK = signal<number>(40);
  showSettings = signal<boolean>(false);
  
  genericSpace = signal<GenericSpaceResult | null>(null);
  blendResult = signal<BlendResult | null>(null);
  errorMessage = signal<string | null>(null);
  notification = signal<string | null>(null);
  
  history = signal<HistoryItem[]>([]);
  currentHistoryItemId = signal<string | null>(null);

  constructor() {
    // Load history from local storage
    const saved = localStorage.getItem('cbt_history');
    if (saved) {
      try {
        this.history.set(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse history', e);
      }
    }
  }

  // Computed Graph Data for Visualization
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
      
      // Add a few representative nodes for the structure
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
        
        // Connect blend to inputs
        links.push({ source: 'a', target: id, value: 2 });
        links.push({ source: 'b', target: id, value: 2 });
        if (gs) {
           links.push({ source: 'g', target: id, value: 1 });
        }
      });
    }

    return { nodes, links };
  });

  toggleSettings() {
    this.showSettings.update(v => !v);
  }

  updateTemperature(event: Event) {
    const val = parseFloat((event.target as HTMLInputElement).value);
    this.temperature.set(val);
  }

  updateTopK(event: Event) {
    const val = parseInt((event.target as HTMLInputElement).value, 10);
    this.topK.set(val);
  }

  async startAnalysis() {
    if (this.conceptA.invalid || this.conceptB.invalid) return;
    
    this.state.set('analyzing');
    this.errorMessage.set(null);
    this.genericSpace.set(null);
    this.blendResult.set(null);
    this.currentHistoryItemId.set(null);

    try {
      // Step 1: Analyze Generic Space
      const resultA = await this.gemini.analyzeGenericSpace(this.conceptA.value!, this.conceptB.value!);
      this.genericSpace.set(resultA);
      
      // Automatically proceed to blending
      await this.performBlend();
      
    } catch (e) {
      this.state.set('error');
      this.errorMessage.set('Analysis failed. The alchemist could not stabilize the inputs.');
      console.error(e);
    }
  }

  async performBlend() {
    const gs = this.genericSpace();
    if (!gs) return;

    this.state.set('blending');
    const currentType = this.blendType(); // Capture type at start of request

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

  setBlendType(type: 'composition' | 'completion' | 'elaboration') {
    this.blendType.set(type);
    if (this.genericSpace()) {
      this.performBlend();
    }
  }

  reset() {
    this.state.set('idle');
    this.genericSpace.set(null);
    this.blendResult.set(null);
    this.currentHistoryItemId.set(null);
  }

  saveBlend(blend: BlendedConcept) {
    const gs = this.genericSpace();
    if (!gs) return;

    // Create a specialized result containing only this blend
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

    // Add to top of history and persist
    this.history.update(h => [newItem, ...h].slice(0, 30));
    this.persistHistory();

    // Trigger notification
    this.notification.set(`Artifact "${blend.name}" successfully archived.`);
    setTimeout(() => this.notification.set(null), 3000);
  }

  rateBlend(blend: BlendedConcept, rating: 'like' | 'dislike') {
    // 1. Determine new rating (toggle logic)
    const newRating = blend.userRating === rating ? undefined : rating;
    
    // 2. Update local blend object in the current result signal
    const currentResult = this.blendResult();
    if (currentResult) {
      const updatedBlends = currentResult.blends.map(b => 
        b.name === blend.name ? { ...b, userRating: newRating } : b
      );
      this.blendResult.set({ ...currentResult, blends: updatedBlends });
    }

    // 3. Update in history if we have a current history context
    const currentId = this.currentHistoryItemId();
    if (currentId) {
      this.history.update(items => items.map(item => {
        if (item.id === currentId) {
          // Clone and update the specific blend within the history item
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

  useAsInput(name: string, target: 'A' | 'B') {
    if (target === 'A') {
      this.conceptA.setValue(name);
    } else {
      this.conceptB.setValue(name);
    }
    
    // Visual feedback
    this.notification.set(`Injecting Artifact "${name}" into Input ${target === 'A' ? 'Alpha' : 'Beta'}.`);
    setTimeout(() => this.notification.set(null), 3000);
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

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
    this.history.update(h => [newItem, ...h].slice(0, 30)); // Limit to 30
    this.persistHistory();
  }

  loadHistory(item: HistoryItem) {
    this.state.set('complete'); 
    this.conceptA.setValue(item.conceptA);
    this.conceptB.setValue(item.conceptB);
    this.blendType.set(item.blendType);
    this.genericSpace.set(item.genericSpace);
    this.blendResult.set(item.blendResult);
    this.currentHistoryItemId.set(item.id);
  }

  clearHistory() {
    this.history.set([]);
    this.persistHistory();
    this.currentHistoryItemId.set(null);
  }

  private persistHistory() {
    localStorage.setItem('cbt_history', JSON.stringify(this.history()));
  }
}