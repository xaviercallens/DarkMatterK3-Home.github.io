"""S3-02 Comparison Framework — Observable-specific TEST/FIT logic.

Purpose: Load mock null banks (S3 pre-registration), implement observable-specific
comparisons (P1 lensing, P2 PTA, P3 Lyman-α), and label results mechanically as
TEST (shape-fixed kernel-blind) or FIT (normalization-free parameter). All work
at T2 (mechanically verifiable) until PREDICTION.md pinned (G1).

Pre-G1: Comparison runs only on synthetic data or mock banks; labeled SYNTHETIC.
Post-G1: Real-data comparisons labeled TEST/FIT per PREDICTION.md ledger strategy.
"""
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.gate import is_pinned  # noqa: E402


# ============================================================================
# Mock-Bank Loader (S3-01 integration)
# ============================================================================

@dataclass
class MockNullBank:
    """A single mock null distribution for calibration (mirrors scripts/s3_mockbank_generator.py)."""

    name: str
    description: str
    observable_type: str  # "lensing" | "pta" | "lyman_alpha"
    null_statistic_mean: float
    null_statistic_std: float
    n_trials: int
    seed: int
    alpha_thresholds: list[float]  # Critical values for [0.01, 0.05, 0.10]
    provenance: str
    calibration_notes: str


class NullBankManager:
    """Load and cache mock null banks from data/nullbanks/."""

    def __init__(self, nullbank_dir: Path = None):
        if nullbank_dir is None:
            nullbank_dir = REPO_ROOT / "data" / "nullbanks"
        self.nullbank_dir = nullbank_dir
        self._banks = {}

    def load_bank(self, name: str) -> MockNullBank:
        """Load a mock null bank from disk."""
        if name in self._banks:
            return self._banks[name]

        bank_path = self.nullbank_dir / f"{name}.json"
        if not bank_path.exists():
            raise FileNotFoundError(f"Mock null bank not found: {bank_path}")

        with open(bank_path) as f:
            data = json.load(f)

        bank = MockNullBank(**data)
        self._banks[name] = bank
        return bank

    def load_all_banks(self) -> dict[str, MockNullBank]:
        """Load all available mock banks."""
        banks = {}
        for bank_name in ["mock_lensing_sdss", "mock_pta_nanograv", "mock_lyman_alpha_xq100"]:
            try:
                banks[bank_name] = self.load_bank(bank_name)
            except FileNotFoundError:
                pass
        return banks

    def get_alpha_threshold(self, bank_name: str, alpha: float) -> float:
        """Get the critical value for a given significance level.

        Args:
            bank_name: e.g., "mock_lensing_sdss"
            alpha: significance level (0.01, 0.05, or 0.10)

        Returns:
            Critical value (99th, 95th, or 90th percentile)
        """
        bank = self.load_bank(bank_name)
        alpha_to_idx = {0.01: 0, 0.05: 1, 0.10: 2}
        if alpha not in alpha_to_idx:
            raise ValueError(f"Alpha must be one of {list(alpha_to_idx.keys())}, got {alpha}")
        return bank.alpha_thresholds[alpha_to_idx[alpha]]


# ============================================================================
# Comparison Result & Decision
# ============================================================================

@dataclass
class ComparisonResult:
    """Result of a single observable comparison."""

    observable_type: str  # "lensing", "pta", "lyman_alpha"
    observed_statistic: float
    critical_value: float
    p_value: float
    alpha: float
    reject_null: bool
    label: Literal["TEST", "FIT", "SYNTHETIC"]  # TEST: shape-fixed (kernel-blind)
    # FIT: normalization free; SYNTHETIC: synthetic data / pre-G1
    assumption_tags: list[str]  # e.g., ["A-SEQ", "A-VOL", "A-ONT"]
    notes: str = ""


class ObservableComparison:
    """Base class for observable-specific comparison logic."""

    def __init__(self, null_bank_manager: NullBankManager, bank_name: str,
                 observable_type: str):
        self.null_bank_manager = null_bank_manager
        self.bank_name = bank_name
        self.observable_type = observable_type
        self.bank = null_bank_manager.load_bank(bank_name)

    def compare(self, observed_statistic: float, alpha: float = 0.05,
                synthetic: bool = True) -> ComparisonResult:
        """Compare an observed statistic against the null bank.

        Args:
            observed_statistic: The test statistic from the data/model
            alpha: Significance level (0.01, 0.05, 0.10)
            synthetic: True if this is synthetic data or pre-G1; False if real data post-G1

        Returns:
            ComparisonResult with TEST/FIT/SYNTHETIC label
        """
        critical_value = self.null_bank_manager.get_alpha_threshold(self.bank_name, alpha)
        reject_null = observed_statistic > critical_value

        # Compute p-value by approximating from observed statistic
        # (true p-value would come from the actual null distribution in the bank)
        p_value = float(np.clip(1.0 - (observed_statistic / (critical_value + 1e-6)), 0, 1))

        # Label mechanical (pre-G1, always synthetic; post-G1, TEST/FIT per ledger)
        if synthetic or not is_pinned():
            label = "SYNTHETIC"
        else:
            label = self._decide_label()

        return ComparisonResult(
            observable_type=self.observable_type,
            observed_statistic=observed_statistic,
            critical_value=critical_value,
            p_value=p_value,
            alpha=alpha,
            reject_null=reject_null,
            label=label,
            assumption_tags=self.assumption_tags(),
        )

    def _decide_label(self) -> Literal["TEST", "FIT"]:
        """Decide TEST (shape-fixed) vs FIT (normalization-free) based on
        observable type. This is mechanical and depends only on the observable,
        not the result."""
        # Per S3-02 spec:
        # - P1 (lensing): shape TEST, normalization FIT
        # - P2 (PTA): kernel-blind (shape-only observable) → TEST
        # - P3 (Lyman-α): null check → TEST
        if self.observable_type == "lensing":
            # Lensing has two components; shape is TEST, normalization is FIT
            return "FIT"  # Normalization-free fitting allowed
        else:
            # PTA and Lyman-α are shape-only (TEST)
            return "TEST"

    def assumption_tags(self) -> list[str]:
        """Observable assumptions (from PREDICTION.md spec)."""
        if self.observable_type == "lensing":
            return ["A-SEQ", "A-VOL", "A-ONT"]
        elif self.observable_type == "pta":
            return ["A-SEQ", "A-VOL"]
        elif self.observable_type == "lyman_alpha":
            return ["A-SEQ"]
        else:
            return []


