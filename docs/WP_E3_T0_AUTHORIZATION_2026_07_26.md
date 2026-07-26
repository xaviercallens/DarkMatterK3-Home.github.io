# WP-E3 — T0 Authorization Record

**Date:** 2026-07-26
**Authority:** Xavier Callens (T0 Owner), confirmed directly in session
("I provide you authority continue on that path"), in response to the single
escalation in `briefs/STREAM3_WPE2_TRIAGE_AND_DIRECTIVES_2026_07_26.md` §7.
Same in-session delegation pattern as `docs/WP_E_T0_AUTHORIZATION_2026_07_25.md`
and `ASSUMPTIONS.md` v2.0.

---

## 1. What was escalated, and what is therefore authorized

§7 of the WP-E2 triage brief requested exactly one decision: whether Stream 3 may
apply the **third null scheme (density-shuffle)** to the **real** `euclid_z_edf_north`
field, directly re-testing the window WP-E published, rather than only to a synthetic
analogue. Stream 3 declined to self-authorize it because it touches real data.

**Authorized (WP-E3):** a real-data, third-scheme robustness re-test of WP-E's published
candidate window, tagged **`SANDBOX-EXPERIMENTAL`** (`EXECUTION_PLAN.md` §4.1 — the
existing label for real-data-touching exploratory work that is never `TEST`/`FIT`),
delivered to a **new** document, `docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md`.

## 2. What this authorization does **not** cover

Recorded explicitly so scope creep cannot later be attributed to this ruling. Each item
was declined in the WP-E2 triage for a reason that authority does not dissolve:

1. **Off-Ramp 3 stays closed.** The Mpc-scale chameleon premise contradicts an adjudicated
   two-model finding (`NO_PREDICTION_BRANCH.md` §8.5, gap G-1 CLOSED-NEGATIVE: mediator
   range never exceeds ~30 μm at any density). CLAUDE.md rule 5 requires a **written T0
   ruling** to override a falsification trigger; "continue on that path" is authorization
   for the escalated re-test, not such a ruling. WP-E3 makes no chameleon-scale claim.
2. **No `TEST`/`FIT` labels.** Gate G1-L is closed and mechanically enforced
   (`pipeline/gate.py`); this authorization does not touch it and cannot.
3. **No overwrite of `docs/WP_E_EMPIRICAL_BOUNDS.md`.** That artifact is complete and
   T0-signed. WP-E3 is additive and cites it.
4. **No new output label.** The re-pasted protocol's `[SYNTHETIC-BOUNDING]` remains
   unused; `SANDBOX-EXPERIMENTAL` is the authorized tag, as T0 already decided on
   2026-07-25.
5. **No new data acquisition.** WP-E3 uses only the already-manifested
   `euclid_z_edf_north` catalogue, verified by checksum before use (see §3).
6. **No falsification framing.** WP-E3 may report that a window does or does not survive
   a third null scheme. It may not report any mechanism or vacuum as falsified — the
   deformation classes are generic stand-ins, not derived from the K3 mathematics
   (WP-E's own §8, and WP-E2 triage §3.1).

## 3. Pre-execution data verification (performed before this record was written)

| Item | Value |
|---|---|
| Catalogue | `euclid_z_edf_north` (Euclid public MER ⋈ phz_photo_z, PDR live query 2026-07-25) |
| Path | `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_north.csv` |
| Rows | 2000 (+1 header) |
| SHA256 (recomputed this session) | `8b5b287f3f03165660e6232b904ee264e705788ffd60e67f54169ea2dddac2be` |
| SHA256 (`data/MANIFEST.md`) | `8b5b287f3f03165660e6232b904ee264e705788ffd60e67f54169ea2dddac2be` |
| Match | ✅ exact — data is unmodified since acquisition |

## 4. Scientific scope of WP-E3 (what it will actually compute)

Reading `scripts/wp_e_gpu_sandbox.py` to specify a faithful re-test surfaced a
methodological detail that WP-E's own report does not foreground, and which makes this
re-test more informative than originally escalated:

**WP-E's `wp_r5_valid` null bank is a coin-flip *mixture*.** Per realization it draws
`rng.integers(2)` and applies **either** z-shuffle **or** angular-CSR (lines ~223–232).
So its reported σ values are computed against a bank whose spread includes
**between-scheme** variance, not only within-scheme sampling variance. That is a
defensible conservative choice, but it is **not** the same statement as "distinguishable
from the z-shuffle null" or "…from the CSR null" — and WP-T6's finding F-SYN-1
(`briefs/STREAM3_AUDIT_DIRECTIVES_2026_07_26.md` §3) showed per-scheme verdicts can
differ *in sign*, not merely in magnitude.

WP-E3 therefore **decomposes** the comparison instead of merely adding to it:

| Null bank | Level | Question it answers |
|---|---|---|
| `mixed_r5` (reproduction of WP-E) | coordinate | reproduces WP-E's published σ as a control |
| `z_shuffle_only` | coordinate | breaks radial–angular correlation |
| `csr_only` | coordinate | breaks angular clustering at fixed radial slicing |
| `density_shuffle` (**new, the escalated addition**) | **field** | is the deformed field's topology explained by its density histogram alone? |

Density-shuffle is a *field-level* (histogram-preserving) null, whereas the other two are
*coordinate-level*; they answer different questions and are not expected to agree
a priori. That difference is the finding to report, not a defect to reconcile.

Two further compliance points, both traceable to prior defects in this repo:
- **float64 throughout.** WP-E ran float32 (`dtype=torch.float32`) and had to retract a
  finding as a float32 artifact (`docs/WP_E_EMPIRICAL_BOUNDS.md` §5). WP-E3 will not
  repeat that failure class, and will report any σ that changes materially between
  precisions.
- **Undefined σ is reported as `None`,** never coerced, when a null bank has zero variance
  (WP-R5 discipline).

## 5. Kill condition, pre-committed

If the primary window (`edf_north`, R ∈ [0.3, 4.0] Mpc) fails to survive the per-scheme
decomposition — i.e. if schemes disagree on whether it is distinguishable — the honest
output is a statement that WP-E's window is **scheme-dependent and must not be cited as a
design constraint by Stream 2's M1 memo** until the dependence is resolved. That negative
is the deliverable in that case, and directive E2.3 already anticipates it.

---

`Generated-by: Claude Opus 5 (Stream 3) | Verified-by: catalogue SHA256 recomputed against
data/MANIFEST.md this session (exact match); WP-E method read directly from
scripts/wp_e_gpu_sandbox.py lines 95–260 (mixture-null and float32 findings traced to
source, not inferred) | Reviewed-by: T0 Y (Xavier, direct in-session authorization
2026-07-26; scope limits in §2 recorded by Stream 3, countermand window open)`
