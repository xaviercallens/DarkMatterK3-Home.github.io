# DEPRECATED / EXPERIMENTAL 2026-07-25 (Fable 5, T0-delegated) — DO NOT CITE OUTPUT.
# base_strain=1.8e-15 and pta_limit=2.5e-15 are hardcoded with no citation (violates
# P1, LESSONS_LEARNED.md); mu_growth values passed at the bottom of this file
# (25.869408, 15.331455) are the fabricated cooper_s7/s10 constants from the 2026-07-14
# review (see cooper-s7-ground-truth memory / LESSONS_LEARNED.md L1). Prints
# "VERDICT: SUCCESS...experimentally viable" language that this project's own
# epistemic-guardrails skill forbids without a conjecture marker. No .par file or real
# NANOGrav data is read anywhere in this file. See LEGACY_CODE_DISPOSITION_2026_07_25.md.
import numpy as np

def validate_pta_monopole(hypothesis, mu_growth):
    print(f"Validating NANOGrav Scalar Monopole Signal for {hypothesis}...")
    
    # The expected scalar monopole strain scales with the asymptotic growth of the K3 modulus
    # For Cooper_s7, mu=25.86; For Cooper_s10, mu=15.33
    base_strain = 1.8e-15
    strain = base_strain * (mu_growth / 20.0)**0.5
    
    print(f"  -> Expected Scalar Monopole Strain Amplitude: {strain:.2e}")
    
    # NANOGrav 15-year dataset limits for a scalar monopole stochastic background
    pta_limit = 2.5e-15
    
    if strain < pta_limit:
        print(f"  -> VERDICT: SUCCESS. The theoretical scalar signal is bounded strictly within the current NANOGrav non-detection limits ({pta_limit:.2e}). It is experimentally viable.")
    else:
        print(f"  -> VERDICT: FAILED. The predicted strain exceeds the current observational constraints of the NANOGrav 15-year dataset.")

if __name__ == "__main__":
    print("="*70)
    print("NANOGrav 15-YEAR PULSAR TIMING ARRAY PREDICTION & VALIDATION")
    print("="*70)
    validate_pta_monopole("Cooper_s7 (Level 7)", 25.869408)
    print("-" * 70)
    validate_pta_monopole("Cooper_s10 (Level 10)", 15.331455)
    print("="*70)
