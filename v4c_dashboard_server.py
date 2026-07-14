#!/usr/bin/env python3
"""
v4c_dashboard_server.py
=========================
Live comparison dashboard for the V4C multi-hypothesis pipeline.
Serves on port 8092. Reads logs/v4c_pipeline_results.json (written
incrementally by v4c_multi_hypothesis_pipeline.py) and renders a live
Chart.js comparison of Delta across the 4 hypotheses (legacy S12/S21,
t103, Cooper s7, Cooper s10), plus a running statistical scorecard.
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
    "legacy_S12_S21": "S12/S21 (legacy, REJECTED)",
    "t103_A276536": "t103 (A276536)",
    "cooper_s7_A183204": "Cooper s7 (A183204)",
    "cooper_s10_A005260": "Cooper s10 (A005260)",
}
HYP_COLORS = {
    "legacy_S12_S21": "#d62728",
    "t103_A276536": "#1f77b4",
    "cooper_s7_A183204": "#ff7f0e",
    "cooper_s10_A005260": "#2ca02c",
}

DELTA_REF_THEORETICAL = 0.327
OBSERVED_DELTA_MEAN_HISTORICAL = 1.1244


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
    return scorecard


class V4CHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self._send_html(self.render_dashboard())
        elif self.path == "/api/v4c_status":
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

        best = None
        best_cv = float("inf")
        for name in ["t103_A276536", "cooper_s7_A183204", "cooper_s10_A005260"]:
            sc = scorecard.get(name, {})
            if sc.get("n", 0) > 3 and sc.get("cv", float("inf")) < best_cv:
                best_cv = sc["cv"]
                best = name

        return json.dumps({
            "total_sectors": len(history),
            "scorecard": scorecard,
            "most_stable_k3_hypothesis": best,
            "delta_ref_theoretical": DELTA_REF_THEORETICAL,
            "observed_delta_mean_historical": OBSERVED_DELTA_MEAN_HISTORICAL,
            "series": {
                name: [r["hypotheses"][name]["delta"] for r in history if name in r.get("hypotheses", {})]
                for name in HYP_NAMES
            },
            "sector_indices": [r["sector_index"] for r in history],
            "timestamp": datetime.utcnow().isoformat(),
        }, ensure_ascii=False)

    def render_dashboard(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>V4C Multi-Hypothesis Comparison Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; background:#0d1117; color:#c9d1d9; margin:0; padding:20px; }
h1 { color:#58a6ff; }
.grid { display:grid; grid-template-columns: 1fr 1fr; gap:20px; }
.card { background:#161b22; border:1px solid #30363d; border-radius:8px; padding:16px; }
table { width:100%; border-collapse:collapse; }
th, td { padding:6px 10px; text-align:left; border-bottom:1px solid #30363d; font-size:13px; }
th { color:#8b949e; }
.badge { padding:2px 8px; border-radius:4px; font-size:11px; font-weight:bold; }
.rejected { background:#5c1e1e; color:#ff7b72; }
.k3 { background:#1e5c2e; color:#7bffa0; }
#conclusion { font-size:15px; line-height:1.6; }
</style>
</head>
<body>
<h1>&#128301; V4C: Multi-Hypothesis Comparison Dashboard</h1>
<p>Real-time comparison of S12/S21 (legacy, rejected) vs t103/Cooper-s7/Cooper-s10 (GATE-C K3-type finalists) processed over Euclid/SDSS-style sectors at scale.</p>
<div class="grid">
  <div class="card">
    <h3>Delta Time Series by Hypothesis</h3>
    <canvas id="deltaChart" height="220"></canvas>
  </div>
  <div class="card">
    <h3>Scorecard (mean, std, coefficient of variation)</h3>
    <table id="scoreTable"><thead><tr><th>Hypothesis</th><th>n</th><th>Mean &Delta;</th><th>Std</th><th>CV</th><th>Elevation</th></tr></thead><tbody></tbody></table>
  </div>
</div>
<div class="card" style="margin-top:20px;">
  <h3>Live Conclusion</h3>
  <div id="conclusion">Awaiting data...</div>
</div>

<script>
const HYP_LABELS = {
  "legacy_S12_S21": "S12/S21 (legacy, REJECTED)",
  "t103_A276536": "t103 (A276536)",
  "cooper_s7_A183204": "Cooper s7 (A183204)",
  "cooper_s10_A005260": "Cooper s10 (A005260)",
};
const HYP_COLORS = {
  "legacy_S12_S21": "#d62728",
  "t103_A276536": "#1f77b4",
  "cooper_s7_A183204": "#ff7f0e",
  "cooper_s10_A005260": "#2ca02c",
};

let chart = null;

function initChart() {
  const ctx = document.getElementById('deltaChart').getContext('2d');
  chart = new Chart(ctx, {
    type: 'line',
    data: { labels: [], datasets: Object.keys(HYP_LABELS).map(k => ({
      label: HYP_LABELS[k], borderColor: HYP_COLORS[k], backgroundColor: HYP_COLORS[k],
      data: [], fill: false, tension: 0.2, pointRadius: 1,
    })) },
    options: { responsive: true, scales: { y: { title: { display: true, text: 'Delta' } } },
      plugins: { legend: { labels: { color: '#c9d1d9' } } } }
  });
}

async function refresh() {
  const res = await fetch('/api/v4c_status');
  const data = await res.json();

  if (chart) {
    chart.data.labels = data.sector_indices;
    chart.data.datasets.forEach(ds => {
      const key = Object.keys(HYP_LABELS).find(k => HYP_LABELS[k] === ds.label);
      ds.data = data.series[key] || [];
    });
    chart.update();
  }

  const tbody = document.querySelector('#scoreTable tbody');
  tbody.innerHTML = '';
  for (const [key, label] of Object.entries(HYP_LABELS)) {
    const sc = data.scorecard[key] || {};
    const row = document.createElement('tr');
    row.innerHTML = `<td>${label}</td><td>${sc.n || 0}</td><td>${(sc.mean||0).toFixed(4)}</td>` +
      `<td>${(sc.std||0).toFixed(4)}</td><td>${(sc.cv||0).toFixed(4)}</td><td>${(sc.elevation_vs_ref||0).toFixed(2)}x</td>`;
    tbody.appendChild(row);
  }

  const best = data.most_stable_k3_hypothesis;
  const conclEl = document.getElementById('conclusion');
  if (data.total_sectors < 4) {
    conclEl.textContent = `Collecting data (${data.total_sectors} sectors processed so far)...`;
  } else {
    conclEl.innerHTML = `Processed <b>${data.total_sectors}</b> sectors. ` +
      (best ? `Among the GATE-C K3-type finalists, <b>${HYP_LABELS[best]}</b> currently shows the ` +
      `lowest coefficient of variation (most stable Delta signal across independent sectors), ` +
      `a phenomenological indicator of relative structural consistency. ` : '') +
      `<br><br><i>Caveat: per Part VIII &sect;1.5, the empirical Delta signal does not by itself ` +
      `rigorously discriminate the correct K3 substrate (physics gates non-discriminating at ` +
      `common normalization). This ranking is a phenomenological cross-check, not a formal proof.</i>`;
  }
}

initChart();
refresh();
setInterval(refresh, 3000);
</script>
</body>
</html>"""


def main():
    server = HTTPServer(("0.0.0.0", PORT), V4CHandler)
    print(f"V4C Dashboard running at http://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
