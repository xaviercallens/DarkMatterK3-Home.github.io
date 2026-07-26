# Stream 3 → T0 / Stream 2 — Correction to the project-health memo of 2026-07-26

**Date:** 2026-07-26
**From:** Stream 3.
**To:** T0 (Xavier), copy to Stream 2.
**Re:** "Overall Project Health, Theory Completion Status, and Roadmap to Finish" (2026-07-26).
**Vendored source:** `briefs/SOURCE_project_health_memo_2026_07_26.md`
SHA256 `b8b546fcedcbcb78972b5a4e08fe83e3695af0e3233c9e819871c365b21ef041`,
triaged against repo HEAD `b4e8edc` on `main`.

**Status:** the memo's Stream 3 section does not match this repo's measured state on any
operational claim. Two of its errors are load-bearing: the roadmap's Step 1 gates Steps 2
and 3, and Step 1 as specified is not a deliverable. Corrections below, each traced to a
command run this session.

---

## 1. Triage of the memo's factual claims (D-3 applied)

| # | Memo claim | Measured state of this repo |
|---|---|---|
| 1 | "The Tesla T4 GPU is running the WP-E Auto-Research Loop" | The running process is `core/t4_worker.py` — the **DarkMatter@Home citizen-science volunteer-compute worker**, dated 2026-07-14 and **removed from the git index** in `a3acf36` ("cleanup — remove legacy core/"). `grep -inE "wp_e\|wpe\|betti\|chameleon\|sweep\|empirical_bounds\|screening"` over it returns **zero hits**. `nvidia-smi` fails with "couldn't communicate with the NVIDIA driver", so `torch.cuda.is_available()` is `False` and it runs on CPU. **The app layer has been mistaken for the science pipeline.** |
| 2 | Stream 3 "Currently Executing WP-E" | **Nothing is executing.** `data/derived/wp_e5*` does not exist. WP-E5 is BUILT / NOT AUDITED / NOT RUN (`TODO.md` §WP-E5). |
| 3 | "What is left: Delivering the WP_E_EMPIRICAL_BOUNDS.md report" | **Delivered 2026-07-25** — `docs/WP_E_EMPIRICAL_BOUNDS.md`, 10,854 bytes, T0-signed. Not pending. Its §8 states in its own words that it "does not test any hypothesis". |
| 4 | Stream 3 "~50% COMPLETE" | The empirical branch reached **Off-Ramp 3 terminus** (`EXECUTION_PLAN.md:190`; G-1 CLOSED-NEGATIVE). A percentage against a closed branch reads as progress toward a result that branch cannot produce. |
| 5 | "strong evidence that the K3 surface has Transcendental Rank T=3 (ρ ≤ 19)"; "massive breakthrough" | T0's own ruling of the same date: **[B] pending Stienstra–Beukers 1985, emitting no prior** (`docs/WP_E5_T0_RULING_IMPLEMENTATION_2026_07_26.md` §2). `grep` for a ρ/T value across `pipeline/` and `checkers/` returns **nothing** — no code here emits either number. Stream 1's brief of the same date records **UNRESOLVED**, S-B 1985 unfetched. |
| 6 | "proving the s₇ symmetric-square identities … is behind us" | `K3_CRITERIA.md:17` lists K-s7 as `TBD-AT-FREEZE`, `SYM2_UNVERIFIED`, `C3B_UNVERIFIED`, status **pending**. `checkers/certificates/` holds C3/C3b certificates for **delta, alpha, eta only** — none for s7 (`C1_mirror_s7.json` is a C1, a different criterion). Separately, this repo's V5 record has **s7 rejected and s10 primary**; that conflict is an open T0 item (`TODO.md` §Blocked). |
| 7 | "With Gate G1-L open, we formally test…" | `gate.labels_unlocked()` → **`False`**, verified this session. The only defined route back is the F-LAB monitoring trigger (`TODO.md` §Awaiting). There is no "open it once the theory is ready" path in `pipeline/gate.py`. |
| 8 | "populate §6 of PREDICTION.md with these exact bounds and pin it (v1.1-PINNED)" | §6 exists and is reserved for exactly this (`## 6. Derived quantities — RESERVED (v1.1)`) — the intent is sound. But `verify_pin_hash()` computes SHA-256 over the **entire body**, so any edit closes G1. Populating §6 is mechanically a **re-pin** and needs the same explicit authorization as the still-unmade Ruling 1 (`TODO.md:10`). |

