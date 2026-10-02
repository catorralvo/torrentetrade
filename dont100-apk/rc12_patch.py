from pathlib import Path

p=Path('dont100-apk/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')

# If patching the raw RC1 payload, keep the RC1.1 functional fixes. If already RC1.1, these are harmless/no-ops.
s=s.replace('window.D100V4={runSeed:(()=>{try{const a=new Uint32Array(1);crypto.getRandomValues(a);return a[0]}catch{return Date.now()}})(),runId:"apk-test"','window.D100V4={runSeed:4,runId:"apk-polish"')
s=s.replace('const BUILD="4.2.0-rc.1"','const BUILD="4.2.0-rc.1.2-polish"')
s=s.replace('const BUILD="4.2.0-rc.1.1-testfix"','const BUILD="4.2.0-rc.1.2-polish"')
s=s.replace('v4.2-rc.1</span>','v4.2-rc.1.2</span>')
s=s.replace('level:Math.min(100,Math.max(1,Number(localStorage.getItem(STORAGE.level)||1))),','level:Math.min(100,Math.max(1,Number(localStorage.getItem(STORAGE.level)||18))),')
s=s.replace('best:Math.min(100,Math.max(1,Number(localStorage.getItem(STORAGE.best)||1))),','best:Math.min(100,Math.max(1,Number(localStorage.getItem(STORAGE.best)||18))),')

# Level-18 keep-up bug fix (only if raw RC1 block still has the timer).
start=s.find('function runKeepUp(')
end=s.find('\nfunction runLaserMaze',start)
if start >= 0 and end > start:
    block=s[start:end]
    block=block.replace('Toca la pelota antes de que caiga.','Toca la pelota cuando baje. No hay límite de tiempo.')
    block=block.replace('Tap the ball before it drops.','Tap the ball as it drops. No time limit.')
    block=block.replace("Touche la balle avant qu'elle tombe.","Touche la balle quand elle descend. Pas de limite de temps.")
    block=block.replace('let x=180,y=90,vx=45,vy=20,last=performance.now(),got=0;c.addEventListener("pointerdown",e=>{','let x=180,y=90,vx=45,vy=20,last=performance.now(),got=0,lastTouch=0;c.addEventListener("pointerdown",e=>{const now=performance.now();')
    block=block.replace('if(Math.hypot(px-x,py-y)<28){vy=-175;vx+=(px-x)*1.1;got++;','if(Math.hypot(px-x,py-y)<30){if(now-lastTouch<240)return;lastTouch=now;vy=-170;vx+=(px-x)*.85;got++;')
    block=block.replace('});later(()=>fail(t("generic.tooSlow")),12000);','});')
    s=s[:start]+block+s[end:]

# Slow down one of the doodle animation drivers if this is raw RC1.
s=s.replace('const swing=Math.sin(t*.012)*10;','const swing=Math.sin(t*.006)*9;')

# Remove prior playtest style block when patching RC1.1 artifact locally, to avoid duplicate rules.
old_marker='/* v4.2 RC1.1 mobile playtest hotfix */'
if old_marker in s:
    a=s.index(old_marker)
    b=s.index('</style>',a)
    s=s[:a]+s[b:]

