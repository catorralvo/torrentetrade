from pathlib import Path
p=Path('dont100-apk/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
def change(name, transform):
 global s
 start=s.index('function '+name+'(')
 end=s.find('\nfunction ',start+10)
 assert end>start,name
 old=s[start:end]
 new=transform(old)
 assert new!=old,name
 s=s[:start]+new+s[end:]
def controls(body, mode):
 if mode=='vertical':
  old='const move=e=>py=Math.max(0,Math.min(170,canvasPointerY(e,c)-25));c.addEventListener("pointerdown",move);c.addEventListener("pointermove",move);'
  new='const ctl=arcadeControlDeck("slide",tr("MUEVE LA BARRA","MOVE PADDLE","DÉPLACE LA RAQUETTE"));bindRelativePad(ctl.pad,dx=>py=Math.max(0,Math.min(170,py+dx*.7)));'
 elif mode=='lane':
  old='const move=e=>{const x=canvasPointerX(e,c);lane=x<135?0:x>225?2:1};c.addEventListener("pointerdown",move);c.addEventListener("pointermove",move);'
  new='const ctl=arcadeControlDeck("slide",tr("CAMBIA DE CARRIL","CHANGE LANE","CHANGE DE VOIE"));let laneTravel=0;bindRelativePad(ctl.pad,dx=>{laneTravel+=dx;while(laneTravel>=38){lane=Math.min(2,lane+1);laneTravel-=38}while(laneTravel<=-38){lane=Math.max(0,lane-1);laneTravel+=38}});'
 elif mode=='gate':
  old='const move=e=>x=canvasPointerX(e,c);c.addEventListener("pointerdown",move);c.addEventListener("pointermove",move);'
  new='const ctl=arcadeControlDeck("slide",tr("ALINEA EL PUNTO","ALIGN THE DOT","ALIGNE LE POINT"));bindRelativePad(ctl.pad,dx=>x=Math.max(8,Math.min(352,x+dx)));'
 else: raise ValueError(mode)
 assert old in body,mode
 return body.replace(old,new)
change('runPong',lambda b:controls(b,'vertical').replace(';later(()=>fail(t("generic.tooSlow")),14000);',';'))
change('runLaneDodge',lambda b:controls(b,'lane'))
change('runGateCrash',lambda b:controls(b,'gate').replace(';later(()=>fail(t("generic.tooSlow")),12000);',';'))
change('runShield',lambda b:b.replace(';later(()=>fail(t("generic.tooSlow")),11500);',';'))
p.write_text(s,encoding='utf-8')
print('Fair-control patch applied')
