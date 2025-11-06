function alternarCurtida(postId) { // Pass postId as an argument
    const icone = document.getElementById(`icone-curtir-${postId}`); // Use dynamic ID

    if (icone) { // Ensure the icon exists before trying to modify it
        icone.classList.toggle('curtido');

        if (icone.classList.contains('fas')) {
            icone.classList.remove('fas');
            icone.classList.add('far');
        } else {
            icone.classList.remove('far');
            icone.classList.add('fas');
        }
    }
}