polish_css = r'''
/* v4.2 RC1.2 — mobile polish pass: notebook-arcade identity + zero-scroll play */
:root{
  --surface:rgba(255,255,255,.94);--surface-2:rgba(255,255,255,.78);--line:rgba(17,17,17,.12);
  --deep:#171717;--paper-shadow:0 14px 34px rgba(25,22,18,.13),0 3px 0 rgba(17,17,17,.10);
}
html,body{height:100%;max-height:100dvh;overflow:hidden}
body{
  min-height:100dvh;overscroll-behavior:none;position:relative;
  background:
    radial-gradient(circle at 12% 2%,color-mix(in srgb,var(--accent) 11%,transparent) 0 18%,transparent 38%),
    radial-gradient(circle at 88% 94%,color-mix(in srgb,var(--accent) 8%,transparent) 0 14%,transparent 36%),
    linear-gradient(180deg,#f8f6f1 0%,#efebe2 100%);
}
body::before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.24;background-image:linear-gradient(rgba(17,17,17,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(17,17,17,.035) 1px,transparent 1px);background-size:24px 24px;mask-image:linear-gradient(to bottom,#000 0 72%,transparent 100%)}
.shell{height:100dvh;min-height:0;max-height:100dvh;overflow:hidden;padding:max(8px,env(safe-area-inset-top)) 10px max(8px,env(safe-area-inset-bottom));gap:7px;position:relative;z-index:1}
.topbar{min-height:47px;padding:4px 7px;border:1.5px solid rgba(17,17,17,.88);border-radius:18px;background:var(--surface-2);box-shadow:0 6px 0 rgba(17,17,17,.07),0 12px 22px rgba(17,17,17,.05);backdrop-filter:blur(10px)}
.logo{font-size:22px;letter-spacing:-1.8px;text-shadow:0 1px 0 #fff}.logo b{background:var(--accent);border:1.5px solid var(--ink);padding:2px 8px 3px;box-shadow:0 3px 0 var(--ink);transform:rotate(-2.5deg)}
.round-btn{width:38px;height:38px;border:1.5px solid var(--ink);box-shadow:0 3px 0 rgba(17,17,17,.16);background:#fff}.round-btn:active{transform:translateY(2px);box-shadow:none}
.lang-select{height:32px;border:1.5px solid var(--ink);box-shadow:0 3px 0 rgba(17,17,17,.12);background:#fff}
.level-chip{display:grid;justify-items:end;gap:1px}.level-chip small{font-size:8px}.level-chip strong{display:grid;place-items:center;min-width:34px;height:29px;padding:0 7px;border:1.5px solid var(--ink);border-radius:10px;background:var(--deep);color:#fff;font-size:17px;box-shadow:0 3px 0 color-mix(in srgb,var(--accent) 55%,#aaa)}
.progress-wrap{padding:5px 9px 7px;border:1px solid rgba(17,17,17,.15);border-radius:14px;background:rgba(255,255,255,.65);box-shadow:0 5px 15px rgba(0,0,0,.035)}
.progress-meta{margin-bottom:5px;font-size:9px}.progress-meta span:first-child{color:var(--ink)}
.progress-track{height:10px;border:1.5px solid var(--ink);background:rgba(255,255,255,.9);box-shadow:inset 0 1px 2px rgba(0,0,0,.08)}
.progress-fill{background:linear-gradient(90deg,color-mix(in srgb,var(--accent) 72%,#111),var(--accent));box-shadow:inset 0 -1px 0 rgba(0,0,0,.13);transition:width .5s cubic-bezier(.22,.8,.22,1)}
.checkpoint{width:7px;height:7px;border-width:1.5px;background:#fff}
.timer-strip{gap:6px;margin-top:0}.timer-box{padding:6px 9px;border:1px solid rgba(17,17,17,.28);border-radius:13px;background:rgba(255,255,255,.82);box-shadow:0 4px 12px rgba(0,0,0,.035)}.timer-box small{font-size:8px}.timer-box strong{font-size:16px}
.game-card{min-height:0!important;flex:1;position:relative;overflow:hidden;padding:13px 14px;border:1.5px solid rgba(17,17,17,.9);border-radius:26px;background:linear-gradient(180deg,rgba(255,255,255,.985),rgba(255,255,255,.93));box-shadow:var(--paper-shadow);animation:cardIn .28s cubic-bezier(.2,.8,.2,1)}
.game-card::before{content:"";position:absolute;left:20px;right:20px;top:-1px;height:5px;border-radius:0 0 7px 7px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 60%,#fff));box-shadow:0 2px 8px color-mix(in srgb,var(--accent) 25%,transparent)}
.game-card::after{content:"";position:absolute;right:-34px;bottom:-34px;width:120px;height:120px;border-radius:50%;border:18px solid color-mix(in srgb,var(--accent) 6%,transparent);pointer-events:none}
@keyframes cardIn{from{opacity:.72;transform:translateY(7px) scale(.992)}to{opacity:1;transform:none}}
.level-head{padding-top:3px;position:relative;z-index:1}.tag{padding:6px 10px;border:1.5px solid var(--ink);background:var(--accent);box-shadow:0 3px 0 var(--ink);transform:rotate(-1deg);letter-spacing:1.1px}.checkpoint-text{font-weight:950;color:#5a554e}
.challenge{margin:7px 0 4px;padding:0 4px;position:relative;z-index:1}.challenge h1{font-size:clamp(28px,8vw,35px);line-height:1.01;margin:0 0 7px;letter-spacing:-1.45px;text-wrap:balance}.challenge p{display:inline-block;max-width:100%;min-height:0;margin:0;padding:6px 9px 7px;border-left:3px solid var(--accent);border-radius:8px;background:color-mix(in srgb,var(--accent) 6%,#fff);color:#403c36;font-size:clamp(14px,4vw,16px);line-height:1.25;font-weight:780;text-align:left;box-shadow:0 1px 0 rgba(17,17,17,.05)}
.play-area{min-height:0;flex:1;padding:7px 5px;margin-top:2px;position:relative;border-radius:20px;background:linear-gradient(180deg,rgba(248,247,243,.7),rgba(255,255,255,.34));border:1px solid rgba(17,17,17,.07);box-shadow:inset 0 1px 10px rgba(17,17,17,.025);z-index:1}
.action-area{position:relative;z-index:2;gap:8px}
.btn,.choice-btn,.tap-main,.hold-btn{border:1.7px solid var(--ink);border-radius:16px;letter-spacing:.15px;transition:transform .09s ease,box-shadow .09s ease,filter .12s ease}.btn:active,.choice-btn:active,.tap-main:active,.hold-btn:active{transform:translateY(3px) scale(.995);filter:saturate(.92)}
.primary,.tap-main{background:linear-gradient(180deg,color-mix(in srgb,var(--accent) 78%,#fff),var(--accent));color:#fff;text-shadow:0 1px 0 rgba(0,0,0,.22);box-shadow:0 6px 0 #181818,0 10px 20px color-mix(in srgb,var(--accent) 16%,transparent)}
.secondary{background:#fff;color:var(--ink);box-shadow:0 5px 0 #cbc6bd}.choice-btn{background:linear-gradient(180deg,#fff,#faf8f3);box-shadow:0 4px 0 #cfcac1}.choice-btn:focus-visible,.btn:focus-visible{outline:3px solid color-mix(in srgb,var(--accent) 45%,transparent);outline-offset:2px}
.mascot-zone{min-height:112px;margin-top:0;z-index:1}.mascot-zone::before{width:170px;height:78px;bottom:11px;background:radial-gradient(ellipse,color-mix(in srgb,var(--accent) 14%,transparent),transparent 70%)}.stickman{max-height:134px;filter:drop-shadow(0 8px 7px rgba(0,0,0,.06))}
.speech{right:1px;top:12px;max-width:min(170px,46vw);padding:8px 11px 9px;border:1.5px solid var(--ink);border-radius:15px 15px 4px 15px;background:#fff;color:#171717;box-shadow:0 4px 0 rgba(17,17,17,.10),0 8px 15px rgba(0,0,0,.05);font-size:11px;line-height:1.22;transform:rotate(1deg)}.speech::after{content:"";position:absolute;right:9px;bottom:-7px;width:12px;height:12px;background:#fff;border-right:1.5px solid #111;border-bottom:1.5px solid #111;transform:rotate(45deg)}
.arcade-wrap{border:2px solid var(--ink);border-radius:20px;background:#fff;box-shadow:0 6px 0 rgba(17,17,17,.16),0 14px 30px color-mix(in srgb,var(--accent) 10%,rgba(0,0,0,.08))}.arcade-canvas{background:linear-gradient(180deg,color-mix(in srgb,#fff 92%,var(--accent) 8%),#fff)}
body.arcade-level .game-card{min-height:0!important}body.arcade-level .play-area{min-height:0;flex:1;padding:6px 4px;margin-top:2px;background:transparent;border-color:transparent;box-shadow:none}body.arcade-level .arcade-wrap,body.arcade-level .arcade-canvas{height:clamp(170px,30dvh,250px)}
.fail-card,.between-card{max-height:calc(100dvh - 105px);overflow:auto;padding:22px 18px;border:1.5px solid var(--ink);border-radius:28px;box-shadow:var(--paper-shadow);position:relative}.between-card{background:radial-gradient(circle at 50% 13%,color-mix(in srgb,var(--accent) 15%,#fff),#fff 48%)}.fail-card{background:radial-gradient(circle at 50% 12%,#ffe3e0,#fff 50%)}
.result-mascot{width:min(220px,61vw);height:142px}.success-mark{width:58px;height:58px;border:2px solid var(--ink);background:var(--accent);box-shadow:0 5px 0 #111}.fail-icon{filter:drop-shadow(0 4px 0 rgba(0,0,0,.08))}
.success-streak{border:1.5px solid var(--ink);background:color-mix(in srgb,var(--accent) 8%,#fff);box-shadow:0 4px 0 rgba(17,17,17,.12)}
footer{flex:none;padding:0 3px;gap:5px;font-size:8px;opacity:.84}.text-btn{text-decoration:none;padding:3px 4px;border-radius:7px}.text-btn:active{background:rgba(17,17,17,.06)}
.polish-burst{position:fixed;inset:0;z-index:120;pointer-events:none;display:grid;place-items:center}.polish-burst i{position:absolute;left:50%;top:47%;width:9px;height:9px;border:1.5px solid #111;border-radius:3px;background:var(--accent);animation:burstDot .68s cubic-bezier(.1,.75,.15,1) forwards}.polish-burst.fail i{background:#ff655e}.polish-burst i:nth-child(2n){border-radius:50%;background:#fff}.polish-burst i:nth-child(3n){width:6px;height:13px}
@keyframes burstDot{0%{opacity:1;transform:translate(-50%,-50%) rotate(0) scale(.6)}100%{opacity:0;transform:translate(calc(-50% + var(--bx)),calc(-50% + var(--by))) rotate(230deg) scale(1.2)}}
body.polish-win .game-card{box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 25%,transparent),var(--paper-shadow)}body.polish-fail .game-card{box-shadow:0 0 0 3px rgba(255,76,67,.18),var(--paper-shadow)}
.stickman.sprite-panic{animation-duration:.38s!important}.stickman.sprite-nervous{animation-duration:.72s!important}.stickman.sprite-dance{animation-duration:1.22s!important}.stickman.sprite-win{animation-duration:.72s!important}.stickman.rope-jump{animation-duration:.46s!important}.jump-rope-loop.rope-spin{animation-duration:.50s!important}
@media(max-height:760px){.shell{gap:5px;padding-top:max(6px,env(safe-area-inset-top));padding-bottom:max(5px,env(safe-area-inset-bottom))}.topbar{min-height:42px;padding:2px 6px}.logo{font-size:20px}.round-btn{width:34px;height:34px}.progress-wrap{padding:3px 8px 5px}.timer-box{padding:4px 8px}.timer-box strong{font-size:14px}.game-card{padding:10px 11px;border-radius:23px}.challenge{margin:5px 0 3px}.challenge h1{font-size:clamp(25px,7.2vw,31px);margin-bottom:5px}.challenge p{font-size:13.5px;padding:5px 8px}.play-area{padding:4px}.mascot-zone{min-height:91px}.stickman{height:108px}.speech{top:6px;font-size:10px;padding:6px 9px}.btn,.choice-btn,.tap-main{min-height:50px}body.arcade-level .arcade-wrap,body.arcade-level .arcade-canvas{height:clamp(150px,27dvh,208px)}}
@media(max-height:650px){.topbar{min-height:38px}.progress-meta{display:none}.progress-wrap{padding:4px 7px}.timer-strip{display:flex}.timer-box{flex:1;padding:3px 7px}.challenge h1{font-size:24px}.challenge p{font-size:12.5px}.mascot-zone{min-height:76px}.stickman{height:91px}.speech{max-width:145px}.game-card{padding-top:9px}.play-area{padding-top:3px;padding-bottom:3px}body.arcade-level .arcade-wrap,body.arcade-level .arcade-canvas{height:148px}}
'''

