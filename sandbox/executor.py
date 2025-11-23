"""Safe code execution for scratchpad snippets (skeleton)."""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict


def run_snippet(path: Path, logs_dir: Path, timeout: int = 10) -> Dict:
    logs_dir.mkdir(parents=True, exist_ok=True)
    output_file = logs_dir / f"exec_{path.stem}_{datetime.utcnow().timestamp()}.log"
    with output_file.open("w", encoding="utf-8") as f:
        try:
            proc = subprocess.run(
                [sys.executable, str(path)],
                stdout=f,
                stderr=subprocess.STDOUT,
                timeout=timeout,
                check=False,
            )
            exit_code = proc.returncode
        except subprocess.TimeoutExpired:
            f.write("Execution timed out\n")
            exit_code = -1
    return {
        "file": str(path),
        "output_path": str(output_file),
        "exit_code": exit_code,
        "started_at": datetime.utcnow().isoformat() + "Z",
    }