Claims 1–4 concern Stream 3's own state and Stream 3 is the authority on them. Claims 5–6
are Stream 1/2 territory; what is recorded above is only what **this** repo can and cannot
certify, which is the input Stream 3 is obliged to give before anything is built on them.

## 2. The two errors that propagate

### 2.1 The M2 mechanism routes through an adjudicated-closed mechanism

The memo's Step 2 asks Stream 2 to derive "the exact theoretical equations linking those
T=3 moduli to the Chameleon Scalar Field that suppresses void formation".

**Directive E2.2 is marked Binding** in `briefs/CROSS_STREAM_CONSOLIDATED_2026_07_26.md:56`:

> Any mechanism whose scale-setting routes through an **Mpc-scale chameleon is dead on
> arrival** and must say so in its own §1 — the ~30 μm ceiling is adjudicated, two-model,
> CLOSED-NEGATIVE (`NO_PREDICTION_BRANCH.md` §8.5).

An M2 derivation built this way would have to open by recording that its own scale-setting
is closed. This is not a veto on Stream 2's moduli work; it is a statement that the
chameleon cannot carry the scale. **Requested: either a T0 ruling reopening the ~30 μm
adjudication (with the two-model evidence that would justify it), or Step 2 rewritten
around a mechanism that does not route through it.**

### 2.2 The Step 1 "bounding box" is not a producible artifact

The memo's worked example is: *"The Chameleon screening radius r_s must be between 1.2 Mpc
and 10.0 Mpc, with a coupling strength α < 0.8, or it violates Euclid/SDSS void data."*
Two independent obstacles:

**(a) Arithmetic.** On `euclid_z_edf_north` at the nbins = 8 the WP-E series uses, the voxel
is 6.04 × 6.55 × 1023.6 Mpc (`pipeline/resolvability.py`). A displacement below the voxel
edge moves points **inside** their existing bins, leaving the binned field bit-identical and
every Betti number unchanged. r_s = 1.2 Mpc is therefore sub-voxel: 6 of the 8 proposed grid
points (75%) are UNRESOLVABLE and none is fully resolvable
(`docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md`). The radial axis cannot be recovered by
refining the grid — r_s = 1 Mpc radially would need 21,266,833 voxels for 1983 objects.

**(b) Inference.** The "or it violates Euclid/SDSS void data" clause is the Zone 2 framing
Stream 3 has asked twice be dropped rather than refined
(`briefs/STREAM3_FEEDBACK_TO_STREAM2_2026_07_26.md` §4). `T(r_s, α)` is, by the WP-E
protocol's own §2.3, a **generic spatial transformation** introduced specifically to avoid
depending on unproven theoretical parameters. A region where a generic warp conflicts with
survey data would constrain **that warp**, not a vacuum that never conjectured it. Deriving
a constraint on a model from a transformation chosen independently of it is the circularity
that ended WP-A2 (`WP_A2_CIRCULARITY_AUDIT.md`).

Supporting measurements, already on record: the 3D β₂ pre-flight returned **NO-GO** (β₂
identically zero in real data *and* mocks at 2 of 3 thresholds — σ undefined, not merely
offset; `data/derived/wp_e_preflight_mock_data_sigma_2026_07_26.json`), and WP-E's headline
6.33σ did not reproduce (2.48σ under the same mixed null bank), with raw σ crossing 3σ in
only one null bank of four and flipping sign in another
(`data/derived/wp_e3_results_2026_07_26.json`).

## 3. What Stream 3 can deliver in place of Step 1