s=s.replace('</style>',polish_css+'\n</style>',1)

polish_js = r'''
function polishFX(kind){
 try{
  document.body.classList.remove('polish-win','polish-fail');
  void document.body.offsetWidth;
  document.body.classList.add(kind==='win'?'polish-win':'polish-fail');
  const b=document.createElement('div');b.className=`polish-burst ${kind==='fail'?'fail':''}`;
  const pts=[[-92,-88],[-46,-112],[4,-104],[54,-91],[95,-62],[111,-8],[92,46],[47,78],[-6,88],[-57,71],[-98,39],[-116,-17]];
  pts.forEach(([x,y])=>{const i=document.createElement('i');i.style.setProperty('--bx',`${x}px`);i.style.setProperty('--by',`${y}px`);b.appendChild(i)});
  document.body.appendChild(b);setTimeout(()=>{b.remove();document.body.classList.remove('polish-win','polish-fail')},760);
 }catch{}
}
'''
if 'function polishFX(kind)' not in s:
    s=s.replace('function pass(){',polish_js+'\nfunction pass(){',1)
s=s.replace('if(state.resolved||state.failed)return;state.resolved=true;state.levelEndMs=Date.now();beginOfficialPause(state.levelEndMs);','if(state.resolved||state.failed)return;polishFX("win");state.resolved=true;state.levelEndMs=Date.now();beginOfficialPause(state.levelEndMs);',1)
s=s.replace('if(state.resolved||state.failed)return;state.failed=true;state.resolved=true;state.streak=0;','if(state.resolved||state.failed)return;polishFX("fail");state.failed=true;state.resolved=true;state.streak=0;',1)

p.write_text(s,encoding='utf-8')
assert '4.2.0-rc.1.2-polish' in s
assert 'No hay límite de tiempo.' in s
assert 'v4.2 RC1.2' in s
assert 'function polishFX(kind)' in s
print('patched',p.stat().st_size)
