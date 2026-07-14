#!/usr/bin/env python3
"""
Phase 4 Discovery Dashboard Server
Runs on port 8080 and displays real-time K3-DISC-0035 filament detection
"""

import json
import os
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

REPO_ROOT = Path(__file__).parent
DISCOVERIES_FILE = REPO_ROOT / 'discoveries.json'
PORT = 8080

class DashboardHandler(SimpleHTTPRequestHandler):
    """HTTP handler for dashboard requests."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.generate_dashboard().encode('utf-8'))
        elif self.path == '/api/discoveries':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_discoveries_json().encode('utf-8'))
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_status_json().encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def load_discoveries(self):
        """Load discoveries from JSON file."""
        if not DISCOVERIES_FILE.exists():
            return []
        
        try:
            with open(DISCOVERIES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return []
    
    def get_discoveries_json(self):
        """Get discoveries as JSON."""
        discoveries = self.load_discoveries()
        
        # Sort by delta descending
        discoveries_sorted = sorted(
            discoveries,
            key=lambda x: float(x.get('delta', 0)),
            reverse=True
        )
        
        # Check for K3-DISC-0035
        k3_disc_0035 = next(
            (d for d in discoveries if d.get('id') == 'K3-DISC-0035'),
            None
        )
        
        return json.dumps({
            'total': len(discoveries),
            'k3_disc_0035_found': k3_disc_0035 is not None,
            'k3_disc_0035': k3_disc_0035,
            'top_anomalies': discoveries_sorted[:20],
            'timestamp': datetime.utcnow().isoformat()
        }, ensure_ascii=False, indent=2)
    
    def get_status_json(self):
        """Get system status as JSON."""
        discoveries = self.load_discoveries()
        
        # Count by delta threshold
        critical = sum(1 for d in discoveries if float(d.get('delta', 0)) > 0.30)
        high = sum(1 for d in discoveries if 0.25 < float(d.get('delta', 0)) <= 0.30)
        medium = sum(1 for d in discoveries if 0.15 < float(d.get('delta', 0)) <= 0.25)
        
        return json.dumps({
            'total_discoveries': len(discoveries),
            'critical_anomalies': critical,
            'high_anomalies': high,
            'medium_anomalies': medium,
            'timestamp': datetime.utcnow().isoformat()
        }, ensure_ascii=False, indent=2)
    
    def generate_dashboard(self):
        """Generate HTML dashboard."""
        discoveries = self.load_discoveries()
        
        # Sort by delta
        discoveries_sorted = sorted(
            discoveries,
            key=lambda x: float(x.get('delta', 0)),
            reverse=True
        )
        
        # Check for K3-DISC-0035
        k3_disc_0035 = next(
            (d for d in discoveries if d.get('id') == 'K3-DISC-0035'),
            None
        )
        
        # Count by threshold
        critical = sum(1 for d in discoveries if float(d.get('delta', 0)) > 0.30)
        high = sum(1 for d in discoveries if 0.25 < float(d.get('delta', 0)) <= 0.30)
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Phase 4 Discovery Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="30">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #00ff88;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{
            color: #00ffff;
            text-shadow: 0 0 20px #00ffff;
            margin-bottom: 20px;
            font-size: 2.5em;
        }}
        .status-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .status-card {{
            background: rgba(26, 31, 58, 0.8);
            border: 2px solid #00ff88;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .status-card h3 {{
            color: #00ffff;
            margin-bottom: 10px;
            font-size: 0.9em;
        }}
        .status-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #ff00ff;
        }}
        .critical-card {{
            border-color: #ff0000;
            background: rgba(58, 26, 26, 0.8);
        }}
        .critical-card .status-value {{
            color: #ff0000;
        }}
        .high-card {{
            border-color: #ffff00;
            background: rgba(58, 58, 26, 0.8);
        }}
        .high-card .status-value {{
            color: #ffff00;
        }}
        .k3-alert {{
            background: linear-gradient(90deg, #ff00ff, #00ffff);
            color: #0a0e27;
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 10px;
            font-weight: bold;
            text-align: center;
            font-size: 1.3em;
            box-shadow: 0 0 30px #ff00ff;
        }}
        .anomaly-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .anomaly-card {{
            background: rgba(26, 31, 58, 0.9);
            border: 2px solid #00ff88;
            padding: 15px;
            border-radius: 8px;
            transition: all 0.3s;
        }}
        .anomaly-card:hover {{
            border-color: #00ffff;
            box-shadow: 0 0 20px #00ffff;
            transform: translateY(-5px);
        }}
        .anomaly-id {{
            color: #00ffff;
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 8px;
        }}
        .anomaly-delta {{
            color: #ff00ff;
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 8px;
        }}
        .anomaly-coords {{
            color: #00ff88;
            font-size: 0.85em;
            margin-bottom: 5px;
        }}
        .anomaly-class {{
            color: #ffff00;
            font-size: 0.85em;
        }}
        .k3-highlight {{
            border: 3px solid #ff00ff;
            background: rgba(42, 26, 58, 0.95);
            box-shadow: 0 0 20px #ff00ff;
        }}
        .k3-highlight .anomaly-id {{
            color: #ff00ff;
            text-shadow: 0 0 10px #ff00ff;
        }}
        .footer {{
            color: #888;
            font-size: 0.8em;
            margin-top: 30px;
            text-align: center;
            padding-top: 20px;
            border-top: 1px solid #00ff88;
        }}
        .section-title {{
            color: #00ffff;
            font-size: 1.3em;
            margin-top: 30px;
            margin-bottom: 15px;
            text-shadow: 0 0 10px #00ffff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Phase 4 Discovery Dashboard</h1>
"""
        
        # K3-DISC-0035 alert if found
        if k3_disc_0035:
            delta = float(k3_disc_0035.get('delta', 0))
            html += f"""
        <div class="k3-alert">
            🌌 MAJOR DISCOVERY: K3-DISC-0035 DETECTED
            <br>
            30° Dark Matter Filament along RA 205° Meridian
            <br>
            Delta = {delta:.4f} | Satellite System with Tidal Stripping
        </div>
"""
        
        # Status cards
        html += """
        <div class="status-grid">
"""
        html += f"""
            <div class="status-card">
                <h3>Total Discoveries</h3>
                <div class="status-value">{len(discoveries)}</div>
            </div>
            <div class="status-card critical-card">
                <h3>Critical (Δ > 0.30)</h3>
                <div class="status-value">{critical}</div>
            </div>
            <div class="status-card high-card">
                <h3>High (Δ > 0.25)</h3>
                <div class="status-value">{high}</div>
            </div>
            <div class="status-card">
                <h3>K3-DISC-0035</h3>
                <div class="status-value">{'✓' if k3_disc_0035 else '✗'}</div>
            </div>
        </div>
"""
        
        # Anomalies section
        html += """
        <div class="section-title">Top 20 Anomalies</div>
        <div class="anomaly-grid">
"""
        
        for discovery in discoveries_sorted[:20]:
            is_k3 = discovery.get('id') == 'K3-DISC-0035'
            card_class = 'anomaly-card k3-highlight' if is_k3 else 'anomaly-card'
            delta = float(discovery.get('delta', 0))
            
            html += f"""
            <div class="{card_class}">
                <div class="anomaly-id">{discovery.get('id', 'Unknown')}</div>
                <div class="anomaly-delta">Δ = {delta:.4f}</div>
                <div class="anomaly-coords">RA {discovery.get('ra', 'N/A')}°, Dec {discovery.get('dec', 'N/A')}°</div>
                <div class="anomaly-class">{discovery.get('classification', 'Unknown')}</div>
            </div>
"""
        
        html += """
        </div>
        <div class="footer">
            Last updated: """ + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC') + """
            <br>
            Auto-refresh every 30 seconds
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def run_server():
    """Run the dashboard server."""
    server = HTTPServer(('0.0.0.0', PORT), DashboardHandler)
    print(f"Phase 4 Dashboard Server running on http://localhost:{PORT}")
    print(f"Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.shutdown()


if __name__ == '__main__':
    run_server()
