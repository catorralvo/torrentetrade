import assert from 'node:assert/strict';
import {loadWorkspace,saveWorkspace,saveProfile,upsertProject,saveScan,setWatch,isWatched,addWatchAlerts,unreadAlerts,markAlertsRead} from '../workspace.mjs';

class MemoryStorage{constructor(){this.m=new Map()}getItem(k){return this.m.has(k)?this.m.get(k):null}setItem(k,v){this.m.set(k,String(v))}}
const storage=new MemoryStorage();
let s=loadWorkspace(storage);
assert.equal(s.projects.length,0);
saveProfile(s,{company_name:'AlpTech SA',canton:'VD',fte:38});
const p=upsertProject(s,{name:'Automation',description:'Automatiser une ligne'});
setWatch(s,p.id,true);
assert.equal(isWatched(s,p.id),true);
const previous=[{program_id:'a',program_name:'Programme A',eligibility:'to_verify',relevance:55,checks:[],blockers:[]}];
saveScan(s,{project_id:p.id,input:{canton:'VD'},results:previous,catalog_version:'v1'});
const current=[{program:{id:'a',name:'Programme A'},eligibility:'probable',relevance:75,checks:[],blockers:[]},{program:{id:'b',name:'Programme B'},eligibility:'probable',relevance:70,checks:[],blockers:[]}];
const alerts=addWatchAlerts(s,p.id,previous,current,'v2');
assert.equal(alerts.length,2);
assert.equal(unreadAlerts(s).length,2);
markAlertsRead(s);assert.equal(unreadAlerts(s).length,0);
saveWorkspace(s,storage);const reloaded=loadWorkspace(storage);
assert.equal(reloaded.profile.company_name,'AlpTech SA');
assert.equal(reloaded.projects[0].name,'Automation');
assert.equal(reloaded.watches[0].enabled,true);
console.log('workspace tests: OK');
