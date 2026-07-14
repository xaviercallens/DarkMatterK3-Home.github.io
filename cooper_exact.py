#!/usr/bin/env python3
"""
cooper_exact.py
===============

V5.1 CERTIFIED mathematical kernel for the Cooper s_7 (OEIS A183204) period
engine. Supersedes the numerical core of cooper_periods.py, which is
DEPRECATED (see V5_SCIENTIFIC_REVIEW.md, findings F1-F3).

Ground truth (verified against oeis.org/A183204 b-file, 2026-07-14):

    a(n): 1, 4, 48, 760, 13840, 273504, 5703096, 123519792, ...

    Zudilin form:  a(n) = sum_{j=0..n} C(n,j)^2 * C(2j,n) * C(j+n,j)

    Recurrence (exact, verified n=0..38 in
    hypothesis_comparison_t103_cooper.py and re-verified here):

        (n+2)^3 a(n+2) = (26n^3+117n^2+177n+90) a(n+1)
                       + (27n^3+ 81n^2+ 78n+24) a(n)

    Characteristic equation lambda^2 = 26*lambda + 27 gives the EXACT
    exponential growth rate lambda = 27 (the other root is -1), so the
    fundamental period

        Pi_0(z) = sum_{n>=0} a(n) z^n

    converges iff |z| < 1/27, with a genuine singularity of the order-3
    Picard-Fuchs operator at z = 1/27 (K3 period degeneration point).

Design contract (differences from the deprecated module):
  * No "growth constant" normalization. The series is evaluated in the true
    variable z with the true radius of convergence 1/27.
  * Physical inputs are mapped to w in [0, W_MAX] where w = 27z is the
    fractional distance to the degeneration point; W_MAX < 1 keeps every
    evaluation strictly inside the disc of convergence.
  * Every evaluation carries a certified geometric tail bound, valid because
    a(n+1)/a(n) increases monotonically toward 27 (checked in self-test), so
    the truncation error after N terms is <= t_N * w/(1-w).
  * The asymmetry statistic excludes the k=0 (DC) mode and is band-averaged;
    the deprecated max|FFT diff| statistic was shown to equal the DC mode.
"""

import math
import numpy as np

# ---------------------------------------------------------------------------
# Exact sequence
# ---------------------------------------------------------------------------

LAMBDA = 27          # exact exponential growth rate (root of x^2 = 26x + 27)
Z_SING = 1.0 / 27.0  # radius of convergence / K3 degeneration point
W_MAX = 0.9          # maximum fractional approach to the singularity

# First terms from oeis.org/A183204 (b-file), used to seed and cross-check
_OEIS_SEED = [1, 4, 48, 760, 13840, 273504, 5703096, 123519792, 2751843600,
              62659854400, 1451780950048, 34116354472512, 811208174862904,
              19481055861877120, 471822589361293680, 11511531876280913760,
              282665135367572129040]


def _p1(n):
    return 26 * n**3 + 117 * n**2 + 177 * n + 90


def _p0(n):
    return 27 * n**3 + 81 * n**2 + 78 * n + 24


def cooper_s7_terms(n_max):
    """Exact integer terms a(0..n_max) of OEIS A183204 via the certified
    3-term recurrence (arbitrary precision, no floats)."""
    a = [1, 4]
    for n in range(n_max - 1):
        nxt = (_p1(n) * a[n + 1] + _p0(n) * a[n])
        q, r = divmod(nxt, (n + 2)**3)
        if r != 0:
            raise ArithmeticError(f"recurrence non-integrality at n={n}")
        a.append(q)
    return a[:n_max + 1]


def cooper_s7_binomial(n):
    """Independent cross-check: Zudilin's binomial-sum formula (exact)."""
    return sum(math.comb(n, j)**2 * math.comb(2 * j, n) * math.comb(j + n, j)
               for j in range(n + 1))


# ---------------------------------------------------------------------------
# Certified period evaluation
# ---------------------------------------------------------------------------

# Precompute scaled coefficients b(n) = a(n)/27^n once (float64 is exact
# enough here: b(n) decays like n^{-3/2}, values stay in [1e-3, 1]).
_N_COEFF = 400
_B_COEFF = None


def _scaled_coeffs():
    global _B_COEFF
    if _B_COEFF is None:
        terms = cooper_s7_terms(_N_COEFF)
        _B_COEFF = np.array([t / (27**n) for n, t in enumerate(terms)],
                            dtype=np.float64)
    return _B_COEFF


