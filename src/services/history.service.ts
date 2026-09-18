import { Injectable, signal, WritableSignal } from '@angular/core';
import { HistoryItem, BlendedConcept, BlendResult, GenericSpaceResult } from '../types';

/**
 * Service responsible for managing the Temporal Ledger (History).
 * Handles persistent storage and volatile memory for conceptual blending operations.
 */
@Injectable({
  providedIn: 'root'
})
export class HistoryService {
  /** The reactive collection of historical records. */
  history: WritableSignal<HistoryItem[]> = signal([]);
  /** The currently active temporal ledger entry identifier. */
  currentHistoryItemId: WritableSignal<string | null> = signal(null);

  constructor() {
    this.loadHistory();
  }

  /**
   * Initializes the temporal ledger from local storage.
   */
  private loadHistory() {
    const saved = localStorage.getItem('cbt_history');
    if (saved) {
      try {
        this.history.set(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse history from local storage', e);
        this.history.set([]);
      }
    }
  }

  /**
   * Appends the output of a completed cognitive loop to the persistent temporal ledger.
   *
   * @param {string} conceptA - Input Concept A.
   * @param {string} conceptB - Input Concept B.
   * @param {BlendResult} result - The output payload.
   * @param {GenericSpaceResult} generic - The abstract topology.
   * @param {'composition' | 'completion' | 'elaboration'} type - The methodological constraint used.
   */
  addToHistory(
    conceptA: string,
    conceptB: string,
    result: BlendResult,
    generic: GenericSpaceResult,
    type: 'composition' | 'completion' | 'elaboration'
  ) {
    const id = Math.random().toString(36).substring(2, 9);
    const newItem: HistoryItem = {
      id,
      timestamp: Date.now(),
      conceptA,
      conceptB,
      genericSpace: generic,
      blendResult: result,
      blendType: type
    };

    this.currentHistoryItemId.set(id);
    this.history.update(h => [newItem, ...h].slice(0, 30));
    this.persistHistory();
  }

  /**
   * Promotes a specific generated artifact into a specialized, manually preserved historical record.
   * @param {BlendedConcept} blend - The specific artifact to archive permanently.
   * @param {string} conceptA - Input Concept A.
   * @param {string} conceptB - Input Concept B.
   * @param {GenericSpaceResult} gs - Generic space result.
   * @param {'composition' | 'completion' | 'elaboration'} blendType - The blend type.
   */
  saveBlend(blend: BlendedConcept, conceptA: string, conceptB: string, gs: GenericSpaceResult, blendType: 'composition' | 'completion' | 'elaboration') {
    const specificResult: BlendResult = {
      analysis: `Archived Artifact: ${blend.name}`,
      blends: [blend]
    };

    const newItem: HistoryItem = {
      id: Math.random().toString(36).substring(2, 9),
      timestamp: Date.now(),
      conceptA,
      conceptB,
      genericSpace: gs,
      blendResult: specificResult,
      blendType,
      isManualSave: true
    };

    this.history.update(h => [newItem, ...h].slice(0, 30));
    this.persistHistory();
  }

  /**
   * Updates an item in the history.
   * @param {string} id - History item ID.
   * @param {HistoryItem} updatedItem - The updated item.
   */
  updateHistoryItem(id: string, updatedItem: HistoryItem) {
     this.history.update(items => items.map(item => item.id === id ? updatedItem : item));
     this.persistHistory();
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
  public persistHistory() {
    localStorage.setItem('cbt_history', JSON.stringify(this.history()));
  }
}
