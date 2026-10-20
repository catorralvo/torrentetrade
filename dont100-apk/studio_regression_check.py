#!/usr/bin/env python3
"""Fail-fast regression checks for the reconstructed DON'T 100 web payload.
Static safeguards only; does NOT replace browser/gameplay QA.
"""
from pathlib import Path
import re
import sys

HTML = Path("dont100-apk/app/src/main/assets/index.html")
PATCH = Path("dont100-apk/rc_gameplayfix_patch.py")
html = HTML.read_text(encoding="utf-8")
patch = PATCH.read_text(encoding="utf-8")
failures = []

def check(label, condition):
    print(("PASS" if condition else "FAIL") + " " + label)
    if not condition:
        failures.append(label)

def function_body(name):
    match = re.search(r"function\s+" + re.escape(name) + r"\s*\(", html)
    if not match:
        return ""
    start = match.start()
    nxt = re.search(r"\nfunction\s+\w+\s*\(", html[match.end():])
    return html[start:match.end() + nxt.start()] if nxt else html[start:]

check("built payload exists", len(html) > 10000)
check("gameplay patch build marker", '4.3.1-gameplayfix' in html)
check("Whack function exists once", len(re.findall(r"function\s+runWhack\s*\(", html)) == 1)
check("Waiter function exists once", len(re.findall(r"function\s+runWaiterBalance\s*\(", html)) == 1)
whack = function_body("runWhack")
waiter = function_body("runWaiterBalance")
check("Whack seven hits to pass", "got>=7" in whack and "return pass()" in whack)
check("Whack X tap fails", "target.bad" in whack and "return fail(" in whack)
check("Whack X expiry bypasses miss", bool(re.search(r"if\s*\(target\.bad\)\s*\{[^}]*next\(\)", whack)))
check("Whack missed good targets fail", "misses>=2" in whack and "return fail(" in whack)
check("Waiter automatic tilt bias", "target+bias-tilt" in waiter)
check("Waiter direction changes", "side*=-1" in waiter)
check("Waiter falls and spills", "Math.abs(glass)>64" in waiter and "spill>.42" in waiter)
check("Waiter timed success", "safe>=8.5" in waiter)
check("Keep-up unlimited time instruction", "No hay límite de tiempo." in html)
check("DPR canvas setup", "devicePixelRatio" in html)
check("Animation loop cleanup", "cancelAnimationFrame" in html)
check("Gameplay patch source retained", "replace_function(s,'runWhack',whack)" in patch and "replace_function(s,'runWaiterBalance',waiter)" in patch)
if failures:
    sys.exit(f"{len(failures)} static regression check(s) failed")
print("Static regression checks passed; browser and real-device QA still required.")
