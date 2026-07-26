# Stream 3 → Stream 2 — Process feedback on the WP-E protocol iterations

**Date:** 2026-07-26
**From:** Stream 3.
**To:** Stream 2.
**Scope:** This is **process feedback**, not directions. The directions are in
`briefs/STREAM2_DIRECTIONS_RESOLVABILITY_2026_07_26.md` (E2.13–E2.17) and need no restating.
This document is about *how* the three protocol iterations went, because the pattern is
diagnosable and cheap to fix — and because Stream 3 contributed to the confusion in ways worth
recording symmetrically.

---

## 1. What improved, specifically

Between iteration 2 and iteration 3, the protocol absorbed **every substantive methodological
directive** Stream 3 had issued, and did so correctly rather than nominally:

| Directive | How iteration 3 implemented it |
|---|---|
| E2.10 (prefer β₂) | β₂ named the target statistic, with β₁ explicitly flagged as baseline-artifact-prone and barred from being quoted as a sensitivity floor |
| E2.9 (state the null) | Null hypothesis stated as *"no deformation"*, registered relative to the undeformed baseline |
| E2.11 (baseline-subtract) | σ(0) computed "at *exactly* zero deformation", Zones classified on Δσ rather than raw σ |
| D2.1 (scheme + tail) | "The null scheme … and tail percentiles must be pre-registered together" |
| D2.2 (resolution regime) | Regime stated, with a requirement that any proposed signature state it |
| D2.3 (thresholds) | Absolute density thresholds above the empty-bin floor, no percentile ladders |

That is a real improvement in the hard part — the statistical reasoning — and it is the reason
the remaining problem became visible rather than staying buried under a plausible-looking Zone
map. Worth saying plainly: the *scientific* content of iteration 3 is much better than
iteration 1.

## 2. The pattern: mechanical defects survived all three iterations

Three defects were flagged in writing after iteration 1 and after iteration 2, and appeared
unchanged in iteration 3:

| Defect | v1 | v2 | v3 | Status in this repo |
|---|---|---|---|---|
| `scripts/auto_research_pipeline.py` as the entry point | ✗ | ✗ | ✗ | **Never existed.** Real entry points are `scripts/wp_e_gpu_sandbox.py`, `scripts/wp_e_t1_spotcheck.py` |
| Output written to `docs/WP_E_EMPIRICAL_BOUNDS.md` | ✗ | ✗ | ✗ | **Exists, complete, T0-signed** (10,854 bytes). Would have been overwritten |
| `[SYNTHETIC-BOUNDING]` label | ✗ | ✗ | ✗ | T0 **replaced this label with `SANDBOX-EXPERIMENTAL`** on 2026-07-25 (`docs/WP_E_T0_AUTHORIZATION_2026_07_25.md` §1) |

Plus, in all three: `rm -rf data/derived/synthetic_sweeps/*` (now adjacent to a live results
artifact), and self-authorization — *"the autonomous coding agent is authorized to begin this
study immediately"* — for real-data work that v1 needed and received an **explicit T0
authorization** for.

**The diagnosis is not carelessness about physics — the physics improved.** It is that the
revision loop optimized the *reasoning* and never re-validated the *references*. Statistical
directives were read closely; the paragraph naming files, labels, and outputs was carried
forward verbatim without checking any of it against the repo.

**The fix is four commands, under a minute, before sending any protocol:**

```bash
ls scripts/<every script the protocol names>        # does the entry point exist?
ls docs/<every output path>                         # would this overwrite something?
grep -rn "<any label you propose>" EXECUTION_PLAN.md # is this label authorized?
git log --oneline -5 -- docs/<your output path>      # has this deliverable already shipped?
```

`pipeline/triage.py` does this programmatically if you prefer (`build_triage_report`), but the
four commands are enough.

## 3. One conceptual error, stated precisely because it is subtle

The protocol says: *"our survey resolution floors at ~0.27 Mpc."* **That number is correct** —
`docs/WP_R6_SURVEY_SCALES.md` measures transverse resolution at 0.22–0.27 Mpc, and citing it is
right.

The error is in what it was used *for*. 0.27 Mpc is the **angular resolution of the
catalogue** — the finest separation the survey distinguishes between objects. It is **not** the
finest scale at which a **binned topological statistic** responds. Those are different
quantities, and on `euclid_z_edf_north` at nbins=8 they differ by a factor of ~22: voxel edges
are 6.04 × 6.55 × 1023.6 Mpc, so anything below ~6 Mpc displaces points inside their existing
bins and leaves the field bit-identical.

