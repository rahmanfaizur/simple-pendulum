"""
Simple Pendulum — numerical simulation and analytical comparison

Author: Faizur Rahman
Institute: BIT Sindri
Department: Chemical Engineering
Registration No.: 23030420034
Email: faizurr464@gmail.com
Instructor: Prof. Ch V Raghunath

Physics
-------
A point mass m hangs from a massless, unstretchable string of length L.
Angle θ is measured from the vertical (θ = 0 is equilibrium).

Forces: gravity mg and string tension S.
Only the azimuthal component drives motion:
    F_θ = -mg sin θ

Newton's second law with tangential acceleration a = L θ̈ gives:
    L θ̈ = -g sin θ
    θ̈ + (g/L) sin θ = 0

For small angles (sin θ ≈ θ) this becomes simple harmonic motion:
    θ(t) = θ₀ cos(ω t),  ω = √(g/L),  T = 2π √(L/g)

Numerically we split into first-order ODEs (ω = θ̇ here is angular velocity):
    dω = -(g/L) sin(θ) dt
    dθ = ω dt
and integrate with the forward Euler method.

Sample problem: m = 40 kg, L = 25 m → T ≈ 10 s for small amplitudes.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

plt.style.use("bmh")
FIGSIZE = (12, 5)
DPI = 150  # lower than paper's 600 for faster interactive use; raise for publication

# Physical constants / sample problem parameters
g = 9.81  # m/s^2
L = 25.0  # m
m = 40.0  # kg

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def analytical_approximation(t, theta0):
    """Small-angle solution: θ(t) = θ₀ cos(√(g/L) t)."""
    return theta0 * np.cos(t * (g / L) ** 0.5)


def RHS(theta, w, dt):
    """Right-hand side of the first-order system for one Euler step."""
    dw = -np.sin(theta) * dt * g / L
    dtheta = w * dt
    return dw, dtheta


def integrate_one_step(theta, w, dt):
    """Forward Euler: advance (θ, ω) by one time step dt."""
    dw, dtheta = RHS(theta, w, dt)
    w = w + dw
    theta = theta + dtheta
    return w, theta


def integrate_n_steps(theta0, w0, dt, n):
    """Integrate for n steps starting from θ(0)=θ₀, ω(0)=w0."""
    theta = [0.0] * (n + 1)
    w = [0.0] * (n + 1)
    theta[0] = theta0
    w[0] = w0
    for i in range(n):
        w[i + 1], theta[i + 1] = integrate_one_step(theta[i], w[i], dt)
    return w, theta


def compute_PE(theta):
    """Gravitational potential energy U = mgL(1 - cos θ)."""
    return m * g * L * (1 - np.cos(theta))


def compute_KE(w):
    """Kinetic energy K = (1/2) m L² ω²."""
    return 0.5 * m * L**2 * np.asarray(w) ** 2


def compute_error(w, theta):
    """Relative change in total mechanical energy from start to end."""
    E0 = compute_PE(theta[0]) + compute_KE(w[0])
    E1 = compute_PE(theta[-1]) + compute_KE(w[-1])
    return np.abs((E0 - E1) / E0)


def main():
    # Small-angle period check: T = 2π √(L/g) ≈ 10 s
    T_period = 2 * np.pi * np.sqrt(L / g)
    print(f"Small-amplitude period T = 2π√(L/g) = {T_period:.3f} s")

    # Two initial angles: 15° and 60°
    theta0_1 = np.pi / 12  # 15°
    theta0_2 = np.pi / 3   # 60°

    T = 20.0  # simulate for 20 seconds
    n = 10000
    t = np.linspace(0, T, n + 1)
    dt = T / float(n)

    w1, theta1 = integrate_n_steps(theta0_1, 0.0, dt, n)
    w2, theta2 = integrate_n_steps(theta0_2, 0.0, dt, n)

    # --- Angular position: numerical vs analytical ---
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    ax.set_title("Angular position")
    ax.plot(
        t,
        theta1,
        "m",
        label=r"$\theta_0 = %.0f^\circ$" % (theta0_1 * 180 / np.pi),
    )
    ax.plot(t, analytical_approximation(t, theta0_1), "m--", label="Approximation")
    ax.plot(
        t,
        theta2,
        "g",
        label=r"$\theta_0 = %.0f^\circ$" % (theta0_2 * 180 / np.pi),
    )
    ax.plot(t, analytical_approximation(t, theta0_2), "g--", label="Approximation")
    ax.set_xlabel(r"$t$, [s]")
    ax.set_ylabel(r"$\theta(t)$, [rad]")
    ax.legend()
    fig.tight_layout()
    path_angle = OUTPUT_DIR / "angular_position.png"
    fig.savefig(path_angle)
    print(f"Saved {path_angle}")
    plt.close(fig)

    # --- Mechanical energy for the large initial angle ---
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    ax.set_title(r"Mechanical energy, $\theta_0 = %.0f^\circ$" % (theta0_2 * 180 / np.pi))
    pe = compute_PE(theta2)
    ke = compute_KE(w2)
    ax.plot(t, pe, label="Potential energy")
    ax.plot(t, ke, label="Kinetic energy")
    ax.plot(t, pe + ke, label="Total energy")
    ax.set_xlabel(r"$t$, [s]")
    ax.set_ylabel(r"$E$, [J]")
    ax.legend(loc=1)
    fig.tight_layout()
    path_energy = OUTPUT_DIR / "mechanical_energy.png"
    fig.savefig(path_energy)
    print(f"Saved {path_energy}")
    plt.close(fig)

    # --- Energy conservation check ---
    print("Relative change in E:")
    print(
        "Theta = %.0f: %.2e"
        % (theta0_1 * 180 / np.pi, compute_error(w1, theta1))
    )
    print(
        "Theta = %.0f: %.2e"
        % (theta0_2 * 180 / np.pi, compute_error(w2, theta2))
    )


if __name__ == "__main__":
    main()
