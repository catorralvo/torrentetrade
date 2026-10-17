import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';

const sourceDir=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(sourceDir);
const template=fs.readFileSync(path.join(sourceDir,'home-template.html'),'utf8');
const {ui,aboutCopy}=vm.runInNewContext(template.slice(template.indexOf('const ui ='),template.indexOf('function updateContactContext'))+'\n({ui,aboutCopy})');
const base='https://torrentetrade.ch';
const paths={fr:'/',en:'/en/',es:'/es/'};
const titles={fr:'Conseil PME Genève & Vaud | Torrente Trade & Advice',en:'SME consulting in Switzerland | Torrente Trade & Advice',es:'Consultoría para pymes en Suiza | Torrente Trade & Advice'};
const starts=['fr','en','es'].map(lang=>template.indexOf('<!-- '+lang.toUpperCase()+' -->'));
const end=template.indexOf('<section class="section about"');
const escape=value=>String(value).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const person={ '@type':'Person','@id':base+'/#carlos-torralvo',name:'Carlos Torralvo',url:base+'/#qui-sommes-nous',sameAs:['https://www.linkedin.com/in/carlos-torralvo/'],worksFor:{'@id':base+'/#organization'}};

for(const [lang,urlPath] of Object.entries(paths)){
 const i=['fr','en','es'].indexOf(lang),copy=ui[lang],about=aboutCopy[lang];
 let html=template.slice(0,starts[0])+template.slice(starts[i],starts[i+1]??end)+template.slice(end);
 const text=(id,value)=>{const re=new RegExp('(<[a-z0-9]+\\b[^>]*\\bid="'+id+'"[^>]*>)[\\s\\S]*?(</[a-z0-9]+>)');if(!re.test(html))throw new Error('Missing '+id);html=html.replace(re,(_,a,b)=>a+escape(value)+b);};
 const attr=(id,name,value)=>{const re=new RegExp('<[a-z0-9]+\\b[^>]*\\bid="'+id+'"[^>]*>');html=html.replace(re,tag=>{const a=new RegExp('\\b'+name+'="[^"]*"');return a.test(tag)?tag.replace(a,()=>name+'="'+escape(value)+'"'):tag.slice(0,-1)+' '+name+'="'+escape(value)+'">';});};
 html=html.replace('<html lang="fr">','<html lang="'+(lang==='fr'?'fr-CH':lang)+'">');
 html=html.replace(/<title>.*?<\/title>/,()=>'<title>'+escape(titles[lang])+'</title>');
 html=html.replace(/<meta name="description"[^>]*>/,()=>'<meta name="description" content="'+escape(copy.description)+'">');
 html=html.replace(/<meta property="og:title"[^>]*>/,()=>'<meta property="og:title" content="'+escape(titles[lang])+'">');
 html=html.replace(/<meta property="og:description"[^>]*>/,()=>'<meta property="og:description" content="'+escape(copy.description)+'">');
 html=html.replace(/<meta property="og:url"[^>]*>/,'<meta property="og:url" content="'+base+urlPath+'">');
 html=html.replace(/<meta property="og:locale"[^>]*>/,'<meta property="og:locale" content="'+({fr:'fr_CH',en:'en_CH',es:'es_CH'}[lang])+'">');
 html=html.replace(/<link rel="canonical"[^>]*>/,'<link rel="canonical" href="'+base+urlPath+'">\n'+Object.entries(paths).map(([l,p])=>'<link rel="alternate" hreflang="'+l+'" href="'+base+p+'">').join('\n')+'\n<link rel="alternate" hreflang="x-default" href="'+base+'/">');
 html=html.replace('.lang-section.en,.lang-section.es{display:none}','');
 html=html.replaceAll('.lang button','.lang a').replaceAll('[aria-pressed=true]','[aria-current=page]');
 html=html.replace('.lang a{','.lang a{display:inline-flex;align-items:center;justify-content:center;text-decoration:none;');
 html=html.replace(/<div class="lang"[^>]*>[\s\S]*?<\/div>/,()=>'<nav class="lang" aria-label="'+escape(copy.language)+'">\n'+Object.keys(paths).map(l=>'<a href="'+paths[l]+'" data-lang="'+l+'" lang="'+l+'" hreflang="'+l+'" aria-label="'+({fr:'Français',en:'English',es:'Español'}[l])+'"'+(l===lang?' aria-current="page"':'')+'>'+l.toUpperCase()+'</a>').join('\n')+'\n</nav>');
 const navIds=['navServices','navApproach','navEquipment','navContact'];
 const targets=['services-'+lang,'approche-'+lang,'equipements-'+lang,'contact'];
 navIds.forEach((id,j)=>{text(id,copy.nav[j]);attr(id,'href','#'+targets[j]);});
 html=html.replace('aria-label="Navigation principale"','aria-label="'+escape(copy.navigation)+'"');
 for(const [id,value] of Object.entries({navAbout:about.nav,aboutTitle:about.title,aboutIntro:about.intro,aboutRole:about.role,aboutLinkedIn:about.link,skipLink:copy.skip,contactIntro:copy.intro,emailLabel:copy.email,typeLabel:copy.type,messageLabel:copy.message,formNote:copy.note,contactLanguages:copy.country+' · Français / English / Español'}))text(id,value);
 html=html.replace(/(<span class="contact-title">)[\s\S]*?<\/span>/,(_,a)=>a+escape(copy.title)+'</span>');
 html=html.replace(/(<button type="submit">)[\s\S]*?<\/button>/,(_,a)=>a+escape(copy.submit)+'</button>');
 attr('contactEmail','placeholder',copy.emailPlaceholder);attr('contactMessage','placeholder',copy.placeholders.Consulting);
 ['Consulting','Purchase','Sale'].forEach((type,j)=>{html=html.replace(new RegExp('(<option value="'+type+'">)[\\s\\S]*?</option>'),(_,a)=>a+escape(copy.options[j])+'</option>');});
 attr('whatsappBtn','aria-label',copy.waLabel);attr('whatsappBtn','href','https://wa.me/41787313361?text='+encodeURIComponent(copy.wa.Consulting));
 html=html.replace(/\b(src|href)="(?![a-z]+:|\/|#)([^"]+)"/g,(_,a,p)=>a+'="/'+p+'"');
 html=html.replace('<a href="mailto:info@torrentetrade.ch">info@torrentetrade.ch</a></div>','<a href="mailto:info@torrentetrade.ch">info@torrentetrade.ch</a><p><a href="https://www.linkedin.com/company/torrentetrade/" target="_blank" rel="noopener noreferrer">LinkedIn · Torrente Trade &amp; Advice</a></p></div>');
 const schema=JSON.parse(template.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
 schema['@graph'][0].alternateName=['Torrente Trade','TT&A'];
 schema['@graph'][0].description=ui.fr.description;
 schema['@graph'].push(person,{'@type':'WebPage','@id':base+urlPath+'#webpage',url:base+urlPath,name:titles[lang],description:copy.description,inLanguage:lang,isPartOf:{'@id':base+'/#website'},about:{'@id':base+'/#organization'},author:{'@id':person['@id']}});
 html=html.replace(/<script type="application\/ld\+json">[\s\S]*?<\/script>/,()=>'<script type="application/ld+json">'+JSON.stringify(schema,null,2)+'</script>');
 const script=`'use strict';
const currentLang=${JSON.stringify(lang)};
const copy=${JSON.stringify(copy)};
const languagePaths=${JSON.stringify(paths)};
const queryParams=new URLSearchParams(window.location.search);
const anchorLanguage=window.location.hash.match(/^#(?:services|approche|equipements)-(fr|en|es)$/);
const requestedLanguage=queryParams.get('lang')||(anchorLanguage&&anchorLanguage[1]);
if(requestedLanguage&&languagePaths[requestedLanguage]&&requestedLanguage!==currentLang){
 const destination=new URL(languagePaths[requestedLanguage],window.location.origin);destination.search=queryParams.toString();destination.searchParams.delete('lang');destination.hash=window.location.hash.replace(/-(fr|en|es)$/, '-'+requestedLanguage);window.location.replace(destination.href);
}
const select=document.getElementById('contactType');
const requestedType=queryParams.get('type');
if(['Consulting','Purchase','Sale'].includes(requestedType))select.value=requestedType;
function updateContactContext(){const type=select.value;document.getElementById('contactMessage').placeholder=copy.placeholders[type]||copy.placeholders.Consulting;document.getElementById('whatsappBtn').href='https://wa.me/41787313361?text='+encodeURIComponent(copy.wa[type]||copy.wa.Consulting);}
document.querySelectorAll('[data-request]').forEach(link=>link.addEventListener('click',()=>{select.value=link.dataset.request;updateContactContext();}));
select.addEventListener('change',updateContactContext);
document.querySelectorAll('.lang a').forEach(link=>link.addEventListener('click',()=>{const destination=new URL(link.href);if(select.value!=='Consulting')destination.searchParams.set('type',select.value);destination.hash=window.location.hash.replace(/-(fr|en|es)$/, '-'+link.dataset.lang);link.href=destination.href;}));
document.getElementById('currentYear').textContent=String(new Date().getFullYear());
updateContactContext();`;
 html=html.replace(/<script>\s*[\s\S]*?<\/script>/,()=>'<script>\n'+script+'\n</script>');
 const output=path.join(root,urlPath==='/'?'index.html':urlPath.slice(1)+'index.html');fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,html);
 console.log(path.relative(root,output));
}

for(const slug of ['conseil-operationnel-pme-suisse','optimisation-couts-pme-suisse','sourcing-equipements-occasion-suisse']){
 const file=path.join(root,slug,'index.html');let html=fs.readFileSync(file,'utf8');
 html=html.replaceAll('href="/?lang=en"','href="/en/"').replaceAll('href="/?lang=es"','href="/es/"');
 html=html.replace(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/,(_,json)=>{const schema=JSON.parse(json);schema['@graph']=schema['@graph'].filter(x=>x['@id']!==person['@id']);schema['@graph'].push(person);const page=schema['@graph'].find(x=>x['@type']==='WebPage');page.author={'@id':person['@id']};return '<script type="application/ld+json">'+JSON.stringify(schema,null,2)+'</script>';});
 fs.writeFileSync(file,html);
}
