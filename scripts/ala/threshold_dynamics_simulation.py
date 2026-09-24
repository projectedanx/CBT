"""
Threshold Dynamics Simulation
Models the evolution of the ALA detection threshold theta(t) as a dynamic physical system.
"""
import matplotlib.pyplot as plt
import numpy as np

def simulate_threshold(alpha: float, beta: float, eta: float, initial_theta: float,
                       fp_loss_gradients: np.ndarray, tp_loss_gradients: np.ndarray,
                       time_steps: int) -> np.ndarray:
    """
    Simulates the threshold trajectory:
    d(theta)/dt = -alpha * Grad(L_FP) + beta * Grad(L_TP) - eta * theta(t)
    """
    theta = np.zeros(time_steps)
    theta[0] = initial_theta
    dt = 1.0 # time step size

    for t in range(1, time_steps):
        d_theta = (-alpha * fp_loss_gradients[t-1]
                   + beta * tp_loss_gradients[t-1]
                   - eta * theta[t-1]) * dt

        theta[t] = max(0.0, theta[t-1] + d_theta) # Threshold cannot be negative

    return theta

def main():
    time_steps = 100
    initial_theta = 0.5
    eta = 0.05 # Decay/Obsolescence rate

    # Simulate loss gradients over time
    # Suppose bursts of False Positives early on, and True Positives later
    fp_loss_gradients = np.random.uniform(0.1, 0.5, time_steps)
    fp_loss_gradients[10:30] += 0.8 # Burst of FPs

    tp_loss_gradients = np.random.uniform(0.0, 0.2, time_steps)
    tp_loss_gradients[60:80] += 0.6 # Burst of TPs (attacks)

    # 1. Under-Damped (High Alpha, Low Beta) -> Sycophantic Blindness
    theta_under = simulate_threshold(alpha=0.4, beta=0.05, eta=eta,
                                     initial_theta=initial_theta,
                                     fp_loss_gradients=fp_loss_gradients,
                                     tp_loss_gradients=tp_loss_gradients,
                                     time_steps=time_steps)

    # 2. Over-Damped (Low Alpha, High Beta) -> Semantic Ossification
    theta_over = simulate_threshold(alpha=0.05, beta=0.4, eta=eta,
                                    initial_theta=initial_theta,
                                    fp_loss_gradients=fp_loss_gradients,
                                    tp_loss_gradients=tp_loss_gradients,
                                    time_steps=time_steps)

    # 3. Critically Damped (Homeostatic Balance)
    # Balanced alpha and beta based on Free Energy Principle
    theta_critical = simulate_threshold(alpha=0.15, beta=0.20, eta=eta,
                                        initial_theta=initial_theta,
                                        fp_loss_gradients=fp_loss_gradients,
                                        tp_loss_gradients=tp_loss_gradients,
                                        time_steps=time_steps)

    plt.figure(figsize=(10, 6))
    plt.plot(theta_under, label='Under-Damped (High \u03b1) - Sycophantic Blindness', color='red', linestyle='--')
    plt.plot(theta_over, label='Over-Damped (High \u03b2) - Semantic Ossification', color='blue', linestyle='-.')
    plt.plot(theta_critical, label='Critically Damped - Homeostasis', color='green', linewidth=2)

    plt.axhline(y=0.8, color='black', linestyle=':', label='Breach Threshold ($\u03c4_{breach}$)')
    plt.axhline(y=0.4, color='gray', linestyle=':', label='Warning Threshold ($\u03c4_{warn}$)')

    plt.title('ALA Threshold Dynamics Simulation $\u03b8(t)$')
    plt.xlabel('Time Steps')
    plt.ylabel('Detection Threshold $\u03b8$')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('threshold_simulation.png')
    print("Simulation complete. Plot saved to threshold_simulation.png.")

if __name__ == "__main__":
    main()