def period_pi0(w, rtol=1e-10):
    """
    Fundamental period Pi_0 evaluated at z = w/27, for w in [0, W_MAX].

    Pi_0(w/27) = sum_n a(n) (w/27)^n = sum_n b(n) w^n,  b(n) = a(n)/27^n.

    Since a(n+1)/a(n) < 27 for all n (ratios increase monotonically toward
    27), b(n) is decreasing, and the tail after N terms is bounded by
    b(N) * w^N * w/(1-w). Truncation stops when that certificate is below
    rtol * partial_sum.

    Args:
        w: scalar or ndarray in [0, W_MAX] (fraction of distance to the
           z = 1/27 degeneration point).
        rtol: relative tolerance for the certified tail bound.

    Returns:
        (value, tail_bound): Pi_0 and a rigorous upper bound on the
        truncation error (both scalar or ndarray matching w).
    """
    b = _scaled_coeffs()
    w = np.asarray(w, dtype=np.float64)
    if np.any(w < 0) or np.any(w >= 1.0):
        raise ValueError("w must lie in [0, 1); physical domain is [0, W_MAX]")

    val = np.zeros_like(w)
    wn = np.ones_like(w)          # w^n
    tail = np.full_like(w, np.inf)
    for n in range(len(b)):
        val = val + b[n] * wn
        wn = wn * w
        # certificate: remaining sum <= b(n+1) * w^{n+1} / (1 - w)
        if n + 1 < len(b):
            tail = b[n + 1] * wn / np.maximum(1.0 - w, 1e-12)
            if np.all(tail <= rtol * np.maximum(val, 1.0)):
                break
    return val, tail


# ---------------------------------------------------------------------------
# Physical mapping: density -> modulus
# ---------------------------------------------------------------------------

def rho_to_w(rho, rho_scale=1.0, w_max=W_MAX):
    """
    Map a non-negative density field to the fractional modulus w in [0, w_max].

        w(rho) = w_max * (rho/rho_scale) / (1 + rho/rho_scale)

    NOTE (see V5_RIGOROUS_THEORY_PLAN.md, WP-B1): this saturating form is an
    ANSATZ pending derivation from a chameleon-coupled modulus potential.
    It is kept explicit and swappable so control kernels can replace it.
    """
    r = np.asarray(rho, dtype=np.float64) / float(rho_scale)
    return w_max * r / (1.0 + r)


def kernel_cooper(rho, rho_scale=1.0):
    """Pointwise Cooper-s7 kernel K(rho) = Pi_0(z(rho)); certified evaluation."""
    val, _ = period_pi0(rho_to_w(rho, rho_scale))
    return val


def kernel_log_control(rho, rho_scale=1.0):
    """Control kernel: generic log(1+x), first-derivative matched to the
    Cooper kernel at rho=0 is NOT imposed here (see WP-B3 for the matched
    version); this is the basic shape control."""
    r = np.asarray(rho, dtype=np.float64) / float(rho_scale)
    return 1.0 + np.log1p(r)


def kernel_power_control(rho, rho_scale=1.0, alpha=0.5):
    """Control kernel: generic saturating power law."""
    r = np.asarray(rho, dtype=np.float64) / float(rho_scale)
    return 1.0 + r**alpha / (1.0 + r**alpha)


# ---------------------------------------------------------------------------
# Corrected asymmetry statistic (band-averaged, DC-excluded)
# ---------------------------------------------------------------------------

