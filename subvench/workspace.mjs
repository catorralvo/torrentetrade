const KEY='subvench:m2:workspace';
const empty=()=>({version:2,profile:{},projects:[],scans:[],watches:[],alerts:[]});
const id=()=>globalThis.crypto?.randomUUID?.()||`${Date.now()}-${Math.random().toString(16).slice(2)}`;

export function loadWorkspace(storage=globalThis.localStorage){
  if(!storage)return empty();
  try{return {...empty(),...JSON.parse(storage.getItem(KEY)||'{}')};}catch{return empty();}
}
export function saveWorkspace(state,storage=globalThis.localStorage){if(storage)storage.setItem(KEY,JSON.stringify(state));return state;}
export function saveProfile(state,profile){state.profile={...state.profile,...profile,updated_at:new Date().toISOString()};return state;}
export function upsertProject(state,project){
  const now=new Date().toISOString();
  const record={...project,id:project.id||id(),created_at:project.created_at||now,updated_at:now};
  const i=state.projects.findIndex(x=>x.id===record.id);
  if(i>=0)state.projects[i]=record;else state.projects.unshift(record);
  return record;
}
export function saveScan(state,{project_id,input,results,catalog_version,engine_version='m2-local'}){
  const scan={id:id(),project_id,input,result_snapshot:results.map(leanResult),catalog_version,engine_version,created_at:new Date().toISOString()};
  state.scans.unshift(scan);state.scans=state.scans.slice(0,100);return scan;
}
export function latestScan(state,projectId){return state.scans.find(x=>x.project_id===projectId)||null;}
export function setWatch(state,projectId,enabled=true){
  const existing=state.watches.find(x=>x.project_id===projectId);
  if(existing){existing.enabled=enabled;existing.updated_at=new Date().toISOString();return existing;}
  const watch={id:id(),project_id:projectId,enabled,created_at:new Date().toISOString(),updated_at:new Date().toISOString()};state.watches.unshift(watch);return watch;
}
export function isWatched(state,projectId){return !!state.watches.find(x=>x.project_id===projectId&&x.enabled);}
export function unreadAlerts(state){return state.alerts.filter(x=>!x.read_at);}
export function markAlertsRead(state){const now=new Date().toISOString();state.alerts.forEach(x=>{if(!x.read_at)x.read_at=now});return state;}
export function addWatchAlerts(state,projectId,previousResults,currentResults,catalogVersion){
  if(!previousResults?.length)return [];
  const before=new Map(previousResults.map(x=>[x.program_id,x]));
  const after=new Map(currentResults.map(leanResult).map(x=>[x.program_id,x]));
  const alerts=[];
  for(const [pid,next] of after){
    const prev=before.get(pid);
    if(!prev&&next.eligibility!=='not_eligible'&&next.relevance>=40)alerts.push(makeAlert(projectId,pid,'new_match','Nouvelle piste détectée',`${next.program_name} correspond désormais au projet (${next.relevance}% de pertinence).`,catalogVersion));
    else if(prev&&prev.availability&&next.availability&&prev.availability!==next.availability)alerts.push(makeAlert(projectId,pid,'program_changed','Disponibilité modifiée',`${next.program_name}: ${prev.availability} → ${next.availability}.`,catalogVersion));
    else if(prev&&prev.eligibility!==next.eligibility)alerts.push(makeAlert(projectId,pid,'eligibility_changed','Éligibilité à revoir',`${next.program_name}: ${prev.eligibility} → ${next.eligibility}.`,catalogVersion));
    else if(prev&&Math.abs((prev.relevance||0)-(next.relevance||0))>=15)alerts.push(makeAlert(projectId,pid,'program_changed','Pertinence modifiée',`${next.program_name}: ${prev.relevance}% → ${next.relevance}%.`,catalogVersion));
  }
  if(alerts.length){state.alerts.unshift(...alerts);state.alerts=state.alerts.slice(0,100);}return alerts;
}
function makeAlert(project_id,program_id,kind,title,body,catalog_version){return{id:id(),project_id,program_id,kind,title,body,catalog_version,created_at:new Date().toISOString(),read_at:null};}
function leanResult(x){return{program_id:x.program?.id||x.program_id,program_name:x.program?.name||x.program_name,eligibility:x.eligibility,relevance:x.relevance,availability:x.availability?.code||x.availability||null,checks:x.checks||[],blockers:x.blockers||[]};}
export function exportWorkspace(state){return JSON.stringify(state,null,2);}
