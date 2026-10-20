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
check("Waiter frame delta supports 30fps", "Math.min(.05,(ts-last)/1000||0)" in waiter)
check("Keep-up unlimited time instruction", "No hay límite de tiempo." in html)
check("DPR canvas setup", "devicePixelRatio" in html)
check("Animation loop cleanup", "cancelAnimationFrame" in html)
check("Gameplay patch source retained", "replace_function(s,'runWhack',whack)" in patch and "replace_function(s,'runWaiterBalance',waiter)" in patch)
# Deterministic approximation of the actual Waiter integration equations.
# Extract the coefficients from the generated JavaScript, so tuning affects tests.
def coefficient(pattern):
    m = re.search(pattern, waiter)
    return float(m.group(1)) if m else None

tilt_rate = coefficient(r"dt\*([\d.]+)\)")
accel = coefficient(r"tilt\*([\d.]+)-glass")
spring = coefficient(r"glass\*([\d.]+)\)\*dt")
damping = coefficient(r"vel\*=([\d.]+)")
check("Waiter physics constants readable", all(v is not None for v in (tilt_rate, accel, spring, damping)))

def waiter_simulation(fps, guided=False):
    # Fixed random scenario: initial rightward bias, then two direction shifts.
    # The guided player compensates the visible bias; idle player never touches.
    if any(v is None for v in (tilt_rate, accel, spring, damping)):
        return "invalid"
    tilt = glass = vel = spill = safe = 0.0
    dt = min(.05, 1.0 / fps)
    for i in range(int(11.0 * fps)):
        t = i / fps
        bias = .165 if t < 4.2 else (-.155 if t < 7.3 else .155)
        target = -bias if guided else 0.0
        tilt += (target + bias - tilt) * min(1, dt * tilt_rate)
        vel += (tilt * accel - glass * spring) * dt
        vel *= damping
        glass += vel * dt
        spill = spill + dt if abs(tilt) > .255 else max(0, spill - dt * 1.7)
        safe += dt
        if abs(glass) > 64 or spill > .42:
            return "fail"
        if safe >= 8.5:
            return "pass"
    return "timeout"

for fps in (30, 60, 120):
    check(f"Waiter idle loses at {fps}fps", waiter_simulation(fps) == "fail")
    check(f"Waiter ideal control can win at {fps}fps", waiter_simulation(fps, guided=True) == "pass")

if failures:
    sys.exit(f"{len(failures)} static regression check(s) failed")
print("Static and deterministic physics checks passed; browser and real-device QA still required.")
