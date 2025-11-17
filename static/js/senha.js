document.addEventListener('DOMContentLoaded', () => {
    // Seleciona o botão de toggle e o campo de senha
    const toggleButton = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('senha');

    if (toggleButton && passwordInput) {
        toggleButton.addEventListener('click', () => {
            // Verifica o tipo atual do campo (se é 'password')
            const isPassword = passwordInput.getAttribute('type') === 'password';

            // Define o novo tipo: se for 'password', muda para 'text'; caso contrário, volta para 'password'
            const newType = isPassword ? 'text' : 'password';
            passwordInput.setAttribute('type', newType);

            // Alterna o ícone (olho aberto <-> olho fechado)
            const icon = toggleButton.querySelector('i');
            if (isPassword) {
                // Está mostrando a senha (troca para olho fechado)
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
                toggleButton.setAttribute('aria-label', 'Esconder Senha');
            } else {
                // Está escondendo a senha (troca para olho aberto)
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
                toggleButton.setAttribute('aria-label', 'Mostrar Senha');
            }
        });
    }
});