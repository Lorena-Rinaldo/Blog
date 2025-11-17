document.addEventListener('DOMContentLoaded', function () {
    const verPostsButtons = document.querySelectorAll('.btn-ver-posts');
    const postsContainer = document.getElementById('posts-container');
    const postsTituloSpan = document.getElementById('posts-filtrados-titulo');

    // NOVA FUNÇÃO: Auxiliar para criar o HTML de um post
    function createPostElement(post) {
        const postElement = document.createElement('p');
        postElement.innerHTML = `
                <a href="/excluirpost/${post.idPost}" onclick="return confirm('Deseja realmente excluir?')">
                    <i class="fa-solid fa-trash"></i>
                </a>
                ${post.idPost} - ${post.titulo} - ${post.conteudo_resumo}
            `;
        return postElement;
    }

    verPostsButtons.forEach(button => {
        button.addEventListener('click', function () {
            const userId = this.dataset.idUsuario;
            // NOVA LINHA: Pega o nome de usuário para o título
            const userName = this.closest('tr').querySelector('td:nth-child(4)').textContent.trim();

            // ATUALIZADO: Usando o nome do usuário no título
            postsTituloSpan.textContent = ` (Usuário: ${userName})`;
            postsContainer.innerHTML = '<p>Carregando posts...</p>'; // Indicador de carregamento

            fetch(`/api/posts_por_usuario/${userId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro na rede ou o servidor não retornou 200 OK');
                    }
                    return response.json();
                })
                .then(data => {
                    postsContainer.innerHTML = ''; // Limpa o conteúdo atual

                    if (data.posts && data.posts.length > 0) {
                        data.posts.forEach(post => {
                            postsContainer.appendChild(createPostElement(post)); // Usa a nova função
                        });
                    } else {
                        postsContainer.innerHTML = '<p>Nenhum post disponível para este usuário!</p>';
                    }
                })
                .catch(error => {
                    console.error('Erro ao buscar posts:', error);
                    postsContainer.innerHTML = '<p>Erro ao carregar posts. Tente novamente.</p>';
                });
        });
    });
});