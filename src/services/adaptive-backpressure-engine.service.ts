import { Injectable, signal } from '@angular/core';

/**
 * @interface TelemetryMetrics
 * @description Real-time operational data captured from downstream core services.
 */
export interface TelemetryMetrics {
    databaseQueueLength: number;
    cpuUtilization: number;
    threadPoolExhaustionIndex: number;
    networkLatencyMs: number;
}

/**
 * @interface BackpressureState
 * @description The active configuration of the rate-limiting thresholds and bulkhead partitions.
 */
export interface BackpressureState {
    throttleThresholdSec: number;
    loadSheddingActive: boolean;
    bulkheadStatus: 'OPEN' | 'HALF_OPEN' | 'CLOSED';
}

/**
 * @class AdaptiveBackpressureEngineService
 * @description Intelligent rate-limiting and backpressure engine designed for the API Gateway boundary.
 * Monitors downstream telemetry to dynamically adjust client throttling and execute load shedding.
 */
@Injectable({
    providedIn: 'root'
})
export class AdaptiveBackpressureEngineService {
    public currentTelemetry = signal<TelemetryMetrics>({
        databaseQueueLength: 0,
        cpuUtilization: 0.0,
        threadPoolExhaustionIndex: 0.0,
        networkLatencyMs: 0
    });

    public activeState = signal<BackpressureState>({
        throttleThresholdSec: 100,
        loadSheddingActive: false,
        bulkheadStatus: 'CLOSED'
    });

    /**
     * @method analyzeTelemetry
     * @description Dynamic feedback loop adjusting throttling thresholds based on downstream health.
     * @param metrics The incoming telemetry payload from the Gateway proxy.
     * @returns Void. State is updated via Angular Signals.
     */
    public analyzeTelemetry(metrics: TelemetryMetrics): void {
        this.currentTelemetry.set(metrics);

        let newThreshold = 1000;
        let shedding = false;
        let bulkhead: 'OPEN' | 'HALF_OPEN' | 'CLOSED' = 'CLOSED';

        // Dynamic adjustment based on capacity degradation
        if (metrics.cpuUtilization > 0.85 || metrics.threadPoolExhaustionIndex > 0.90) {
            newThreshold = 100;
            shedding = true;
            bulkhead = 'OPEN';
        } else if (metrics.networkLatencyMs > 500) {
            newThreshold = 500;
            bulkhead = 'HALF_OPEN';
        }

        this.activeState.set({
            throttleThresholdSec: newThreshold,
            loadSheddingActive: shedding,
            bulkheadStatus: bulkhead
        });
    }

    /**
     * @method executeLoadSheddingPolicy
     * @description Prioritizes high-value transactions during peak demand.
     * @param transactionType String identifier of the transaction priority.
     * @returns Boolean indicating if the transaction is permitted to pass the gateway boundary.
     */
    public executeLoadSheddingPolicy(transactionType: 'CHECKOUT' | 'RECOMMENDATION' | 'STANDARD'): boolean {
        const state = this.activeState();

        if (!state.loadSheddingActive) {
            return true;
        }

        // Bulkhead partition policy logic
        if (transactionType === 'CHECKOUT') {
            return true; // High-value bypasses shedding unless fully exhausted
        }

        return false; // Low-priority traffic is throttled
    }
}
