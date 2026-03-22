document.addEventListener('DOMContentLoaded', () => {
    const completeButtons = document.querySelectorAll('.btn-complete');

    completeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const card = btn.closest('.job-card');
            const badge = card.querySelector('.badge');

            // Cambiar estado del Badge
            badge.textContent = 'Completado';
            badge.classList.remove('pending');
            badge.classList.add('done');

            // Cambiar estado del Botón
            btn.textContent = '✓ Completado';
            btn.disabled = true;
            btn.style.opacity = '0.6';
            btn.classList.remove('btn-complete'); // Evita que se dispare de nuevo

            alert('¡Trabajo marcado como completado!');
        });
    });
});