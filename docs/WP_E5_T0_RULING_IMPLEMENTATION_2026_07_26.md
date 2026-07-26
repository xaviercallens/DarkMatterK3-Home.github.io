# WP-E5 — Implementation record for the T0 cross-stream consolidation (2026-07-26)

**Date:** 2026-07-26
**From:** Stream 3, implementing the "CROSS-STREAM CONSOLIDATION: T0 Rulings, Stream 3
Answers, and WP-E Execution Protocol" directive (Xavier, T0, pasted in-session).
**Triage status (D-3):** every artifact and claim in the directive checked against this
repo before execution. Adopted with **one ruling held for T0 re-decision** (§1) and
**four documented deviations** (§3), each with its measured reason.

---

## 1. Ruling 1 (annotate PREDICTION.md) — HELD, not executed. The premise is mechanically false here.

The ruling authorizes adding `[RETRACTED: E-007, see NO_PREDICTION_BRANCH.md]` next to the
ρ=4/T=18 claim, on the stated premise that *"altering the text explicitly warns readers
without invalidating the cryptographic hashes of the pre-registration methodology."*

**Measured facts, this repo, this session:**

1. `pipeline/gate.py::verify_pin_hash()` computes SHA-256 over the **entire document body**
   with only the `PINNED:`/`DERIVED:` header lines stripped (`_strip_header_lines`,
   gate.py:68–80). **Any** body edit — including a one-word annotation — changes the hash,
   `verify_pin_hash()` returns `False`, and **G1 closes**: `require_pinned_for_real_data()`
   raises, and the gate test suite fails. The premise "without invalidating the hashes" is
   false for this repo's mechanism. (There is also no git hook enforcing immutability —
   `.git/hooks/` is empty of live hooks — so nothing would even warn before the breakage;
   the pin's only guardian is the hash check itself.)
2. The claim sits at **line 51** here (`✅ C1 Kodaira classification complete (ρ=4, T=18
   confirmed)`), not line 49 — line numbers drifted across repos again.
3. **An in-band retraction already exists inside the pinned body**, at line 151:
   *"Blocker before any lattice-dependent step: correct C1/C2 recompute for the A279619
   partner (F6 — the previous ρ=4/T=18 is retracted)."* It was present at pin time (the pin
   verifies `True` today), so the document already discharges the epistemic duty the ruling
   targets — a reader of the pinned text encounters the retraction in the section that
   governs use of the value.

**Disposition:** the intent of Ruling 1 is already satisfied in-band at line 151; executing
the edit at line 51 would close G1 as a side effect the ruling explicitly did not intend.
Held for T0 with two executable variants, pick either or neither:

- **(a) Annotate + re-hash in one commit** — the annotation is added and the `PINNED:`
  header is recomputed over the annotated body, with this document recording that the diff
  is the one-line annotation and nothing else (git shows it). This is mechanically a
  re-pin, which Ruling 1 forbids as worded; it needs an explicit "re-hash authorized" from
  you.
- **(b) Leave the body untouched** — line 151 already carries the in-band retraction;
  optionally strengthen discoverability outside the hashed body (e.g. a reader note in
  `NO_PREDICTION_BRANCH.md`, already cross-referenced).

Stream 3 default until countermanded: **(b)**. No edit has been made; `verify_pin_hash()`
remains `True`.

## 2. Rulings 2 and 3 — adopted as written

- **D-3 dead, GPU budget → WP-E:** already the operative state (`_evaluate_sector` was
  de-fabricated in WP-T3; `run_batch()` remains gated; no verdicts exist — confirmed by
  `find` across repo and external disk). Nothing further to do.
- **E-011 (ρ ≤ 19, T ≥ 3) accepted as [B] pending Stienstra–Beukers 1985, emitting no
  prior:** matches this repo's standing behaviour — `D3_batch_runner_phase2` reports
  ρ/T as honest `NaN`; F-AUD-1 remains open. This also resolves §3(d) of
  `briefs/STREAM3_TO_STREAM2_DIRECTIVE_RESPONSE_2026_07_26.md`: the operative status is
  **[B]-pending-citation, no prior emitted** — superseding Stream 2's scoreboard line
  ("DERIVED [B] … independently reproduced") *and* consistent with Stream 1's UNRESOLVED
  warning. One ruling now exists; both streams should cite it.

