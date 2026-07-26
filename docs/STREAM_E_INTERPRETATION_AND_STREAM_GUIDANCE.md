# Stream E Experiment Interpretation and Guidance for Streams 1 and 2

**Branch**: `feature/rust-kernel-boinc-scale`  
**Scope**: interpretation of the artifacts actually produced in `artifacts/stream_e/`  
**Epistemic status**: engineering audit and decision guidance; no new physics claim

## 1. Executive interpretation

The experiment established that the existing Python exact-rational C1 checker can be exposed through a batch-oriented interface and executed as independent `(candidate, N1)` cells. It did not establish that a Rust kernel, BOEINC deployment, or GPU implementation is correct or faster, because none of those three systems performed the recorded computations.

The strongest persisted mathematical result is:

- Cooper `s7 = (13, 4, -27, 3)` returned `PASS(50)` and `PASS(100)` with denominator margin `1` in the generated batch artifact.
- These are finite-order C1 results. They strengthen the tested bound but do not prove all-order mirror-map integrality.
- The values were computed by the existing Python `Fraction` implementation, not by an independent implementation.

The main engineering result is:

- Local sequential work cells, JSON result packaging, and a checkpoint file were demonstrated.
- This is a useful orchestration prototype.
- It is not yet a native BOEINC work-unit implementation, a distributed quorum validator, a measured Rust acceleration, or a GPU capacity result.

Therefore the experiment should change workflow confidence, not candidate ranking. It makes repeated C1 checks easier to organize, but it supplies no new discriminator between `t103`, `s7`, and `s10`.

## 2. Evidence ledger

### 2.1 Directly supported by persisted artifacts

| Finding | Evidence | Interpretation |
|---|---|---|
| `s7` passes C1 through `N1=50` | `boinc_batch_results.json` | Exact finite-order integrality evidence |
| `s7` passes C1 through `N1=100` | `boinc_batch_results.json` | Stronger finite-order integrality evidence |
| Two local cells completed without reported exceptions | `boinc_batch_results.json` | Local batch plumbing works for this sample |
| Four local cells were recorded for `alpha` and `s7` at `N1={50,100}` | `large_gpu_run_report.json` | Small sequential orchestration smoke test |
| A checkpoint was written | `large_gpu_run_checkpoint.pkl` | Serialization exists; recovery correctness is not yet established |

### 2.2 Session observations not backed by a committed report

- The parity script printed `38/38` for six known-good operators and two perturbed controls.
- An interactive `s7` run printed `PASS(200)`.
- Rust tooling was installed, but the MSVC linker was unavailable during the attempted crate build.

These observations may guide the next run, but they should not be cited as durable evidence until emitted into versioned JSON or Markdown reports with commands, versions, timings, and hashes.

### 2.3 Not established

- **No Rust kernel**: `stream_e_c1_oracle.py` imports and calls the Python reference checker directly.
- **No independent parity**: the so-called parity gate executes the same Python implementation through a subprocess wrapper. It tests CLI consistency and controls, not Rust-versus-Python equality.
- **No BOEINC integration**: `stream_e_boinc_schema.py` is a local dataclass executor. It does not extend the existing BOEINC generator, XML templates, client, server, or reconciliation tests.
- **No exact-result validator**: the local validator compares a hash derived from only operator, `N1`, verdict, and margin. It does not compare the complete canonical result payload and could accept differing coefficients.
- **No GPU computation**: `stream_e_large_gpu_run.py` invokes CPU Python C1 checks. It performs no CUDA allocation, FFT, `nvidia-smi` sampling, 384³ grid, or VRAM enforcement.
- **No full large run**: the report covers two candidates and two orders, reports `interrupted: true`, and contains inconsistent state (`total_batches=6` while only two candidates are listed).
- **No demonstrated kill/resume**: writing and reloading a checkpoint is not equivalent to killing a process after completed shards and proving continuation from the last durable shard.
- **No scaling conclusion**: no `scaling_ladder_report.json` or complete timing ladder exists. Speedup and practical `N1=500` claims are unsupported.
- **No CI conclusion**: repository guardrails and pipeline tests were not recorded as run in the experiment artifacts.

## 3. Scientific interpretation

### 3.1 What C1 licenses

