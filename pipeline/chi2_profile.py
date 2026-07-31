"""
χ² profile-likelihood profiler for Lyα P1D analysis (WP-E6-P2B).

ENGINEERING / DESIGN (per CLAUDE.md rule 3 — no TEST, no FIT labels).

This module implements profile-likelihood minimization of χ² over nuisance parameters
(zrei, ha, hs, taueff) for a 9-bin DESI Lyα forest power-spectrum mock grid at z=4.2.

Degrees of freedom:
  - Absolute goodness-of-fit per (m,f) cell: 9 bins − 4 profiled nuisances = 5 dof.
  - Exclusion contours from Δχ² over the (m,f) grid: 2 dof (Wilks' theorem).
    Both interpretations are correct for different questions; see brief for detail.

Profile-likelihood method: iminuit.Minuit with L-BFGS-B bounds.
Covariance inversion: scipy.linalg.cho_factor/cho_solve for numerical stability
  and automatic non-PD detection.

References:
  - ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md §2 (nuisance profiling design).
  - integration_iminuit.py (in-repo pattern, bounds/initialization).
  - Hartlap et al. 2007, A&A 464, 399 (covariance correction; may already be
    applied upstream — see docstrings).
"""

import numpy as np
from scipy import linalg
from iminuit import Minuit
from typing import NamedTuple, Optional, Tuple


# Nuisance parameter bounds (traced to ANALYSIS_PROTOCOL §2.2, integration_iminuit.py)
NUISANCE_BOUNDS = {
    "zrei": (6.05, 14.91),      # Trained LHS support from param.pkl
    "ha": (0.066, 3.989),       # Trained LHS support from param.pkl
    "hs": (-0.987, 0.996),      # Trained LHS support from param.pkl
    "taueff": (0.3, 1.8),       # PRIOR BOX (not trained support) — flagged in §2.2
}

# Initialization: training-LHS medians from wp_e6_grid_controls_report_2026_07_28.json
NUISANCE_INIT = {
    "zrei": 10.5,
    "ha": 2.0,
    "hs": 0.0,
    "taueff": 1.0,
}


class ProfileLikelihoodResult(NamedTuple):
    """Result of a single profile-likelihood minimization.

    Attributes:
        chi2_min: Minimized χ² (absolute goodness-of-fit, 5 dof per cell).
        nuisance_params: Best-fit dict {zrei, ha, hs, taueff}.
        nuisance_errors: Estimated 1σ errors from Minuit {zrei, ha, hs, taueff}.
        at_boundary: Boolean, True if any nuisance parameter is at a bound.
        n_calls: Number of χ² function evaluations by minimizer.
        valid_minimum: Boolean, True if Minuit reports valid = True.
        messages: List of warning strings if optimizer reports issues.
    """
    chi2_min: float
    nuisance_params: dict
    nuisance_errors: dict
    at_boundary: bool
    n_calls: int
    valid_minimum: bool
    messages: list


def hartlap_correction(n_realizations: int, n_bins: int = 9) -> float:
    """
    Hartlap factor for inverse-covariance bias correction.

    Hartlap et al. 2007, A&A 464, 399, eq. (7):
      Ĉ⁻¹_unbiased = [(N − p − 2) / (N − 1)] · Ĉ⁻¹_naive

    Args:
        n_realizations: Number of mock realizations N used to build sample covariance.
        n_bins: Covariance dimension p (default 9 for 9-bin DESI z=4.2 subset).

    Returns:
        Hartlap factor. Raises ValueError if N ≤ p + 2 (invalid regime).

    Raises:
        ValueError: If N <= p+2 (factor would be non-positive or undefined).
    """
    if n_realizations <= n_bins + 2:
        raise ValueError(
            f"Hartlap correction requires N > p + 2; got N={n_realizations}, "
            f"p={n_bins}. Use at least {n_bins + 3} realizations."
        )
    return (n_realizations - n_bins - 2) / (n_realizations - 1)


