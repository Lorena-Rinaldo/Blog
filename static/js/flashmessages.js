document.addEventListener('DOMContentLoaded', function () {
    const flashPopup = document.getElementById('flashPopup');
    if (flashPopup) {
        flashPopup.classList.add('show'); // Mostra a pop-up
        setTimeout(() => {
            flashPopup.classList.remove('show'); // Esconde depois de 3 segundos
        }, 3000);
    }
});