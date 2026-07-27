# D0 Verification — Low-Tier Agent Execution Plan

**Date:** 2026-07-27
**Stream:** 3 (Experimentation & Pre-Registration)
**Purpose:** Clear the D0 gate that blocks WP-E6 Acceleration Directives 1–5.
**Tiering rule (per CLAUDE.md / session policy):** mechanical + verifiable → Haiku; judgment-bearing → Sonnet; delicate/epistemic → Opus (not used here).

---

## Why D0 exists

The WP-E6 Acceleration Manifesto names specific GitHub repos as drop-in dependencies
(`brian-i/sweeps`, `Jiaxi-Yu/modelling_spectro_sys`, `CobayaSampler/bao_data`, `desihub/*`)
and assumes a **pre-trained mixed-(m,f) FDM emulator exists**.

Neither claim has been independently verified. Both originated in a synthesis document, not a
primary source check. Adopting an unverified or misdescribed dependency is precisely the class of
defect that fails T0 adversarial review *after* engineering time is spent.

**D0 converts assumptions into checked facts before any integration work begins.**

---

## Token-optimization rules (apply to ALL agents)

These are binding. They exist because agent cost is the live constraint this session.

1. **Do NOT read `/home/callensxavier_gmail_com/literature_review/` in bulk.** It is ~35k words of
   synthesis, and it is the very thing being audited — reading it back in is circular AND expensive.
   Read at most ONE named file if explicitly told to.
2. **Hard cap on web calls** — stated per agent below. Stop at the cap and report what you have.
3. **Write findings to your output file as you go.** Do not accumulate a giant final message.
4. **Final reply to coordinator: ≤ 200 words.** The file is the deliverable, not the chat message.
5. **No speculation.** If you cannot verify something within budget, the verdict is
   `UNVERIFIED` — never `PROBABLY EXISTS`. `UNVERIFIED` is a valid, useful, honest outcome.
6. **Read-only.** No commits, no pushes, no dependency installs, no repo mutation outside your
   own output file.

---

## Agent D0-A — Tooling repo verification

- **Tier:** Haiku (mechanical lookup, binary verdicts)
- **Web budget:** ≤ 12 fetch/search calls total
- **Output:** `briefs/D0_VERIFICATION/D0A_TOOLING_REPOS.md`

### Scope (exactly these 5 targets, nothing more)

| # | Target | Claim under test |
|---|--------|------------------|
| 1 | `brian-i/sweeps` | Exists; is a parallel parameter-sweep framework with JSON config |
| 2 | `Jiaxi-Yu/modelling_spectro_sys` | Exists; injects DESI spectroscopic systematics into mocks |
| 3 | `CobayaSampler/bao_data` | Exists; ships DESI **DR1** likelihood + covariance (not DR2/mock-only) |
| 4 | `desihub/desisim` | Exists; can generate synthetic Lyα spectra |
| 5 | `desihub/desispec` | Exists; is the spectroscopic reduction pipeline |

### Definition of Done

Output file contains, for each of the 5 targets, a row with **every** field populated:

- `VERDICT`: one of `CONFIRMED` / `EXISTS_BUT_MISDESCRIBED` / `NOT_FOUND` / `UNVERIFIED`
- `URL`: canonical URL actually resolved (or `n/a`)
- `LAST_COMMIT`: date, or `unknown`
- `STARS`: count, or `unknown`
- `ACTUAL_PURPOSE`: one line, from the repo's own README — **not** from the manifesto
- `FIT_FOR_CLAIMED_USE`: `yes` / `no` / `partial` + one-line reason
- `EVIDENCE`: the URL or snippet that justifies the verdict

Plus a **`## Fallbacks`** section: for every target NOT `CONFIRMED`, name a real, verified
alternative (e.g. if `brian-i/sweeps` is absent → `joblib.Parallel` / `multiprocessing.Pool` /
`snakemake`), or state `no fallback needed`.

### Validation (how the coordinator checks this agent)

- Any `CONFIRMED` row must carry a resolving URL in `EVIDENCE`. A verdict without evidence is rejected.
- `ACTUAL_PURPOSE` must NOT be a paraphrase of the claim in the table above — that would indicate
  the agent confirmed the claim by restating it rather than by reading the repo.
- Coordinator spot-checks 2 of 5 URLs by hand.

### Stop conditions

- Hit 12 web calls → write up what you have, mark the rest `UNVERIFIED`, stop.
- A target 404s → verdict `NOT_FOUND`, move on immediately. Do not hunt for similarly-named repos
  beyond one single search.

---

## Agent D0-B — Q1 emulator re-survey

- **Tier:** Sonnet (requires judgment: "does this emulator actually span mixed (m,f)?")
- **Web budget:** ≤ 18 fetch/search calls total
- **Output:** `briefs/D0_VERIFICATION/D0B_EMULATOR_Q1.md`

