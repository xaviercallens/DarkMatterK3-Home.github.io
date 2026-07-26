#!/usr/bin/env python3
"""Stream E E4: BOINC work-unit schema for C1 verification.

Defines the work-unit structure for embarrassingly parallel C1 checks:
- Input: (candidate_name_or_tuple, N1)
- Output: JSON certificate with exact-equality validator
- Validator: bit-for-bit determinism hash match

Work units are shardable by candidate and N1 value.
"""
import json
import hashlib
from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path

from checkers.check_C1_mirror_integrality import verify_c1, ORDER3_AZ_COOPER


@dataclass
class C1WorkUnit:
    """BOINC work unit for C1 verification."""
    wu_id: str
    candidate: str
    order3_abcd: tuple
    n1: int
    status: str = "pending"  # pending, completed, failed
    result: Optional[dict] = None
    validator_hash: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["order3_abcd"] = list(self.order3_abcd)
        return d

    def compute(self) -> bool:
        """Execute the work unit. Return True iff successful."""
        try:
            self.result = verify_c1(self.order3_abcd, N1=self.n1)
            self.status = "completed"
            
            # Compute determinism validator hash
            payload = {
                "order3": list(self.order3_abcd),
                "N1": self.n1,
                "verdict": self.result["verdict"],
                "margin": self.result["margin_max_denominator"],
            }
            payload_str = json.dumps(payload, sort_keys=True)
            self.validator_hash = hashlib.sha256(payload_str.encode()).hexdigest()
            return True
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            return False

    def validate_exact_equality(self, other: "C1WorkUnit") -> bool:
        """Check bit-exact equality with another work unit (same input)."""
        if self.order3_abcd != other.order3_abcd or self.n1 != other.n1:
            return False
        if self.status != "completed" or other.status != "completed":
            return False
        if self.validator_hash != other.validator_hash:
            return False
        if self.result["verdict"] != other.result["verdict"]:
            return False
        if self.result["margin_max_denominator"] != other.result["margin_max_denominator"]:
            return False
        return True


def create_work_unit_batch(candidates: list[str], n1_values: list[int]) -> list[C1WorkUnit]:
    """Create a batch of work units for a Cartesian product of candidates × N1 values."""
    work_units = []
    wu_counter = 0
    
    for candidate in candidates:
        for n1 in n1_values:
            wu_id = f"c1_wu_{wu_counter:06d}"
            
            # Resolve candidate name to order3 tuple
            if candidate in ORDER3_AZ_COOPER:
                order3 = ORDER3_AZ_COOPER[candidate]
            else:
                try:
                    parts = [int(x.strip()) for x in candidate.split(",")]
                    if len(parts) != 4:
                        raise ValueError(f"invalid tuple: {candidate}")
                    order3 = tuple(parts)
                except Exception as e:
                    print(f"ERROR: invalid candidate {candidate}: {e}")
                    continue
            
            wu = C1WorkUnit(
                wu_id=wu_id,
                candidate=candidate,
                order3_abcd=order3,
                n1=n1,
            )
            work_units.append(wu)
            wu_counter += 1
    
    return work_units


def execute_work_unit_batch(work_units: list[C1WorkUnit], output_dir: Optional[Path] = None) -> dict:
    """Execute a batch of work units. Return summary report."""
    output_dir = output_dir or Path(__file__).parent / "artifacts" / "stream_e"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = {
        "total": len(work_units),
        "completed": 0,
        "failed": 0,
        "work_units": [],
    }
    
    for wu in work_units:
        success = wu.compute()
        results["work_units"].append(wu.to_dict())
        if success:
            results["completed"] += 1
        else:
            results["failed"] += 1
    
    # Write results to file
    results_file = output_dir / "boinc_batch_results.json"
    results_file.write_text(json.dumps(results, indent=2))
    
    return results


def validate_batch_determinism(work_units_1: list[C1WorkUnit], work_units_2: list[C1WorkUnit]) -> bool:
    """Verify bit-exact equality between two batches (determinism test)."""
    if len(work_units_1) != len(work_units_2):
        return False
    
    for wu1, wu2 in zip(work_units_1, work_units_2):
        if not wu1.validate_exact_equality(wu2):
            return False
    
    return True


if __name__ == "__main__":
    # Example: create and execute a small batch
    candidates = ["alpha", "s7", "s10"]
    n1_values = [50, 100]
    
    print("=" * 80)
    print("Stream E E4: BOINC Work-Unit Batch Execution")
    print("=" * 80)
    
    work_units = create_work_unit_batch(candidates, n1_values)
    print(f"\nCreated {len(work_units)} work units")
    
    results = execute_work_unit_batch(work_units)
    print(f"\nResults: {results['completed']}/{results['total']} completed, {results['failed']} failed")
    print(f"Results written to: artifacts/stream_e/boinc_batch_results.json")
    
    # Determinism test: run the same batch again
    print("\n[DETERMINISM TEST] Running same batch again...")
    work_units_2 = create_work_unit_batch(candidates, n1_values)
    execute_work_unit_batch(work_units_2)
    
    if validate_batch_determinism(work_units, work_units_2):
        print("✓ Determinism test PASSED: bit-exact equality verified")
    else:
        print("✗ Determinism test FAILED")
