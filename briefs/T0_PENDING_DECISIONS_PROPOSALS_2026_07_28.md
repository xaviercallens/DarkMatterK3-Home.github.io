# T0 Pending Decisions — Proposals & Rationales (2026-07-28)

**Status:** DECISION-REQUEST (no action taken on any item below without T0 sign-off)
**Scope:** everything still awaiting a T0 call after today's two ratifications
(S2 `256017d`: G0→LIVE + G1 Route A opened; S3 `7d0b2ce`: ANALYSIS_PROTOCOL→LIVE).
Those two are **done** and are not re-argued here.

Each item: the decision, the proposal, the rationale, and what happens on approval.

---

## D1. Grid countermand window — close it

**Decision needed:** the 56-cell WP-E6 grid (S3 `27cff4a`, T0-delegated with an explicit
countermand window) has stood unamended since 2026-07-27. Formally close the window or amend.

**Proposal: CLOSE the window; the grid stands as pinned.**

**Rationale:**
- All three built-in controls pass (`data/derived/wp_e6_grid_controls_report_2026_07_28.json`,
  S3 `20c9494`): f=0 column byte-identical across all 8 masses (max|diff| = 0.0); m=−19.1
  null row max deviation 1.72%, well under the 10% defect threshold; mass-contrast positive
  control shows a 35× suppression ratio, so the null-row result is a real recovery, not vacuous.
- Every cell sits inside the emulator's verified trained support (grid anchor commit message,
  `27cff4a`).
- Two sessions of downstream design work (grid controls, ANALYSIS_PROTOCOL) surfaced no reason
  to amend. Leaving the window open indefinitely adds ambiguity with no remaining upside.

**On approval:** one-line countermand-log entry in the grid file marking the window CLOSED;
no other change.

---

## D2. Paper `PLAN.md` §5 — five sub-decisions (Stream 1, `paper/PLAN.md`)

### D2.1 Scope: Option A vs B (§1.3)

**Proposal: Option A** — one paper, lattice/monodromy material included as the
clearly-labeled numerically-supported + conditional sections (§6, §8).

**Rationale:** the plan's own verdict (§1.2) is that no single ingredient carries a paper
alone; the assembled package is the contribution. Option B removes the doubly-verified
U⊕⟨14⟩ identification — the program's strongest novel computational content — and defers it
to a paper 2 with no current route to making the recognition step exact. The section files
are already organized so that falling back to B later (drop `06-lattice.tex` +
`08-dolgachev-doran.tex`) is cheap if referees force it; the reverse migration is not.
Choosing A now keeps the option-B exit open.

### D2.2 Venue

**Proposal: Experimental Mathematics**, per the plan's own §2 ranking.

**Rationale:** the paper's genre — exact computation + numerical recognition + formal
verification with full disclosure — is that journal's core identity, and the Gorodetsky
template paper (the paper's central citation) is published there. JSC only fits the
Option-B scope; ITP/CPP is a different (formalization-led) paper and is preserved as a
possible second publication seeded by §9.

### D2.3 Authorship & AI-acknowledgment wording

**Proposal:** sole author Xavier Callens, affiliation "Independent Researcher"; a dedicated
acknowledgment paragraph stating that computations, drafting, and verification tooling were
AI-assisted (naming the model families), that every claim traces to a named public artifact
(Lean file, checker certificate, or pinned reference), and that all mathematical claims were
verified by the named mechanical checkers rather than taken from model output.

**Rationale:** matches the paper's already-built claims-inventory discipline (§3) and current
journal norms of explicit AI-use disclosure; "Independent Researcher" resolves the empty
affiliation on the masthead without waiting. **This is the most T0-personal item in this
brief** — the proposal is a default to edit, not a recommendation to accept verbatim.
Final wording is yours.

### D2.4 ρ = 19 / T = 3 presentation (§8)

**Proposal: keep as a conditional proposition** (current draft), not demoted to a remark.

**Rationale:** the result is Tier B — derived (E-011, Zarhin route), independently
re-derived via the Nikulin complement (NS rank 19, S2 G0 certificate, now LIVE) — with its
conditionality (A–vS model's PF operator being L₃, very-general-member caveat) stated in the
hypotheses. A proposition with explicit hypotheses is both more honest and more citable than
a remark, and the tier discipline is exactly what the paper is selling. Demoting it would
understate a result the program has now verified by two independent routes.

### D2.5 Internal manuscript citation

**Proposal: cite it explicitly** as an unpublished internal report (title, year, repo +
commit hash), rather than folding §9's dependence in silently.

**Rationale:** provenance honesty is cheaper than the alternative — silent reuse invites a
self-plagiarism question at review, and a hash-pinned citation matches how every other
artifact in the claims inventory is sourced.

---

## D3. WP-E7 eBOSS LRG catalog: Option A vs B (S3, investigation brief `159b58c`)

**Decision needed:** which DR16 catalog is WP-E7's primary LRG sample — now a clean choice,
not a mystery (see `WP_E7_EBOSS_LRG_SAMPLE_IDENTITY_INVESTIGATION_2026_07_28.md` §4).

**Proposal: Option A** — fetch the SDSS-recommended combined LRGpCMASS sample
(377,458 rows, 9,493 deg²) as primary; keep the already-fetched eBOSS-only files
(174,816 rows, 4,242 deg²) as a documented secondary/cross-check sample.

**Rationale:**
- WP-E7's own preflight (`docs/WP_E7_DESI_RESOLVABILITY_PREFLIGHT_2026_07_27.md`) frames the
  purpose as z>0.6 clustering resolvability — exactly the use for which SDSS's DR16
  documentation explicitly recommends LRGpCMASS "in place of the z>0.6 bin from BOSS."
- It is the larger, higher-density sample, and the fetch script's own comment already
  intended it (the mismatch was a filename bug, not a design choice).
- Keeping the eBOSS-only files as a labeled secondary preserves Option B's isolation
  use-case at zero cost.

**On approval:** fetch the four `eBOSS_LRGpCMASS_clustering_{data,random}-{NGC,SGC}-vDR16.fits`
files via `scripts/fetch_data.py` (manifest updated per protocol), fix the
`EBOSS_LRG_FILES` dict + comment in `scripts/data_fetchers.py`, and relabel the eBOSS-only
entries as secondary in `data/MANIFEST.md`. WP-E7 occupancy ratification then proceeds on
the combined sample.

---

## D4. Standing non-science item (not a T0 gate, listed for completeness)

**GitHub token audit — browser-only, Xavier.** Two broad-scope classic PATs are live; the
old `.bashrc` token was replaced locally today but is still valid server-side, and the
replacement was itself exposed in transit. Full sweep at github.com/settings/tokens:
revoke everything not in active use; consider a fine-grained PAT for the three repos.
No repo action possible from this side.

---

## Not pending (for the record)

- **S2 G1 Route A** — opened today (`256017d`); execution of G1-a is the next S2 work item,
  no further decision needed to start.
- **S3 ANALYSIS_PROTOCOL** — LIVE (`7d0b2ce`); desisim N=50 timing run and Part C masking
  fix are authorized, no further decision needed to start.

---
Generated-by: Fable 5 (coordinator session 2026-07-28) | Verified-by: every number and
option traced to the named source document this session (grid controls report, WP-E7
investigation brief §2c/§4, paper PLAN.md §§1–5, T0 decision records) | Reviewed-by: T0 N (this document is the review request)
