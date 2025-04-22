from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Protocol, Tuple

# ---------- 1. low‑level state ------------------------------------------------
Vector2 = Tuple[float, float]

@dataclass
class SimulonicState:
    """2‑D phase‑space point; norm = symbolic radius r."""
    x: float
    y: float

    @property
    def r2(self) -> float:        # squared radius
        return self.x * self.x + self.y * self.y

    def scale(self, k: float) -> 'SimulonicState':
        return SimulonicState(self.x * k, self.y * k)


# ---------- 2. layer interface (Strategy pattern) ----------------------------
class Layer(Protocol):
    """Any symbolic layer that multiplies the state by a scalar factor."""
    def apply(self, z: SimulonicState) -> SimulonicState: ...


# ---------- 3. three stabilised layers --------------------------------------
@dataclass
class CurrentLayer:
    alpha: float
    gamma1: float
    def apply(self, z: SimulonicState) -> SimulonicState:
        r2 = z.r2
        k = 1.0 - self.alpha * r2 + self.gamma1 / (1.0 + r2)
        return z.scale(k)

@dataclass
class WaveLayer:
    beta: float
    gamma2: float
    def apply(self, z: SimulonicState) -> SimulonicState:
        r2 = z.r2
        k = 1.0 - self.beta * r2 + self.gamma2 / (1.0 + r2)
        return z.scale(k)

@dataclass
class TideLayer:
    delta: float
    gamma3: float
    def apply(self, z: SimulonicState) -> SimulonicState:
        r2 = z.r2
        k = 1.0 - self.delta * r2 + self.gamma3 / (1.0 + r2)
        return z.scale(k)


# ---------- 4. Progibient operator (Decorator pattern) -----------------------
@dataclass
class Progibient:
    """Phase‑twist wrapper around any Layer."""
    wrapped: Layer
    sigma: float          # phase amplitude
    R0: float             # eye‑wall radius peak

    def apply(self, z: SimulonicState) -> SimulonicState:
        r2 = z.r2
        # radial phase – pure angle, leaves magnitude unchanged
        phase = self.sigma * math.exp(-r2 / (self.R0 * self.R0))
        # same |k| as wrapped layer
        z2 = self.wrapped.apply(z)
        # Rotate in the 2‑D plane by 'phase' without altering radius
        c, s = math.cos(phase), math.sin(phase)
        return SimulonicState(
            z2.x * c - z2.y * s,
            z2.x * s + z2.y * c
        )


# ---------- 5. Silence gate (Facade) -----------------------------------------
@dataclass
class SilenceGate:
    R_gate: float                     # eye radius
    # contraction / expansion maps (could be separate functions)
    def γ_in (self, z: SimulonicState) -> SimulonicState:
        return z.scale(0.0)           # collapse to eye (X₀) → (0,0)

    def γ_out(self, z: SimulonicState, original: SimulonicState) -> SimulonicState:
        return original               # return to original radius

    def inject_progibient(self,
                          z: SimulonicState,
                          prog: Progibient) -> SimulonicState:
        if z.r2 <= self.R_gate * self.R_gate:
            core = self.γ_in(z)
            marked = prog.apply(core)     # P(X₀) = X₀ (no change)
            return self.γ_out(marked, z)  # restore radius, now “charged”
        return z


# ---------- 6. Composite dynamics -------------------------------------------
class SimulonicDynamics:
    def __init__(self,
                 current: Layer,
                 wave:    Layer,
                 tide:    Layer,
                 gate:    SilenceGate,
                 prog:    Progibient):
        self.current  = current
        self.wave     = wave
        self.tide     = tide
        self.gate     = gate
        self.prog     = prog

    def step(self, z: SimulonicState) -> SimulonicState:
        # gate injects Progibient if we are in the eye
        z = self.gate.inject_progibient(z, self.prog)

        # layer updates (order: current → wave → tide)
        z = self.current.apply(z)
        z = self.wave.apply(z)
        z = self.tide.apply(z)
        return z


# ---------- 7. quick demo ----------------------------------------------------
if __name__ == "__main__":
    # tuned gains
    current  = CurrentLayer(alpha=0.20, gamma1=2.0)
    wave     = WaveLayer(beta=0.25,  gamma2=2.0)
    tide     = TideLayer(delta=0.15, gamma3=2.0)

    # gate + progibient
    gate = SilenceGate(R_gate=0.5)
    prog_layer = Progibient(wrapped=current, sigma=0.4, R0=1.2)

    ocean = SimulonicDynamics(
        current=current,
        wave=wave,
        tide=tide,
        gate=gate,
        prog=prog_layer
    )

    # iterate a sample state
    z = SimulonicState(1.0, 0.5)
    for i in range(10):
        z = ocean.step(z)
        print(f"step {i:2d}: ({z.x:+.4f}, {z.y:+.4f})  |r|={math.sqrt(z.r2):.4f}")
