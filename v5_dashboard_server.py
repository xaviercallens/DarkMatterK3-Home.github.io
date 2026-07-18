#!/usr/bin/env python3
"""
v5_dashboard_server.py
=========================
Live comparison dashboard for the V5 multi-hypothesis pipeline.
Serves on port 8092. Reads logs/v4c_pipeline_results.json and renders
a stunning live Chart.js comparison.
"""

import json
import statistics
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

REPO_ROOT = Path(__file__).parent
RESULTS_FILE = REPO_ROOT / "logs" / "v4c_pipeline_results.json"
PORT = 8092

HYP_NAMES = ["legacy_S12_S21", "t103_A276536", "cooper_s7_A183204", "cooper_s10_A005260"]
HYP_LABELS = {
    "legacy_S12_S21": "S12/S21 (Legacy)",
    "t103_A276536": "t103 (A276536)",
    "cooper_s7_A183204": "Cooper s7 (A183204)",
    "cooper_s10_A005260": "Cooper s10 (A005260)",
}

DUAL_SCALE_NAMES = ["H1_CDM_Subhalo", "H4_K3_Vacuum"]
DUAL_SCALE_LABELS = {
    "H1_CDM_Subhalo": "H1: CDM Subhalo",
    "H4_K3_Vacuum": "H4: K3 Vacuum",
}

DELTA_REF_THEORETICAL = 0.327

def load_results():
    if not RESULTS_FILE.exists():
        return []
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def compute_scorecard(history):
    scorecard = {}
    for name in HYP_NAMES:
        deltas = [r["hypotheses"][name]["delta"] for r in history if name in r.get("hypotheses", {})]
        if not deltas:
            scorecard[name] = {"n": 0}
            continue
        mean = statistics.mean(deltas)
        std = statistics.pstdev(deltas) if len(deltas) > 1 else 0.0
        cv = (std / mean) if mean else 0.0
        elevation = mean / DELTA_REF_THEORETICAL if DELTA_REF_THEORETICAL else 0.0
        scorecard[name] = {
            "n": len(deltas), "mean": mean, "std": std, "cv": cv,
            "elevation_vs_ref": elevation,
            "min": min(deltas), "max": max(deltas),
        }
    for name in DUAL_SCALE_NAMES:
        scores = [r["hypotheses"][name]["score"] for r in history if name in r.get("hypotheses", {}) and "score" in r["hypotheses"][name]]
        if not scores:
            scorecard[name] = {"n": 0}
            continue
        mean = statistics.mean(scores)
        std = statistics.pstdev(scores) if len(scores) > 1 else 0.0
        cv = (std / mean) if mean else 0.0
        scorecard[name] = {
            "n": len(scores), "mean": mean, "std": std, "cv": cv,
            "elevation_vs_ref": 0,
            "min": min(scores), "max": max(scores),
        }
    return scorecard

