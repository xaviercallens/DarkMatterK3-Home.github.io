# refs/ — Cited Literature and Measured-Value Files

**Status:** First transcription pass complete (2026-07-17). This directory is the
only admissible source for literature values in this program (`epistemic-guardrails`
rule 5: no numbers from memory). Every entry below was **fetched from its source and
verified from the fetched content itself** — titles/authors read off the retrieved
documents, sequence values cross-checked against independent in-repo closed forms —
never transcribed from a model's recall.

## Manifest

| # | File | Source (verified from fetched content) | SHA256 | Retrieved | Verification |
|---|---|---|---|---|---|
| 1 | `oeis/b005260.txt` | OEIS A005260 b-file, https://oeis.org/A005260/b005260.txt | `6f8e3d990b77368f…` (full hash in cert) | 2026-07-17 | **PASS(all)** — 835/835 terms (n=0..834) match a(n)=Σₖ C(n,k)⁴ recomputed exactly; see `oeis/VERIFICATION_CERTIFICATE.json` |
| 2 | `oeis/b183204.txt` | OEIS A183204 b-file, https://oeis.org/A183204/b183204.txt | in cert | 2026-07-17 | **PASS(all)** — 703/703 terms match the Zudilin closed form Σⱼ C(n,j)²C(2j,n)C(j+n,j) |
| 3 | `oeis/b276536.txt` | OEIS A276536 b-file, https://oeis.org/A276536/b276536.txt | in cert | 2026-07-17 | **PASS(all)** — 555/555 terms match Σₖ C(n,k)C(2k,k)³ |
| 4 | `oeis/A005260.json`, `oeis/A183204.json`, `oeis/A276536.json` | OEIS entry records (JSON), oeis.org search API | (committed content is the record) | 2026-07-17 | Carry the formal definitions and the Cooper (2012) citation used below |
| 5 | `papers/AESZ_tables_calabi_yau_equations_math0507430.pdf` | Almkvist, van Enckevort, van Straten, Zudilin, *Tables of Calabi–Yau equations*, arXiv:math/0507430**v2** (9 Oct 2010), 130 pp. — title/authors/version verified from the fetched PDF's page 1 | `3230b365d75df8b546f1c0f3d89ec53a78cdb6b5d15873525b735a78da0b251d` | 2026-07-17 | Identity verified visually from page 1; content not yet transcribed into machine-readable form (that is per-use work, done criterion-by-criterion) |
| 6 | `papers/Gorodetsky_sporadic_apery_like_sequences_2102.11839.pdf` | Ofir Gorodetsky, *New representations for all sporadic Apéry-like sequences, with applications to congruences*, arXiv:2102.11839**v2** (5 Jan 2025), 20 pp. — covers all 15 sporadic sequences of Zagier, Almkvist–Zudilin, and Cooper; identity verified from fetched pages 1–2 | `520da4b0171128d22971d7398f79a1aa6cd760c2412b34a78ba5120adc371ee1` | 2026-07-17 | §1 used to resolve `TIER_LEDGER.md` TL-001 (operator order); its tables are the open-access tabulation of the sporadic families, incl. the Zagier (order-2) and Almkvist–Zudilin (order-3) parameter triples |

## Entries requiring human action (NEEDS-HUMAN)

| Item | Exact citation (source: fetched OEIS A183204/A005260 entry records, #4 above) | What's needed |
|---|---|---|
| Cooper (2012), primary source | Shaun Cooper, *Sporadic sequences, modular forms and new series for 1/pi*, Ramanujan J., December 2012, Volume 29, Issue 1, pp. 163–183. DOI: `10.1007/s11139-011-9357-3` | Not on arXiv (searched; the six "sporadic sequences" arXiv hits are all secondary). Springer paywall — Xavier: retrieve the PDF via institutional access and drop it in `papers/` with its SHA256 added here. Until then, the Gorodetsky paper (#6) serves as the fetchable tabulation of Cooper's sequences. |
| S₂₂ candidate | — | **No citable defining recurrence found** in OEIS records fetched or in-repo certified code. Per `K3_CRITERIA.md` §1: "a candidate without a citable defining recurrence at freeze time is dropped, not guessed." S₂₂ stays flagged; nothing was invented for it. |
| Measured values (ρ_DM,local; PTA sensitivity curves) | — | Deliberately **not** fetched: these edge into the gated observational-data path (`prereg-pipeline`, gate G1) and are only needed at `PREDICTION.md` pin time (§3 P2). To be added post-gate via the same fetch-verify-checksum discipline. |

## Note on the Γ₀(11) / (11,5,125) constants

The retracted netrunner report (`CORRECTION_NETRUNNER_FABRICATION.md`) invoked a
denominator `1 + 11z + 125z²`. The fetched Gorodetsky paper's Almkvist–Zudilin
table does contain a real sporadic entry with parameters (a,b,c) = (11,5,125) (the
η sequence) — i.e., those constants exist in the literature. This changes nothing
about the retraction: the report's *data* was a random mock grid and its claims
remain void; but future work on the η family should cite that table, not the
retracted report.

## Contract for future entries

1. Fetch to disk with `curl` (or by human upload) — never write file contents
   through a model's context.
2. SHA256 recorded here in the same commit that adds the file.
3. Verify identity from the fetched content (title page, definition lines), and
   where a sequence/table has an independent in-repo closed form, cross-check
   term-by-term and emit a certificate JSON.
4. Anything that cannot be fetched-and-verified gets a NEEDS-HUMAN row with an
   exact citation of what is missing — never a from-memory substitute.

---

`Generated-by: Fable-tier session, 2026-07-17 | Verified-by: sha256sum + term-by-term cross-check certificates (oeis/VERIFICATION_CERTIFICATE.json) + fetched-page identity checks | Reviewed-by: pending Xavier`
