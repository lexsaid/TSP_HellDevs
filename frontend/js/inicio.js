document.addEventListener('DOMContentLoaded', () => {
    const openMenu = document.getElementById('openMenu');
    const sideMenu = document.getElementById('sideMenu');
    const overlay = document.getElementById('menuOverlay');
    const btnLogout = document.getElementById('btnLogout');

    // Función para abrir
    openMenu.addEventListener('click', () => {
        sideMenu.classList.add('active');
        overlay.classList.add('active');
    });

    // Función para cerrar (clic en la capa oscura)
    overlay.addEventListener('click', () => {
        sideMenu.classList.remove('active');
        overlay.classList.remove('active');
    });

    // Cerrar Sesión
    btnLogout.addEventListener('click', (e) => {
        e.preventDefault();
        // Redirige al login
        window.location.href = "login.html";
    });
});