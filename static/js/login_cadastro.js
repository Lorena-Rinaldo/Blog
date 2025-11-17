// 1. Usa o evento 'DOMContentLoaded' para garantir que o HTML está pronto
document.addEventListener('DOMContentLoaded', (event) => {
    // 2. Tenta encontrar o input de login pelo ID
    const userInput = document.getElementById('user');

    if (userInput) {
        // 3. Aplica o foco de forma forçada
        userInput.focus();
    }

    // 4. (Opcional) Código para esconder a mensagem flash
    var flashPopup = document.getElementById('flashPopup');
    if (flashPopup) {
        setTimeout(function () {
            flashPopup.style.display = 'none';
        }, 5000);
    }
});