document.addEventListener('DOMContentLoaded', function () {
    const ellipsisIcons = document.querySelectorAll('.ellipsis-icon');

    ellipsisIcons.forEach(icon => {
        icon.addEventListener('click', function (event) {
            event.stopPropagation(); // Impede que o clique se propague para o document
            const postId = this.id.split('-')[1];
            const menuOptions = document.getElementById(`menuOptions-${postId}`);

            // Fecha outros menus antes de abrir este
            document.querySelectorAll('.opcoes-menu.show-menu').forEach(openMenu => {
                if (openMenu.id !== `menuOptions-${postId}`) {
                    openMenu.classList.remove('show-menu');
                }
            });

            menuOptions.classList.toggle('show-menu');
        });
    });

    // Fechar o menu se clicar em qualquer lugar fora dele
    document.addEventListener('click', function (event) {
        let clickedInsideEllipsis = false;
        let clickedInsideMenu = false;

        ellipsisIcons.forEach(icon => {
            if (icon.contains(event.target)) {
                clickedInsideEllipsis = true;
            }
        });

        document.querySelectorAll('.opcoes-menu').forEach(menu => {
            if (menu.contains(event.target)) {
                clickedInsideMenu = true;
            }
        });

        if (!clickedInsideEllipsis && !clickedInsideMenu) {
            document.querySelectorAll('.opcoes-menu.show-menu').forEach(openMenu => {
                openMenu.classList.remove('show-menu');
            });
        }
    });
});

