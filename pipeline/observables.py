"""S3-02 Observable Computation Framework (stubs for T2 tier).

Purpose: Define the interface for model-observable computation. These stubs
will be filled with real derivations from PREDICTION.md once G1 opens.

Pre-G1: Stubs return synthetic/dummy values for testing pipeline logic.
Post-G1: Implementations compute observables from m_φ, α_D, Λ_D parameters.

Each observable has:
1. Observable.compute() → float (test statistic from model)
2. Observable.label() → str (TEST, FIT, or SYNTHETIC)
3. Observable.assumptions() → list[str] (dependencies: A-SEQ, etc.)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

from pipeline.gate import is_pinned


# ============================================================================
# Observable Interface
# ============================================================================

class Observable(ABC):
    """Base class for model observables."""

    @abstractmethod
    def compute(self) -> float:
        """Compute the test statistic from the model.

        Pre-G1: Return stub value.
        Post-G1: Compute from PREDICTION.md parameters (m_φ, α_D, Λ_D).
        """
        pass

    @abstractmethod
    def name(self) -> str:
        """Observable name (e.g., 'lensing_core_radius')."""
        pass

    @abstractmethod
    def label(self) -> Literal["TEST", "FIT", "SYNTHETIC"]:
        """TEST: shape-fixed (kernel-blind).
        FIT: normalization-free fitting allowed.
        SYNTHETIC: pre-G1 or synthetic input."""
        pass

    @abstractmethod
    def assumptions(self) -> list[str]:
        """Assumption dependencies (e.g., ['A-SEQ', 'A-VOL', 'A-ONT'])."""
        pass

    def description(self) -> str:
        """Optional: human-readable description of this observable."""
        return f"{self.name()} observable"


# ============================================================================
# P1 Observable: Weak-Lensing Stacked Profiles (Lensing Shape)
# ============================================================================

@dataclass
class LensingObservableConfig:
    """Configuration for P1 lensing observable (placeholder for PREDICTION.md)."""

    # Post-G1 will read from PREDICTION.md:
    # m_phi: float  # Scalar mass from MVM matching
    # alpha_D: float  # Dark matter coupling strength
    # lambda_D: float  # Dark matter decay length scale
    # v_0: float  # Local velocity dispersion

    # Pre-G1 (synthetic testing):
    stub_core_radius_scaling: float = 1.0  # Core radius deviation from NFW


class LensingObservable(Observable):
    """P1: Weak-lensing halo core-radius scaling (shape-only observable).

    Shape profile: r_c vs M_halo
    Normalization: Amplitude (free parameter)
    Label: FIT (normalization-free fitting allowed)
    Assumptions: [A-SEQ, A-VOL, A-ONT] (moduli-dependent)
    """

    def __init__(self, config: LensingObservableConfig = None):
        self.config = config or LensingObservableConfig()

    def compute(self) -> float:
        """Compute core-radius scaling statistic.

        Pre-G1: Return stub value.
        Post-G1: Compute from m_φ, α_D, Λ_D via halo-model RG flow.
        """
        if is_pinned():
            # Post-G1: Real computation (TODO: fill from PREDICTION.md)
            # Step 1: Load m_φ, α_D, Λ_D from PREDICTION.md
            # Step 2: Compute moduli values (𝒱, g_s) from Free-Parameter Ledger
            # Step 3: Run halo-model RG flow to get r_c scaling
            # Step 4: Return test statistic
            pass  # Placeholder
        return self.config.stub_core_radius_scaling

    def name(self) -> str:
        return "lensing_core_radius"

    def label(self) -> Literal["TEST", "FIT", "SYNTHETIC"]:
        # Lensing allows normalization fitting (post-G1)
        return "SYNTHETIC" if not is_pinned() else "FIT"

    def assumptions(self) -> list[str]:
        return ["A-SEQ", "A-VOL", "A-ONT"]

    def description(self) -> str:
        return "P1: Weak-lensing halo core-radius scaling (shape + norm)"


# ============================================================================
# P2 Observable: Pulsar-Timing Residuals (PTA Spectrum)
# ============================================================================

@dataclass
class PTAObservableConfig:
    """Configuration for P2 PTA observable."""

    # Post-G1 will read from PREDICTION.md:
    # m_phi: float  # Scalar mass (determines PTA frequency f = m_phi / π)
    # rho_local: float  # Local ultralight DM density (~1e-24 g/cm³)

    # Pre-G1 (synthetic testing):
    stub_pta_lrt: float = 3.5  # Stub log-likelihood ratio for signal detection


class PTAObservable(Observable):
    """P2: Pulsar-timing residuals from ultralight modulus.

    Observable: nHz-band stochastic signal (frequency f = m_φ / π)
    Label: TEST (shape-only, kernel-blind)
    Assumptions: [A-SEQ, A-VOL] (mass + coupling)
    """

    def __init__(self, config: PTAObservableConfig = None):
        self.config = config or PTAObservableConfig()

    def compute(self) -> float:
        """Compute PTA log-likelihood ratio.

        Pre-G1: Return stub value.
        Post-G1: Compute from m_φ via Bayesian model selection.
        """
        if is_pinned():
            # Post-G1: Real computation (TODO: fill from PREDICTION.md)
            # Step 1: Load m_φ from PREDICTION.md
            # Step 2: Set frequency f = m_φ / π
            # Step 3: Load local DM density ρ_local
            # Step 4: Compute amplitude set by ρ_local
            # Step 5: Run Bayesian model selection (signal + GW background vs GW-only)
            # Step 6: Return 2 × Δ log L
            pass  # Placeholder
        return self.config.stub_pta_lrt

    def name(self) -> str:
        return "pta_lrt"

    def label(self) -> Literal["TEST", "FIT", "SYNTHETIC"]:
        # PTA is shape-only (TEST): no fitting allowed
        return "SYNTHETIC" if not is_pinned() else "TEST"

    def assumptions(self) -> list[str]:
        return ["A-SEQ", "A-VOL"]

    def description(self) -> str:
        return "P2: Pulsar-timing residuals (nHz scalar signal)"


# ============================================================================
# P3 Observable: Lyman-α Null Check
# ============================================================================

@dataclass
class LymanAlphaObservableConfig:
    """Configuration for P3 Lyman-α observable (null check)."""

    # Lyman-α should be null (no modification to small-scale power under ΛCDM)
    # Pre-G1 (synthetic testing):
    stub_lya_chi2: float = 10.0  # Should ≈ χ²(10) mean under null


class LymanAlphaObservable(Observable):
    """P3: Lyman-α small-scale power (null check).

    Observable: χ² goodness-of-fit over k-bins
    Purpose: Verify ultralight DM does NOT modify small-scale power
    Label: TEST (null check only)
    Assumptions: [A-SEQ] (existence of ultralight DM)
    """

    def __init__(self, config: LymanAlphaObservableConfig = None):
        self.config = config or LymanAlphaObservableConfig()

    def compute(self) -> float:
        """Compute Lyman-α χ² goodness-of-fit.

        Pre-G1: Return stub value (should accept null).
        Post-G1: Compare model power spectrum to Lyman-α constraints.
        """
        if is_pinned():
            # Post-G1: Real computation (TODO: fill from PREDICTION.md)
            # Step 1: Load model parameters (if any ultralight contribution)
            # Step 2: Compute power spectrum P(k) with ultralight DM
            # Step 3: Compare to Lyman-α public data (k-bins)
            # Step 4: Compute χ² goodness-of-fit
            # Step 5: Return χ² value (should accept null under ΛCDM)
            pass  # Placeholder
        return self.config.stub_lya_chi2

    def name(self) -> str:
        return "lyman_alpha_chi2"

    def label(self) -> Literal["TEST", "FIT", "SYNTHETIC"]:
        # Lyman-α is null check (TEST): no fitting allowed
        return "SYNTHETIC" if not is_pinned() else "TEST"

    def assumptions(self) -> list[str]:
        return ["A-SEQ"]

    def description(self) -> str:
        return "P3: Lyman-α small-scale power spectrum (null check)"


# ============================================================================
# Observable Registry & Orchestrator
# ============================================================================

class ObservableRegistry:
    """Manage all model observables."""

    def __init__(self):
        self.observables = {
            "lensing": LensingObservable(),
            "pta": PTAObservable(),
            "lyman_alpha": LymanAlphaObservable(),
        }

    def compute_all(self) -> dict[str, float]:
        """Compute all observables.

        Returns:
            Dict of observable_name -> test_statistic
        """
        return {
            name: obs.compute()
            for name, obs in self.observables.items()
        }

    def get_observable(self, name: str) -> Observable:
        """Get a specific observable by name."""
        if name not in self.observables:
            raise KeyError(f"Observable {name} not found. Available: {list(self.observables.keys())}")
        return self.observables[name]

    def list_observables(self) -> list[str]:
        """List all observable names."""
        return list(self.observables.keys())

    def observable_info(self, name: str) -> dict:
        """Get metadata for an observable."""
        obs = self.get_observable(name)
        return {
            "name": obs.name(),
            "description": obs.description(),
            "label": obs.label(),
            "assumptions": obs.assumptions(),
            "statistic": obs.compute(),
        }

    def all_info(self) -> dict[str, dict]:
        """Get metadata for all observables."""
        return {
            name: self.observable_info(name)
            for name in self.list_observables()
        }