class V5Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self._send_html(self.render_dashboard())
        elif self.path == "/api/v5_status":
            self._send_json(self.render_status_json())
        else:
            self.send_response(404)
            self.end_headers()

    def _send_html(self, body):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def _send_json(self, body):
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def render_status_json(self):
        history = load_results()
        scorecard = compute_scorecard(history)
        
        series = {}
        for name in HYP_NAMES:
            series[name] = [r["hypotheses"][name]["delta"] for r in history if name in r.get("hypotheses", {})]
        for name in DUAL_SCALE_NAMES:
            series[name] = [r["hypotheses"][name]["score"] for r in history if name in r.get("hypotheses", {}) and "score" in r["hypotheses"][name]]

        return json.dumps({
            "total_sectors": len(history),
            "scorecard": scorecard,
            "series": series,
            "sector_indices": [r["sector_index"] for r in history],
            "data_sources": [r.get("source", "Unknown") for r in history],
            "timestamp": datetime.utcnow().isoformat(),
        }, ensure_ascii=False)

    def render_dashboard(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>V5 Dual-Scale Pipeline Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
<style>
:root {
  --bg-gradient: linear-gradient(135deg, #09090e 0%, #11111c 100%);
  --glass-bg: rgba(255, 255, 255, 0.03);
  --glass-border: rgba(255, 255, 255, 0.08);
  --accent-blue: #3b82f6;
  --accent-purple: #8b5cf6;
  --text-main: #e2e8f0;
  --text-muted: #94a3b8;
}

* { box-sizing: border-box; }

body { 
  font-family: 'Inter', sans-serif; 
  background: var(--bg-gradient); 
  color: var(--text-main); 
  margin: 0; 
  padding: 30px; 
  min-height: 100vh;
}

h1 { 
  font-weight: 800; 
  font-size: 2.5rem;
  background: linear-gradient(to right, #60a5fa, #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 10px;
}

.subtitle {
  color: var(--text-muted);
  font-size: 1.1rem;
  margin-bottom: 40px;
  font-weight: 300;
}

.grid { 
  display: grid; 
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); 
  gap: 30px; 
}

.card { 
  background: var(--glass-bg); 
  border: 1px solid var(--glass-border); 
  border-radius: 16px; 
  padding: 24px; 
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.4);
}

.card h3 {
  margin-top: 0;
  font-weight: 600;
  color: #fff;
  border-bottom: 1px solid var(--glass-border);
  padding-bottom: 12px;
  margin-bottom: 20px;
}

table { 
  width: 100%; 
  border-collapse: collapse; 
}

th, td { 
  padding: 12px; 
  text-align: left; 
  border-bottom: 1px solid var(--glass-border); 
  font-size: 14px; 
}

th { 
  color: var(--text-muted); 
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 12px;
}

tr:hover {
  background: rgba(255, 255, 255, 0.02);
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--glass-bg);
  border-radius: 50px;
  border: 1px solid var(--glass-border);
  font-weight: 600;
  margin-bottom: 30px;
  animation: pulse 2s infinite;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 10px #10b981;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.stat-val { font-weight: 600; color: #fff; }
</style>
</head>
<body>

<div class="status-indicator">
  <div class="dot"></div>
  <span id="pipelineStatus">Connecting to Pipeline...</span>
</div>

<h1>V5 Euclid Dual-Scale Pipeline</h1>
<p class="subtitle">Live tracking of topological anomalies and subhalo interactions across observational Euclid/SDSS sectors.</p>

<div class="grid">
  <div class="card">
    <h3>K3 Topology Asymmetry (&Delta;)</h3>
    <canvas id="deltaChart" height="250"></canvas>
  </div>
  <div class="card">
    <h3>Dual-Scale Hypothesis Scores</h3>
    <canvas id="dualChart" height="250"></canvas>
  </div>
</div>

<div class="card" style="margin-top:30px;">
  <h3>Live Metrics Scorecard</h3>
  <table id="scoreTable">
    <thead>
      <tr>
        <th>Hypothesis / Model</th>
        <th>Processed</th>
        <th>Mean Value</th>
        <th>Std Dev</th>
        <th>Var Coeff (CV)</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>
</div>

<script>
const HYP_LABELS = {
  "legacy_S12_S21": "S12/S21 (Legacy)",
  "t103_A276536": "t103 (A276536)",
  "cooper_s7_A183204": "Cooper s7",
  "cooper_s10_A005260": "Cooper s10",
};

const DUAL_SCALE_LABELS = {
  "H1_CDM_Subhalo": "H1: CDM Subhalo",
  "H4_K3_Vacuum": "H4: K3 Vacuum",
};

const COLORS = {
  "legacy_S12_S21": "#ef4444",
  "t103_A276536": "#3b82f6",
  "cooper_s7_A183204": "#f59e0b",
  "cooper_s10_A005260": "#10b981",
  "H1_CDM_Subhalo": "#8b5cf6",
  "H4_K3_Vacuum": "#ec4899",
};

let deltaChart = null;
let dualChart = null;

Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = 'Inter';

function initCharts() {
  const ctxDelta = document.getElementById('deltaChart').getContext('2d');
  deltaChart = new Chart(ctxDelta, {
    type: 'line',
    data: { 
      labels: [], 
      datasets: Object.keys(HYP_LABELS).map(k => ({
        label: HYP_LABELS[k], 
        borderColor: COLORS[k], 
        backgroundColor: COLORS[k] + '20',
        data: [], fill: true, tension: 0.4, pointRadius: 2,
        borderWidth: 2
      })) 
    },
    options: { 
      responsive: true, 
      scales: { 
        y: { grid: { color: 'rgba(255,255,255,0.05)' } },
        x: { grid: { color: 'rgba(255,255,255,0.05)' } }
      },
      plugins: { legend: { position: 'top' } } 
    }
  });

  const ctxDual = document.getElementById('dualChart').getContext('2d');
  dualChart = new Chart(ctxDual, {
    type: 'bar',
    data: { 
      labels: [], 
      datasets: Object.keys(DUAL_SCALE_LABELS).map(k => ({
        label: DUAL_SCALE_LABELS[k], 
        backgroundColor: COLORS[k], 
        data: [], borderRadius: 4,
      })) 
    },
    options: { 
      responsive: true, 
      scales: { 
        y: { grid: { color: 'rgba(255,255,255,0.05)' } },
        x: { grid: { color: 'rgba(255,255,255,0.05)' } }
      },
      plugins: { legend: { position: 'top' } } 
    }
  });
}

async function refresh() {
  try {
    const res = await fetch('/api/v5_status');
    const data = await res.json();

    document.getElementById('pipelineStatus').innerHTML = `Live: <b>${data.total_sectors}</b> sectors processed. Latest source: <b>${data.data_sources[data.data_sources.length - 1] || 'None'}</b>`;

    if (deltaChart) {
      deltaChart.data.labels = data.sector_indices;
      deltaChart.data.datasets.forEach(ds => {
        const key = Object.keys(HYP_LABELS).find(k => HYP_LABELS[k] === ds.label);
        ds.data = data.series[key] || [];
      });
      deltaChart.update();
    }

    if (dualChart) {
      dualChart.data.labels = data.sector_indices;
      dualChart.data.datasets.forEach(ds => {
        const key = Object.keys(DUAL_SCALE_LABELS).find(k => DUAL_SCALE_LABELS[k] === ds.label);
        ds.data = data.series[key] || [];
      });
      dualChart.update();
    }

    const tbody = document.querySelector('#scoreTable tbody');
    tbody.innerHTML = '';
    const allLabels = {...HYP_LABELS, ...DUAL_SCALE_LABELS};
    
    for (const [key, label] of Object.entries(allLabels)) {
      const sc = data.scorecard[key] || {};
      const row = document.createElement('tr');
      row.innerHTML = `
        <td><span style="color:${COLORS[key]};font-weight:bold;margin-right:8px;">&bull;</span> ${label}</td>
        <td>${sc.n || 0}</td>
        <td class="stat-val">${(sc.mean||0).toFixed(4)}</td>
        <td>${(sc.std||0).toFixed(4)}</td>
        <td>${(sc.cv||0).toFixed(4)}</td>
      `;
      tbody.appendChild(row);
    }
  } catch(e) {
    document.getElementById('pipelineStatus').innerHTML = `Error connecting to pipeline data...`;
  }
}

initCharts();
refresh();
setInterval(refresh, 3000);
</script>
</body>
</html>"""

def main():
    server = HTTPServer(("0.0.0.0", PORT), V5Handler)
    print(f"V5 Dashboard running at http://localhost:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    main()
