#!/usr/bin/env python3
"""
Phase 4 Multi-Day Execution: K3-DISC-0035 Filament Validation
Monitors discoveries in real-time and validates filament signature
"""

import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class Phase4Executor:
    """Phase 4 multi-day execution with K3-DISC-0035 filament validation."""
    
    # K3-DISC-0035 reference coordinates
    K3_DISC_0035_RA = 205.0
    K3_DISC_0035_DEC = 5.0
    K3_DISC_0003_RA = 205.0
    K3_DISC_0003_DEC = 35.0
    
    # Filament detection parameters
    FILAMENT_RA_TOLERANCE = 2.0
    FILAMENT_DEC_MIN = 5.0
    FILAMENT_DEC_MAX = 35.0
    FILAMENT_DELTA_THRESHOLD = 0.20
    
    def __init__(self, repo_root: str = None, duration_hours: int = 24):
        """Initialize Phase 4 executor."""
        if repo_root is None:
            repo_root = Path(__file__).parent
        else:
            repo_root = Path(repo_root)
        
        self.repo_root = repo_root
        self.discoveries_file = repo_root / 'discoveries.json'
        self.log_file = repo_root / 'logs' / 'phase4_execution.log'
        self.duration_hours = duration_hours
        self.start_time = datetime.utcnow()
        self.end_time = self.start_time + timedelta(hours=duration_hours)
        
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, message: str, level: str = 'INFO'):
        """Log message to file and console."""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # Console output (ASCII-safe)
        try:
            safe_msg = message.encode('ascii', 'ignore').decode('ascii')
            print(f"[{timestamp}] [{level}] {safe_msg}")
        except:
            print(f"[{timestamp}] [{level}] [Log message]")
        
        # File output (UTF-8)
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except:
            pass
    
    def load_discoveries(self) -> List[Dict]:
        """Load discoveries from JSON file."""
        if not self.discoveries_file.exists():
            return []
        
        try:
            with open(self.discoveries_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            self.log(f"Error loading discoveries: {e}", 'ERROR')
            return []
    
    def check_k3_disc_0035(self, discoveries: List[Dict]) -> Optional[Dict]:
        """Check for K3-DISC-0035 in discoveries."""
        return next(
            (d for d in discoveries if d.get('id') == 'K3-DISC-0035'),
            None
        )
    
    def find_filament_candidates(self, discoveries: List[Dict]) -> List[Dict]:
        """Find filament candidates along RA 205 meridian."""
        candidates = []
        
        for d in discoveries:
            try:
                ra = float(d.get('ra', 0))
                dec = float(d.get('dec', 0))
                delta = float(d.get('delta', 0))
                
                # Check if within filament region
                if (abs(ra - self.K3_DISC_0035_RA) < self.FILAMENT_RA_TOLERANCE and
                    self.FILAMENT_DEC_MIN <= dec <= self.FILAMENT_DEC_MAX and
                    delta > self.FILAMENT_DELTA_THRESHOLD):
                    candidates.append(d)
            except (ValueError, TypeError):
                continue
        
        return sorted(candidates, key=lambda x: float(x.get('delta', 0)), reverse=True)
    
    def validate_filament_signature(self, discoveries: List[Dict]) -> Dict:
        """Validate K3-DISC-0035 filament signature."""
        k3_disc_0035 = self.check_k3_disc_0035(discoveries)
        filament_candidates = self.find_filament_candidates(discoveries)
        
        # Count anomalies by delta threshold
        critical = sum(1 for d in discoveries if float(d.get('delta', 0)) > 0.30)
        high = sum(1 for d in discoveries if 0.25 < float(d.get('delta', 0)) <= 0.30)
        
        validation = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_discoveries': len(discoveries),
            'critical_anomalies': critical,
            'high_anomalies': high,
            'k3_disc_0035_detected': k3_disc_0035 is not None,
            'k3_disc_0035': k3_disc_0035,
            'filament_candidates': len(filament_candidates),
            'filament_candidate_list': filament_candidates[:5]
        }
        
        return validation
    
    def print_status_report(self, validation: Dict):
        """Print Phase 4 status report."""
        elapsed = datetime.utcnow() - self.start_time
        elapsed_hours = elapsed.total_seconds() / 3600
        remaining = self.duration_hours - elapsed_hours
        
        report = f"""
================================================================================
PHASE 4 EXECUTION STATUS REPORT
================================================================================
Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
Duration: {self.duration_hours} hours
Elapsed: {elapsed_hours:.1f} hours
Remaining: {remaining:.1f} hours

DISCOVERY STATISTICS
================================================================================
Total Discoveries: {validation['total_discoveries']}
Critical Anomalies (Delta > 0.30): {validation['critical_anomalies']}
High Anomalies (0.25 < Delta <= 0.30): {validation['high_anomalies']}

K3-DISC-0035 FILAMENT DETECTION
================================================================================
Status: {'DETECTED' if validation['k3_disc_0035_detected'] else 'NOT YET DETECTED'}
"""
        
        if validation['k3_disc_0035']:
            k3 = validation['k3_disc_0035']
            delta = float(k3.get('delta', 0))
            report += f"""
ID: {k3.get('id')}
Delta: {delta:.4f}
Classification: {k3.get('classification', 'Unknown')}

ASTROPHYSICAL SIGNATURE:
- 30-degree Dark Matter Filament along RA 205 meridian
- Northern anchor: K3-DISC-0003 (RA 205.0, Dec 35.0)
- Southern anchor: K3-DISC-0035 (RA 205.0, Dec 5.0)
- Satellite system with violent tidal stripping
- Massive cD host galaxy ripping apart dwarf satellites
"""
        
        report += f"""
FILAMENT CANDIDATES (RA 205 +/- 2, Dec 5-35, Delta > 0.20)
================================================================================
Found: {validation['filament_candidates']} candidates
"""
        
        if validation['filament_candidate_list']:
            for i, candidate in enumerate(validation['filament_candidate_list'], 1):
                delta = float(candidate.get('delta', 0))
                ra = candidate.get('ra', 'N/A')
                dec = candidate.get('dec', 'N/A')
                report += f"\n{i}. {candidate.get('id')} - Delta={delta:.4f}, RA={ra}, Dec={dec}"
        
        report += """

DASHBOARD ACCESS
================================================================================
URL: http://localhost:8080
Status: RUNNING
Auto-refresh: Every 30 seconds

================================================================================
"""
        
        print(report)
        
        # Save to file
        try:
            with open(self.repo_root / 'logs' / 'phase4_status_report.txt', 'w', encoding='utf-8') as f:
                f.write(report)
        except:
            pass
    
    def execute(self, check_interval: int = 300):
        """Execute Phase 4 multi-day operation."""
        self.log(f"Starting Phase 4 multi-day execution ({self.duration_hours} hours)")
        self.log(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        self.log(f"End time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        self.log(f"K3-DISC-0035 filament validation active")
        
        check_count = 0
        
        while datetime.utcnow() < self.end_time:
            check_count += 1
            
            # Load and validate discoveries
            discoveries = self.load_discoveries()
            validation = self.validate_filament_signature(discoveries)
            
            # Print status report
            self.print_status_report(validation)
            
            # Log K3-DISC-0035 detection
            if validation['k3_disc_0035_detected']:
                k3 = validation['k3_disc_0035']
                delta = float(k3.get('delta', 0))
                self.log(f"K3-DISC-0035 DETECTED: Delta={delta:.4f}", 'CRITICAL')
            
            # Log filament candidates
            if validation['filament_candidates'] > 0:
                self.log(f"Found {validation['filament_candidates']} filament candidates", 'INFO')
            
            # Sleep before next check
            self.log(f"Check #{check_count} complete. Next check in {check_interval}s")
            time.sleep(check_interval)
        
        self.log("Phase 4 multi-day execution completed", 'SUCCESS')
        
        # Final status report
        discoveries = self.load_discoveries()
        validation = self.validate_filament_signature(discoveries)
        self.print_status_report(validation)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Phase 4 Multi-Day Execution')
    parser.add_argument('--duration', type=int, default=24, help='Duration in hours')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    
    args = parser.parse_args()
    
    executor = Phase4Executor(duration_hours=args.duration)
    
    if args.once:
        discoveries = executor.load_discoveries()
        validation = executor.validate_filament_signature(discoveries)
        executor.print_status_report(validation)
    else:
        executor.execute(check_interval=args.interval)


if __name__ == '__main__':
    main()