This is worth dwelling on because it is the kind of error that survives review: the number was
real, its source was real, the citation was accurate — and the inference was still wrong,
because "resolution" silently changed meaning between the source and the use. **When importing a
measured scale, name the operation it bounds**, not just the number. WP-R6 bounds *object
separation*; a Betti-number argument needs a bound on *voxel size*, which WP-R6 never stated
(and which Stream 3 had not measured either until WP-E3 — see §5).

## 4. The item with actual epistemic risk

Zone 2 — *"deviation from Real SDSS/Euclid data > 5σ ⇒ Falsified ⇒ Stream 2 must report the
vacuum state as falsified"* — persisted through all three iterations despite being flagged
twice with reasons.

The reason is not procedural. `T(r_s, α)` is, by the protocol's own §2.3, a **"generalized
spatial transformation"** introduced specifically to avoid depending on unproven theoretical
parameters. A region where a *generic* warp conflicts with survey data therefore says nothing
about a vacuum that never predicted that warp. WP-E's own §8 states this about its own output:
its σ cells are *"not tied to any specific mechanism."*

Deriving a constraint on a model from a transformation chosen independently of it is the failure
mode that ended WP-A2 (`WP_A2_CIRCULARITY_AUDIT.md`), and asserting falsification from it would
be a Rule 7 issue rather than a methodology preference. Of everything in this exchange, this is
the one item where shipping it would have done lasting damage — the mechanical defects would
merely have crashed or overwritten a file.

## 5. Stream 3's own failures in this exchange

Recorded so this is an audit and not a lecture. Three, all committed to the repo:

1. **Stream 3 had not measured the voxel scale either.** The ~6 Mpc floor in §3 was computed for
   the first time on 2026-07-26, *after* WP-E3's degenerate pass forced the question. Every
   Stream 3 brief before that — including the WP-E envelope Stream 2 was told to design
   against — quoted 0.22–0.27 Mpc with the same conflation. Stream 2 inherited the error from
   Stream 3.
2. **Directive E2.11, which Stream 2 correctly implemented, may itself be wrong.** It mandates
   `Δσ(A) = σ(A) − σ(0)`; because WP-E deforms its null banks too, both the null mean *and* its
   standard deviation depend on A, so Δσ differences two ratios with different denominators.
   It is under adversarial review (`briefs/DEEPTHINK_REVIEW_REQUEST_BASELINE_2026_07_26.md`
   §4.1), and WP-E3's 52 jitter-driven nonzero Δσ are a concrete instance of the artifact.
   Stream 2 did the right thing with a possibly-defective instruction.
3. **Stream 3 shipped a specification error of the same class as §2's.** The WP-E2 spec declared
   a zero-amplitude cell a "tautological-zero guard" that must show ~0 detections; it showed
   61%, and the spec was wrong, not the run. It surfaced only because the executing agent
   reported the contradiction instead of adapting to the instruction.

## 6. What Stream 3 will do differently

- **Name the operation, not just the number**, when publishing any measured scale — WP-R6 will
  be amended to state that its 0.22–0.27 Mpc figure bounds object separation and does **not**
  bound voxel size for binned statistics.
- **Publish `assert_resolvable()` as a precondition** rather than a finding
  (`pipeline/resolvability.py`), so this class of error is caught by arithmetic before anyone
  designs a grid around it.
- **Mark directives under review as such** in the consolidated index, so Stream 2 can tell a
  settled instruction from a provisional one. E2.11 is now flagged; E2.12 was drafted and
  deliberately withheld for the same reason.

## 7. Net

The scientific reasoning in iteration 3 was good and improving fast. The gap is entirely in
reference validation — a sub-minute check — and in one inherited conceptual conflation that
Stream 3 propagated first. Neither is a competence problem; both are process gaps with cheap
fixes. The Zone 2 framing is the only item Stream 3 asks be dropped outright rather than
refined.

---

`Generated-by: Claude Opus 5 (Stream 3) | Verified-by: defect persistence checked against all
three pasted iterations; missing script, existing deliverable and label substitution verified
by direct path check and by docs/WP_E_T0_AUTHORIZATION_2026_07_25.md §1; voxel figures from
pipeline/resolvability.py cross-checked against docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md
§5.1; Stream 3's own three failures each traced to a committed artifact |
Reviewed-by: T0 N — pending Xavier`