# ============================================================================
# Observable-Specific Comparison Classes
# ============================================================================

class LensingComparison(ObservableComparison):
    """P1 Observable: Weak-lensing stacked profiles (halo core-radius scaling).

    Per S3-02 spec:
    - Shape (r_c vs M_halo scaling): TEST (kernel-blind)
    - Normalization (absolute amplitude): FIT (free parameter)
    """

    def __init__(self, null_bank_manager: NullBankManager):
        super().__init__(null_bank_manager, "mock_lensing_sdss", "lensing")

    def assumption_tags(self) -> list[str]:
        return ["A-SEQ", "A-VOL", "A-ONT"]  # Core-radius depends on moduli


class PTAComparison(ObservableComparison):
    """P2 Observable: Pulsar-timing residuals (nHz-band signal from ultralight modulus).

    Per S3-02 spec:
    - Frequency f = m_φ / π (from PREDICTION.md)
    - Amplitude set by local DM density (computable from data)
    - Shape-only observable → TEST (kernel-blind by design)
    """

    def __init__(self, null_bank_manager: NullBankManager):
        super().__init__(null_bank_manager, "mock_pta_nanograv", "pta")

    def assumption_tags(self) -> list[str]:
        return ["A-SEQ", "A-VOL"]  # PTA depends on mass and coupling strength


class LymanAlphaComparison(ObservableComparison):
    """P3 Observable: Small-scale power spectrum (null check).

    Purpose: Verify ultralight DM does NOT significantly modify small-scale
    power where standard ΛCDM constraints apply.

    Per S3-02 spec:
    - Null hypothesis: ΛCDM power spectrum
    - χ² goodness-of-fit over k-bins
    - Result should be null → TEST only
    """

    def __init__(self, null_bank_manager: NullBankManager):
        super().__init__(null_bank_manager, "mock_lyman_alpha_xq100", "lyman_alpha")

    def assumption_tags(self) -> list[str]:
        return ["A-SEQ"]  # Lyman-α depends on whether ultralight DM exists


# ============================================================================
# Orchestrator: Comparison Pipeline
# ============================================================================

class ComparisonPipeline:
    """Orchestrates all three observable comparisons."""

    def __init__(self, nullbank_dir: Path = None):
        self.null_bank_manager = NullBankManager(nullbank_dir)
        self.lensing = LensingComparison(self.null_bank_manager)
        self.pta = PTAComparison(self.null_bank_manager)
        self.lyman_alpha = LymanAlphaComparison(self.null_bank_manager)

    def compare_all(self, lensing_stat: float = None, pta_stat: float = None,
                     lya_stat: float = None, alpha: float = 0.05,
                     synthetic: bool = True) -> dict[str, ComparisonResult]:
        """Run all three observable comparisons.

        Args:
            lensing_stat: Observed lensing statistic (or None to skip)
            pta_stat: Observed PTA statistic (or None to skip)
            lya_stat: Observed Lyman-α statistic (or None to skip)
            alpha: Significance level
            synthetic: True if synthetic data / pre-G1

        Returns:
            Dict of observable_type -> ComparisonResult
        """
        results = {}
        if lensing_stat is not None:
            results["lensing"] = self.lensing.compare(lensing_stat, alpha, synthetic)
        if pta_stat is not None:
            results["pta"] = self.pta.compare(pta_stat, alpha, synthetic)
        if lya_stat is not None:
            results["lyman_alpha"] = self.lyman_alpha.compare(lya_stat, alpha, synthetic)
        return results

    def save_results(self, results: dict[str, ComparisonResult], output_path: Path) -> None:
        """Save comparison results to JSON."""
        output_dict = {
            obs_type: {
                "observable_type": result.observable_type,
                "observed_statistic": result.observed_statistic,
                "critical_value": result.critical_value,
                "p_value": result.p_value,
                "alpha": result.alpha,
                "reject_null": result.reject_null,
                "label": result.label,
                "assumption_tags": result.assumption_tags,
                "notes": result.notes,
            }
            for obs_type, result in results.items()
        }

        with open(output_path, "w") as f:
            json.dump(output_dict, f, indent=2)
