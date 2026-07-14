#!/usr/bin/env python3
"""
Automated Discovery Analyzer for Phase 4 Multi-Day Execution

Monitors discoveries.json in real-time, analyzes anomalies for:
- K3-DISC-0035 filament signature (30° RA 205° meridian)
- Tidal stripping indicators (satellite systems with high Δ)
- Quorum consensus status
- Generates alerts and analysis reports
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import hashlib
import time

class DiscoveryAnalyzer:
    """Analyzes discoveries for K3/T2 signatures and anomalies."""
    
    # K3-DISC-0035 reference (30° filament along RA 205°)
    K3_DISC_0035_RA = 205.0
    K3_DISC_0035_DEC = 5.0
    K3_DISC_0003_RA = 205.0
    K3_DISC_0003_DEC = 35.0
    FILAMENT_RA_TOLERANCE = 2.0  # ±2° in RA
    FILAMENT_DEC_SPAN = 30.0     # 30° span from Dec 35° to Dec 5°
    
    # Alert thresholds
    DELTA_CRITICAL = 0.30        # High anomaly
    DELTA_SIGNIFICANT = 0.25     # Moderate anomaly
    DELTA_INTERESTING = 0.15     # Interesting but not critical
    
    def __init__(self, repo_root: str = None):
        """Initialize analyzer with repo root path."""
        if repo_root is None:
            repo_root = Path(__file__).parent
        else:
            repo_root = Path(repo_root)
        
        self.repo_root = repo_root
        self.discoveries_file = repo_root / 'discoveries.json'
        self.alerts_file = repo_root / 'logs' / 'discovery_alerts.log'
        self.analysis_file = repo_root / 'logs' / 'discovery_analysis.json'
        self.last_analyzed_hash = None
        
        # Ensure log directory exists
        self.alerts_file.parent.mkdir(parents=True, exist_ok=True)
    
    def load_discoveries(self) -> List[Dict]:
        """Load discoveries from JSON file."""
        if not self.discoveries_file.exists():
            return []
        
        try:
            with open(self.discoveries_file, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            self.log_alert(f"Error loading discoveries: {e}", level='ERROR')
            return []
    
    def log_alert(self, message: str, level: str = 'INFO'):
        """Log alert message to file and console."""
        timestamp = datetime.utcnow().isoformat()
        alert_entry = f"[{timestamp}] [{level}] {message}"
        
        print(alert_entry)
        
        with open(self.alerts_file, 'a', encoding='utf-8') as f:
            f.write(alert_entry + '\n')
    
    def is_filament_candidate(self, discovery: Dict) -> bool:
        """Check if discovery is part of the RA 205° filament."""
        try:
            ra = float(discovery.get('ra', 0))
            dec = float(discovery.get('dec', 0))
            
            # Check RA proximity to 205°
            ra_match = abs(ra - self.K3_DISC_0035_RA) < self.FILAMENT_RA_TOLERANCE
            
            # Check Dec span (5° to 35°)
            dec_match = self.K3_DISC_0035_DEC <= dec <= self.K3_DISC_0003_DEC
            
            return ra_match and dec_match
        except (ValueError, TypeError):
            return False
    
    def is_tidal_stripping_signature(self, discovery: Dict) -> bool:
        """Check for tidal stripping indicators (satellite system + high Δ)."""
        try:
            classification = discovery.get('classification', '').lower()
            delta = float(discovery.get('delta', 0))
            
            is_satellite = 'satellite' in classification
            is_high_delta = delta > self.DELTA_SIGNIFICANT
            
            return is_satellite and is_high_delta
        except (ValueError, TypeError):
            return False
    
    def analyze_discovery(self, discovery: Dict) -> Dict:
        """Analyze a single discovery for significance."""
        analysis = {
            'id': discovery.get('id'),
            'timestamp': datetime.utcnow().isoformat(),
            'delta': float(discovery.get('delta', 0)),
            'classification': discovery.get('classification', 'unknown'),
            'alerts': []
        }
        
        delta = analysis['delta']
        
        # Check for K3-DISC-0035 specifically
        if discovery.get('id') == 'K3-DISC-0035':
            analysis['alerts'].append({
                'type': 'K3_DISC_0035_DETECTED',
                'severity': 'CRITICAL',
                'message': 'K3-DISC-0035 (30° filament, satellite system, tidal stripping) detected',
                'delta': delta
            })
        
        # Check for filament candidates
        if self.is_filament_candidate(discovery):
            analysis['alerts'].append({
                'type': 'FILAMENT_CANDIDATE',
                'severity': 'HIGH',
                'message': f"Filament candidate along RA 205° meridian (Δ={delta:.4f})",
                'coordinates': {
                    'ra': discovery.get('ra'),
                    'dec': discovery.get('dec')
                }
            })
        
        # Check for tidal stripping
        if self.is_tidal_stripping_signature(discovery):
            analysis['alerts'].append({
                'type': 'TIDAL_STRIPPING',
                'severity': 'HIGH',
                'message': f"Tidal stripping signature: satellite system with Δ={delta:.4f}",
                'classification': analysis['classification']
            })
        
        # Delta-based alerts
        if delta > self.DELTA_CRITICAL:
            analysis['alerts'].append({
                'type': 'CRITICAL_ANOMALY',
                'severity': 'CRITICAL',
                'message': f"Critical anomaly detected (Δ={delta:.4f} > {self.DELTA_CRITICAL})",
                'delta': delta
            })
        elif delta > self.DELTA_SIGNIFICANT:
            analysis['alerts'].append({
                'type': 'SIGNIFICANT_ANOMALY',
                'severity': 'HIGH',
                'message': f"Significant anomaly detected (Δ={delta:.4f} > {self.DELTA_SIGNIFICANT})",
                'delta': delta
            })
        elif delta > self.DELTA_INTERESTING:
            analysis['alerts'].append({
                'type': 'INTERESTING_ANOMALY',
                'severity': 'MEDIUM',
                'message': f"Interesting anomaly detected (Δ={delta:.4f} > {self.DELTA_INTERESTING})",
                'delta': delta
            })
        
        return analysis
    
    def analyze_all_discoveries(self) -> Dict:
        """Analyze all discoveries and generate report."""
        discoveries = self.load_discoveries()
        
        if not discoveries:
            self.log_alert("No discoveries found", level='INFO')
            return {'discoveries': [], 'summary': {}}
        
        # Calculate hash to detect changes
        discoveries_json = json.dumps(discoveries, sort_keys=True)
        current_hash = hashlib.md5(discoveries_json.encode()).hexdigest()
        
        if current_hash == self.last_analyzed_hash:
            return None  # No changes since last analysis
        
        self.last_analyzed_hash = current_hash
        
        # Analyze each discovery
        analyses = []
        critical_alerts = []
        high_alerts = []
        
        for discovery in discoveries:
            analysis = self.analyze_discovery(discovery)
            analyses.append(analysis)
            
            # Collect alerts by severity
            for alert in analysis.get('alerts', []):
                if alert['severity'] == 'CRITICAL':
                    critical_alerts.append(alert)
                elif alert['severity'] == 'HIGH':
                    high_alerts.append(alert)
        
        # Generate summary
        summary = {
            'total_discoveries': len(discoveries),
            'total_analyzed': len(analyses),
            'critical_alerts': len(critical_alerts),
            'high_alerts': len(high_alerts),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Log critical alerts immediately
        for alert in critical_alerts:
            self.log_alert(f"CRITICAL: {alert['message']}", level='CRITICAL')
        
        # Log high alerts
        for alert in high_alerts:
            self.log_alert(f"HIGH: {alert['message']}", level='WARNING')
        
        # Check for K3-DISC-0035 specifically
        k3_disc_0035 = next(
            (d for d in discoveries if d.get('id') == 'K3-DISC-0035'),
            None
        )
        
        if k3_disc_0035:
            delta = float(k3_disc_0035.get('delta', 0))
            self.log_alert(
                f"K3-DISC-0035 DETECTED: Δ={delta:.4f} | "
                f"RA {k3_disc_0035.get('ra')}°, Dec {k3_disc_0035.get('dec')}° | "
                f"30° Dark Matter Filament | Satellite System with Tidal Stripping",
                level='CRITICAL'
            )
            summary['k3_disc_0035_found'] = True
            summary['k3_disc_0035_delta'] = delta
        
        return {
            'analyses': analyses,
            'summary': summary,
            'critical_alerts': critical_alerts,
            'high_alerts': high_alerts
        }
    
    def save_analysis(self, analysis: Dict):
        """Save analysis report to file."""
        if analysis is None:
            return
        
        try:
            with open(self.analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
        except IOError as e:
            self.log_alert(f"Error saving analysis: {e}", level='ERROR')
    
    def generate_html_report(self, analysis: Dict) -> str:
        """Generate HTML report of discoveries and alerts."""
        if not analysis:
            return ""
        
        summary = analysis.get('summary', {})
        critical_alerts = analysis.get('critical_alerts', [])
        high_alerts = analysis.get('high_alerts', [])
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Discovery Analysis Report</title>
    <style>
        body {{ font-family: monospace; background: #0a0e27; color: #00ff88; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        h1 {{ color: #00ffff; text-shadow: 0 0 10px #00ffff; }}
        .summary {{ background: #1a1f3a; border: 1px solid #00ff88; padding: 15px; margin: 15px 0; }}
        .critical {{ background: #3a1a1a; border: 2px solid #ff0000; padding: 15px; margin: 15px 0; }}
        .alert {{ background: #2a2a1a; border: 1px solid #ffff00; padding: 10px; margin: 10px 0; }}
        .k3-highlight {{ background: #2a1a3a; border: 2px solid #ff00ff; padding: 15px; margin: 15px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Discovery Analysis Report</h1>
        <div class="summary">
            <p><strong>Total Discoveries:</strong> {summary.get('total_discoveries', 0)}</p>
            <p><strong>Critical Alerts:</strong> <span style="color: #ff0000;">{summary.get('critical_alerts', 0)}</span></p>
            <p><strong>High Alerts:</strong> <span style="color: #ffff00;">{summary.get('high_alerts', 0)}</span></p>
            <p><strong>Timestamp:</strong> {summary.get('timestamp', 'N/A')}</p>
        </div>
"""
        
        if summary.get('k3_disc_0035_found'):
            html += f"""
        <div class="k3-highlight">
            <h2>🌌 K3-DISC-0035 DETECTED</h2>
            <p><strong>Delta:</strong> {summary.get('k3_disc_0035_delta', 'N/A')}</p>
            <p><strong>Signature:</strong> 30° Dark Matter Filament along RA 205° Meridian</p>
            <p><strong>Classification:</strong> Satellite System with Violent Tidal Stripping</p>
            <p><strong>Astrophysical Insight:</strong> Massive host galaxy ripping apart orbiting dwarf galaxies at southern anchor of supercluster filament</p>
        </div>
"""
        
        if critical_alerts:
            html += "<h2>Critical Alerts</h2>"
            for alert in critical_alerts:
                html += f"""
        <div class="critical">
            <p><strong>{alert.get('type')}:</strong> {alert.get('message')}</p>
        </div>
"""
        
        if high_alerts:
            html += "<h2>High Priority Alerts</h2>"
            for alert in high_alerts[:10]:  # Limit to 10
                html += f"""
        <div class="alert">
            <p><strong>{alert.get('type')}:</strong> {alert.get('message')}</p>
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        return html
    
    def run_continuous(self, interval: int = 300):
        """Run analyzer continuously at specified interval (seconds)."""
        self.log_alert(f"Starting continuous discovery analysis (interval: {interval}s)", level='INFO')
        
        try:
            while True:
                analysis = self.analyze_all_discoveries()
                
                if analysis:
                    self.save_analysis(analysis)
                    
                    # Generate and save HTML report
                    html_report = self.generate_html_report(analysis)
                    report_path = self.repo_root / 'logs' / 'discovery_analysis.html'
                    with open(report_path, 'w') as f:
                        f.write(html_report)
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            self.log_alert("Discovery analyzer stopped by user", level='INFO')
        except Exception as e:
            self.log_alert(f"Analyzer error: {e}", level='ERROR')


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated Discovery Analyzer')
    parser.add_argument('--repo-root', default=None, help='Repository root path')
    parser.add_argument('--interval', type=int, default=300, help='Analysis interval in seconds')
    parser.add_argument('--once', action='store_true', help='Run analysis once and exit')
    
    args = parser.parse_args()
    
    analyzer = DiscoveryAnalyzer(repo_root=args.repo_root)
    
    if args.once:
        analysis = analyzer.analyze_all_discoveries()
        if analysis:
            analyzer.save_analysis(analysis)
            print(json.dumps(analysis, indent=2))
    else:
        analyzer.run_continuous(interval=args.interval)


if __name__ == '__main__':
    main()
