import { matchPrograms, inferProjectTypes } from './engine.mjs';

const $ = (s)=>document.querySelector(s);
const labels={confirmed:'Éligibilité confirmée sur les critères saisis',probable:'Probablement éligible',to_verify:'À vérifier',not_eligible:'Non éligible'};
let programs=[];

async function boot(){
  const r=await fetch('./data/programs.json');
  programs=await r.json();
  $('#verifiedCount').textContent=programs.length;
  $('#run').addEventListener('click',run);
  $('#example').addEventListener('click',fillExample);
}
function val(id){return $(id)?.value ?? ''}
function tri(id){const v=val(id); return v==='yes'?true:v==='no'?false:null}
function profileFromForm(){return {canton:val('#canton'),fte:Number(val('#fte')||0),description:val('#description'),industry_hightech:tri('#industry'),rd_or_production_in_canton:tri('#localRD'),industrial_company:tri('#industrial'),production_tool_in_canton:tri('#productionTool'),is_startup:tri('#startup'),market_established:tri('#market'),project_started:tri('#started'),swiss_research_partner:tri('#researchPartner'),geneva_research_partner:tri('#genevaPartner'),foreign_local_partner:tri('#foreignPartner'),local_jobs_impact:tri('#jobsImpact'),project_types:inferProjectTypes(val('#description'))};}
function money(f){if(!f)return 'Selon dossier';const parts=[];if(f.amount_max_chf)parts.push(`jusqu’à CHF ${f.amount_max_chf.toLocaleString('fr-CH')}`);if(f.amount_max_eur)parts.push(`jusqu’à EUR ${f.amount_max_eur.toLocaleString('fr-CH')}`);if(f.rate_max)parts.push(`${Math.round(f.rate_max*100)}% max.`);return parts.join(' • ')||f.note||'Selon dossier';}
function run(){const p=profileFromForm();if(!p.description.trim()){$('#results').innerHTML='<div class="empty">Décrivez votre projet pour lancer l’analyse.</div>';return;}const results=matchPrograms(programs,p);const good=results.filter(x=>x.eligibility!=='not_eligible'&&x.relevance>=40);$('#summary').hidden=false;$('#summary').innerHTML=`<strong>${good.length}</strong> pistes à examiner sur <strong>${programs.length}</strong> dispositifs vérifiés. <span>Thèmes détectés: ${p.project_types.join(', ')||'aucun — précisez le projet'}.</span>`;$('#results').innerHTML=results.filter(x=>x.relevance>=38||x.eligibility==='not_eligible').map(card).join('');}
function list(items,klass=''){return items?.length?`<ul class="${klass}">${items.map(x=>`<li>${x}</li>`).join('')}</ul>`:''}
function card(x){const p=x.program;return `<article class="result ${x.eligibility}"><div class="score"><b>${x.relevance}</b><span>match</span></div><div class="resultMain"><div class="row"><div><div class="authority">${p.authority}</div><h3>${p.name}</h3></div><span class="badge">${labels[x.eligibility]}</span></div><div class="amount">${money(p.funding)}</div>${x.blockers.length?`<details open><summary>Pourquoi exclu</summary>${list(x.blockers,'bad')}</details>`:''}${x.reasons.length?`<details><summary>Pourquoi cette piste apparaît</summary>${list(x.reasons,'good')}</details>`:''}${x.checks.length?`<details><summary>À confirmer</summary>${list(x.checks,'warn')}</details>`:''}<details><summary>Conditions et documents</summary>${list(p.hard_requirements)}${list(p.documents)}</details><div class="foot"><span>Vérifié le ${p.verified_on}</span><a href="${p.source}" target="_blank" rel="noopener">Source officielle ↗</a></div></div></article>`}
function fillExample(){$('#canton').value='VD';$('#fte').value='38';$('#industry').value='yes';$('#localRD').value='yes';$('#industrial').value='yes';$('#productionTool').value='yes';$('#startup').value='no';$('#market').value='yes';$('#started').value='no';$('#researchPartner').value='unknown';$('#genevaPartner').value='unknown';$('#foreignPartner').value='unknown';$('#jobsImpact').value='yes';$('#description').value="Nous sommes une PME industrielle vaudoise. Nous voulons automatiser une ligne de production et développer un prototype de nouveau produit. Budget prévu CHF 240'000 avec un bureau d'ingénierie externe. Le projet n'a pas encore commencé.";run();}
boot();