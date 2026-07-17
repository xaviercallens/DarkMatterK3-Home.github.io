# Experimentation Layer — Dual-Scale Evolution Infrastructure

**Status:** Active (v1.0, Stream 3)  
**Last updated:** 2026-07-17

This document describes the improved experimentation layer for the V5 pipeline, focusing on parametric exploration, dual-scale signal recovery, and structured experiment tracking.

---

## 1. Overview

The experimentation layer provides three main capabilities:

1. **Parametric Exploration** (`pipeline/experiments.py`)
   - Power curve estimation: how signal recovery scales with amplitude
   - False-positive rate calibration: type-I error control across alpha levels
   - Effect size metrics: Cohen's d and SNR for signal-to-noise assessment

2. **Dual-Scale Analysis** (`pipeline/scales.py`)
   - FFT-based scale decomposition (coarse vs. fine frequencies)
   - Per-scale signal recovery metrics
   - Scale-mixing analysis: orthogonality and cross-correlation

3. **Experiment Tracking** (`pipeline/experiment_log.py`)
   - Structured JSON logging with full provenance (git hash, timestamp, config)
   - Auto-generation of `OBSERVATIONAL_REPORT.md` summaries
   - Mechanical labeling (SYNTHETIC, TEST, FIT) per CLAUDE.md

---

## 2. Quick Start

### Run the Full Experimentation Suite

```bash
python scripts/run_experimentation_suite.py
```

Options:
- `--quick`: Reduce trial counts for fast iteration
- `--field-size N`: Test field size (default: 24, meaning 24³)
- `--output-dir DIR`: Experiment log directory (default: `logs/`)

Output:
- `logs/experiments.json`: Structured log of all experiments
- `OBSERVATIONAL_REPORT.md`: Auto-generated summary

### Run Tests

```bash
make pipeline-tests
```

This runs all pipeline tests including the new 16 merge-blocking tests for the experimentation layer.

---

## 3. Module Reference

### 3.1 Parametric Exploration (`pipeline/experiments.py`)

#### `ExperimentConfig`
Configuration dataclass for an experiment run.

```python
from pipeline.experiments import ExperimentConfig

config = ExperimentConfig(
    field_size=24,
    amplitude=2.0,
    noise_sigma=0.05,
    alpha=0.05,
    n_null_trials=300,
    seed_base=1000,
)
```

#### `estimate_power_curve(config, amplitudes, trials_per_amplitude, device)`
Computes rejection rate as a function of signal amplitude.

```python
import numpy as np
from pipeline.experiments import estimate_power_curve

config = ExperimentConfig(field_size=16, n_null_trials=100)
amplitudes = np.array([0.5, 1.0, 2.0, 3.0])

power = estimate_power_curve(config, amplitudes, trials_per_amplitude=15)

print(power.amplitudes)
print(power.rejection_rates)       # Power at each amplitude
print(power.ci_lower)               # 95% CI lower bound
print(power.ci_upper)               # 95% CI upper bound
```

Returns: `PowerCurve(amplitudes, rejection_rates, ci_lower, ci_upper)`

#### `estimate_false_positive_rate(config, alphas, trials_per_alpha, device)`
Estimates the empirical false-positive rate (type-I error) across nominal alpha levels.

```python
from pipeline.experiments import estimate_false_positive_rate

config = ExperimentConfig(field_size=16)
alphas = np.array([0.01, 0.05, 0.10])

calib = estimate_false_positive_rate(config, alphas, trials_per_alpha=20)

print(calib.fp_rates)  # Empirical FP rates
print(calib.ci_lower)  # Confidence intervals
```

Returns: `CalibrationCurve(alphas, fp_rates, ci_lower, ci_upper)`

#### `compute_effect_sizes(config, device)`
Computes standardized effect sizes.

```python
from pipeline.experiments import compute_effect_sizes

config = ExperimentConfig(field_size=16, amplitude=2.0)
effects = compute_effect_sizes(config)

print(effects["cohens_d"])      # Cohen's d (effect size)
print(effects["snr"])           # Signal-to-noise ratio
print(effects["null_mean"])     # Mean of null distribution
print(effects["signal_mean"])   # Mean of signal distribution
```

Returns: `dict` with keys `cohens_d`, `snr`, `null_mean`, `null_std`, `signal_mean`, `signal_std`

---

### 3.2 Dual-Scale Analysis (`pipeline/scales.py`)

#### `decompose_scales(field, cutoff_freq)`
Decomposes a 3D field into coarse (low-frequency) and fine (high-frequency) components via FFT.

```python
from pipeline.scales import decompose_scales
from pipeline.synthetic import signal_field

field = signal_field(24, seed=42, amplitude=2.0)
decomp = decompose_scales(field, cutoff_freq=6.0)

print(decomp.coarse)       # Low-freq component
print(decomp.fine)         # High-freq component
print(decomp.cutoff_freq)  # Frequency cutoff used
```