### Scope

Answer ONE question: **Does a publicly obtainable flux-power (P₁D) emulator span mixed
fuzzy-dark-matter parameter space — i.e. both axion mass m_φ AND FDM mass fraction f_FDM
as free parameters?**

Prior finding to re-test (from `WP_E6_V2_PROPOSAL_LYA_P1D_2026_07_27.md`): **NO** — because
LaCE / cup1d / lym1d are ΛCDM-shaped; axionCAMB fixes only the linear transfer function;
axionHMcode targets the wrong observable and is calibrated only near 1e-21 eV; and the
Liu/Gong/Zhou 2026 emulator had no code release found.

You are re-testing that finding, not assuming it. It may have changed; it may have been wrong.

### Definition of Done

Output file contains:

1. **Headline verdict**, one of:
   - `EMULATOR_AVAILABLE` — with repo/DOI + install path + evidence it spans BOTH m_φ and f_FDM
   - `PARTIAL` — something covers pure-FDM or fixed-f only; state precisely what is missing
   - `CONFIRMED_ABSENT` — prior finding re-validated; Option B (custom build) is the live path
2. **Per-candidate table** (LaCE, cup1d, lym1d, axionCAMB, axionHMcode, Liu/Gong/Zhou 2026,
   + any new candidate found) with columns:
   `candidate | code public? | observable | m_φ free? | f_FDM free? | verdict | evidence URL`
3. **The f_FDM column is the decisive one.** An emulator with m_φ free but f_FDM fixed at 1
   (pure FDM) does NOT satisfy the requirement. Say so explicitly.
4. **If `CONFIRMED_ABSENT`:** a short Option-B costing — how many hydro sims, which existing
   sim suite could seed it, rough wall-clock. 5 lines max, clearly labelled an estimate.

### Validation

- Verdict must be justified by a **primary source** (repo, paper, Zenodo/DOI) — never by a
  secondary summary or by this project's own documents.
- If `EMULATOR_AVAILABLE`, the coordinator will independently open the link before acting on it,
  because this verdict alone would unblock ~2–3 weeks of otherwise-necessary work.
- Author-contact is **NOT authorized** (CLAUDE.md rule 4: public products only). If the only route
  to a code release is emailing authors, the verdict is `CONFIRMED_ABSENT` with that noted as a
  T0-overridable item.

### Stop conditions

- 18 web calls → write up, stop.
- Found a clearly `EMULATOR_AVAILABLE` case with both parameters free → stop early, report it.
  Do not keep surveying; the question is answered.

---

## Agent D0-C — Local environment & dependency audit

- **Tier:** Haiku (pure mechanical local inspection)
- **Web budget:** ZERO. No network calls at all.
- **Output:** `briefs/D0_VERIFICATION/D0C_ENV_AUDIT.md`

### Scope

Inventory what the Stream 3 environment already has, so the manifesto's
"update requirements.txt" step is based on fact rather than guesswork.

Repo root: `/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home`

Check and report:
1. Python version; whether a project venv exists (and where) vs system python
2. Installed / not-installed for: `numpy scipy matplotlib astropy h5py pandas pyvo
   cobaya iminuit scikit-learn celerite corner emcee getdist`
3. Existing `requirements.txt` / `pyproject.toml` / `environment.yml` — path + current contents
4. Free disk on `/mnt/disks/disk-socrateai-local-1` (the 500 GB data disk) and confirm
   `data/raw` is still a symlink pointing there
5. Whether the existing test suite still passes — run it, report the count, do not fix anything
6. `git status` cleanliness + current branch + whether local is ahead of origin

### Definition of Done

Output file contains:
- A `HAVE / MISSING` table for every package listed above (no blanks)
- The exact `pip install` line needed to close the gap — one line, copy-pasteable
- Test suite result as `N passed / M failed` (if it fails, paste the first failing test name only)
- Disk free in GB, and symlink target confirmed or flagged broken
- `git status` summary — clean/dirty, branch, ahead/behind

### Validation

- Every package row must show HAVE or MISSING — never blank, never "probably".
- Test count must be a real number from a real run. If the suite cannot be run, say why in one
  line; do not estimate or infer from a previous session's numbers.
- **Do NOT install anything.** Report the gap; installation is a separate, human-approved step.

### Stop conditions

- Test suite runs > 10 minutes → kill it, report `TIMEOUT`, continue with the rest.

---

## Coordinator gate — what happens after D0

| D0 outcome | Consequence |
|---|---|
| D0-A: `brian-i/sweeps` NOT_FOUND | Directive 2 → plain `joblib`/`multiprocessing` fallback. No blocker. |
| D0-A: `modelling_spectro_sys` NOT_FOUND | Directive 1 systematics injection → hand-rolled from DESI instrument docs. Adds ~3 days. |
| D0-A: `bao_data` lacks DR1 P1D | Directive 3 → build covariance from mock ensembles as originally planned. |