## 3. The revised WP-E protocol — adopted, with four documented deviations

The protocol's structure is accepted in full: data-kind branching (D-5), Phase 0 baseline
gate (fix 3), Phase 1 closure/null with assert-FAIL semantics (D-1/S3-02), Phase 2
baseline-subtracted sweep, Phase 3 zones. Deviations, each measured:

| # | Directive says | Implemented as | Measured reason |
|---|---|---|---|
| 1 | Thin slices **Δz = 0.01** | `--dz` parameter; **both** Δz = 0.01 and Δz = 0.20 run and reported side by side | σ_z at the field's median z (1.39) is **0.119** — Δz = 0.01 is **12× finer than the photo-z error kernel**, the exact trap the directive's own §3 names; and a Δz = 0.01 slice of `edf_north` holds **≤ 25 objects** (topologically empty). Δz = 0.20 reaches ~196 objects. |
| 2 | Deliverable is `docs/WP_E_EMPIRICAL_BOUNDS.md` | `docs/WP_E_EMPIRICAL_BOUNDS_2D_2026_07_26.md`, cross-linked | The original is a **complete, T0-signed artifact** of the 3D study. Overwriting a signed record — even under T0 authority — destroys the audit trail; adjacency preserves both. |
| 3 | Zone 2 named "**Falsified**" | `ZONE_2_GENERIC_DEFORMATION_EXCLUDED`, with an explicit note | `T(r_s, α)` is a generic warp, not K3-derived (WP-E §8; WP-E2 triage §3.1). A generic deformation conflicting with data excludes **that warp**, not any vacuum. The zone semantics are unchanged; only the claim's scope is stated honestly. |
| 4 | §5 commands: `wpe_preflight_baseline.py --mock lCDM_angular_mock.fits --real euclid_q1_photoz_slice.fits` | Same script names, real arguments | **Neither .fits file exists** anywhere in this repo or the external disk; the data here are CSV catalogues (Euclid PDR `euclid_z_edf_*`, not "Q1"). 7th occurrence of the referenced-artifact pattern; per D-3 the gap is reported and the scripts are built against the artifacts that exist. |

One statistic correction inside the protocol, from its own §5: Phase 0/2 prose says β₂,
but **there is no β₂ in 2D** — the 2D observable set is β₀ (components) and β₁
(loops/voids-in-projection). The directive's own execution command already says
`--observable betti_1_2D`; the implementation follows the command.

## 4. What is being built (WP-E5, in flight at time of writing)

- `pipeline/topology2d.py` — 2D Betti numbers with an **independent** cubical Euler
  characteristic asserted equal to β₀ − β₁ on every call; 12 hand-computed golden tests
  green.
- `pipeline/transverse.py` — slice selection, fixed-grid 2D projection, transverse-Mpc
  conversion, 2D resolvability check, matched 2D mocks.
- `scripts/wpe_preflight_baseline.py` (Phase 0), `scripts/wpe_closure_tests.py` (Phase 1,
  with negative controls that exit nonzero on failure), `scripts/wpe_transverse_sweep.py`
  (Phases 2–3, gated on Phase 0's persisted GO). All results persisted to
  `data/derived/wp_e5_*.json` **before** any summary is printed — the JSON is the
  artifact, the print is a convenience (lesson of WP-E3's lost run and wrong printed
  verdict).

Prior 3D pre-flight note: `data/derived/wp_e_preflight_mock_data_sigma_2026_07_26.json`
returned **NO-GO** for the 3D β₂ framing (statistic degenerate, σ undefined at 2 of 3
thresholds). That NO-GO applies to the *3D* framing this directive supersedes for photo-z
fields; the 2D framing gets its own Phase 0 verdict and inherits nothing.

---

`Generated-by: Claude Fable 5 (Stream 3) | Verified-by: §1 facts executed this session
(verify_pin_hash source read at gate.py:68–104, pin currently True, line numbers from grep,
.git/hooks listing); §3 deviation 1 from the measured z-distribution (n=1983, med z 1.39,
max dz=0.01 slice = 25 objects); deviation 4 by find across repo and external disk |
Reviewed-by: T0 N — §1 explicitly awaits Xavier's pick of (a)/(b); countermand window open
on all four deviations`