Returns: `ScaleDecomposition(coarse, fine, cutoff_freq)`

#### `compute_scale_metrics(field, scale)`
Computes signal recovery metrics for a single scale.

```python
from pipeline.scales import compute_scale_metrics

metrics = compute_scale_metrics(decomp.coarse, scale="coarse")

print(metrics.energy_ratio)        # (signal energy) / (total energy)
print(metrics.contrast_recovery)   # Normalized contrast
print(metrics.snr_per_scale)       # Signal-to-noise ratio
print(metrics.peak_frequency)      # Dominant frequency
```

Returns: `ScaleMetrics(scale, energy_ratio, contrast_recovery, snr_per_scale, peak_frequency)`

#### `analyze_scale_mixing(full_field, decomp)`
Quantifies cross-talk between coarse and fine scales.

```python
from pipeline.scales import analyze_scale_mixing

mixing = analyze_scale_mixing(field, decomp)

print(mixing["orthogonality_violation"])   # Should be near 0
print(mixing["energy_conservation_error"]) # Should be < 1%
print(mixing["cross_correlation"])         # Should be near 0
```

Returns: `dict` with keys for orthogonality, energy conservation, and cross-correlation

---

### 3.3 Experiment Tracking (`pipeline/experiment_log.py`)

#### `ExperimentLogger`
Logs experiments to a structured JSON file with full provenance.

```python
from pipeline.experiment_log import ExperimentLogger

logger = ExperimentLogger(log_path="logs/experiments.json")

# Log a power curve experiment
logger.log_experiment(
    experiment_type="power_curve",
    config={"field_size": 24, "amplitudes": [0.5, 1.0, 2.0]},
    results={"rejection_rates": [0.3, 0.7, 0.95]},
    label="SYNTHETIC",
)

# Query summary
summary = logger.get_summary(experiment_type="power_curve")
print(summary["count"])  # Number of power curve experiments
```

#### `ObservationalReportWriter`
Auto-generates `OBSERVATIONAL_REPORT.md` from experiment logs.

```python
from pipeline.experiment_log import ObservationalReportWriter

reporter = ObservationalReportWriter()
reporter.write_report_stub()  # Creates OBSERVATIONAL_REPORT.md stub
```

---

## 4. Workflow: Running a Full Analysis

### Step 1: Generate Synthetic Data and Run Experiments
```bash
python scripts/run_experimentation_suite.py --quick --field-size 24
```

### Step 2: Review Logged Experiments
```bash
cat logs/experiments.json | python -m json.tool | head -100
```

### Step 3: Review Auto-Generated Report
```bash
cat OBSERVATIONAL_REPORT.md
```

### Step 4 (T0 only): Interpret Results
Edit `OBSERVATIONAL_REPORT.md` to add:
- Context (which hypothesis this tests)
- Interpretation (what do the numbers mean?)
- Epistemic tier (Tier A/B/C per VISION.md §2)
- Next steps (what experiment to run next?)

---

## 5. Testing

All new modules are covered by merge-blocking tests:

- `pipeline/tests/test_experiments.py`: 16 tests for parametric exploration
  - Power curve estimation
  - False-positive rate calibration
  - Effect size computation

- Tests verify:
  - Rejection rates increase with amplitude
  - Confidence intervals are valid (lower ≤ rate ≤ upper)
  - Effect sizes scale as expected
  - Scale decomposition reconstructs the field
  - Scale mixing analysis has correct properties

Run tests:
```bash
pytest pipeline/tests/test_experiments.py -v
```

---

## 6. Pre-Registration & Gating

All experimentation respects CLAUDE.md rules:

1. **Gate G1**: Real-data comparisons blocked until `PREDICTION.md` is pinned
2. **Result Labels**: Mechanical (SYNTHETIC, TEST, FIT)
3. **Provenance**: Every result includes git hash, timestamp, config
4. **Immutability**: Logged experiments can only be appended (JSON)

---

## 7. Next Steps (WP S3-03 per EXECUTION_PLAN.md)

1. **Systematic Parameter Sweep**: Run power curves across (field_size, noise_sigma)
2. **Cross-Scale Comparison**: Compare signal recovery at coarse vs. fine scales
3. **Weak Lensing Integration**: Add weak-lensing observable to scale metrics
4. **PTA Bridge**: Extend dual-scale analysis to gravitational wave timings

---

## 8. References

- **CLAUDE.md**: Non-negotiable rules (rule 2: gate G1, rules 3–4: pre-reg discipline)
- **EXECUTION_PLAN.md**: WP S3-02 (pipeline tests), WP S3-03 (parametric exploration)
- **VISION.md**: §3–§4 (epistemic tiers, F-theory hypotheses)
- **PREDICTION.md**: Pinning gate G1 (currently unpinned)
