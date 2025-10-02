function alternarCurtida() {
    // 1. Encontra o elemento do ícone pelo ID
    const icone = document.getElementById('icone-curtir');
    
    // 2. Alterna a classe de cor 'curtido'
    icone.classList.toggle('curtido');
    
    // 3. Alterna entre o ícone vazado (far) e o preenchido (fas)
    if (icone.classList.contains('fas')) {
        // Se já está sólido, volta para regular
        icone.classList.remove('fas');
        icone.classList.add('far');
    } else {
        // Se está regular, muda para sólido
        icone.classList.remove('far');
        icone.classList.add('fas');
    }
}