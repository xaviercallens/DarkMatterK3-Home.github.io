"""Gate G1 control-example tests (golden-good pinned / golden-bad unpinned)."""
import hashlib

import pytest

import pipeline.gate as gate


def _write_prediction(path, body: str, pin: bool):
    if pin:
        sha = hashlib.sha256(body.encode()).hexdigest()
        text = f"PINNED: {sha}\n{body}"
    else:
        text = body
    path.write_text(text)


def test_unpinned_prediction_blocks_real_data(tmp_path, monkeypatch):
    p = tmp_path / "PREDICTION.md"
    _write_prediction(p, "Status: draft\n", pin=False)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    assert gate.is_pinned() is False
    with pytest.raises(gate.GateError):
        gate.require_pinned_for_real_data()


def test_pinned_prediction_with_valid_hash_opens_gate(tmp_path, monkeypatch):
    p = tmp_path / "PREDICTION.md"
    _write_prediction(p, "Status: frozen\nm_phi: 1e-23 eV\n", pin=True)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    assert gate.is_pinned() is True
    assert gate.verify_pin_hash() is True
    gate.require_pinned_for_real_data()  # must not raise


def test_pinned_header_with_tampered_body_fails_hash_check(tmp_path, monkeypatch):
    p = tmp_path / "PREDICTION.md"
    _write_prediction(p, "Status: frozen\nm_phi: 1e-23 eV\n", pin=True)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    # Tamper with the body after pinning without updating the hash.
    tampered = p.read_text().replace("1e-23 eV", "1e-20 eV")
    p.write_text(tampered)

    assert gate.is_pinned() is True  # header still present
    assert gate.verify_pin_hash() is False  # but content no longer matches


def test_missing_prediction_file_is_unpinned(tmp_path, monkeypatch):
    monkeypatch.setattr(gate, "PREDICTION_PATH", tmp_path / "does_not_exist.md")
    assert gate.is_pinned() is False