A result `PASS(N1)` means that every inverse mirror-map coefficient tested through order `N1` is integral under the fixed normalization. It is exact arithmetic and therefore stronger than a floating-point consistency check at the same order. It remains bounded evidence rather than an all-order theorem.

The correct language is:

> `s7` satisfies the tested C1 mirror-map integrality condition through `N1=100` in the Python reference implementation.

The incorrect language is:

> `s7` is proved to be the unique physical K3 substrate.

### 3.2 What the experiment says about the finalists

- **s7**: operationally mature. It has a known order-3 operator and persisted C1 results through `N1=100` in this experiment.
- **s10**: remains a viable literature-anchored finalist, but this experiment did not persist a new `s10` result artifact.
- **t103**: remains the most important unresolved case. The current Stream E interface cannot test it until Stream 2 supplies or confirms its normalized `(a,b,c,d)` operator. Absence of a C1 result is missing evidence, not failure.
- **S12**: its rejection rests on the separately reported minimal ODE order and non-integral mirror coefficient, not on Stream E.

No ranking change among `t103`, `s7`, and `s10` follows from this experiment. A candidate being easier to compute or having a more complete certificate trail is an engineering advantage, not a geometric discriminator.

### 3.3 Relation to observational Delta

The measured galaxy-distribution asymmetry does not distinguish the finalists under the current common-normalization model. Stream E added no joint likelihood, candidate-specific forward model, or out-of-sample observational test. Therefore observational Delta must not be used to promote `s7` over `t103` or `s10` at this stage.

## 4. Guidelines for Stream 1

Stream 1 should treat the result as a constraint on claim discipline and as a request for missing theory inputs.

### 4.1 Immediate actions

1. **Keep the finalist set open**: retain `t103`, `s7`, and `s10`; do not promote `s7` solely because its C1 path is currently executable.
2. **Supply the normalized t103 operator**: derive and review the order-3 Picard-Fuchs operator in the same normalization expected by C1. Include provenance and a recurrence-to-operator derivation.
3. **Separate theorem, computation, and phenomenology**:
   - exact recurrence verification is not full K3 classification;
   - finite C1 is not an all-order theorem;
   - observational Delta is not candidate identification.
4. **Replace selection language with maturity language** where appropriate: `s7` is currently the most certificate-ready finalist, not necessarily the uniquely selected substrate.
5. **Define candidate-specific discriminants before using data**: identify an observable or invariant that differs across finalists after nuisance parameters and common normalization are fixed.

### 4.2 Theory work packages

| Priority | Work package | Definition of done |
|---|---|---|
| P0 | t103 normalized operator | Reviewed `(a,b,c,d)` tuple plus derivation and golden low-order coefficients |
| P0 | Full gate matrix | For each finalist: ODE minimality, MUM/Fuchs data, C1, C3, C3b, modularity status, provenance |
| P1 | All-order integrality route | State whether a modular parametrization, recurrence theorem, or arithmetic-geometry argument could promote finite C1 evidence |
| P1 | Candidate-specific observable | Forward prediction differs among at least two finalists and includes uncertainty propagation |
| P2 | Formalization boundary | Explicitly list what Lean proves, what exact Python checks, and what remains imported from literature |

### 4.3 Decision rule for Stream 1

Do not select a unique substrate until one of these occurs:

- one or more finalists fail a predeclared mathematical gate;
- an all-order theorem separates the finalists;
- a candidate-specific, preregistered observational prediction produces a robust out-of-sample distinction.

Until then, report a Pareto set rather than a winner.

## 5. Guidelines for Stream 2

Stream 2 owns the authoritative criterion definitions, candidate set, tolerances, and promotion of certificates. Its next work should convert the prototype into an auditable ranking pipeline.

### 5.1 Freeze authoritative inputs

1. Declare whether `ORDER3_AZ_COOPER` is the source of truth.
2. Version each operator by name, `(a,b,c,d)`, normalization, source, and content hash.
3. Add `t103` only after its operator is reviewed; represent it as `NOT_TESTED` beforehand, never `FAIL`.
4. Freeze standard C1 rungs such as `N1={50,100,200}`. Use `N1=500` only after measured runtime and memory results exist.

### 5.2 Build an auditable certificate matrix