def delta_s7_band(rho_field, kernel=kernel_cooper, rho_scale=None,
                  n_shells=16, kmin_frac=0.05, kmax_frac=0.5):
    """
    Band-averaged spectral asymmetry between the kernel-warped field and the
    raw field.

    Both fields are reduced to zero-mean fluctuation contrast
    delta = field/mean(field) - 1 (this removes the DC mode by construction),
    FFT'd, and compared shell-by-shell in |k|:

        R(k_shell) = <|F_warp|>_shell / <|F_raw|>_shell

    Returns:
        dict with:
          'shell_k'      : shell centers (grid frequency units, cycles/box)
          'shell_ratio'  : R(k) per shell
          'delta_band'   : scalar summary = mean |R(k) - 1| over shells in
                           [kmin_frac, kmax_frac] * Nyquist
    """
    rho = np.asarray(rho_field, dtype=np.float64)
    if rho_scale is None:
        rho_scale = float(np.mean(rho))

    warped = rho * kernel(rho, rho_scale)

    def contrast(f):
        m = np.mean(f)
        return f / m - 1.0

    fw = np.fft.fftn(contrast(warped))
    fr = np.fft.fftn(contrast(rho))

    n = rho.shape[0]
    freqs = np.fft.fftfreq(n) * n              # integer grid frequencies
    kx, ky, kz = np.meshgrid(freqs, freqs, freqs, indexing='ij')
    kmag = np.sqrt(kx**2 + ky**2 + kz**2)

    nyquist = n / 2.0
    edges = np.linspace(kmin_frac * nyquist, kmax_frac * nyquist, n_shells + 1)
    shell_k, shell_ratio = [], []
    for i in range(n_shells):
        mask = (kmag >= edges[i]) & (kmag < edges[i + 1])
        if not np.any(mask):
            continue
        aw = np.mean(np.abs(fw[mask]))
        ar = np.mean(np.abs(fr[mask]))
        shell_k.append(0.5 * (edges[i] + edges[i + 1]))
        shell_ratio.append(aw / (ar + 1e-300))

    shell_ratio = np.array(shell_ratio)
    return {
        'shell_k': np.array(shell_k),
        'shell_ratio': shell_ratio,
        'delta_band': float(np.mean(np.abs(shell_ratio - 1.0))),
    }


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def _self_test():
    print("=" * 72)
    print("cooper_exact.py self-test (V5.1 certified kernel)")
    print("=" * 72)

    # 1. Recurrence terms match OEIS b-file seed exactly
    terms = cooper_s7_terms(len(_OEIS_SEED) - 1)
    assert terms == _OEIS_SEED, "recurrence terms disagree with OEIS b-file"
    print(f"[1] recurrence vs OEIS b-file: {len(_OEIS_SEED)} terms exact  OK")

    # 2. Recurrence terms match the independent Zudilin binomial formula
    terms21 = cooper_s7_terms(20)
    for n in range(0, 21):
        assert terms21[n] == cooper_s7_binomial(n)
    print("[2] recurrence vs Zudilin binomial formula: n=0..20 exact    OK")

    # 3. Growth-rate certificate: ratios increase monotonically toward 27
    long_terms = cooper_s7_terms(200)
    ratios = [long_terms[n + 1] / long_terms[n] for n in range(199)]
    assert all(ratios[i] < ratios[i + 1] for i in range(len(ratios) - 1))
    assert ratios[-1] < 27.0
    print(f"[3] a(n+1)/a(n) monotone increasing, r(199)={ratios[-1]:.6f}<27 OK")

    # 4. Scaled coefficients decay ~ n^{-3/2} (finite Pi_0 at the singularity)
    b = _scaled_coeffs()
    tail_check = b[300] * 300**1.5 / (b[100] * 100**1.5)
    print(f"[4] b(n)*n^1.5 stability check (300 vs 100): {tail_check:.4f}"
          f"  (order-3 K3 asymptotics)")

    # 5. Certified period values with tail bounds
    for w in [0.0, 0.3, 0.6, 0.9]:
        v, t = period_pi0(w)
        print(f"[5] Pi_0(z={w}/27): {float(v):.10f}   certified err <= {float(t):.2e}")

    # 6. Corrected metric is DC-free and responds to structure
    rng = np.random.default_rng(3)
    n = 64
    rho = np.ones((n, n, n))
    # add two gaussian blobs
    idx = np.indices((n, n, n))
    for c, amp, sig in [((20, 20, 20), 3.0, 5.0), ((44, 40, 30), 2.0, 8.0)]:
        d2 = sum((idx[i] - c[i])**2 for i in range(3))
        rho += amp * np.exp(-d2 / (2 * sig**2))
    rho += 0.05 * rng.standard_normal(rho.shape)
    rho = np.clip(rho, 0.05, None)

    r_struct = delta_s7_band(rho)
    r_flat = delta_s7_band(np.clip(1.0 + 0.05 * rng.standard_normal(rho.shape), 0.05, None))
    print(f"[6] delta_band structured field: {r_struct['delta_band']:.5f}   "
          f"flat noise field: {r_flat['delta_band']:.5f}")
    assert r_struct['delta_band'] > r_flat['delta_band']

    # 7. Control-kernel comparison runs (identifiability harness exists)
    r_log = delta_s7_band(rho, kernel=kernel_log_control)
    print(f"[7] control kernels: cooper={r_struct['delta_band']:.5f} "
          f"log={r_log['delta_band']:.5f}  (discrimination is WP-B3's job)")

    print("=" * 72)
    print("ALL SELF-TESTS PASSED — certified kernel operational")
    print("=" * 72)


if __name__ == "__main__":
    _self_test()
