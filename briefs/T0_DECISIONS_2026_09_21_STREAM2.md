> **Delivered copy (untracked) — source of truth: Stream 2 repo `briefs/T0_DECISIONS_2026_09_21_STREAM2.md`, main @ 749a3e6, release v0.3.11-criteria-canonical. Dropped here by the Stream 2 session on 2026-09-21; not committed — the owning session decides.**

# T0 decisions — 2026-09-21 (Stream 2 record)

**Ruled by:** T0 (Xavier Callens), in the Stream 2 session of 2026-09-21. **Recorded by:** Claude
(Fable 5.1). Numbering continues `briefs/T0_DECISIONS_2026_09_16_STREAM2.md` (D6′).

## D7′ — the ρ = 20 cut is ADOPTED in this repository too

**Context.** Stream 3 reported (`briefs/STREAM3_TO_STREAMS1_2_T0_RULING_RHO20_ADOPTED_2026_09_21.md`,
filed here as received) that T0 had adopted decision D-1 of its
`T0_DECISION_REQUEST_K3_SELECTION_2026_09_21.md`, recorded there as ruling R1 with the T0 text
*"adopt decision 1 and implement what you could at this stage waiting for others streams"*.
A ruling given to another session is not applied here on report alone (lesson of 2026-09-16, D6′:
a menu choice is not a ruling), so T0 was asked directly in this session whether the adoption holds
for this repository with Stream 3's narrow reading.

**T0 text (verbatim, this session):** *"oui je confirme la coupure aussi sur ce repo."*

**What is adopted.** The program adopts **ρ = 20** as a selection criterion: a K3 candidate is a
member of a register family whose transcendental lattice has rank 2 and is positive definite, so
classification runs by positive-definite binary quadratic forms, finite at each discriminant.
Inside the two register families this is the CM-point locus computed in `CM_POINTS_RHO20.json` and
`A2_MEMBERSHIP.json` (Tier B).

**What is NOT adopted — the ruling does not say it, and each item needs its own T0 text:**

- **No ranking of cooper_s7 over cooper_s10 and no minimum-|D| rule.** "A₂ is in the s7 family and
  not in the s10 family" stays a lattice fact. Note the register's GE-14: two known principles point
  at *different* members (the (−2)-walls at D = −28, −7; the minimal discriminant at D = −3), and
  the ruling chooses between them no more than it chooses a candidate.
- **No corroboration claim.** Elliptic point ⇒ CM is forced (`ELLIPTIC_POINTS_ARE_CM.json`); the
  binary-form side and the modular side agree by Shioda–Inose.
- **cooper_s10 stays ADVISORY.** D6′ is untouched; the adoption promotes no s10 row and does not
  make `C2_cooper_s10_v4_DRAFT.json` LIVE.
- **No physical reading.** No (m, f) prior, m_φ, α_D or Λ_D follows from any CM point; that map is
  Tier C, BLOCKED under F5b, and the tadpole is unposable without B₃ (ledger item 4). The flux
  literature read on 2026-09-21 supplies no bound on |D| for a one-parameter family
  (`briefs/T0_DECISION_REQUEST_FLUX_BOUND_ON_D_2026_09_21.md`).
- **`K3_CRITERIA.md` is not frozen or edited by this ruling.** How the cut enters the criteria
  (a new criterion? wording? which coordinate for C3 — Stream 3's D-2; the two-entry register —
  their D-3) is still open and goes through the §6 amendment protocol.
- **Gate T3 is not adopted** by this ruling (decision 2 of the K3×T² proposal, still open).

**Known limits the adoption inherits (unchanged by it).** The CM table is complete on the
discriminants it lists and silent elsewhere (window −v² ≤ 44); z-values are numeric recognitions
through a relation certified PASS(40); "v·ω = 0 ⇒ ρ = 20, T_X = v^⊥" is the cited Dolgachev 1996 §7
framework, not proved here; CM points are dense on the modular curve, so the cut yields a finite
list only per discriminant.

**Actions taken under D7′ (same PR).**
1. `CLAUDE.md` ledger: item 8 added (dated).
2. `TODO.md`: the "ρ = 20 fork" item closed with this record; the remaining open T0 items kept.
3. Six checkers and one renderer: "not adopted" wording replaced by the narrow adoption; all
   certificates re-emitted and briefs re-rendered. **No computed value changes** — verified by
   diffing the certificates before and after with the status / not-claimed / hash / version fields
   set aside.
4. Stream 3 told: their mirror drift detector will fail closed on the new certificate hashes, by
   design; they re-read, re-run the controls and re-mirror.

## D8′ — `K3_CRITERIA.md`: amendments AM-1…AM-5, and the canonical copy

**How this was ruled.** T0 was presented with four questions, each option stating its consequence,
and selected one option per question. They are rulings, not work-item picks — the questions asked
which reading the program adopts, and one option spelled out an F1 removal. Recorded verbatim so a
future session does not read "approved via menu" and revert it (the D6′ lesson).

