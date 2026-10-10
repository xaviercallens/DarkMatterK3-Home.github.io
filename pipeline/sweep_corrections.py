#!/usr/bin/env python3
"""
WP-E6-SWEEP — theory-side corrections C1/C2/C3 as ruled (briefs/T0_RULING_SWEEP_C1_C5_EB_2026_10_10.md).

ENGINEERING / DESIGN label. This module performs no model–data comparison. Authority: T0's instruction of 2026-10-10
("implement on my behalf"), taking the recommended options of `T0_DECISION_REQUEST_SWEEP_THEORY_CORRECTIONS_2026_09_17.md`;
effective only once the ruling file is merged and named by `sweep.REAL_DATA_RULING_PIN`.

  C2(b)  patchy reionization: upstream's fixed `with_patchy` factor, read from the hash-pinned upstream corrector pickle
         (lya-mfdm 9182aa4). It corrects the SIMULATIONS, not the data.
  C1(c-SiIII)  the Si III–Lyα oscillation shape is upstream's  g(k) = a_auto exp(k/k_auto) + a_cross exp(k/k_cross) cos(2271 k)
         at the 16 native k; its AMPLITUDE s is a profiled 5th nuisance:  correction = 1 + s·g(k).  s = 1 is upstream's
         fixed value (fitted on Boera et al. 2019), s = 0 is "no Si III". Prior BOX s ∈ [0, 4] (non-negative: the
         metal–Lyα correlation amplitude is not negative; 4× upstream allows for a different dataset's amplitude). It is a prior-
         BOX, not a trained-support extremum; a best fit pinned at an edge is reported as such.
  C3(a)  no resolution template (the provider's default: the correlated covariance template handles it).
  pixel window: upstream's fixed multiplier, bundled with C2(b) as part of "upstream total"; its effect is ≤ 0.001 σ in every band.

Si II, Mg II and C IV doublets are NOT modelled (logged as a known limitation; with 5 nuisances 4 dof remain).
"""
import hashlib
import pickle
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
CORRECTOR_WITH_PATCHY = REPO_ROOT / "phase1_work" / "agent1_emulator" / "lya-mfdm" / "emu" / "lya_corrector_with_patchy.pkl"
CORRECTOR_SHA256 = "4d36fcf27e43ef3bd5e654b65f6ff481014b00c86f60035cfe18f19ea6a0cd6d"
Z_KEY = "4.2"
SIII_PRIOR_BOX = (0.0, 4.0)
SIII_INIT = 1.0                      # upstream's own amplitude
NATIVE_LOG10K = np.round(np.arange(-2.2, -0.65, 0.1), 1)


class CorrectorPinError(RuntimeError):
    pass


class _Stub:
    """Receives upstream's `__main__.LyaCorrector` state; no code of the upstream repo is imported or run."""


class _RestrictedUnpickler(pickle.Unpickler):
    _ALLOWED = {("numpy.core.multiarray", "_reconstruct"), ("numpy._core.multiarray", "_reconstruct"),
                ("numpy", "ndarray"), ("numpy", "dtype"), ("numpy.core.multiarray", "scalar"), ("numpy._core.multiarray", "scalar")}

    def find_class(self, module, name):
        if (module, name) == ("__main__", "LyaCorrector"):
            return _Stub
        if (module, name) in self._ALLOWED:
            return super().find_class(module, name)
        raise CorrectorPinError(f"refusing to unpickle {module}.{name}")


def load_corrector(path=CORRECTOR_WITH_PATCHY, sha256=CORRECTOR_SHA256):
    raw = Path(path).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != sha256:
        raise CorrectorPinError(f"corrector pickle sha256 {got} != pinned {sha256}")
    import io
    obj = _RestrictedUnpickler(io.BytesIO(raw)).load()
    for attr in ("pixel_multiplier", "patchy_dict", "siiii_dict", "target_k", "apply_patchy"):
        if not hasattr(obj, attr):
            raise CorrectorPinError(f"corrector lacks attribute {attr}")
    if not obj.apply_patchy:
        raise CorrectorPinError("expected the with_patchy variant")
    if not np.allclose(np.asarray(obj.target_k, dtype=float), 10.0 ** NATIVE_LOG10K, rtol=1e-9):
        raise CorrectorPinError("corrector target_k is not the 16 native emulator k")
    return obj


def siiii_shape(corr, z=Z_KEY):
    """g(k) at the 16 native k, so that upstream's Si III correction is 1 + g."""
    k_auto, k_cross, a_auto, a_cross = corr.siiii_dict[z]
    k = np.asarray(corr.target_k, dtype=float)
    return a_auto * np.exp(k / k_auto) + a_cross * np.exp(k / k_cross) * np.cos(2271.0 * k)


def fixed_multiplier(corr, z=Z_KEY):
    """pixel window × patchy reionization at z (the parts of the correction that are NOT profiled)."""
    return np.asarray(corr.pixel_multiplier, dtype=float) * np.asarray(corr.patchy_dict[z], dtype=float)


def multiplier(corr, s, z=Z_KEY):
    """The 16-vector multiplier for Si III amplitude s: pixel × (1 + s·g) × patchy. s = 1 reproduces upstream's total."""
    # same multiplication order as upstream's get_total_correction, so s = 1 is bit-identical to it
    out = np.asarray(corr.pixel_multiplier, dtype=float).copy()
    out *= (1.0 + float(s) * siiii_shape(corr, z))
    out *= np.asarray(corr.patchy_dict[z], dtype=float)
    return out


def upstream_total(corr, z=Z_KEY):
    """upstream's own get_total_correction, recomputed from the stored arrays (control for `multiplier(corr, 1.0)`)."""
    return (np.asarray(corr.pixel_multiplier, dtype=float) * (1.0 + siiii_shape(corr, z))
            * np.asarray(corr.patchy_dict[z], dtype=float))
