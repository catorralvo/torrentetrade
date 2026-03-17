// Cambio idioma
function setLang(lang){
document.querySelectorAll('.lang').forEach(el=>el.style.display='none');
document.querySelector('.'+lang).style.display='block';
}

// Idioma por defecto
setLang('fr');

// Animaciones scroll
const faders = document.querySelectorAll('.fade');

const observer = new IntersectionObserver(entries=>{
entries.forEach(entry=>{
if(entry.isIntersecting){
entry.target.classList.add('show');
}
});
});

faders.forEach(el=>observer.observe(el));