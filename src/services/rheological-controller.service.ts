import { Injectable, signal, WritableSignal, computed, Signal } from '@angular/core';
import { RheologicalMode, RheologicalState, TelemetryMetrics } from '../types';

/**
 * The Rheological Mode Switcher (RMS) operates as a Layer-1 meta-architectural component.
 * It regulates the viscosity (thermodynamic flow of probability mass) within the latent space.
 */
@Injectable({
  providedIn: 'root'
})
export class RheologicalControllerService {
  /** The current active mode, representing the system's operational viscosity. */
  currentMode: WritableSignal<RheologicalMode> = signal('CLOUD');

  /** The physical constants mapped to the Crystal (High Viscosity) state. */
  private readonly CRYSTAL_STATE: RheologicalState = {
    mode: 'CRYSTAL',
    temperature: 0.0,
    topP: 0.10,
    adjectivalBound: 0,
    pydanticSchemaEnforcement: true,
    saltedTags: ['<data_x9f2>', '</data_x9f2>']
  };

  /** The physical constants mapped to the Cloud (Low Viscosity) state. */
  private readonly CLOUD_STATE: RheologicalState = {
    mode: 'CLOUD',
    temperature: 0.85,
    topP: 0.90,
    adjectivalBound: 3,
    pydanticSchemaEnforcement: false,
    structuralRedundancyRatio: 0.15
  };

  /** Reactive signal providing the physical configuration of the active rheological state. */
  currentState: Signal<RheologicalState> = computed(() => {
    return this.currentMode() === 'CRYSTAL' ? this.CRYSTAL_STATE : this.CLOUD_STATE;
  });

  /**
   * Monitors real-time execution telemetry to identify boundary transitions.
   * Based on the viscosity formula: dP/dT = L / (T * delta_V)
   *
   * @param metrics Current telemetry reading of semantic stability and entropy.
   */
  evaluateTelemetry(metrics: TelemetryMetrics): void {
    // Sharp rise in semantic entropy or topological tearing -> Performance Collapse Zone (Increase Viscosity)
    if (metrics.semanticSaponificationIndex > 0.04 || metrics.betti1PersistentLoops > 0) {
      if (this.currentMode() !== 'CRYSTAL') {
        console.warn('RMS: Semantic Entropy Spike Detected. Increasing Viscosity (Cooling to Crystal Mode).');
        this.currentMode.set('CRYSTAL');
      }
    }
    // This implies a need to decrease viscosity under 'Repetition Loop' conditions, handled theoretically
    // For now, if metrics are well within safe bounds, relax back to CLOUD mode
    else if (metrics.semanticSaponificationIndex < 0.01 && metrics.confidenceFidelityDivergenceIndex < 0.05) {
      if (this.currentMode() !== 'CLOUD') {
        console.log('RMS: Stable conditions. Decreasing Viscosity (Heating to Cloud Mode).');
        this.currentMode.set('CLOUD');
      }
    }
  }

  /**
   * Forces the system into a specific rheological state, bypassing telemetry for explicit programmatic compulsion.
   * @param mode The target mode to enforce.
   */
  forceMode(mode: RheologicalMode): void {
    this.currentMode.set(mode);
  }
}