class Chi2Profiler:
    """
    χ² profile-likelihood profiler over 4 nuisance parameters.

    Wraps iminuit.Minuit to minimize χ² over (zrei, ha, hs, taueff) at fixed
    (m, f) parameter values, returning best-fit nuisances and minimized χ².

    The covariance may be pre-Hartlap-corrected (preferred) or raw sample,
    with correction applied on-the-fly via the `hartlap_n` parameter.

    Attributes:
        p_data: 9-element observed power spectrum (data vector).
        cov_inv: 9×9 inverse covariance matrix (Hartlap-corrected if applicable).
        predict_pk: Callable predict_pk(m, f, zrei, ha, hs, taueff) → 9-element array.
        hartlap_n: Optional N for on-the-fly Hartlap correction (else None).
    """

    def __init__(
        self,
        p_data: np.ndarray,
        cov_inv: np.ndarray,
        predict_pk,
        hartlap_n: Optional[int] = None,
        hartlap_p: int = 9,
    ):
        """
        Initialize profiler.

        Args:
            p_data: 9-element observed power spectrum.
            cov_inv: 9×9 inverse covariance matrix. If pre-Hartlap-corrected, pass
                hartlap_n=None (default). If raw sample covariance, pass hartlap_n=N_realizations
                to apply correction on-the-fly.
            predict_pk: Callable predict_pk(m, f, zrei, ha, hs, taueff) → 9-element array.
            hartlap_n: Optional. If provided, apply Hartlap correction to cov_inv:
                cov_inv_corrected = hartlap_factor(hartlap_n, hartlap_p) * cov_inv.
                Raises ValueError if hartlap_n <= hartlap_p + 2.
            hartlap_p: Covariance dimension for Hartlap formula (default 9).

        Raises:
            ValueError: If hartlap_n is provided but invalid (≤ p + 2).
            ValueError: If cov_inv is not positive-definite (detected via cho_factor).
        """
        self.p_data = np.asarray(p_data, dtype=np.float64)
        if self.p_data.shape != (9,):
            raise ValueError(f"p_data must have shape (9,), got {self.p_data.shape}")

        # Apply Hartlap correction if requested.
        if hartlap_n is not None:
            hf = hartlap_correction(hartlap_n, hartlap_p)
            self.cov_inv = hf * np.asarray(cov_inv, dtype=np.float64)
        else:
            self.cov_inv = np.asarray(cov_inv, dtype=np.float64)

        if self.cov_inv.shape != (9, 9):
            raise ValueError(
                f"cov_inv must have shape (9, 9), got {self.cov_inv.shape}"
            )

        # Validate positive-definiteness via Cholesky decomposition.
        # This will raise LinAlgError if cov_inv is not positive-definite.
        try:
            self._cho_factor = linalg.cho_factor(self.cov_inv)
        except linalg.LinAlgError as e:
            raise ValueError(
                f"Provided cov_inv is not positive-definite: {e}. "
                "Check that the inverse covariance matrix is valid."
            ) from e

        self.predict_pk = predict_pk
        self.hartlap_n = hartlap_n

    def _chi2_single_cell(self, m, f, zrei, ha, hs, taueff):
        """
        Compute χ² for a single (m, f) cell at given nuisance parameters.

        Args:
            m, f: FDM model parameters (scalar).
            zrei, ha, hs, taueff: IGM nuisance parameters (scalar).

        Returns:
            χ² = (p_pred - p_data)ᵀ Σ⁻¹ (p_pred - p_data).
        """
        p_pred = np.asarray(self.predict_pk(m, f, zrei, ha, hs, taueff), dtype=np.float64)
        if p_pred.shape != (9,):
            raise ValueError(
                f"predict_pk must return shape (9,), got {p_pred.shape}"
            )
        diff = p_pred - self.p_data
        # Compute quadratic form: χ² = diff @ cov_inv @ diff.
        # Direct computation; Cholesky factor is kept only for PD validation during init.
        chi2_val = float(diff @ self.cov_inv @ diff)
        return chi2_val

    def profile_likelihood(
        self, m: float, f: float, verbose: bool = False
    ) -> ProfileLikelihoodResult:
        """
        Minimize χ² over nuisance parameters (zrei, ha, hs, taueff) at fixed (m, f).

        Args:
            m: FDM log10 mass parameter.
            f: FDM abundance parameter.
            verbose: If True, print Minuit summary after minimization.

        Returns:
            ProfileLikelihoodResult with χ²_min and best-fit nuisances.
        """
        # Wrap chi2 function for the fixed (m, f) point.
        def chi2_nuisances(zrei, ha, hs, taueff):
            return self._chi2_single_cell(m, f, zrei, ha, hs, taueff)

        # Initialize Minuit.
        mi = Minuit(
            chi2_nuisances,
            zrei=NUISANCE_INIT["zrei"],
            ha=NUISANCE_INIT["ha"],
            hs=NUISANCE_INIT["hs"],
            taueff=NUISANCE_INIT["taueff"],
        )

        # Set bounds from integrated training support.
        for param_name, (lower, upper) in NUISANCE_BOUNDS.items():
            mi.limits[param_name] = (lower, upper)

        # Set error definition for χ² (least-squares).
        mi.errordef = Minuit.LEAST_SQUARES

        # Minimize.
        mi.migrad()

        # Extract results.
        chi2_min = mi.fval
        nuisance_params = dict(zip(mi.parameters, mi.values))
        nuisance_errors = dict(zip(mi.parameters, mi.errors))
        n_calls = mi.nfcn
        valid_minimum = mi.valid

        # Check if any parameter is at boundary (within 1e-4 of limit).
        at_boundary = False
        at_limit_params = []
        for param_name in mi.parameters:
            val = mi.values[param_name]
            lower, upper = NUISANCE_BOUNDS[param_name]
            if abs(val - lower) < 1e-4 or abs(val - upper) < 1e-4:
                at_boundary = True
                at_limit_params.append(param_name)

        # Collect warnings.
        messages = []
        if not valid_minimum:
            messages.append("Minuit did not converge to valid minimum")
        if at_boundary:
            messages.append(
                f"Nuisance parameters at boundary: {', '.join(at_limit_params)}. "
                f"Interior minimization may be unreliable."
            )

        if verbose:
            print(mi)

        return ProfileLikelihoodResult(
            chi2_min=chi2_min,
            nuisance_params=nuisance_params,
            nuisance_errors=nuisance_errors,
            at_boundary=at_boundary,
            n_calls=n_calls,
            valid_minimum=valid_minimum,
            messages=messages,
        )

    def profile_likelihood_grid(
        self,
        m_vals: np.ndarray,
        f_vals: np.ndarray,
        verbose: bool = False,
    ) -> dict:
        """
        Compute profile-likelihood χ² over a grid of (m, f) values.

        Args:
            m_vals: 1D array of FDM mass parameters.
            f_vals: 1D array of FDM abundance parameters.
            verbose: If True, print progress for each cell.

        Returns:
            Dictionary with keys:
                "m_vals", "f_vals": Input grids.
                "chi2_grid": 2D array of shape (len(m_vals), len(f_vals)).
                "best_fits": 2D array of shape (len(m_vals), len(f_vals), 4)
                    where last dim is [zrei, ha, hs, taueff].
                "at_boundary": 2D boolean array, True where optimizer hit a bound.
                "messages": List of any warning strings across all cells.
        """
        chi2_grid = np.zeros((len(m_vals), len(f_vals)), dtype=np.float64)
        best_fits = np.zeros((len(m_vals), len(f_vals), 4), dtype=np.float64)
        at_boundary_grid = np.zeros((len(m_vals), len(f_vals)), dtype=bool)
        all_messages = []

        for i, m in enumerate(m_vals):
            for j, f in enumerate(f_vals):
                result = self.profile_likelihood(m, f, verbose=verbose)
                chi2_grid[i, j] = result.chi2_min
                best_fits[i, j] = [
                    result.nuisance_params["zrei"],
                    result.nuisance_params["ha"],
                    result.nuisance_params["hs"],
                    result.nuisance_params["taueff"],
                ]
                at_boundary_grid[i, j] = result.at_boundary
                all_messages.extend(result.messages)

        return {
            "m_vals": m_vals,
            "f_vals": f_vals,
            "chi2_grid": chi2_grid,
            "best_fits": best_fits,
            "at_boundary": at_boundary_grid,
            "messages": all_messages,
        }
