#!/usr/bin/env python3
"""
Compile PHASE4_FORMAL_REPORT_MASTER.tex to PDF using subprocess.
Handles MiKTeX installation detection and pdflatex execution.
"""

import subprocess
import sys
import os
from pathlib import Path

def find_pdflatex():
    """Find pdflatex executable in common MiKTeX installation paths."""
    common_paths = [
        r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe",
        r"C:\Program Files (x86)\MiKTeX\miktex\bin\pdflatex.exe",
        r"D:\MiKTeX\miktex\bin\x64\pdflatex.exe",
        r"D:\MiKTeX\miktex\bin\pdflatex.exe",
    ]
    
    for path in common_paths:
        if Path(path).exists():
            return path
    
    # Try to find via registry or environment
    try:
        result = subprocess.run(
            ["where", "pdflatex"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except Exception:
        pass
    
    return None

def compile_pdf(tex_file, output_dir=None):
    """Compile TeX file to PDF using pdflatex (twice for TOC)."""
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_dir)
    
    tex_path = output_dir / tex_file
    if not tex_path.exists():
        print(f"ERROR: {tex_path} not found")
        return False
    
    pdflatex = find_pdflatex()
    if not pdflatex:
        print("ERROR: pdflatex not found. Install MiKTeX and try again.")
        return False
    
    print(f"Found pdflatex: {pdflatex}")
    print(f"Compiling: {tex_path}")
    
    # First pass
    print("\n[PASS 1] Compiling for references...")
    try:
        result = subprocess.run(
            [pdflatex, "-interaction=nonstopmode", str(tex_path)],
            cwd=str(output_dir),
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode != 0:
            print("STDERR:", result.stderr[-500:] if result.stderr else "")
            print("STDOUT (last 500 chars):", result.stdout[-500:] if result.stdout else "")
    except subprocess.TimeoutExpired:
        print("ERROR: First pass timed out (120s)")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # Second pass (for TOC)
    print("\n[PASS 2] Compiling for table of contents...")
    try:
        result = subprocess.run(
            [pdflatex, "-interaction=nonstopmode", str(tex_path)],
            cwd=str(output_dir),
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode != 0:
            print("STDERR:", result.stderr[-500:] if result.stderr else "")
            print("STDOUT (last 500 chars):", result.stdout[-500:] if result.stdout else "")
    except subprocess.TimeoutExpired:
        print("ERROR: Second pass timed out (120s)")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    pdf_file = output_dir / tex_file.replace(".tex", ".pdf")
    if pdf_file.exists():
        print(f"\n✅ SUCCESS: {pdf_file}")
        print(f"File size: {pdf_file.stat().st_size / 1024 / 1024:.2f} MB")
        return True
    else:
        print(f"\n❌ FAILED: PDF not generated at {pdf_file}")
        return False

if __name__ == "__main__":
    repo_root = Path(__file__).parent
    success = compile_pdf("PHASE4_FORMAL_REPORT_MASTER.tex", repo_root)
    sys.exit(0 if success else 1)
