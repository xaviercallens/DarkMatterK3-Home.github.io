# refs/ — Cited Literature and Measured-Value Files

**Status:** Empty. No files transcribed yet — this is the human task flagged as the
critical path in `PREDICTION_REVIEW_T0.md` §4 ("refs/ manifest entries ... transcription
PR merged").

## Purpose

Every numeric constant or literature value used anywhere in this program (Cooper
sequence papers, AESZ elliptic-surface tables, measured public values like local
dark-matter density or PTA sensitivity curves) must be transcribed here as a file with
a SHA256 and an explicit citation — never quoted from a model's memory
(`epistemic-guardrails` rule 5). `PREDICTION.md` §0's Provenance block cites these
files by hash; `checkers/*.py` (Stream 2, not yet implemented) read literature data
from here, never the network, per `K3_CRITERIA.md` §3.

## Expected contents (per current cross-references)

- Cooper (2012) — source paper for the candidate sequences' recurrences.
- AESZ tables — elliptic-surface classification data (Kodaira fiber content, C2).
- Measured-values file — local dark-matter density (with published uncertainty),
  NANOGrav/EPTA sensitivity curves — cited by `PREDICTION.md` §3 P2 and
  `PREDICTION_APPENDIX_A.md` A.4.

## Manifest

| File | Source citation | SHA256 | Added | Used by |
|---|---|---|---|---|
| _(none yet)_ | | | | |

---

`Generated-by: Claude Sonnet 5 (T2 plumbing — directory scaffold only, no content) | Verified-by: none | Reviewed-by: T0 N`