| question put to T0 | option selected, verbatim |
|---|---|
| *"AM-2 — Critère C3 : le texte actuel de C3 ne contient AUCUNE exigence d'intégralité (« L₃ = Sym²(L₂) pour un L₂ explicitement exhibé »). Quelle lecture adoptes-tu ?"* | **"Lecture littérale"** — *"L'intégralité ne fait pas partie de C3. La constante c (s7 : 1, s10 et s18 : 2) est RAPPORTÉE comme attribut, jamais porte ni score. s7 et s10 passent C3."* |
| *"AM-3 — Critère C2 (contenu en fibres de Kodaira) : c'est une erreur de catégorie pour ce registre (ledger point 3, certificats rétractés E-007). Le remplacer par la porte de réseau T2 … ?"* | **"Oui, remplacer"** — *"C2 devient « Réseau transcendant (T2) ». L'ancien texte Kodaira est conservé barré avec sa référence de rétractation. s7 LIVE, s10 DRAFT (inchangé)."* |
| *"AM-4 — Adopter T1 et T3 comme portes de COHÉRENCE (jamais scorées), avec la formulation corrigée « deux calculs disjoints sur le même opérateur », et resserrer le drapeau Atkin–Lehner de T3 ?"* | **"Oui, adopter + resserrer"** — *"T1 et T3 entrent comme portes de cohérence sans score. Le drapeau ATKIN_LEHNER_ACTION_UNVERIFIED devient « action vérifiée au niveau réseau ; certificat de réseau s10 DRAFT ». Limites gardées : aucun candidat réel en désaccord, dents directionnelles."* |
| *"AM-1 + AM-5 — Où vit le K3_CRITERIA.md canonique, avec le nouveau critère C6 (coupure ρ = 20, texte étroit) ?"* | **"Ici, dans Stream 2"** — *"Stream 2 possède la sélection. Fichier créé à la racine à partir de la copie Stream 1 + les amendements que tu approuves ; Stream 1 et 3 gardent un miroir épinglé par hachage qui échoue fermé en cas de dérive."* |

**What was done, exactly.** Two commits, so §6's "exact diff" requirement is met by git: first the
**byte-identical seed** from Stream 1's copy at `6c09d2d` (sha256 `66d76883ad4a8e9b…`, matching the
source file), then the amendments. **§1 (the FROZEN candidate register) is untouched** — the only
removed lines are the old C2 block, the "repo of record" line and the §5 table.

Three things the amendment proposal did not cover, decided while writing and recorded here:

1. **§5's status table is removed, not edited.** It named `scripts/render_status_table.py`, which
   **does not exist in this repository and never has** (absence verified 2026-07-26; the
   `criteria-checkers` skill records citing it as a phantom-artifact incident). The table that
   stood there was the pre-2026-07-18 skeleton — `SYM2_UNVERIFIED` for s7/s10 — contradicting every
   certificate on `main`; copying it into the canonical file would have given a stale table fresh
   authority, and hand-editing it is the integrity incident §5 itself forbids. §5 now says in band
   that the table of record is `data/certificates/`, and writing the renderer is an open item.
2. **§4 gains one sentence: a DRAFT certificate is neither a pass nor a failure.** Without it, the
   amended C2 plus `cooper_s10`'s DRAFT lattice certificate would read as "fails a hard criterion ⇒
   F1 removal" — the accidental removal that reading I of AM-2 was refused for. C6, T1 and T3 are
   recorded as *not scored at all*, neither hard nor soft.
3. **The Atkin–Lehner flag is retired, not renamed.** A single concatenated flag would re-merge the
   mathematics and the process that were deliberately split. `check_T3_level_consistency.py` now
   carries `atkin_lehner_action: {verified: true, evidence: ATKIN_LEHNER_DISC_FORM.json,
   pass_order_n: 30}`, and `LATTICE_CERT_DRAFT` stands alone as `cooper_s10`'s one open flag.
   `T3_LEVEL_CONSISTENCY.json` re-emitted (sha256 `1b6bb9b69adb9bb2…`), 25/25 controls green.

**Unchanged by D8′:** the freeze status (thresholds remain SKELETON; §7 still blocks v1.0, so
AutoEvolve may not score), §1's frozen register, `cooper_s10`'s DRAFT status (D6′), and the stale
`t103` row, whose T0 flag from Stream 1 remains unanswered and is now visible in the file's header.

---
*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: T0 text quoted verbatim from this
session; Stream 3's record read at its source (`briefs/T0_RULINGS_2026_09_21.md`, their repository) |
Reviewed-by: T0 Y for the ruling itself; the narrow reading is recorded as Stream 3 proposed it and
as T0 was asked to confirm it, and is countermandable*
