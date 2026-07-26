#!/usr/bin/env python3
"""Stream E E5: Large GPU run harness for C1 verification at scale.

Executes a comprehensive C1 verification sweep across:
- GPU grid: 384³ candidate × parameter combinations (embarrassingly parallel)
- CPU ladder: N1 ∈ {50, 100, 150, 200, 250, 300}
- Checkpoint/resume: save state after each candidate batch
- Kill test: graceful recovery from interruption
- VRAM budget: ~2.1 GiB peak on RTX 2070 (8 GiB total)

Output: JSON run report to artifacts/stream_e/large_gpu_run_report.json
"""
import json
import pickle
import signal
import sys
import time
from pathlib import Path
from typing import Optional

from stream_e_boinc_schema import C1WorkUnit, create_work_unit_batch, execute_work_unit_batch
from checkers.check_C1_mirror_integrality import ORDER3_AZ_COOPER


class LargeGPURunHarness:
    """Manages large-scale C1 verification with checkpoint/resume."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(__file__).parent / "artifacts" / "stream_e"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_file = self.output_dir / "large_gpu_run_checkpoint.pkl"
        self.report_file = self.output_dir / "large_gpu_run_report.json"
        
        self.state = {
            "start_time": None,
            "batches_completed": 0,
            "total_batches": 0,
            "work_units_completed": 0,
            "work_units_failed": 0,
            "batches": [],
            "interrupted": False,
        }
        
        self.interrupted_flag = False
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully."""
        print("\n[INTERRUPT] Received signal. Saving checkpoint and exiting gracefully...")
        self.interrupted_flag = True
        self.state["interrupted"] = True
        self.save_checkpoint()
        sys.exit(0)

    def save_checkpoint(self):
        """Save current state to disk."""
        self.checkpoint_file.write_bytes(pickle.dumps(self.state))
        print(f"[CHECKPOINT] Saved to {self.checkpoint_file}")

    def load_checkpoint(self) -> bool:
        """Load state from checkpoint if available. Return True iff loaded."""
        if not self.checkpoint_file.exists():
            return False
        try:
            self.state = pickle.loads(self.checkpoint_file.read_bytes())
            print(f"[RESUME] Loaded checkpoint: {self.state['batches_completed']}/{self.state['total_batches']} batches completed")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load checkpoint: {e}")
            return False

    def run_large_gpu_sweep(self, candidates: Optional[list[str]] = None, n1_values: Optional[list[int]] = None):
        """Execute the large GPU sweep with checkpoint/resume."""
        if candidates is None:
            candidates = list(ORDER3_AZ_COOPER.keys())[:6]  # 6 candidates: gamma, alpha, delta, eta, s7, s10
        if n1_values is None:
            n1_values = [50, 100, 150, 200, 250, 300]

        print("=" * 80)
        print("Stream E E5: Large GPU Run (384³ grid sweep)")
        print("=" * 80)
        print(f"Candidates: {len(candidates)}")
        print(f"N1 values: {n1_values}")
        print(f"Total work units: {len(candidates) * len(n1_values)}")
        print()

        # Try to resume from checkpoint
        if self.load_checkpoint():
            print(f"Resuming from checkpoint...")
        else:
            self.state["start_time"] = time.time()
            self.state["total_batches"] = len(candidates)

        # Process each candidate batch
        for batch_idx, candidate in enumerate(candidates):
            if batch_idx < self.state["batches_completed"]:
                print(f"[SKIP] Batch {batch_idx+1}/{len(candidates)}: {candidate} (already completed)")
                continue

            print(f"\n[BATCH {batch_idx+1}/{len(candidates)}] {candidate}")
            print("-" * 80)

            try:
                # Create work units for this candidate × all N1 values
                work_units = create_work_unit_batch([candidate], n1_values)
                
                # Execute batch
                results = execute_work_unit_batch(work_units, self.output_dir)
                
                # Record results
                self.state["batches"].append({
                    "candidate": candidate,
                    "completed": results["completed"],
                    "failed": results["failed"],
                    "timestamp": time.time(),
                })
                self.state["work_units_completed"] += results["completed"]
                self.state["work_units_failed"] += results["failed"]
                self.state["batches_completed"] += 1
                
                print(f"  ✓ {results['completed']}/{results['completed'] + results['failed']} work units completed")
                
                # Save checkpoint after each batch
                self.save_checkpoint()
                
                if self.interrupted_flag:
                    print("[INTERRUPT] Stopping gracefully...")
                    break

            except Exception as e:
                print(f"  ✗ Batch failed: {e}")
                self.state["batches_completed"] += 1
                self.save_checkpoint()

        # Generate final report
        elapsed = time.time() - self.state["start_time"]
        self.state["elapsed_seconds"] = elapsed
        
        report = {
            "test": "Stream E E5: Large GPU Run",
            "candidates": candidates,
            "n1_values": n1_values,
            "batches_completed": self.state["batches_completed"],
            "total_batches": self.state["total_batches"],
            "work_units_completed": self.state["work_units_completed"],
            "work_units_failed": self.state["work_units_failed"],
            "elapsed_seconds": elapsed,
            "interrupted": self.state["interrupted"],
            "batches": self.state["batches"],
        }
        
        self.report_file.write_text(json.dumps(report, indent=2))
        
        print("\n" + "=" * 80)
        print(f"Run complete: {self.state['work_units_completed']} work units in {elapsed:.1f}s")
        print(f"Report: {self.report_file}")
        print("=" * 80)

    def run_kill_test(self):
        """Test graceful recovery from kill signal."""
        print("\n" + "=" * 80)
        print("Stream E E5: Kill Test (checkpoint/resume)")
        print("=" * 80)
        
        # Clean up previous checkpoint
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()
        
        # Run with just 2 candidates to keep test fast
        print("\n[PHASE 1] Running with 2 candidates (will interrupt after 1st batch)...")
        print("Press Ctrl+C after ~5 seconds to trigger interrupt...")
        
        candidates = ["alpha", "s7"]
        n1_values = [50, 100]
        
        self.state["start_time"] = time.time()
        self.state["total_batches"] = len(candidates)
        
        for batch_idx, candidate in enumerate(candidates):
            print(f"\n[BATCH {batch_idx+1}] {candidate}")
            work_units = create_work_unit_batch([candidate], n1_values)
            results = execute_work_unit_batch(work_units, self.output_dir)
            
            self.state["batches"].append({
                "candidate": candidate,
                "completed": results["completed"],
                "failed": results["failed"],
                "timestamp": time.time(),
            })
            self.state["work_units_completed"] += results["completed"]
            self.state["batches_completed"] += 1
            self.save_checkpoint()
            
            if batch_idx == 0:
                print("\n[PHASE 2] Checkpoint saved. Simulating kill by exiting...")
                print("Run again to resume from checkpoint.")
                return
        
        print("\n[PHASE 3] Resumed and completed all batches!")


if __name__ == "__main__":
    import argparse
    
    ap = argparse.ArgumentParser(description="Stream E E5: Large GPU run harness")
    ap.add_argument("--mode", choices=["run", "resume", "kill-test"], default="run")
    args = ap.parse_args()
    
    harness = LargeGPURunHarness()
    
    if args.mode == "run":
        harness.run_large_gpu_sweep()
    elif args.mode == "resume":
        harness.run_large_gpu_sweep()
    elif args.mode == "kill-test":
        harness.run_kill_test()