For every candidate and criterion, record:

- status: `PASS`, `FAIL`, `CONDITIONAL`, or `NOT_TESTED`;
- bound or tolerance;
- exact operator/version hash;
- implementation and commit hash;
- certificate path and SHA-256;
- runtime and resource metadata;
- first failing coefficient or residual when applicable.

Never rank `NOT_TESTED` below `PASS` as if it were negative evidence. Track evidence completeness separately from scientific score.

### 5.3 Correct validation policy

- **C1**: compare canonical complete payloads or exact coefficient arrays, excluding only explicitly non-semantic metadata. Replicate each distributed cell twice and require exact equality.
- **C3**: follow its arithmetic model; do not inherit a C1 rule automatically.
- **C3b**: Stream 2 must declare the admissible numerical tolerance, convergence policy, precision, and platform sensitivity before any port.
- Include mutation tests that alter a coefficient while preserving verdict and margin; the validator must reject them.

### 5.4 CI and review policy

1. Invoke checker tests explicitly in CI rather than silently depending on `pytest.ini` discovery.
2. Require golden-good and golden-bad controls for every implementation.
3. Require an independent implementation before calling a result parity evidence. A wrapper around the reference is not independent.
4. Quarantine generated certificates under `artifacts/stream_e/certificates/`; promote them only after Stream 2 review.
5. Preserve the original reference certificate and attach the accelerated implementation as corroborating provenance.

### 5.5 Ranking policy

Use two axes:

- **Scientific gate score**: mathematical criteria only.
- **Evidence maturity score**: coverage, independent replication, bounds, provenance, and review status.

Do not let implementation speed, certificate availability, or literature familiarity leak into the scientific gate score.

## 6. Corrected engineering sequence

The next engineering steps should follow the original gates rather than treating the Python prototype as completion.

1. Install or expose the MSVC C++ build tools and verify `link.exe` from a developer shell.
2. Implement `rust/k3_kernel` with `num-bigint` and `num-rational`.
3. Compare exact Rust coefficient arrays against Python for all 36 cells and both bad controls.
4. Persist the parity matrix with implementation hashes and timings.
5. Run a measured Rust/Python scaling ladder; do not state a speedup beforehand.
6. Extend the existing `core_boinc` generator and tests instead of maintaining a parallel local executor.
7. Canonicalize full result JSON and test mutation rejection.
8. Implement the separate CUDA/FFT capacity runner with occupancy checks, measured VRAM, real shards, and a genuine kill/resume test.
9. Run repository guardrails and checker tests, then record their exact commands and outputs.

GPU and C1 should remain separate: exact C1 is a CPU big-integer workload; the RTX 2070 is relevant to the field/FFT pipeline, not to the current C1 wrapper.

## 7. Stop/go decisions

### Go now

- Use the Python batch wrapper for small, controlled C1 jobs.
- Ask Stream 1 for the normalized t103 operator.
- Build the complete Stream 2 candidate-by-criterion evidence matrix.
- Fix certificate provenance and CI coverage.

### Conditional go

- Run higher `N1` Python checks only with checkpointing, timing, memory reporting, and durable artifacts.
- Prototype distributed work units only after canonical result validation is fixed.

### Stop

- Do not merge claims that the Rust kernel, BOEINC system, or 384³ GPU run is complete.
- Do not cite `38/38` as Rust parity.
- Do not cite the four-cell CPU run as a GPU capacity test.
- Do not use the experiment to uniquely select `s7`.
- Do not describe finite-order C1 as a proof.

## 8. Bottom line

The experiment is valuable as a diagnostic. It exposed the correct computational unit, confirmed that exact C1 jobs can be packaged deterministically, and reinforced `s7` through a persisted `PASS(100)` result. More importantly, it exposed the present bottleneck: not raw compute, but evidence separation and provenance.

For Stream 1, the highest-value next result is the normalized `t103` operator and a candidate-specific discriminator. For Stream 2, it is a complete, versioned gate matrix with correct exact validators and explicit C3b tolerance. For Stream E, it is still the native Rust parity gate followed by measured scaling. Until those are complete, the scientifically defensible conclusion is that `t103`, `s7`, and `s10` remain finalists with unequal evidence maturity, not unequal demonstrated truth.
