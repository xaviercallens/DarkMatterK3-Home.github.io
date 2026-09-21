"""DIAGNOSIS ONLY — not a result, writes nothing into data/. Reproduces the S2 seed1 sweep with
the predictor wrapped so an invalid native P1D is RECORDED (with its exact arguments) instead of
killing the sweep. Each forked worker appends to one O_APPEND file, which is fork-safe for short
lines. Sentinel return keeps the sweep going so we see every occurrence, not just the first.
"""
import json, os, sys, time, warnings
warnings.filterwarnings("ignore")
ROOT = "/mnt/disks/disk-socrateai-local-1/callensxavier_home_data/DarkMatterK3-Home.github.io"
SC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT + "/pipeline"); sys.path.insert(0, ROOT + "/phase1_work/agent1_emulator")
import numpy as np, torch
torch.set_num_threads(1)
import emu_predict as E, keff, sweep

LOG = SC + "/invalid_args.jsonl"
OUT = SC + "/diag_out"
os.makedirs(OUT, exist_ok=True)
open(LOG, "w").close()

pack = E.load()
native = lambda m, f, zrei, ha, hs, taueff: E.predict_pk(pack, m, f, zrei, ha, hs, taueff, "4.2")
k_eff = keff.load_k_eff()
mult = np.ones(keff.NATIVE_LOG10K.size)

def predict(m, f, zrei, ha, hs, taueff):
    v = np.asarray(native(m, f, zrei, ha, hs, taueff), dtype=float) * mult
    if not np.all(np.isfinite(v)) or np.any(v <= 0):
        rec = {"pid": os.getpid(), "m": m, "f": f, "zrei": zrei, "ha": ha, "hs": hs,
               "taueff": taueff, "n_nonpos": int((v <= 0).sum()),
               "n_nonfinite": int((~np.isfinite(v)).sum()),
               "min": None if not np.isfinite(np.nanmin(v)) else float(np.nanmin(v)),
               "raw": [float(x) if np.isfinite(x) else str(x) for x in v[:4]]}
        fd = os.open(LOG, os.O_WRONLY | os.O_APPEND)
        os.write(fd, (json.dumps(rec) + "\n").encode()); os.close(fd)
        return np.full(len(k_eff), 1e-30)          # sentinel: huge chi2, keeps the sweep alive
    return keff.predict_at_keff(v, k_eff)

MED = json.load(open(keff.GRID_CONTROLS_JSON))["igm_nuisance_point"]
NUIS = [MED["zrei"], MED["ha"], MED["hs"], MED["taueff"]]
cov = np.load(ROOT + "/data/derived/wp_e6_sweep_cov_agg9_sys_z4p2_2026_09_17.npy")
L = np.linalg.cholesky(cov)
truth = predict(-22.0, 0.35, *NUIS)
obs = truth + L @ np.random.default_rng(1).standard_normal(9)
t = time.time()
rec = sweep.run_sweep(obs, cov, predict, "synthetic", OUT + "/S2_seed1_DIAG.json",
                      workers=int(os.environ.get("SWEEP_WORKERS", "7")),
                      meta={"DIAGNOSIS": "sentinel predictor; NOT A RESULT"})
n = sum(1 for _ in open(LOG))
print("sweep finished in %.0f s; invalid-prediction events: %d" % (time.time() - t, n))
if n:
    seen = [json.loads(l) for l in open(LOG)]
    cells = sorted({(r["m"], r["f"]) for r in seen})
    print("distinct (m,f) cells with invalid predictions: %d ->" % len(cells), cells)
    for r in seen[:10]:
        print("   ", {k: (round(v, 5) if isinstance(v, float) else v)
                      for k, v in r.items() if k != "raw"})
    for nm in ("zrei", "ha", "hs", "taueff"):
        vals = [r[nm] for r in seen]
        print("   %-7s bad range [%.5f, %.5f]" % (nm, min(vals), max(vals)))
