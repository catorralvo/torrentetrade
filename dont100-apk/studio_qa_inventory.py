#!/usr/bin/env python3
"""Produce an auditable, machine-readable DON'T 100 QA inventory.
Reports observations without claiming that 36 games have been played.
"""
from pathlib import Path
import hashlib
import json
import re

path=Path("dont100-apk/app/src/main/assets/index.html")
html=path.read_text(encoding="utf-8")
functions=sorted(set(re.findall(r"function\s+(run[A-Za-z0-9_]+)\s*\(",html)))
report={
 "scope":"static inventory, not interactive gameplay validation",
 "payload_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
 "payload_bytes":path.stat().st_size,
 "game_functions":functions,
 "game_function_count":len(functions),
 "build_marker":"4.3.1-gameplayfix" if "4.3.1-gameplayfix" in html else "unknown",
 "features":{
  "whack":bool(re.search(r"function\s+runWhack\s*\(",html)),
  "waiter":bool(re.search(r"function\s+runWaiterBalance\s*\(",html)),
  "studio_finish":"STUDIO FINISH" in html,
  "reduced_motion":"prefers-reduced-motion" in html,
  "high_dpi":"devicePixelRatio" in html,
  "three_languages":all(x in html for x in ('"EN"','"FR"','"ES"')),
 },
 "limitations":["Function count is not the number of playable arcade modes.",
                "No screenshot, browser input, device FPS or real Android playthrough was run."]
}
out=Path("dont100-apk/studio_qa_report.json")
out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2,ensure_ascii=False))