### Coordinator correction (post-D0-A, spot-checked 2026-07-27)

D0-A marked `CobayaSampler/bao_data` **CONFIRMED / FIT_FOR_CLAIMED_USE: yes**. Coordinator spot-check
(`gh api repos/CobayaSampler/bao_data/contents`) shows the Lyα files present are
`desi_2024_gaussian_bao_Lya_GCcomb_{mean,cov}.txt` — a **compressed Gaussian BAO distance summary**
(D_M/r_d, D_H/r_d + a small covariance), identical in kind to the LRG/QSO/ELG/BGS files in the same
repo. This is the BAO peak-position fit result, **not** the flux-power spectrum P₁D(k) across k-bins
that the mixed-(m,f) FDM sweep needs.

**Row 3 verdict downgraded: CONFIRMED → PARTIAL.** The repo is real and does ship DESI DR1 Lyα data,
but not the observable Directive 3 requires. Treat `bao_data` as useful only for a downstream
BAO-consistency cross-check, not as the primary covariance source for the P₁D sweep. Directive 3's
covariance must still be built from mocks (`desisim`, confirmed real) or sourced from the DESI DR1
Lyα P1D measurement paper directly (separate from this repo) — same fallback as if `bao_data` had
been NOT_FOUND.
| D0-B: `CONFIRMED_ABSENT` | **Q1 answered.** Escalate to T0: authorize Option B custom emulator build (~2–3 wks). Directive 4 is NOT a drop-in. |
| D0-B: `EMULATOR_AVAILABLE` | **Major unblock.** Coordinator verifies link personally, then Phase 1 fast-tracks to ~1 week. |
| D0-C: heavy gaps | Single approved `pip install` line, then proceed. |

**Directive 5 (SBPs / ShapeFit) stays deferred regardless** — it compresses and decorrelates around
a P₁D model that does not exist until Directive 4 resolves. Sequencing it earlier would be
optimizing a model that isn't there yet.

---

## D0 CLOSED — 2026-07-27, consolidated verdict

All three agents completed; coordinator independently re-verified D0-A's row 3 and the entirety of
D0-B's headline finding (see corrections above and commentary below).

| Sub-gate | Verdict | Consequence |
|---|---|---|
| D0-A tooling repos | 4/5 CONFIRMED, 1 downgraded to PARTIAL (`bao_data`: real DR1 Lyα data, but BAO-distance summary, not P1D(k)) | Directives 1, 2 unblocked as designed. Directive 3 covariance must come from `desisim` mocks or the DESI Lyα P1D paper directly, not `bao_data`. |
| D0-B Q1 emulator | **EMULATOR_AVAILABLE** (coordinator-independently verified: arXiv:2606.06969 real, `github.com/jianxiangl-astro/lya-mfdm` real+public+trained weights present) | **Major unblock.** Directive 4 is a real integration task (~1 week), not a 2–3 week custom build. Q1 is CLOSED. |
| D0-C local environment | 8/14 target packages present; 6 missing (`h5py getdist iminuit cobaya scikit-learn celerite`); test suite 427/427 green; disk 418GB free; `data/raw` symlink valid+populated; git: main branch, 4 local commits ahead of origin, clean otherwise | One approved `pip install h5py getdist iminuit cobaya scikit-learn celerite` closes the gap. No installs run yet — human-approved step. |

**Still open before Phase 1 can fully proceed:**
1. Approve and run the D0-C install line (not yet executed — D0-C was read-only per spec)
2. Verify the `lya-mfdm` emulator actually loads/runs and its calibration domain (z=5.0/4.6/4.2,
   the trained mass/fraction grid) covers what DESI z≈2.2–4.4 needs — this was explicitly out of
   D0-B's scope and is real Phase-1 risk, not a formality
3. No LICENSE file was visible on `lya-mfdm` — check before any redistribution/derivative use
4. 4 local commits sitting unpushed on Stream 3 `main` — flagged, not actioned (pushing is a
   separate, confirm-first action)

**D0 is closed.** Directives 1–4 of the WP-E6 Acceleration Manifesto are cleared to proceed once
the Phase-1 items above are handled. Directive 5 (SBP/ShapeFit) stays deferred per original design.

---

## What D0 explicitly does NOT do

- Does not install packages
- Does not clone any repo
- Does not commit or push
- Does not touch `PREDICTION.md` (pinned) or `K3_CRITERIA.md` (a real but UNRELATED file -- K3 geometric selection criteria, not a physics parameter grid; see correction note 2026-07-27 evening)
- Does not run any analysis, sweep, or fit
- Does not contact any external author

D0 is verification only. Every one of the above is a separate, gated, human-approved step.
