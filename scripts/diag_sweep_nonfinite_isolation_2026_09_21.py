"""Isolate whether the NaN nuisance is a fork/pool artifact. One cell, real code path."""
import json, os, sys, warnings
warnings.filterwarnings("ignore")
R="/mnt/disks/disk-socrateai-local-1/callensxavier_home_data/DarkMatterK3-Home.github.io"
SC=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,R+"/pipeline"); sys.path.insert(0,R+"/phase1_work/agent1_emulator")
import numpy as np, torch
torch.set_num_threads(1)
import emu_predict as E, keff, sweep
LOG=SC+"/iso_events.jsonl"
pack=E.load(); k_eff=keff.load_k_eff(); mult=np.ones(keff.NATIVE_LOG10K.size)
def predict(m,f,zrei,ha,hs,taueff):
    if not all(np.isfinite([zrei,ha,hs,taueff])):
        fd=os.open(LOG,os.O_WRONLY|os.O_APPEND)
        os.write(fd,(json.dumps({"pid":os.getpid(),"stage":"nonfinite_PARAMS","m":m,"f":f})+"\n").encode()); os.close(fd)
        return np.full(len(k_eff),1e-30)
    v=np.asarray(E.predict_pk(pack,m,f,zrei,ha,hs,taueff,"4.2"),dtype=float)*mult
    if not np.all(np.isfinite(v)) or np.any(v<=0):
        fd=os.open(LOG,os.O_WRONLY|os.O_APPEND)
        os.write(fd,(json.dumps({"pid":os.getpid(),"stage":"invalid_EMULATOR","m":m,"f":f})+"\n").encode()); os.close(fd)
        return np.full(len(k_eff),1e-30)
    return keff.predict_at_keff(v,k_eff)
MED=json.load(open(keff.GRID_CONTROLS_JSON))["igm_nuisance_point"]
NUIS=[MED["zrei"],MED["ha"],MED["hs"],MED["taueff"]]
cov=np.load(R+"/data/derived/wp_e6_sweep_cov_agg9_sys_z4p2_2026_09_17.npy")
obs=predict(-22.0,0.35,*NUIS)+np.linalg.cholesky(cov)@np.random.default_rng(1).standard_normal(9)
W=int(sys.argv[1]); CELLS=sys.argv[2] if len(sys.argv)>2 else "one"
mg=np.array([-22.5]) if CELLS=="one" else sweep.M_GRID
fg=np.array([0.05])  if CELLS=="one" else sweep.F_GRID
open(LOG,"w").close()
rec=sweep.run_sweep(obs,cov,predict,"synthetic",SC+f"/iso_w{W}.json",m_grid=mg,f_grid=fg,
                    workers=W,meta={"DIAGNOSIS":"isolation; NOT A RESULT"})
n=sum(1 for _ in open(LOG))
print(f"workers={W} cells={len(mg)*len(fg)}: nonfinite/invalid events = {n}; "
      f"chi2_min={rec['cells'][0]['chi2_min']:.5f} valid={rec['cells'][0]['valid_minimum']}")