Not a bounding box on (r_s, α). A **measurability floor**, most of which is already
computed and T0-signed:

| Quantity | Value | Source |
|---|---|---|
| Transverse floor for a binned topological statistic | **≈ 6 Mpc** at nbins = 8 | `pipeline/resolvability.py` |
| Radial sensitivity on photo-z fields | **None** (voxel 1023.6 Mpc; ~8189 Mpc comoving depth) | WP-E3 §5.1 |
| Spectroscopic alternative | `sdss_z_coma_cluster`, 50 objects, β₁ = β₂ = 0 at every resolution tested | WP-H |
| Best reachable transverse voxel, 2D projection at nbins ≈ 32–64 | **~1 Mpc**, occupancy still non-trivial | WP-E5 design |

Under **E2.17**, a mechanism whose signature is untestable is a **complete** M1/M2
deliverable, not a failure: "this mechanism would produce structure at a scale our data
cannot resolve, and here is the number" is more defensible than a Zone map computed on
unresolvable cells. The Phase M directive §1 already authorizes a reported NO with equal
prominence.

**The one genuinely open piece of Stream 3 work is WP-E5** — the 2D transverse study, which
reaches ~1 Mpc transverse voxels by abandoning radial information deliberately rather than
by accident. It is built and unaudited; its Phase 0 verdict, GO or NO-GO, is the next real
artifact this stream can produce.

## 4. Requests to T0

| # | Request | Why it blocks |
|---|---|---|
| R-1 | **Rule on E2.2 vs. Step 2** — reopen the ~30 μm chameleon adjudication, or redirect Step 2 to a mechanism whose scale-setting survives it. | Stream 2 is reportedly days from an M2 derivation that E2.2 requires be rejected on arrival. Highest-cost item here. |
| R-2 | **Withdraw or restate Step 1.** Stream 3 cannot produce an (r_s, α) bounding box; it can produce the §3 measurability floor. Steps 2 and 3 both gate on this. | §2.2 |
| R-3 | **Ruling 1 variant pick** (a) annotate + re-hash or (b) leave body untouched — and note that the memo's §6 population is the *same* decision at larger scope. | `TODO.md:10`; §1 claim 8 |
| R-4 | **s7-vs-s10 ruling.** The memo treats s7 as settled and load-bearing; this repo has it rejected, uncertified for C3/C3b, with s10 primary. | `TODO.md`; §1 claim 6 |
| R-5 | **Confirm the ρ/T status line** all three streams cite: [B]-pending-S-B-1985, no prior emitted. Three different statuses are currently in circulation. | §1 claim 5 |

## 5. What is not in dispute

The memo's account of the **guardrails** is accurate and worth preserving: the E-007
retraction, the E-010/E-012 hallucinated-pipeline defect, and the photometric-3D illusion
were each caught before they reached a result, by the two-model rule and adversarial review.
Stream 3's own contribution to that record includes three self-reported failures
(`briefs/STREAM3_FEEDBACK_TO_STREAM2_2026_07_26.md` §5). The corrections above are that same
process operating one step earlier, on a summary rather than on a result — which is where
`epistemic-guardrails` Finding F-A locates the highest concentration of tier violations.

---

`Generated-by: Claude Opus 5 (Stream 3) | Verified-by: gate state via pipeline.gate
(verify_pin_hash True, labels_unlocked False) this session; claim 1 by ps/nvidia-smi/grep over
core/t4_worker.py and git ls-files (untracked); claim 2 by ls data/derived/; claim 3 by ls -la
docs/WP_E_EMPIRICAL_BOUNDS.md; claims 5-6 by grep over pipeline+checkers and ls
checkers/certificates/ and K3_CRITERIA.md:17; claim 8 by PREDICTION.md heading grep; §2.2
voxel figures from pipeline/resolvability.py cross-checked against
docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md §5.1; source vendored via
pipeline.triage.vendor_source | Reviewed-by: T0 N — pending Xavier; §4 is five open requests`
