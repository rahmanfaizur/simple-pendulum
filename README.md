# Simple Pendulum

**Author:** Faizur Rahman  
**Institute:** BIT Sindri  
**Department:** Chemical Engineering  
**Registration No.:** 23030420034  
**Email:** faizurr464@gmail.com  
**Instructor:** Prof. Ch V Raghunath

Numerical study of the simple pendulum: physics, small-angle analytical solution, Euler integration, and energy conservation.

## Setup

```bash
cd simplePend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

**Script (saves plots to `output/`):**

```bash
source .venv/bin/activate
python simple_pendulum.py
```

**Notebook:**

```bash
source .venv/bin/activate
jupyter notebook simple_pendulum.ipynb
```

## What this models

A point mass \(m\) on a massless unstretchable string of length \(L\). Angle \(\theta\) from vertical. Equation of motion:

\[
\ddot{\theta} + \frac{g}{L}\sin\theta = 0
\]

Small angles: \(\theta(t) = \theta_0\cos(\sqrt{g/L}\, t)\), period \(T = 2\pi\sqrt{L/g}\).

Sample problem: \(m = 40\,\mathrm{kg}\), \(L = 25\,\mathrm{m}\) → \(T \approx 10\,\mathrm{s}\).
