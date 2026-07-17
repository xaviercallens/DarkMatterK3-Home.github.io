"""Structured experiment logging and OBSERVATIONAL_REPORT.md auto-update.

Logs all experiments to a structured JSON file with full provenance,
then mechanically updates OBSERVATIONAL_REPORT.md with summary statistics.
"""
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


class ExperimentLogger:
    """Records experiments with full provenance: config, results, git hash, date."""

    def __init__(self, log_path: Path | str = None, repo_root: Path | str = None):
        """
        Parameters
        ----------
        log_path : Path | str
            Path to experiments log JSON. Defaults to logs/experiments.json.
        repo_root : Path | str
            Repository root for git provenance. Defaults to current directory.
        """
        self.repo_root = Path(repo_root or ".")
        self.log_path = Path(log_path or self.repo_root / "logs" / "experiments.json")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        # Load or initialize log
        if self.log_path.exists():
            with open(self.log_path) as f:
                self.experiments = json.load(f)
        else:
            self.experiments = []

    def _get_git_hash(self) -> str:
        """Get current HEAD commit hash."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.stdout.strip()
        except Exception:
            return "unknown"

    def log_experiment(
        self,
        experiment_type: str,
        config: dict,
        results: dict,
        label: str = "SYNTHETIC",
    ) -> None:
        """Log an experiment with full provenance.

        Parameters
        ----------
        experiment_type : str
            Type of experiment (e.g., "power_curve", "calibration", "scale_mixing")
        config : dict
            Experiment configuration (amplitudes, noise, field size, etc.)
        results : dict
            Results dictionary (power curve, false-positive rates, metrics, etc.)
        label : str
            Result label ("SYNTHETIC", "TEST", or "FIT")
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "git_hash": self._get_git_hash(),
            "experiment_type": experiment_type,
            "config": config,
            "results": results,
            "label": label,
        }
        self.experiments.append(entry)
        self._save()

    def _save(self) -> None:
        """Save experiments to JSON."""
        with open(self.log_path, "w") as f:
            json.dump(self.experiments, f, indent=2)

    def get_summary(self, experiment_type: str = None) -> dict:
        """Summarize logged experiments (optionally filtered by type).

        Parameters
        ----------
        experiment_type : str, optional
            Filter to this experiment type

        Returns
        -------
        dict
            Summary with counts, date ranges, result labels
        """
        filtered = self.experiments
        if experiment_type:
            filtered = [e for e in filtered if e["experiment_type"] == experiment_type]

        if not filtered:
            return {"count": 0, "experiments": []}

        labels = [e["label"] for e in filtered]
        git_hashes = set(e["git_hash"] for e in filtered)

        return {
            "count": len(filtered),
            "experiment_type": experiment_type or "all",
            "date_range": {
                "earliest": filtered[0]["timestamp"],
                "latest": filtered[-1]["timestamp"],
            },
            "label_distribution": {
                "SYNTHETIC": labels.count("SYNTHETIC"),
                "TEST": labels.count("TEST"),
                "FIT": labels.count("FIT"),
            },
            "git_commits_involved": list(git_hashes),
        }


class ObservationalReportWriter:
    """Auto-generates OBSERVATIONAL_REPORT.md from experiment logs."""

    def __init__(
        self,
        report_path: Path | str = None,
        log_path: Path | str = None,
        repo_root: Path | str = None,
    ):
        """
        Parameters
        ----------
        report_path : Path | str
            Path to OBSERVATIONAL_REPORT.md. Defaults to repo root.
        log_path : Path | str
            Path to experiments.json log.
        repo_root : Path | str
            Repository root.
        """
        self.repo_root = Path(repo_root or ".")
        self.report_path = Path(report_path or self.repo_root / "OBSERVATIONAL_REPORT.md")
        self.logger = ExperimentLogger(log_path, repo_root)

    def write_report_stub(self) -> None:
        """Write a stub report (to be filled in by T0 after analysis)."""
        summary = self.logger.get_summary()

        stub = f"""# OBSERVATIONAL_REPORT.md — Stream 3 Experimentation Results

**Status:** EXPERIMENTAL SUMMARY (draft, pending T0 analysis)

## Summary
- **Total experiments logged:** {summary.get('count', 0)}
- **Label distribution:** {summary.get('label_distribution', {})}
- **Git commits:** {', '.join(summary.get('git_commits_involved', ['unknown']))}
- **Date range:** {summary.get('date_range', {}).get('earliest', 'N/A')} to {summary.get('date_range', {}).get('latest', 'N/A')}

## Experiment Log
Structured log: `logs/experiments.json`

Each entry contains:
- `timestamp`: when the experiment ran
- `git_hash`: commit at time of run
- `experiment_type`: power curve, calibration, scale mixing, etc.
- `config`: experimental configuration
- `results`: computed metrics
- `label`: SYNTHETIC (pre-pin), TEST (post-pin synthetic), or FIT (post-pin real)

## Interpretation
*Awaiting T0 review and analysis per EXECUTION_PLAN.md WP S3-03.*

---

*Auto-generated by pipeline.experiment_log.ObservationalReportWriter.*
"""

        with open(self.report_path, "w") as f:
            f.write(stub)

    def write_summary_table(self) -> None:
        """Append a summary table of key metrics (power, calibration, effect sizes)."""
        # Placeholder: full implementation requires aggregating across experiments
        # For now, write the stub and let T0 fill in the table
        self.write_report_stub()
