# Stream E → Stream 2: Assistance Offer and Handoff Contract

**Branch**: `feature/rust-kernel-boinc-scale`
**Generated-by**: Claude Opus 4.8 (T1 planner) | **Verified-by**: recon of `checkers/**` and `scripts/s2_01b_golden_data/**` | **Reviewed-by**: pending T0

---

## 1. What Stream 2 is currently bounded by

Stream 2 owns the criterion checkers and the candidate ranking. From the fixtures and READMEs in
`scripts/s2_01b_golden_data/`, the declared sequence is:

```
S2-01b  C3b Shioda-Inose moduli map checker   (golden fixtures exist)
S2-02   generic checkers C1-C5
S2-04   ranking run -> K3_SELECTION_REPORT.md with per-candidate C3b grades
```

Two of those steps are wall-clock bound rather than idea bound:

- **`stress_test_high_order_s7`** is specified at `N=200` and exists precisely to show the margin
  does not drift between `N=50` and `N=200`. High-order runs are the expensive ones.
- **S2-04 ranking** applies checkers across *all* candidates, i.e. a `candidate × criterion × N`
  grid. That is exactly the shape BOEINC fan-out is for.

Stream E does not need to understand the geometry to remove that bound. It only needs to make the
same computation faster and shardable, while proving it did not change a single digit.

---

## 2. Concrete offer

### 2.1 A fast exact C1 oracle, batch mode

After task **E2** is green (bit-exact parity, see `STREAM_E_HAIKU_TASKCARDS.md`), Stream 2 gets:

```
k3c1 --batch operators.json --N1 200 --out artifacts/stream_e/certificates/
```

- input: a JSON list of `{"name": str, "abcd": [a,b,c,d]}`
- output: one certificate per operator, plus `index.json` summarising
  `PASS(N1)` / `FAIL(first non-integral order)` per operator
- guarantee: byte-identical to `checkers/check_C1_mirror_integrality.py` for every operator where
  both can run

This lets Stream 2 raise `N1` from 50 to a few hundred as a routine action rather than a
scheduled event, which directly strengthens the `A(N₁-bounded)` bound that C1 carries.

### 2.2 A shardable ranking grid

Task **E4** defines a BOEINC work unit as one `(operator, N1)` cell with an **exact-equality**
validator. S2-04's ranking grid maps onto that with no new infrastructure: one work unit per
`(candidate, criterion, N)` cell, quorum of 2 bit-identical results.

### 2.3 A high-order stress capability

`stress_test_high_order_s7` at `N=200` becomes cheap enough to run for *every* candidate, not
just `s7`, turning a single stress case into a systematic column in the ranking table.

---

## 3. What Stream E needs from Stream 2 (the ask)

Three things, all cheap, and all needed before Stream E can help without guessing:

1. **Authoritative operator list.** Confirm that `ORDER3_AZ_COOPER` in `checkers/check_C3_sym2.py`
   is the single source of truth for `(a,b,c,d)` tuples, and that the six names
   `gamma, alpha, delta, eta, s7, s10` are the intended set. Stream E's `src/operators.rs` mirrors
   that table and must not diverge.

2. **Ruling on the C3b comparison model.** This matters and Stream E will not decide it
   unilaterally:
   - **C1 is exact rational.** Parity is bit-exact equality. Settled.
   - **C3b is float-margin based.** `scripts/s2_01b_golden_data/README.md` specifies
     `margin < 1e-15` as "excellent", `> 1e-8` as "suspect", and `CONDITIONAL` when there is no
     convergence. A bit-exact parity gate is therefore **not** applicable to C3b.

   Stream E needs Stream 2 to state the admissible C3b comparison tolerance before any C3b port
   is attempted. Until then Stream E ports **C1 only**, which is why the task cards stop there.

3. **Confirmation of the intended test path.** `scripts/s2_01b_golden_data/README.md` says the
   fixtures are loaded by `pipeline/checkers/test_c3b.py`, but the checker tests actually live at
   `checkers/tests/test_c3b_moduli_map.py`, and `pytest.ini` has
   `testpaths = . api core` — which does **not** include `checkers/`. So the C3b golden tests are
   not run by a bare `pytest` invocation.

   Stream E has deliberately **not** edited `pytest.ini`, because that file governs what Stream 3's
   merge-blocking CI executes. Stream 2 should decide whether `checkers/` joins `testpaths` or
   whether an explicit invocation is added to the workflow. Flagging it, not fixing it.

---

## 4. Division of responsibility

| Concern | Owner |
|---|---|
| Criterion definitions, normalisation, tier semantics | **Stream 2** |
| What counts as PASS/FAIL, and the C3b tolerance | **Stream 2** |
| Which candidates are in scope | **Stream 2** |
| Making the checkers fast, parallel, and shardable | **Stream E** |
| Proving the fast version equals the reference | **Stream E** |
| Certificate emission plumbing and storage layout | **Stream E** |
| Interpreting a certificate as evidence about geometry | **Stream 2** |

Stream E writes certificates to `artifacts/stream_e/certificates/` and **never** to
`checkers/certificates/`. Promotion of a Rust-computed certificate into `checkers/certificates/`
is a **Stream 2 decision**, taken after parity is green — not a Stream E action.

---

## 5. Epistemic guarantee, stated precisely

A faster implementation changes *who computed* a number, not what the number licenses.

- C1 stays `Tier B → A(N₁-bounded) on pass`.
- Raising `N1` from 50 to 500 raises the bound. It does not convert finite-order integrality
  evidence into a proof of integrality, and Stream E documents will not describe it as such.
- Every Rust-emitted certificate carries `computed_by: "rust/k3_kernel@<git-sha>"` next to the
  unchanged `tier` string, so provenance is never ambiguous.
- Stream E adds no assumption tag. C1's `assumptions: []` is preserved verbatim.

---

## 6. Sequencing against Stream 1 / 2 / 3

Stream E is designed to be dependency-free in the outward direction:

- It **does not block** on Stream 1 or Stream 2 theory completion. The C1 port is defined entirely
  by the existing Python reference and existing certificates.
- It **does not block** Stream 3. Work is on a separate branch in a separate worktree, the GPU
  half has a hard pre-flight occupancy gate, and `pipeline/**` is on the do-not-touch list.
- The one place Stream E **waits** on Stream 2 is the C3b tolerance ruling (§3.2). That is why the
  task cards scope the port to C1 and stop.

Suggested handoff point: once **E2** reports `PARITY: 36/36 cells exact`, Stream 2 can start using
the batch oracle immediately, in parallel with Stream E continuing on E3–E5.

---

## 7. Open questions for Stream 2

1. Is `ORDER3_AZ_COOPER` authoritative, and is the six-name set complete for ranking purposes?
2. What is the admissible C3b margin tolerance for a reimplementation to be considered equivalent?
3. Should `checkers/` be added to `pytest.ini` `testpaths`, or invoked explicitly in CI?
4. Is `t103` (A276536) expected to get a C1 certificate? It appears in
   `sections/sec_hypothesis_foundry_update.md` with `mirror_map_integral: null`, and there is no
   `checkers/certificates/C1_mirror_t103.json`. If Stream 2 supplies the `(a,b,c,d)` tuple,
   Stream E can produce that certificate as a first application of the batch oracle.
5. What `N1` should the ranking run standardise on, given that Stream E will report measured
   cost at `N1 ∈ {50,100,200,300,500}` in `artifacts/stream_e/SCALING_REPORT.md`?
