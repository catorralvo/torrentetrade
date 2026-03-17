// Cambio de idioma
function setLanguage(lang) {
    const sections = document.querySelectorAll('.lang');
    sections.forEach(sec => sec.style.display = 'none');
    document.querySelector('.' + lang).style.display = 'block';
}

setLanguage('fr'); // Francés por defecto

// Formulario para enviar correctamente
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e){
        // Formspree envia el formulario
        // Se puede agregar alerta
        alert("Merci, votre message a été envoyé !");
    });
});